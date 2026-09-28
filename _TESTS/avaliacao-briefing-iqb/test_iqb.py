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
