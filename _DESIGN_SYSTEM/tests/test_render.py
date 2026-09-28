from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document
from pypdf import PdfReader
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render.py"


def content(kind: str, artifact: str) -> dict:
    blocks = [
        {"id": "h-1", "type": "heading", "data": {"text": "Seção principal", "level": 2}},
        {"id": "p-1", "type": "paragraph", "data": {"text": "Evidência resumida e verificável."}, "citation_ids": ["F01"]},
        {"id": "t-1", "type": "table", "data": {"headers": ["Medida", "Valor"], "rows": [["Casos", "12"]]}, "export": {"csv": True, "variant_key": "medidas"}},
    ]
    return {
        "schema_version": "1.0.0", "deliverable_type": kind, "locale": "pt-BR",
        "title": "Avaliação de exemplo", "summary": "Resumo curto.", "blocks": blocks,
        "citations": [{"id": "F01", "source_id": "documento-1", "locator": "p. 2"}],
        "metadata": {"artifact_id": artifact, "content_version": "1.0.0", "completeness": "partial"},
    }


class TableRowsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("render", SCRIPT)
        cls.render = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.render)

    def test_column_key_differs_from_label(self):
        self.assertEqual(self.render.table_rows({"data": {
            "columns": [{"key": "count", "label": "Quantidade"}],
            "rows": [{"count": 12}],
        }}), (["Quantidade"], [["12"]]))

    def test_reordered_columns(self):
        self.assertEqual(self.render.table_rows({"data": {
            "columns": [{"key": "b", "label": "B"}, {"key": "a", "label": "A"}],
            "rows": [{"a": 1, "b": 2}],
        }}), (["B", "A"], [["2", "1"]]))

    def test_zero_and_false_are_preserved(self):
        for value, expected in [(0, "0"), (False, "False")]:
            with self.subTest(value=value):
                self.assertEqual(self.render.table_rows({"data": {
                    "columns": [{"key": "count", "label": "Quantidade"}],
                    "rows": [{"count": value}],
                }}), (["Quantidade"], [[expected]]))

    def test_missing_field_is_empty(self):
        self.assertEqual(self.render.table_rows({"data": {
            "columns": [{"key": "count", "label": "Quantidade"}], "rows": [{}],
        }}), (["Quantidade"], [[""]]))

    def test_simple_headers_and_list_rows(self):
        self.assertEqual(self.render.table_rows({"data": {
            "headers": ["Medida", "Valor"], "rows": [["Casos", "12"]],
        }}), (["Medida", "Valor"], [["Casos", "12"]]))

    def test_string_headers_with_object_rows(self):
        self.assertEqual(self.render.table_rows({"data": {
            "headers": ["x"], "rows": [{"x": "v"}],
        }}), (["x"], [["v"]]))

    def test_column_without_label(self):
        self.assertEqual(self.render.table_rows({"data": {
            "columns": [{"key": "k"}], "rows": [{"k": "v"}],
        }}), (["k"], [["v"]]))


