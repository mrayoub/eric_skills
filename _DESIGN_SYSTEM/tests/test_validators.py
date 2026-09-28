from __future__ import annotations

import copy
import importlib.util
import json
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


if __name__ == "__main__":
    unittest.main()
