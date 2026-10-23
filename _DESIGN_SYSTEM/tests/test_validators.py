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


class ExecutivePresentationRulesTests(unittest.TestCase):
    def setUp(self):
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/executive_presentation/input.json"
        self.content = json.loads(path.read_text(encoding="utf-8"))

    def test_complete_sample_is_valid(self):
        self.assertEqual(validators.run(self.content), [])

    def test_generic_heading_is_rejected(self):
        self.content["blocks"][0]["data"]["text"] = "Contexto"
        self.assertTrue(any("título de slide" in error for error in validators.run(self.content)))

    def test_long_heading_is_rejected(self):
        self.content["blocks"][0]["data"]["text"] = " ".join(["palavra"] * 15)
        self.assertTrue(any("título de slide" in error for error in validators.run(self.content)))

    def test_dense_section_is_rejected(self):
        for count, words in ((5, 1), (4, 18)):
            with self.subTest(count=count, words=words):
                item = copy.deepcopy(self.content)
                extra = [{"id": f"extra-{i}", "type": "paragraph",
                          "data": {"text": " ".join(["texto"] * words)}} for i in range(count)]
                item["blocks"][1:1] = extra
                self.assertTrue(any("divida em mais slides" in error for error in validators.run(item)))

    def test_missing_or_long_summary_is_rejected(self):
        for summary in ("", " ".join(["palavra"] * 40)):
            with self.subTest(summary=summary):
                item = copy.deepcopy(self.content)
                item["summary"] = summary
                self.assertTrue(any("summary:" in error for error in validators.run(item)))

    def test_partial_presentation_bypasses_semantic_rules(self):
        self.content["metadata"]["completeness"] = "partial"
        self.content["blocks"][0]["data"]["text"] = "Contexto"
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            path = folder / "input.json"
            path.write_text(json.dumps(self.content), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--out-dir", str(folder / "out"),
                                     "--formats", "md"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


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


class ObjectivityValidatorTests(unittest.TestCase):
    def test_absolute_vocabulary_flagged(self):
        content = {"deliverable_type": "x", "citations": [], "blocks": [
            {"id": "b1", "type": "paragraph", "data": {"text": "Isso comprovadamente funciona."}},
        ]}
        self.assertTrue(any("vocabulário absoluto" in e for e in validators.run(content)))

    def test_numeric_claim_without_citation_flagged(self):
        content = {"deliverable_type": "x", "citations": [], "blocks": [
            {"id": "b1", "type": "metric", "data": {"value": "Redução de 42% no tempo médio"}},
        ]}
        self.assertTrue(any("sem citation_ids" in e for e in validators.run(content)))

    def test_numeric_claim_with_citation_passes(self):
        content = {"deliverable_type": "x", "citations": [{"id": "c1", "source": "planilha.xlsx"}],
                   "blocks": [{"id": "b1", "type": "metric", "citation_ids": ["c1"],
                               "data": {"value": "Redução de 42% no tempo médio"}}]}
        self.assertEqual(validators.run(content), [])

    def test_heading_and_table_not_in_scope(self):
        content = {"deliverable_type": "x", "citations": [], "blocks": [
            {"id": "b1", "type": "heading", "data": {"text": "Resultados de 2026"}},
        ]}
        self.assertEqual(validators.run(content), [])


class CdtValidationTests(unittest.TestCase):
    def setUp(self):
        samples = ROOT.parent / "_SAMPLES_ENTREGAVEIS"
        self.content = json.loads((samples / "cdt/input.json").read_text(encoding="utf-8"))
        self.analysis = json.loads((samples / "cdt_analysis/input.json").read_text(encoding="utf-8"))
        self.cdt = load_module("cdt_validator", ROOT / "scripts/validators/cdt.py")

    def block(self, key, content=None):
        return next(block for block in (content or self.content)["blocks"] if block["data"].get("section_key") == key)

    def errors(self, content=None):
        return validators.run(content or self.content)

    def text(self, key, value, content=None):
        self.block(key, content)["data"]["text"] = value

    def check(self):
        """Roda o checar_cdt.py da skill sobre os dois arquivos."""
        script = ROOT.parent / "gerador-cdt/scripts/checar_cdt.py"
        with tempfile.TemporaryDirectory() as temp:
            paths = [Path(temp) / "cdt.json", Path(temp) / "analise.json"]
            for path, content in zip(paths, (self.content, self.analysis)):
                path.write_text(json.dumps(content), encoding="utf-8")
            result = subprocess.run([sys.executable, str(script), *map(str, paths)], capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout)

    def with_gap(self, readiness="Com lacunas a preencher: horas mensais de hoje nos Benefícios."):
        """Benefícios com lacuna, os dois arquivos parciais e a análise listando a lacuna."""
        self.text("benefits", "Reduz as horas mensais da nossa equipe com complementos de "
                              "[COMPLETAR: horas mensais gastas hoje] para 15.")
        for content in (self.content, self.analysis):
            content["metadata"]["completeness"] = "partial"
        self.text("readiness", readiness, self.analysis)
        self.text("data_to_obtain", "Lacunas a preencher, em ordem de prioridade:", self.analysis)

    def test_samples_are_valid(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.errors(self.analysis), [])
        self.assertEqual(self.check(), (0, self.check()[1]))

    def test_official_document_has_only_the_four_jira_fields(self):
        keys = [block["data"]["section_key"] for block in self.content["blocks"] if block["type"] == "paragraph"]
        self.assertEqual(keys, ["jira_title", "description", "justification", "benefits"])
        self.content["blocks"].append({"id": "theme", "type": "paragraph", "citation_ids": ["FIC-01"],
                                       "data": {"section_key": "theme", "text": "Governança e Gestão"}})
        self.assertTrue(any("só Rótulo Epic, Descrição, Justificativa e Benefícios" in error for error in self.errors()))

    def test_epic_label_comes_first(self):
        blocks = self.content["blocks"]
        blocks[:2], blocks[2:4] = blocks[2:4], blocks[:2]
        self.assertTrue(any("fora de ordem" in error for error in self.errors()))

    def test_epic_label_names_the_technology_not_a_person(self):
        self.text("jira_title", "Assistente conversacional para consulta de pendências")
        errors = " ".join(self.errors())
        self.assertIn("sugere uma pessoa", errors)
        self.assertIn("artefato tecnológico", errors)
        self.text("jira_title", "Interface conversacional com IA para consulta de pendências no sistema X")
        self.assertEqual(self.errors(), [])

    def test_description_has_the_five_questions_in_one_block(self):
        description = self.block("description")["data"]["text"]
        self.text("description", description.replace("**Como o processo funciona hoje?**", "**Processo atual**"))
        self.assertTrue(any("Como o processo funciona hoje?" in error for error in self.errors()))

    def test_description_questions_follow_the_communique_order(self):
        description = self.block("description")["data"]["text"]
        first, rest = description.split("**Quem é impactado?**")
        self.text("description", "**Quem é impactado?**" + rest + "\n\n" + first)
        self.assertTrue(any("ordem do comunicado" in error for error in self.errors()))

    def test_every_question_needs_an_answer(self):
        description = self.block("description")["data"]["text"]
        start = description.index("**Quem é impactado?**") + len("**Quem é impactado?**")
        end = description.index("**Como o processo funciona hoje?**")
        self.text("description", description[:start] + "\n\n" + description[end:])
        self.assertTrue(any("pergunta sem resposta" in error for error in self.errors()))

    def test_priorities_split_into_three_groups(self):
        description = self.block("description")["data"]["text"]
        self.text("description", description.split("**Essencial**")[0] + "Primeiro o formulário.")
        self.assertTrue(any("essencial, importante e fora do escopo" in error for error in self.errors()))

    def test_missing_data_becomes_a_gap_to_fill(self):
        self.with_gap()
        code, report = self.check()
        self.assertEqual(code, 0, report)
        self.assertEqual(sorted(report["gaps"]), ["benefits"])

    def test_gap_needs_partial_state_in_both_files(self):
        self.text("benefits", "Reduz para 15 as horas mensais de [COMPLETAR: horas mensais gastas hoje].")
        self.assertTrue(any("marque completeness partial" in error for error in self.errors()))

    def test_open_points_are_not_written_in_the_cdt(self):
        self.text("benefits", "Reduz as horas mensais da equipe; meta a confirmar com a gestão.")
        self.assertTrue(any("ponto em aberto" in error for error in self.errors()))

    def test_cdt_does_not_ask_questions_outside_the_subtitles(self):
        self.text("justification", "Retrabalho contínuo: quantas horas ainda vamos perder?")
        self.assertTrue(any("pergunta no texto" in error for error in self.errors()))

    def test_gaps_must_reach_the_analysis(self):
        self.with_gap()
        self.text("data_to_obtain", "Nenhum dado pendente.", self.analysis)
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertTrue(any("liste as lacunas" in error for error in report["errors"]))

    def test_analysis_states_the_gaps(self):
        self.with_gap("Pronta para envio.")
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertTrue(any("Com lacunas a preencher" in error for error in report["errors"]))

    def test_written_by_the_management_in_first_person(self):
        self.text("justification", "Retrabalho contínuo: a gestão da área segue sem visão dos prazos.")
        self.assertTrue(any("primeira pessoa" in error for error in self.errors()))

    def test_ai_sounding_expressions_are_rejected(self):
        self.text("benefits", self.block("benefits")["data"]["text"] + " Além disso, a solução é robusta.")
        self.assertTrue(any("cara de IA" in error for error in self.errors()))

    def test_both_files_declare_the_same_state(self):
        self.analysis["metadata"]["completeness"] = "partial"
        code, report = self.check()
        self.assertEqual(code, 1)
        self.assertTrue(any("mesmo estado" in error for error in report["errors"]))

    def test_field_without_source_or_pending_is_rejected(self):
        self.block("benefits").pop("citation_ids")
        self.assertTrue(any("sem fonte" in error and "benefits" in error for error in self.errors()))

    def test_jira_fields_do_not_cite_sources(self):
        self.text("benefits", self.block("benefits")["data"]["text"] + " Fonte: relatório final.")
        self.assertTrue(any("fonte citada em campo do Jira" in error for error in self.errors()))

    def test_markdown_only_in_description(self):
        self.text("justification", "- Retrabalho contínuo: horas da equipe.")
        self.assertTrue(any("Markdown fora da Descrição" in error for error in self.errors()))
        self.assertIn("**", self.block("description")["data"]["text"])

    def test_long_texts_are_rejected(self):
        self.text("benefits", "palavra " * 81)
        self.assertTrue(any("longos demais" in error for error in self.errors()))

    def test_rendered_cdt_is_plain_copy_and_paste(self):
        render = load_module("render_cdt", SCRIPT)
        shown = render.presentation_content(self.content)
        self.assertEqual(shown["citations"], [])
        self.assertFalse(any("citation_ids" in block for block in shown["blocks"]))
        self.assertIn("citation_ids", self.block("benefits"))
        markdown = render.render_md(shown)
        self.assertTrue(markdown.startswith("## Rótulo Epic"))
        self.assertNotIn("FIC-0", markdown)
        self.assertNotIn(self.content["title"], markdown)

    def test_analysis_highlights_checklist_and_priorities(self):
        keys = [block["data"]["section_key"] for block in self.analysis["blocks"] if block["type"] == "paragraph"]
        self.assertEqual(keys[:3], ["readiness", "publication_checklist", "data_to_obtain"])
        self.text("data_to_obtain", "Falta a regra de campos.", self.analysis)
        table = next(block for block in self.analysis["blocks"] if block["id"] == "data_to_obtain-table")
        table["data"]["headers"] = table["data"]["headers"][1:] + ["Prioridade"]
        self.assertTrue(any("coluna 'Prioridade' primeiro" in error for error in self.errors(self.analysis)))

    def test_checklist_needs_all_six_items_with_status(self):
        block = self.block("publication_checklist", self.analysis)
        block["data"]["text"] = "\n".join(line for line in block["data"]["text"].splitlines()
                                          if not line.startswith("- Responsáveis"))
        self.assertTrue(any("Responsáveis" in error for error in self.errors(self.analysis)))

    def test_rules_and_responsibles_are_answered_in_the_checklist(self):
        block = self.block("publication_checklist", self.analysis)
        block["data"]["text"] = "\n".join("- Responsáveis: atendido." if line.startswith("- Responsáveis") else line
                                          for line in block["data"]["text"].splitlines())
        self.assertTrue(any("'Responsáveis' não tem campo" in error for error in self.errors(self.analysis)))

    def test_checklist_gap_blocks_complete_version(self):
        block = self.block("publication_checklist", self.analysis)
        block["data"]["text"] = block["data"]["text"].replace("- Responsáveis: atendido.", "- Responsáveis: parcial.")
        self.assertTrue(any("checklist não atendidos" in error for error in self.errors(self.analysis)))

    def test_quality_review_requires_strengths_and_weaknesses(self):
        self.text("quality_review", "Pontos fortes: escopo claro.", self.analysis)
        self.assertTrue(any("Pontos fracos" in error for error in self.errors(self.analysis)))

    def test_sections_are_single_column_with_bold_in_html(self):
        render = load_module("render_single_column", SCRIPT)
        for kind in ("cdt", "cdt_analysis"):
            self.assertIn(kind, render.pdf_module().SINGLE_COLUMN_TYPES)
        tokens = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))
        profiles = json.loads((ROOT / "profiles.json").read_text(encoding="utf-8"))
        profile = render.validate(self.content, profiles)
        page = render.render_html(render.presentation_content(self.content), tokens, profile)
        self.assertNotIn("section-pair", page)
        self.assertIn("<strong>Essencial</strong>", page)
        self.assertNotIn("**", page)


if __name__ == "__main__":
    unittest.main()