class RenderTests(unittest.TestCase):
    def render(self, item: dict, formats: str, folder: Path):
        source = folder / "input.json"
        source.write_text(json.dumps(item, ensure_ascii=False))
        result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder), "--formats", formats], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_portrait_and_landscape_and_semantic_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            result = self.render(content("innovation_potential_assessment", "potencial-01"), "html,pdf,docx,md,txt,csv", folder)
            self.assertEqual(len(PdfReader(str(folder / "potencial-01-v1.0.0.pdf")).pages), 1)
            page = PdfReader(str(folder / "potencial-01-v1.0.0.pdf")).pages[0]
            self.assertLess(float(page.mediabox.width), float(page.mediabox.height))
            doc = Document(folder / "potencial-01-v1.0.0.docx")
            self.assertIn("Seção principal", "\n".join(p.text for p in doc.paragraphs))
            self.assertIn("Fontes: F01", "\n".join(p.text for p in doc.paragraphs))
            self.assertIn("Seção principal", (folder / "potencial-01-v1.0.0.md").read_text())
            self.assertIn("Seção principal", (folder / "potencial-01-v1.0.0.html").read_text())
            self.assertIn("medidas", " ".join(result["files"]))
            first = (folder / "potencial-01-v1.0.0.html").read_bytes()
            self.render(content("innovation_potential_assessment", "potencial-01"), "html,pdf,docx,md,txt,csv", folder)
            self.assertEqual(first, (folder / "potencial-01-v1.0.0.html").read_bytes())

            self.render(content("four_d_workshop_record", "workshop-4d-01"), "pdf", folder)
            page = PdfReader(str(folder / "workshop-4d-01-v1.0.0.pdf")).pages[0]
            self.assertGreater(float(page.mediabox.width), float(page.mediabox.height))

    def test_card_is_one_page_and_presentation_is_editable(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            card = content("test_card", "TC-01")
            card["blocks"] = [
                {"id": f"f-{i}", "type": "paragraph", "data": {"section_key": key, "text": label}}
                for i, (key, label) in enumerate(zip(("hypothesis", "test", "measure", "criteria"),
                                                   ("Acreditamos que", "Para verificar, vamos", "Vamos medir", "Estaremos certos se")), 1)
            ]
            self.render(card, "pdf,docx,md", folder)
            self.assertEqual(len(PdfReader(str(folder / "TC-01-v1.0.0.pdf")).pages), 1)
            self.assertIn("Acreditamos que", (folder / "TC-01-v1.0.0.md").read_text())
            presentation = content("executive_presentation", "apresentacao-01")
            self.render(presentation, "pptx,pdf", folder)
            prs = Presentation(folder / "apresentacao-01-v1.0.0.pptx")
            self.assertGreaterEqual(len(prs.slides), 2)
            self.assertEqual(len(PdfReader(str(folder / "apresentacao-01-v1.0.0.pdf")).pages), len(prs.slides))
            self.assertTrue(any("Seção principal" in shape.text for slide in prs.slides for shape in slide.shapes if shape.has_text_frame))
            self.assertTrue(any("Fontes" in shape.text for shape in prs.slides[-1].shapes if shape.has_text_frame))

    def test_rejects_wrong_orientation(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            item = content("innovation_scorecard", "score-01")
            item["metadata"]["orientation"] = "portrait"
            source = folder / "input.json"
            source.write_text(json.dumps(item))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("orientation", result.stderr)

    def test_complete_cards_require_four_fields_and_learning_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            card = content("test_card", "TC-02")
            card["metadata"]["completeness"] = "complete"
            card["blocks"] = [
                {"id": key, "type": "paragraph", "data": {"section_key": key, "text": key}}
                for key in ("hypothesis", "test", "measure", "criteria")
            ]
            self.render(card, "md", folder)
            card["blocks"].pop()
            source = folder / "input.json"
            source.write_text(json.dumps(card))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder), "--formats", "md"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Conteúdo inválido", result.stderr)

            learning = content("learning_card", "LC-02")
            learning["metadata"]["completeness"] = "complete"
            learning["blocks"] = [
                {"id": key, "type": "paragraph", "data": {"section_key": key, "text": key}}
                for key in ("hypothesis", "observations", "learning", "action")
            ]
            source.write_text(json.dumps(learning))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder), "--formats", "md"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            learning["blocks"][1]["citation_ids"] = ["F01"]
            self.render(learning, "md", folder)

    def test_every_type_has_schema_and_complete_sections_are_enforced(self):
        profiles = json.loads((ROOT / "profiles.json").read_text())
        sections = json.loads((ROOT / "response-sections.json").read_text())
        for kind, profile in profiles["types"].items():
            self.assertTrue(profile.get("schema"), kind)
            self.assertTrue((ROOT / "contracts" / profile["schema"]).is_file(), kind)
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for kind, keys in sections.items():
                item = content(kind, kind)
                item["metadata"]["completeness"] = "complete"
                item["blocks"] = [
                    {"id": key, "type": "paragraph", "data": {"section_key": key, "text": "Síntese registrada."}, "citation_ids": ["F01"]}
                    for key in keys
                ]
                if kind == "innovation_potential_assessment":
                    item["blocks"].insert(0, {
                        "id": "scores", "type": "table", "data": {
                            "section_key": "scores", "columns": ["criterion", "score", "weight", "justification"],
                            "rows": [{"criterion": key, "score": 80, "weight": weight, "justification": "Evidência de teste."}
                                     for key, weight in [("impact", 0.30), ("viability", 0.25),
                                                         ("strategic_alignment", 0.20), ("urgency", 0.15), ("innovation", 0.10)]],
                            "overall_score": 80.0, "classification": "priorizar",
                        },
                    })
                self.render(item, "md", folder)
                item["blocks"].pop()
                source = folder / "input.json"
                source.write_text(json.dumps(item))
                result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder), "--formats", "md"], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0, kind)


if __name__ == "__main__":
    unittest.main()
