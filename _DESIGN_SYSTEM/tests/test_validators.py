from __future__ import annotations

import copy
import importlib.util
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/render.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validators = load_module("deliverable_validators", ROOT / "scripts/validators/__init__.py")


def section(content, key):
    return next(block["data"] for block in content["blocks"] if block["data"].get("section_key") == key)


class BriefingValidationTests(unittest.TestCase):
    def setUp(self):
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json"
        if not path.exists():
            self.skipTest("Amostra IQB ausente")
        self.content = json.loads(path.read_text(encoding="utf-8"))

    def render(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            path = folder / "input.json"
            path.write_text(json.dumps(self.content), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path),
                                     "--out-dir", str(folder / "output"), "--formats", "md"],
                                    capture_output=True, text=True)
            if result.returncode:
                self.assertFalse((folder / "output").exists(), "Falha deve ocorrer antes de criar arquivos")
            return result

    def test_missing_nested_citation_in_partial_content(self):
        section(self.content, "scores")["dimensions"]["clarity"]["items"][0]["citation_id"] = "NAO-EXISTE"
        self.content["metadata"]["completeness"] = "partial"
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("citações aninhadas", result.stderr)

    def test_empty_briefing_known_absence_uses_real_iqb_calculation(self):
        iqb = load_module("iqb_known_absence", ROOT.parent / "avaliacao-briefing-iqb/scripts/iqb.py")
        data = section(self.content, "scores")
        evaluations = {}
        for dimension, detail in data["dimensions"].items():
            for item in detail["items"]:
                item["answer"] = False
                item["evidence"] = "Ausência conhecida: briefing fictício examinado e vazio."
                item["evidence_source"] = "absent"
            evaluations[dimension] = [{"criterion_id": item["criterion_id"], "answer": item["answer"],
                                       "evidence": item["evidence"]} for item in detail["items"]]
        calculated = iqb.calculate_iqb_from_evaluations(evaluations)
        for dimension, result in calculated["scores"].items():
            data["dimensions"][dimension].update(result)
            data["dimensions"][dimension]["veto_detail"] = "Veto fictício por ausência conhecida no briefing vazio."
            data["dimensions"][dimension]["justification"] = "Todos os critérios foram examinados no exemplo vazio."
        data["anti_clustering"].update(triggered=calculated["anti_clustering"]["triggered"],
                                       original_scores=calculated["anti_clustering"]["original_scores"],
                                       span=calculated["span"],
                                       re_evaluation_notes="Reauditoria fictícia dos quarenta critérios confirmou a ausência conhecida de conteúdo.")
        section(self.content, "iqb").update(score=calculated["iqb_score"], classification=calculated["classification"],
                                             diagnosis=calculated["diagnosis"])
        section(self.content, "strengths")["items"] = []
        section(self.content, "provocations")["items"] = []
        self.content["summary"] = "Briefing fictício examinado e vazio; nenhum ponto forte sustentado ou pergunta relevante registrado."
        self.assertEqual(sum(len(items) for items in evaluations.values()), 40)
        self.assertTrue(all(item["answer"] is False for items in evaluations.values() for item in items))
        self.assertEqual(calculated["iqb_score"], 1.0)
        self.assertEqual(calculated["classification"], "Insuficiente")
        self.assertTrue(all(detail["veto_triggered"] for detail in calculated["scores"].values()))
        original = copy.deepcopy(self.content)
        self.assertEqual(validators.run(self.content), [])
        exported = self.render()
        self.assertEqual(exported.returncode, 0, exported.stderr)
        self.assertEqual(self.content, original)

    def test_original_sample_is_valid_and_unchanged(self):
        original = copy.deepcopy(self.content)
        self.assertEqual(validators.run(self.content), [])
        self.assertEqual(self.content, original)

    def test_inconsistent_iqb_and_classification(self):
        section(self.content, "iqb").update(score=1, classification="Excelente")
        errors = validators.run(self.content)
        self.assertTrue(any("iqb.score" in error for error in errors))
        self.assertTrue(any("iqb.classification" in error for error in errors))

    def test_duplicate_criterion_id(self):
        section(self.content, "scores")["dimensions"]["clarity"]["items"][1]["criterion_id"] = "CLA-01"
        errors = validators.run(self.content)
        self.assertTrue(any("criterion_id" in error and "CLA-01" in error and "CLA-02" in error for error in errors))

    def test_veto_caps_final_score(self):
        detail = section(self.content, "scores")["dimensions"]["evidence"]
        detail["items"][5]["answer"] = False
        detail["veto_triggered"] = True
        self.assertTrue(any("scores.evidence.final_score" in error for error in validators.run(self.content)))

    def test_tampered_yes_count(self):
        section(self.content, "scores")["dimensions"]["clarity"]["yes_count"] = 9
        self.assertTrue(any("scores.clarity.yes_count" in error for error in validators.run(self.content)))

    def test_renderer_rejects_inconsistent_iqb(self):
        section(self.content, "iqb")["score"] = 1
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Inconsistência semântica", result.stderr)

    def test_parity_with_iqb_script(self):
        path = ROOT.parent / "avaliacao-briefing-iqb/scripts/iqb.py"
        if not path.exists():
            self.skipTest("Script IQB ausente")
        iqb = load_module("iqb", path)
        validator = load_module("briefing_validator", ROOT / "scripts/validators/briefing_validation.py")
        for name in ("YES_COUNT_TO_RAW_SCORE", "VETO_ITEM_IDS", "VETO_MAX_SCORES", "RAW_SCORE_TO_LABEL"):
            self.assertEqual(getattr(validator, name), getattr(iqb, name), name)

    def test_tampered_anti_clustering(self):
        section(self.content, "scores")["anti_clustering"].update(span=0, triggered=True)
        errors = validators.run(self.content)
        self.assertTrue(any("anti_clustering.span" in error for error in errors))
        self.assertTrue(any("anti_clustering.triggered" in error for error in errors))

    def test_partial_content_skips_semantics_but_default_runs_them(self):
        section(self.content, "iqb")["score"] = 1
        self.content["metadata"]["completeness"] = "partial"
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)
        del self.content["metadata"]["completeness"]
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Inconsistência semântica", result.stderr)

    def test_nested_citation_list(self):
        item = section(self.content, "scores")["dimensions"]["clarity"]["items"][0]
        item["details"] = {"sources": [{"citation_ids": ["FIC-01", "NAO-EXISTE"]}]}
        self.content["metadata"]["completeness"] = "partial"
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("citações aninhadas", result.stderr)
        item["details"]["sources"][0]["citation_ids"] = ["FIC-01"]
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)


