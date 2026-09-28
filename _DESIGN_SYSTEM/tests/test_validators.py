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


if __name__ == "__main__":
    unittest.main()
