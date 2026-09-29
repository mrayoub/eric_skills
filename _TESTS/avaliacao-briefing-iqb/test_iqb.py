from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "avaliacao-briefing-iqb/scripts/iqb.py"
spec = importlib.util.spec_from_file_location("iqb", SCRIPT)
iqb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iqb)


def answers(value):
    prefixes = {"clarity": "CLA", "evidence": "EVI", "outcomes": "OUT", "actionability": "ACT"}
    return {
        dimension: [{"criterion_id": f"{prefix}-{index:02d}", "answer": value, "evidence": "x"}
                    for index in range(1, 11)]
        for dimension, prefix in prefixes.items()
    }


INVALID_EVIDENCE = [("missing", None), ("null", None), ("false", False), ("true", True),
                    ("zero", 0), ("number", 10), ("decimal", 10.5), ("list", []),
                    ("object", {}), ("empty", ""), ("whitespace", " \n\t ")]


class IqbTests(unittest.TestCase):
    def test_all_false_is_insufficient(self):
        result = iqb.calculate_iqb_from_evaluations(answers(False))
        self.assertEqual(result["iqb_score"], 1.0)
        self.assertEqual(result["classification"], "Insuficiente")

    def test_all_true_is_excellent(self):
        result = iqb.calculate_iqb_from_evaluations(answers(True))
        self.assertEqual(result["iqb_score"], 5.0)
        self.assertEqual(result["classification"], "Excelente")

    def test_missing_evi_03_is_rejected(self):
        data = answers(True)
        del data["evidence"][2]
        with self.assertRaises(ValueError):
            iqb.calculate_iqb_from_evaluations(data)

    def test_string_answer_is_rejected(self):
        data = answers(True)
        data["clarity"][0]["answer"] = "yes"
        with self.assertRaises(ValueError):
            iqb.calculate_iqb_from_evaluations(data)

    def test_evidence_requires_nonempty_string(self):
        for label, value in INVALID_EVIDENCE:
            with self.subTest(case=label):
                data = answers(True)
                if label == "missing":
                    del data["clarity"][0]["evidence"]
                else:
                    data["clarity"][0]["evidence"] = value
                with self.assertRaisesRegex(ValueError, "CLA-01: evidence or an explicit absence note is required"):
                    iqb.calculate_iqb_from_evaluations(data)

    def test_cli_null_evidence_is_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "respostas.json"
            for label, value in INVALID_EVIDENCE:
                data = answers(True)
                if label == "missing":
                    del data["clarity"][0]["evidence"]
                else:
                    data["clarity"][0]["evidence"] = value
                serialized = json.dumps(data)
                path.write_text(serialized, encoding="utf-8")
                for source in (str(path), "-"):
                    with self.subTest(case=label, source="stdin" if source == "-" else "file"):
                        process = subprocess.run([sys.executable, str(SCRIPT), source],
                                                 input=serialized if source == "-" else None,
                                                 capture_output=True, text=True)
                        self.assertEqual(process.returncode, 2, process.stderr)
                        result = json.loads(process.stdout)
                        self.assertEqual(set(result), {"status", "error"})
                        self.assertEqual(result["status"], "error")
                        self.assertIn("CLA-01", result["error"])
                        self.assertIn("evidence or an explicit absence note is required", result["error"])

    def test_explicit_absence_note_remains_valid_for_negative_answer(self):
        data = answers(False)
        note = "Não há fonte disponível para este critério"
        data["clarity"][0]["evidence"] = note
        result = iqb.calculate_iqb_from_evaluations(data)
        self.assertEqual(result, iqb.calculate_iqb_from_evaluations(answers(False)))
        self.assertIs(data["clarity"][0]["answer"], False)
        self.assertEqual(data["clarity"][0]["evidence"], note)

    def test_empty_evidence_is_rejected(self):
        data = answers(True)
        data["clarity"][0]["evidence"] = ""
        with self.assertRaises(ValueError):
            iqb.calculate_iqb_from_evaluations(data)

    def test_evidence_veto_caps_score_at_one(self):
        data = answers(True)
        data["evidence"][5]["answer"] = False
        result = iqb.calculate_iqb_from_evaluations(data)
        self.assertEqual(result["scores"]["evidence"]["final_score"], 1)
        self.assertIs(result["scores"]["evidence"]["veto_triggered"], True)

    def test_identical_scores_trigger_anti_clustering(self):
        result = iqb.calculate_iqb_from_evaluations(answers(True))
        self.assertEqual(result["span"], 0)
        self.assertIs(result["anti_clustering"]["triggered"], True)

    def test_cli_success_and_missing_item_error(self):
        complete = answers(True)
        incomplete = answers(True)
        del incomplete["evidence"][2]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "respostas.json"
            for data, code in [(complete, 0), (incomplete, 2)]:
                with self.subTest(code=code):
                    path.write_text(json.dumps(data), encoding="utf-8")
                    process = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                             capture_output=True, text=True)
                    self.assertEqual(process.returncode, code, process.stderr)
                    result = json.loads(process.stdout)
                    if code == 0:
                        self.assertEqual(result["iqb_score"], 5.0)
                        self.assertEqual(result["status"], "complete")
                        self.assertEqual(result["rubric_version"], iqb.IQB_RUBRIC_VERSION)
                        result.pop("status")
                        result.pop("rubric_version")
                        self.assertEqual(result, iqb.calculate_iqb_from_evaluations(data))
                    else:
                        self.assertEqual(result["status"], "error")
                        self.assertIn("error", result)
        process = subprocess.run([sys.executable, str(SCRIPT), "-"],
                                 input=json.dumps(complete), capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)["iqb_score"], 5.0)


if __name__ == "__main__":
    unittest.main()
