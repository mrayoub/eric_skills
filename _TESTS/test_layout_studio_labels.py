"""O Layout Studio mostra os mesmos rótulos em português do renderizador."""
from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LayoutStudioLabelsTests(unittest.TestCase):
    def test_labels_match_renderer(self) -> None:
        spec = importlib.util.spec_from_file_location("render_labels", ROOT / "_DESIGN_SYSTEM/scripts/render.py")
        render = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(render)
        page = (ROOT / "_LAYOUT_STUDIO/index.html").read_text(encoding="utf-8")
        match = re.search(r"const DELIVERABLE_LABELS = (\{.*?\});", page, re.S)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)), render.DELIVERABLE_LABELS)


if __name__ == "__main__":
    unittest.main()
