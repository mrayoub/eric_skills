from __future__ import annotations

import json
import copy
import importlib.util
import os
import re
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


def pdf_available() -> bool:
    try:
        import weasyprint
        return True
    except (ImportError, OSError):
        return False


def content(kind: str, artifact: str) -> dict:
    blocks = [
        {"id": "h-1", "type": "heading", "data": {"text": "Seção principal", "level": 2}},
        {"id": "p-1", "type": "paragraph", "data": {"text": "Evidência resumida e verificável."}, "citation_ids": ["F01"]},
        {"id": "t-1", "type": "table", "data": {"headers": ["Medida", "Valor"], "rows": [["Casos", "12"]]}, "export": {"csv": True, "variant_key": "medidas"}},
    ]
    if kind in ("test_card", "learning_card"):
        keys = ("hypothesis", "test", "measure", "criteria") if kind == "test_card" else ("hypothesis", "observations", "learning", "action")
        blocks = [{"id": key, "type": "paragraph", "data": {
            "section_key": key, "text": "Evidência resumida e verificável."}} for key in keys]
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


REQUIRED_SECTION_TYPES = ("four_d_workshop_record", "three_e_workshop_record", "three_e_report",
                          "five_c_workshop_record", "five_c_report", "innovation_scorecard")


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("required_sections_render", SCRIPT)
        cls.renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.renderer)
        cls.profiles = json.loads((ROOT / "profiles.json").read_text())
        cls.sections = json.loads((ROOT / "response-sections.json").read_text())

    def complete_section_document(self, kind):
        item = content(kind, kind)
        item["metadata"]["completeness"] = "complete"
        item["blocks"] = [{"id": key, "type": "paragraph", "data": {
            "section_key": key, "text": "Registro fictício " + key}, "citation_ids": ["F01"]}
            for key in self.sections[kind]]
        return item

    def render(self, item: dict, formats: str, folder: Path):
        source = folder / "input.json"
        source.write_text(json.dumps(item, ensure_ascii=False))
        result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder), "--formats", formats], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["unavailable"], {})
        return output

    def test_null_completeness_enforces_complete_validation(self):
        learning = self.card_document("learning_card", "partial")
        report = content("three_e_report", "invalid-report")
        potential = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/innovation_potential_assessment/input.json").read_text())
        next(block["data"] for block in potential["blocks"] if block["data"].get("section_key") == "scores")["overall_score"] = 80
        for original in (learning, report, potential):
            for state in ("complete", "missing", None):
                with self.subTest(kind=original["deliverable_type"], state=state):
                    item = copy.deepcopy(original)
                    if state == "missing":
                        item["metadata"].pop("completeness", None)
                    else:
                        item["metadata"]["completeness"] = state
                    before = copy.deepcopy(item)
                    with self.assertRaises(ValueError):
                        self.renderer.validate(item, self.profiles)
                    self.assertEqual(item, before)

    def test_editable_formats_show_identity_and_state(self):
        for kind in ("three_e_report", "learning_card", "executive_presentation"):
            item = self.card_document(kind, "partial") if kind == "learning_card" else content(kind, "identity-test")
            identity = f'ID {item["metadata"]["artifact_id"]} · versão 1.0.0 · Parcial'
            with tempfile.TemporaryDirectory() as temp:
                folder = Path(temp)
                editable = "pptx" if kind == "executive_presentation" else "docx"
                self.render(item, "md,txt," + editable, folder)
                stem = item["metadata"]["artifact_id"] + "-v1.0.0"
                for fmt in ("md", "txt", editable):
                    with self.subTest(kind=kind, format=fmt):
                        path = folder / f"{stem}.{fmt}"
                        if fmt == "docx":
                            text = "\n".join(p.text for p in Document(path).paragraphs)
                            self.assertIn(identity, text)
                        elif fmt == "pptx":
                            for slide in Presentation(path).slides:
                                text = "\n".join(shape.text for shape in slide.shapes if shape.has_text_frame)
                                self.assertIn(identity, text)
                        else:
                            self.assertIn(identity, path.read_text())

    def test_identity_for_all_states_and_supported_profiles(self):
        for kind in ("briefing_one_page", "three_e_report", "learning_card", "executive_presentation"):
            source = ROOT.parent / "_SAMPLES_ENTREGAVEIS" / kind / "input.json"
            original = json.loads(source.read_text())
            for state in ("partial", "inconclusive", "complete", "missing", None):
                with self.subTest(kind=kind, state=state), tempfile.TemporaryDirectory() as temp:
                    item = copy.deepcopy(original)
                    if state == "missing":
                        item["metadata"].pop("completeness", None)
                    else:
                        item["metadata"]["completeness"] = state
                    label = {"partial": "Parcial", "inconclusive": "Inconclusivo"}.get(state, "Completo")
                    identity = f'ID {item["metadata"]["artifact_id"]} · versão {item["metadata"]["content_version"]} · {label}'
                    before = copy.deepcopy(item)
                    self.renderer.validate(item, self.profiles)
                    folder = Path(temp)
                    has_pdf = pdf_available()
                    editable = "pptx" if kind == "executive_presentation" else "docx"
                    self.render(item, "md,txt,html," + editable + (",pdf" if has_pdf else ""), folder)
                    stem = item["metadata"]["artifact_id"] + "-v" + item["metadata"]["content_version"]
                    for fmt in ("md", "txt", "html"):
                        self.assertIn(identity, (folder / f"{stem}.{fmt}").read_text())
                    if editable == "docx":
                        self.assertIn(identity, "\n".join(p.text for p in Document(folder / f"{stem}.docx").paragraphs))
                    else:
                        presentation = Presentation(folder / f"{stem}.pptx")
                        for slide in presentation.slides:
                            footers = [shape for shape in slide.shapes if shape.has_text_frame and identity in shape.text]
                            self.assertEqual(len(footers), 1)
                            footer = footers[0]
                            self.assertLessEqual(footer.top + footer.height, presentation.slide_height)
                            self.assertLessEqual(footer.left + footer.width, presentation.slide_width)
                            other_text = [shape for shape in slide.shapes if shape.has_text_frame and shape.shape_id != footer.shape_id]
                            self.assertGreaterEqual(footer.top, max(shape.top + shape.height for shape in other_text))
                            self.assertEqual(footer.text_frame.paragraphs[0].font.name, "Roboto")
                            self.assertGreaterEqual(footer.text_frame.paragraphs[0].font.size.pt, 7.5)
                        html = (folder / f"{stem}.html").read_text()
                        self.assertEqual(html.count(f'<footer class="meta">{identity}</footer>'), len(presentation.slides))
                        self.assertTrue(any("Fontes" in shape.text for shape in presentation.slides[-1].shapes if shape.has_text_frame))
                    if has_pdf:
                        pdf = PdfReader(folder / f"{stem}.pdf")
                        for page in pdf.pages:
                            self.assertIn(identity, " ".join(page.extract_text().split()))
                        if kind == "learning_card":
                            self.assertEqual(len(pdf.pages), 1)
                            self.assertIn("Test Card sample-test-card v1.0.0", pdf.pages[0].extract_text())
                        if kind == "executive_presentation":
                            self.assertEqual(len(pdf.pages), len(presentation.slides))
                    canonical = json.loads((folder / f"{stem}.json").read_text())
                    self.assertEqual(canonical, before)
                    self.assertEqual(item, before)

    def test_identity_uses_only_provided_date(self):
        item = content("three_e_report", "dated-identity")
        before = copy.deepcopy(item)
        self.assertEqual(self.renderer.identity_line(item), "ID dated-identity · versão 1.0.0 · Parcial")
        self.assertEqual(item, before)
        item["metadata"]["date"] = "2026-08-21"
        self.assertEqual(self.renderer.identity_line(item), "ID dated-identity · versão 1.0.0 · Parcial · data 2026-08-21")
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.render(item, "md,txt,html,docx", folder)
            for fmt in ("md", "txt", "html"):
                self.assertIn("data 2026-08-21", (folder / f"dated-identity-v1.0.0.{fmt}").read_text())
            self.assertIn("data 2026-08-21", "\n".join(p.text for p in Document(folder / "dated-identity-v1.0.0.docx").paragraphs))

    def test_reader_labels_are_portuguese_and_canonical_keys_are_preserved(self):
        for kind, label in [
            ("experiment_plan", "Plano de experimentação"),
            ("test_card", "Cartão de teste"),
            ("executive_presentation", "Apresentação executiva"),
        ]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as folder:
                path = Path(folder)
                item = content(kind, "linguagem")
                result = self.render(item, "html", path)
                html_path = next(path / name for name in result["files"] if name.endswith(".html"))
                rendered = html_path.read_text()
                self.assertIn(f'<span class="eyebrow">{label}</span>', rendered)
                self.assertIn("Evidência resumida e verificável.", rendered)
                self.assertNotIn(f'>{kind.replace("_", " ")}</span>', rendered)
                if kind != "executive_presentation":
                    self.assertIn("Parcial", rendered)
                    self.assertNotIn("perfil report_portrait", rendered)
                json_path = next(path / name for name in result["files"] if name.endswith(".json"))
                self.assertEqual(json.loads(json_path.read_text()), item)

    def test_iqb_accepts_zero_to_three_strengths_and_questions(self):
        original = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json").read_text())
        for key in ("strengths", "provocations"):
            for count in range(4):
                with self.subTest(section=key, count=count):
                    item = copy.deepcopy(original)
                    next(b["data"] for b in item["blocks"] if b["data"].get("section_key") == key)["items"] = [f"Achado fictício {index}" for index in range(count)]
                    if count == 0:
                        item["summary"] += " Nenhum item sustentado registrado nesta seção do exemplo fictício."
                    before = copy.deepcopy(item)
                    self.renderer.validate(item, self.profiles)
                    self.assertEqual(item, before)
        item = copy.deepcopy(original)
        note = "Não há pontos fortes sustentados nem perguntas relevantes neste exemplo fictício."
        item["summary"] = note
        for block in item["blocks"]:
            if block["data"].get("section_key") in ("strengths", "provocations"):
                block["data"]["items"] = []
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.render(item, "md,html,docx", folder)
            stem = item["metadata"]["artifact_id"] + "-v" + item["metadata"]["content_version"]
            for fmt in ("md", "html"):
                self.assertIn(note, (folder / f"{stem}.{fmt}").read_text())
            self.assertIn(note, "\n".join(p.text for p in Document(folder / f"{stem}.docx").paragraphs))
            canonical = json.loads((folder / f"{stem}.json").read_text())
            self.assertEqual(canonical, item)

    def test_iqb_rejects_four_strengths_or_questions(self):
        original = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json").read_text())
        for key in ("strengths", "provocations"):
            for case in ("four", "missing"):
                with self.subTest(section=key, case=case):
                    item = copy.deepcopy(original)
                    if case == "missing":
                        item["blocks"] = [b for b in item["blocks"] if b["data"].get("section_key") != key]
                    else:
                        next(b["data"] for b in item["blocks"] if b["data"].get("section_key") == key)["items"] = ["Achado fictício"] * 4
                    with self.assertRaisesRegex(ValueError, "Conteúdo inválido"):
                        self.renderer.validate(item, self.profiles)

    def test_iqb_derivatives_keep_scores_vetoes_and_audit(self):
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json"
        if not path.exists():
            self.skipTest("Amostra IQB ausente")
        item = json.loads(path.read_text(encoding="utf-8"))
        scores = next(block["data"] for block in item["blocks"] if block["id"] == "scores")
        scores["dimensions"]["clarity"]["items"][0]["citation_id"] = "FIC-01"
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.render(item, "md,docx,html,txt", folder)
            stem = f"{item['metadata']['artifact_id']}-v{item['metadata']['content_version']}"
            doc = Document(folder / f"{stem}.docx")
            doc_text = "\n".join([p.text for p in doc.paragraphs] +
                                 [" | ".join(cell.text for cell in row.cells)
                                  for table in doc.tables for row in table.rows])
            for format in ("md", "docx", "html", "txt"):
                with self.subTest(format=format):
                    text = doc_text if format == "docx" else (folder / f"{stem}.{format}").read_text(encoding="utf-8")
                    if format == "html":
                        text = re.sub(r"<style>.*?</style>", "", text, flags=re.DOTALL)
                        text = re.sub(r"<[^>]*>", " ", text.replace("</tr>", "</tr>\n"))
                    for prefix in ("CLA", "EVI", "OUT", "ACT"):
                        for index in range(1, 11):
                            self.assertIn(f"{prefix}-{index:02d}", text)
                    self.assertTrue("Nota bruta" in text, f"{format}: Nota bruta ausente")
                    self.assertTrue("Nota final" in text, f"{format}: Nota final ausente")
                    self.assertIn(scores["dimensions"]["clarity"]["justification"], text)
                    self.assertIn("Auditoria de agrupamento", text)
                    self.assertRegex(text, rf"Amplitude[\s:|]+{scores['anti_clustering']['span']}\b")
                    self.assertTrue(any("CLA-01" in line and "FIC-01" in line for line in text.splitlines()))

    def test_card_grid_citations_survive_md_txt(self):
        for second_refs in (["F02"], ["F01", "F02"]):
            with self.subTest(second_refs=second_refs), tempfile.TemporaryDirectory() as temp:
                item = content("four_d_report", "grid-citations")
                cards = [{"title": "Primeiro card", "text": "Primeiro achado", "citation_ids": ["F01"]},
                         {"title": "Segundo | card\r\ncontinuação", "text": "Segundo | achado\nOutra linha", "citation_ids": second_refs},
                         {"title": "Terceiro card", "text": "Achado sem fonte"}]
                item["blocks"] = [{"id": "grid", "type": "card_grid", "data": {"cards": cards}, "citation_ids": ["FB"]}]
                item["citations"] = [{"id": key, "source_id": "fonte-ficticia-" + key} for key in ("F01", "F02", "FB")]
                before = copy.deepcopy(item)
                folder = Path(temp)
                self.render(item, "md,txt,html,docx", folder)
                for fmt in ("md", "txt"):
                    rendered = (folder / f"grid-citations-v1.0.0.{fmt}").read_text()
                    rows = [line for line in rendered.splitlines() if line.startswith(("| Primeiro card |", "| Segundo", "| Terceiro card |"))]
                    self.assertEqual(len(rows), 3)
                    self.assertIn("Fontes: F01", rows[0])
                    self.assertNotIn("F02", rows[0])
                    self.assertIn("Fontes: " + ", ".join(second_refs), rows[1])
                    self.assertNotIn("Fontes:", rows[2])
                    self.assertTrue(all("FB" not in row for row in rows))
                    self.assertIn("Fontes: FB", rendered.splitlines())
                    self.assertIn("- F01: fonte-ficticia-F01", rendered)
                    self.assertIn("- F02: fonte-ficticia-F02", rendered)
                    self.assertIn(r"Segundo \| card<br>continuação", rows[1])
                    self.assertIn(r"Segundo \| achado<br>Outra linha", rows[1])
                    self.assertNotIn("\r", rows[1])
                html = (folder / "grid-citations-v1.0.0.html").read_text()
                articles = re.findall(r'<article class="grid-card[^"]*">(.*?)</article>', html, re.DOTALL)
                self.assertEqual([re.findall(r"<sup>\[(.*?)\]</sup>", article) for article in articles],
                                 [["F01"], second_refs, []])
                doc = Document(folder / "grid-citations-v1.0.0.docx")
                cells = [cell.text for table in doc.tables for row in table.rows for cell in row.cells]
                self.assertEqual(len(cells), 3)
                self.assertIn("Fontes: F01", cells[0])
                self.assertIn("Fontes: " + ", ".join(second_refs), cells[1])
                self.assertNotIn("Fontes:", cells[2])
                self.assertTrue(any(p.text == "Fontes: FB" for p in doc.paragraphs))
                self.assertEqual(item, before)
                item["blocks"][0]["data"]["cards"][0]["citation_ids"] = ["UNKNOWN"]
                with self.assertRaisesRegex(ValueError, "citações inexistentes"):
                    self.renderer.validate(item, self.profiles)

    def test_md_escapes_pipes(self):
        item = content("innovation_potential_assessment", "pipe-test")
        item["blocks"][2]["data"]["rows"] = [["Casos", "a|b"]]
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.render(item, "md", folder)
            self.assertIn(r"a\|b", (folder / "pipe-test-v1.0.0.md").read_text(encoding="utf-8"))

    @unittest.skipUnless(pdf_available(), "WeasyPrint/pango indisponível")
    def test_iqb_pdf_keeps_wide_table_columns(self):
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json"
        if not path.exists():
            self.skipTest("Amostra IQB ausente")
        item = json.loads(path.read_text(encoding="utf-8"))
        scores = next(block["data"] for block in item["blocks"] if block["id"] == "scores")
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.render(item, "pdf", folder)
            stem = f"{item['metadata']['artifact_id']}-v{item['metadata']['content_version']}"
            reader = PdfReader(folder / f"{stem}.pdf")
            text = " ".join(" ".join(page.extract_text() for page in reader.pages).split())
            for label in ("Citação", "Nota bruta", "Nota final", "Rótulo", "Justificativa", "Auditoria de agrupamento"):
                self.assertTrue(label in text, f"PDF: coluna/seção {label!r} ausente")
            for detail in scores["dimensions"].values():
                self.assertTrue(detail["justification"] in text, "PDF: justificativa cortada")

    @unittest.skipUnless(pdf_available(), "WeasyPrint/pango indisponível")
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

    @unittest.skipUnless(pdf_available(), "WeasyPrint/pango indisponível")
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

    def test_missing_pdf_backend_still_renders_other_formats(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            backend = folder / "backend"
            backend.mkdir()
            (backend / "weasyprint.py").write_text('raise OSError("pango ausente (simulado)")\n', encoding="utf-8")
            source = folder / "input.json"
            source.write_text(json.dumps(content("learning_card", "LC-fallback")), encoding="utf-8")
            out = folder / "output"
            env = {**os.environ, "PYTHONPATH": str(backend)}
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(out),
                                     "--formats", "pdf,md,docx"], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["unavailable"], {"pdf": "OSError: pango ausente (simulado)"})
            self.assertIn("AVISO: PDF não gerado", result.stderr)
            self.assertIn("brew install pango", result.stderr)
            self.assertTrue((out / "LC-fallback-v1.0.0.md").is_file())
            self.assertTrue((out / "LC-fallback-v1.0.0.docx").is_file())
            manifest = json.loads((out / output["manifest"]).read_text())
            self.assertEqual(manifest["unavailable"], output["unavailable"])
            self.assertNotIn("LC-fallback-v1.0.0.pdf", output["files"])
            self.assertFalse((out / "LC-fallback-v1.0.0.pdf").exists())

    def test_pdf_write_failure_removes_partial_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            backend = folder / "backend"
            backend.mkdir()
            (backend / "weasyprint.py").write_text(
                "from pathlib import Path\n"
                "class HTML:\n"
                "    def __init__(self, **kwargs): pass\n"
                "    def write_pdf(self, path):\n"
                "        Path(path).write_bytes(b'PDF incompleto')\n"
                "        raise OSError('x' * 400)\n", encoding="utf-8")
            source = folder / "input.json"
            source.write_text(json.dumps(content("learning_card", "LC-write-failure")), encoding="utf-8")
            out = folder / "output"
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(out),
                                     "--formats", "pdf,md,docx"],
                                    env={**os.environ, "PYTHONPATH": str(backend)}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(len(output["unavailable"]["pdf"]), 300)
            self.assertFalse((out / "LC-write-failure-v1.0.0.pdf").exists())
            self.assertTrue((out / "LC-write-failure-v1.0.0.md").exists())
            self.assertTrue((out / "LC-write-failure-v1.0.0.docx").exists())

    @unittest.skipUnless(pdf_available(), "WeasyPrint/pango indisponível")
    def test_oversized_card_remains_fatal(self):
        item = content("test_card", "TC-oversized")
        item["blocks"] = [
            {"id": key, "type": "paragraph", "data": {"section_key": key, "text": "Conteúdo longo para verificar o limite do card. " * 80}}
            for key in ("hypothesis", "test", "measure", "criteria")
        ]
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source = folder / "input.json"
            source.write_text(json.dumps(item), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder),
                                     "--formats", "pdf,md"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("excedeu uma página", result.stderr)
            self.assertNotIn("AVISO: PDF não gerado", result.stderr)
            self.assertFalse((folder / "TC-oversized-v1.0.0.pdf").exists())
            self.assertFalse((folder / "TC-oversized-v1.0.0.manifest.json").exists())

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

    def card_document(self, kind, state):
        keys = ("hypothesis", "test", "measure", "criteria") if kind == "test_card" else ("hypothesis", "observations", "learning", "action")
        item = content(kind, "TC-state" if kind == "test_card" else "LC-state")
        item["metadata"]["completeness"] = state
        item["blocks"] = [{"id": key, "type": "paragraph", "data": {
            "section_key": key, "text": "Pendente: registrar " + key}} for key in keys]
        item["citations"] = []
        if state == "complete":
            item["citations"] = [{"id": "F01", "source_id": "registro-ficticio"}]
            if kind == "learning_card":
                item["metadata"].update(test_card_id="TC-executed", test_card_version="1")
                item["blocks"][1]["citation_ids"] = ["F01"]
        return item

    def test_cards_keep_four_fields_for_all_states(self):
        for kind in ("test_card", "learning_card"):
            for state in ("complete", "partial", "inconclusive"):
                original = self.card_document(kind, state)
                with self.subTest(kind=kind, state=state, case="valid"):
                    self.renderer.validate(original, self.profiles)
                    self.assertEqual(original, self.card_document(kind, state))
                for case in ("only_hypothesis", "missing", "duplicate", "inverted", "extra", "blank", "page_break", "list", "table", "card_grid"):
                    with self.subTest(kind=kind, state=state, case=case):
                        item = copy.deepcopy(original)
                        if case == "only_hypothesis":
                            item["blocks"] = item["blocks"][:1]
                        elif case == "missing":
                            item["blocks"].pop()
                        elif case == "duplicate":
                            item["blocks"][2]["data"]["section_key"] = item["blocks"][0]["data"]["section_key"]
                        elif case == "inverted":
                            item["blocks"][2:4] = reversed(item["blocks"][2:4])
                        elif case == "extra":
                            item["blocks"].append({"id": "extra", "type": "paragraph", "data": {"text": "Extra"}})
                        elif case == "blank":
                            item["blocks"][2]["data"]["text"] = " \n\t "
                        else:
                            item["blocks"][2]["type"] = case
                            data = item["blocks"][2]["data"]
                            if case == "list":
                                data["items"] = ["Item diferente"]
                            elif case == "table":
                                data.update(headers=["Coluna"], rows=[["Linha diferente"]])
                            elif case == "card_grid":
                                data["cards"] = [{"title": "Card próprio", "text": "Texto diferente"}]
                        before = copy.deepcopy(item)
                        with self.assertRaises(ValueError):
                            self.renderer.validate(item, self.profiles)
                        self.assertEqual(item, before)
            with self.subTest(kind=kind, case="CLI"), tempfile.TemporaryDirectory() as temp:
                item = self.card_document(kind, "partial")
                item["blocks"] = item["blocks"][:1]
                folder = Path(temp)
                source = folder / "input.json"
                source.write_text(json.dumps(item))
                result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                         "--out-dir", str(folder / "output"), "--formats", "md"],
                                        capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((folder / "output").exists())
            with self.subTest(kind=kind, case="default_complete"):
                item = self.card_document(kind, "complete")
                del item["metadata"]["completeness"]
                self.renderer.validate(item, self.profiles)
                if kind == "learning_card":
                    del item["metadata"]["test_card_id"]
                    with self.assertRaisesRegex(ValueError, "Conteúdo inválido"):
                        self.renderer.validate(item, self.profiles)

    def test_partial_cards_preserve_pending_fields_in_exports(self):
        for kind in ("test_card", "learning_card"):
            for state in ("partial", "inconclusive"):
                with self.subTest(kind=kind, state=state), tempfile.TemporaryDirectory() as temp:
                    item = self.card_document(kind, state)
                    texts = (["Hipótese pendente de definição.", "Pendente: definir teste antes da coleta.",
                              "Pendente: definir medida antes da coleta.", "Pendente: definir critério antes da coleta."]
                             if kind == "test_card" else
                             ["Hipótese do teste ainda não informada.", "Não observado: coleta ainda não realizada.",
                              "Aprendizado pendente de observação.", "Ação pendente de análise."])
                    for block, text, block_type in zip(item["blocks"], texts, ("paragraph", "heading", "callout", "metric")):
                        block["data"]["text"] = text
                        block["type"] = block_type
                    before = copy.deepcopy(item)
                    folder = Path(temp)
                    has_pdf = pdf_available()
                    self.render(item, "md,html,docx" + (",pdf" if has_pdf else ""), folder)
                    self.assertEqual(item, before)
                    stem = item["metadata"]["artifact_id"] + "-v1.0.0"
                    exports = {fmt: (folder / f"{stem}.{fmt}").read_text() for fmt in ("md", "html")}
                    exports["docx"] = "\n".join(p.text for p in Document(folder / f"{stem}.docx").paragraphs)
                    if has_pdf:
                        exports["pdf"] = "\n".join(p.extract_text() for p in PdfReader(folder / f"{stem}.pdf").pages)
                    for fmt, rendered in exports.items():
                        for text in texts:
                            self.assertIn(text.casefold(), " ".join(rendered.split()).casefold(), (kind, state, fmt, text))
                    item["blocks"][0]["citation_ids"] = ["INEXISTENTE"]
                    with self.assertRaisesRegex(ValueError, "citações inexistentes"):
                        self.renderer.validate(item, self.profiles)

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
            learning["metadata"].update(completeness="complete", test_card_id="TC-02", test_card_version="1.0.0")
            learning["blocks"] = [
                {"id": key, "type": "paragraph", "data": {"section_key": key, "text": key}}
                for key in ("hypothesis", "observations", "learning", "action")
            ]
            source.write_text(json.dumps(learning))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(folder), "--formats", "md"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            learning["blocks"][1]["citation_ids"] = ["F01"]
            self.render(learning, "md", folder)

    def test_learning_card_link_required_only_for_complete_content(self):
        sample = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/learning_card/input.json").read_text())
        for field, value in [("test_card_id", None), ("test_card_version", None),
                             ("test_card_id", ""), ("test_card_id", "invalid id"),
                             ("test_card_version", ""), ("test_card_version", "invalid version")]:
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as temp:
                item = json.loads(json.dumps(sample))
                if value is None:
                    del item["metadata"][field]
                else:
                    item["metadata"][field] = value
                folder = Path(temp)
                source = folder / "input.json"
                source.write_text(json.dumps(item))
                result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                         "--out-dir", str(folder / "output"), "--formats", "md"],
                                        capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Conteúdo inválido", result.stderr)
                self.assertFalse((folder / "output").exists())
        with tempfile.TemporaryDirectory() as temp:
            sample["metadata"]["completeness"] = "partial"
            del sample["metadata"]["test_card_id"]
            del sample["metadata"]["test_card_version"]
            self.render(sample, "md", Path(temp))

    def test_learning_card_link_versions_and_visible_exports(self):
        sample = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/learning_card/input.json").read_text())
        for version in ("1", "1.0.0"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as temp:
                sample["metadata"]["test_card_version"] = version
                folder = Path(temp)
                formats = "html,docx,md,txt" + (",pdf" if pdf_available() else "")
                self.render(sample, formats, folder)
                stem = "sample-learning-card-v1.0.0"
                link = "Test Card: sample-test-card v" + version
                for extension in ("md", "txt"):
                    self.assertIn(link, (folder / f"{stem}.{extension}").read_text())
                self.assertIn("Test Card sample-test-card v" + version,
                              (folder / f"{stem}.html").read_text())
                self.assertIn(link, "\n".join(p.text for p in Document(folder / f"{stem}.docx").paragraphs))
                if pdf_available():
                    text = "\n".join(p.extract_text() for p in PdfReader(folder / f"{stem}.pdf").pages)
                    self.assertIn("Test Card sample-test-card v" + version, text)

    def test_required_sections_reject_hidden_block_types(self):
        for kind in REQUIRED_SECTION_TYPES:
            original = self.complete_section_document(kind)
            for index, section_block in enumerate(original["blocks"]):
                for block_type in ("page_break", "list", "table", "card_grid"):
                    with self.subTest(kind=kind, section=section_block["id"], block_type=block_type):
                        item = copy.deepcopy(original)
                        block = item["blocks"][index]
                        block["type"] = block_type
                        if block_type == "list":
                            block["data"]["items"] = ["Item próprio da lista"]
                        elif block_type == "table":
                            block["data"].update(headers=["Coluna"], rows=[["Linha própria da tabela"]])
                        elif block_type == "card_grid":
                            block["data"]["cards"] = [{"title": "Card próprio", "text": "Texto próprio da grade"}]
                        with self.assertRaisesRegex(ValueError, "Conteúdo inválido"):
                            self.renderer.validate(item, self.profiles)
            with self.subTest(kind=kind, boundary="CLI"), tempfile.TemporaryDirectory() as temp:
                item = copy.deepcopy(original)
                item["blocks"][0]["type"] = "page_break"
                folder = Path(temp)
                source = folder / "input.json"
                source.write_text(json.dumps(item))
                result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                         "--out-dir", str(folder / "output"), "--formats", "md"],
                                        capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Conteúdo inválido", result.stderr)
                self.assertFalse((folder / "output").exists())

    def test_required_sections_reject_missing_blank_and_uncited_summaries(self):
        for kind in REQUIRED_SECTION_TYPES:
            original = self.complete_section_document(kind)
            for index, section_block in enumerate(original["blocks"]):
                cases = ["missing_section", "blank_text", "missing_type", "missing_data"]
                if kind.startswith("five_c"):
                    cases += ["missing_citations", "empty_citations"]
                for case in cases:
                    with self.subTest(kind=kind, section=section_block["id"], case=case):
                        item = copy.deepcopy(original)
                        block = item["blocks"][index]
                        if case == "missing_section":
                            item["blocks"].pop(index)
                        elif case == "blank_text":
                            block["data"]["text"] = " \n\t "
                        elif case == "missing_type":
                            del block["type"]
                        elif case == "missing_data":
                            del block["data"]
                        elif case == "missing_citations":
                            del block["citation_ids"]
                        else:
                            block["citation_ids"] = []
                        with self.assertRaisesRegex(ValueError, "Conteúdo inválido"):
                            self.renderer.validate(item, self.profiles)

    def test_required_section_text_survives_exports(self):
        allowed = ("paragraph", "heading", "callout", "metric")
        for kind_index, kind in enumerate(REQUIRED_SECTION_TYPES):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                item = self.complete_section_document(kind)
                item["blocks"] = []
                texts = []
                for section_index, key in enumerate(self.sections[kind]):
                    for variant, block_type in enumerate(allowed):
                        text = f"Registro fictício {kind_index} seção {section_index} variante {variant}."
                        texts.append(text)
                        item["blocks"].append({"id": f"{key}-{block_type}", "type": block_type,
                                               "data": {"section_key": key, "text": text}, "citation_ids": ["F01"]})
                item["blocks"].insert(2, {"id": "extra-break", "type": "page_break", "data": {}})
                item["blocks"] += [
                    {"id": "extra-list", "type": "list", "data": {"items": ["Lista complementar"]}},
                    {"id": "extra-table", "type": "table", "data": {"headers": ["Coluna"], "rows": [["Tabela complementar"]]}},
                    {"id": "extra-grid", "type": "card_grid", "data": {"cards": [{"title": "Card complementar", "text": "Texto complementar"}]}},
                ]
                folder = Path(temp)
                has_pdf = pdf_available()
                formats = "html,md,txt,docx" + (",pdf" if has_pdf else "")
                self.render(item, formats, folder)
                stem = f"{kind}-v1.0.0"
                exports = {fmt: (folder / f"{stem}.{fmt}").read_text() for fmt in ("html", "md", "txt")}
                doc = Document(folder / f"{stem}.docx")
                exports["docx"] = "\n".join([p.text for p in doc.paragraphs] +
                                            [cell.text for table in doc.tables for row in table.rows for cell in row.cells])
                if has_pdf:
                    exports["pdf"] = "\n".join(page.extract_text() for page in PdfReader(folder / f"{stem}.pdf").pages)
                for fmt, rendered in exports.items():
                    normalized = " ".join(rendered.split())
                    for text in texts:
                        self.assertIn(text.casefold(), normalized.casefold(), (kind, fmt, text))

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