class LearningCardValidationTests(unittest.TestCase):
    def test_link_cannot_reference_learning_card_itself(self):
        content = {"deliverable_type": "learning_card", "metadata": {
            "artifact_id": "LC-01", "test_card_id": "LC-01", "test_card_version": "1"}}
        self.assertTrue(any("test_card_id" in error for error in validators.run(content)))
        content["metadata"]["test_card_id"] = "TC-01"
        original = copy.deepcopy(content)
        self.assertEqual(validators.run(content), [])
        self.assertEqual(content, original)


class PotentialValidationTests(unittest.TestCase):
    def setUp(self):
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/innovation_potential_assessment/input.json"
        if not path.exists():
            self.skipTest("Amostra de potencial ausente")
        self.content = json.loads(path.read_text(encoding="utf-8"))

    def test_original_sample_is_valid_and_unchanged(self):
        original = copy.deepcopy(self.content)
        self.assertEqual(validators.run(self.content), [])
        self.assertEqual(self.content, original)

    def test_returned_scores_roundtrip_precision(self):
        score = load_module("score_precision", ROOT.parent / "potencial-inovacao/scripts/score.py")
        cases = [(69.91, 69.91, 69.95, 70.04, 70.04),
                 (24.125, 75.999, 43.345, 0.005, 99.994)]
        cases += [(value,) * 5 for value in (0, 39.9, 40, 40.1, 69.9, 70, 70.1, 100)]
        for values in cases:
            with self.subTest(values=values):
                result = score.calculate_innovation_score({
                    criterion["key"]: {"score": value, "justification": "Exemplo fictício"}
                    for criterion, value in zip(score.CRITERIA, values)
                })
                content = copy.deepcopy(self.content)
                data = section(content, "scores")
                data["rows"] = [{"criterion": key, "score": note["score"],
                                 "weight": result["criteria_weights"][key],
                                 "justification": note["justification"]}
                                for key, note in result["scores"].items()]
                data["overall_score"] = result["overall_score"]
                data["classification"] = result["classification"]
                self.assertEqual(validators.run(content), [])
                if values == cases[0]:
                    with tempfile.TemporaryDirectory() as temp:
                        folder = Path(temp)
                        path = folder / "input.json"
                        path.write_text(json.dumps(content), encoding="utf-8")
                        exported = subprocess.run([sys.executable, str(SCRIPT), str(path),
                                                   "--out-dir", str(folder / "output"), "--formats", "md"],
                                                  capture_output=True, text=True)
                        self.assertEqual(exported.returncode, 0, exported.stderr)

    def test_changed_classification(self):
        section(self.content, "scores")["classification"] = "priorizar"
        self.assertTrue(any("scores.classification" in error for error in validators.run(self.content)))

    def test_changed_weight(self):
        section(self.content, "scores")["rows"][0]["weight"] = 0.50
        self.assertTrue(any("weight" in error for error in validators.run(self.content)))

    def test_duplicate_criterion(self):
        section(self.content, "scores")["rows"][1]["criterion"] = "impact"
        self.assertTrue(any("criterion" in error and "duplicados" in error for error in validators.run(self.content)))

    def test_parity_with_score_script(self):
        path = ROOT.parent / "potencial-inovacao/scripts/score.py"
        if not path.exists():
            self.skipTest("Script de potencial ausente")
        score = load_module("score", path)
        validator = load_module("potential_validator", ROOT / "scripts/validators/innovation_potential_assessment.py")
        self.assertEqual(validator.WEIGHTS, {item["key"]: item["weight"] for item in score.CRITERIA})
        data = section(self.content, "scores")
        result = score.calculate_innovation_score({row["criterion"]: {
            "score": row["score"], "justification": row["justification"],
        } for row in data["rows"]})
        self.assertEqual(data["overall_score"], result["overall_score"])
        for value in (0, 39.9, 40, 69.9, 70, 100):
            with self.subTest(value=value):
                result = score.calculate_innovation_score({key: {"score": value, "justification": "x"}
                                                          for key in validator.WEIGHTS})
                self.assertEqual(validator.classify(result["overall_score"]), result["classification"])

    def test_parity_with_score_script_on_random_scores(self):
        path = ROOT.parent / "potencial-inovacao/scripts/score.py"
        if not path.exists():
            self.skipTest("Script de potencial ausente")
        score = load_module("score", path)
        rng = random.Random(20260928)
        for _ in range(2000):
            notes = {item["key"]: {"score": rng.choice([rng.randint(0, 100), round(rng.uniform(0, 100), 1)]),
                                   "justification": "x"} for item in score.CRITERIA}
            result = score.calculate_innovation_score(notes)
            data = section(self.content, "scores")
            data["rows"] = [{"criterion": key, "score": note["score"], "weight": result["criteria_weights"][key],
                             "justification": "x"} for key, note in notes.items()]
            data["overall_score"] = result["overall_score"]
            data["classification"] = result["classification"]
            self.assertEqual(validators.run(self.content), [], notes)

    def test_changed_total(self):
        section(self.content, "scores")["overall_score"] = 80
        self.assertTrue(any("overall_score" in error for error in validators.run(self.content)))

    def test_whitespace_justification(self):
        section(self.content, "scores")["rows"][0]["justification"] = "   "
        self.assertTrue(any("justification" in error for error in validators.run(self.content)))

    def test_schema_and_semantic_rejections_before_output(self):
        for case, message in [("boolean", "Conteúdo inválido"), ("missing", "Conteúdo inválido"),
                              ("duplicate_block", "Conteúdo inválido"),
                              ("total", "Inconsistência semântica")]:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp:
                content = copy.deepcopy(self.content)
                data = section(content, "scores")
                if case == "boolean":
                    data["rows"][0]["score"] = True
                elif case == "missing":
                    content["blocks"] = [b for b in content["blocks"] if b["data"].get("section_key") != "scores"]
                elif case == "duplicate_block":
                    block = copy.deepcopy(next(b for b in content["blocks"] if b["id"] == "scores"))
                    block["id"] = "scores-copy"
                    content["blocks"].append(block)
                else:
                    data["overall_score"] = 80
                folder = Path(temp)
                path = folder / "input.json"
                path.write_text(json.dumps(content), encoding="utf-8")
                result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--out-dir",
                                         str(folder / "output"), "--formats", "md"], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertFalse((folder / "output").exists())


if __name__ == "__main__":
    unittest.main()
