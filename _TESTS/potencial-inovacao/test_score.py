from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "potencial-inovacao/scripts/score.py"
spec = importlib.util.spec_from_file_location("score", SCRIPT)
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)
KEYS = [criterion["key"] for criterion in score.CRITERIA]


def scores(value=80, justification="Evidência registrada"):
    return {key: {"score": value, "justification": justification} for key in KEYS}


class ScoreTests(unittest.TestCase):
    def test_published_scores_drive_total_and_classification(self):
        values = (69.91, 69.91, 69.95, 70.04, 70.04)
        result = score.calculate_innovation_score({
            key: {"score": value, "justification": "Exemplo fictício"}
            for key, value in zip(KEYS, values)
        })
        self.assertEqual([item["score"] for item in result["scores"].values()],
                         [69.9, 69.9, 70.0, 70.0, 70.0])
        self.assertEqual(result["overall_score"], 69.9)
        self.assertEqual(result["classification"], "monitorar")

    def test_two_and_three_decimal_scores_publish_one_decimal(self):
        for value, published, classification in [(42.14, 42.1, "monitorar"),
                                                  (39.949, 39.9, "arquivar"),
                                                  (69.951, 70.0, "priorizar")]:
            with self.subTest(value=value):
                result = score.calculate_innovation_score(scores(value))
                self.assertEqual([note["score"] for note in result["scores"].values()], [published] * 5)
                self.assertEqual(result["overall_score"], published)
                self.assertEqual(result["classification"], classification)

    def test_boolean_is_rejected(self):
        with self.assertRaises(ValueError):
            score.calculate_innovation_score(scores(True, "x"))

    def test_empty_justification_is_incomplete(self):
        result = score.calculate_innovation_score(scores(80, ""))
        self.assertEqual(result["status"], "incomplete")
        self.assertIsNone(result["classification"])
        self.assertIsNone(result["overall_score"])
        self.assertEqual(result["missing_justification"], KEYS)
        self.assertEqual(result["missing_criteria"], [])

    def test_whitespace_justification_is_incomplete(self):
        result = score.calculate_innovation_score(scores(80, "   "))
        self.assertEqual(result["status"], "incomplete")
        self.assertIsNone(result["classification"])
        self.assertIsNone(result["overall_score"])
        self.assertEqual(result["missing_justification"], KEYS)

    def test_supported_scores_are_complete(self):
        result = score.calculate_innovation_score(scores())
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["overall_score"], 80.0)
        self.assertEqual(result["classification"], "priorizar")

    def test_supported_zero_is_valid(self):
        result = score.calculate_innovation_score(scores(0))
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["overall_score"], 0.0)
        self.assertEqual(result["classification"], "arquivar")

    def test_missing_criterion_is_incomplete(self):
        data = scores()
        del data["urgency"]
        result = score.calculate_innovation_score(data)
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["missing_criteria"], ["urgency"])
        self.assertIsNone(result["overall_score"])

    def test_numeric_string_is_rejected(self):
        with self.assertRaises(ValueError):
            score.calculate_innovation_score(scores("80"))

    def test_out_of_range_and_nan_are_rejected(self):
        for value in (100.5, float("nan")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                score.calculate_innovation_score(scores(value))

    def test_classification_boundaries(self):
        for value, classification in [(0, "arquivar"), (39.9, "arquivar"), (40.0, "monitorar"),
                                       (40.1, "monitorar"), (69.9, "monitorar"), (70.0, "priorizar"),
                                       (70.1, "priorizar"), (100, "priorizar")]:
            with self.subTest(value=value):
                result = score.calculate_innovation_score(scores(value))
                self.assertEqual(result["overall_score"], value)
                self.assertEqual(result["classification"], classification)

    def test_cli_file_success_and_boolean_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "notas.json"
            for value, code, status in [(80, 0, "complete"), (True, 2, "error")]:
                with self.subTest(value=value):
                    path.write_text(json.dumps(scores(value)), encoding="utf-8")
                    result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, code, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["status"], status)

    def test_weighted_contributions_and_version(self):
        result = score.calculate_innovation_score(scores())
        self.assertEqual(result["weighted"], {
            "impact": 24.0, "viability": 20.0, "strategic_alignment": 16.0,
            "urgency": 12.0, "innovation": 8.0,
        })
        self.assertEqual(result["rubric_version"], "1.2.0-portable")

    def test_cli_stdin(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "-"],
                                input=json.dumps(scores()), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["classification"], "priorizar")


if __name__ == "__main__":
    unittest.main()
