"""Observable PPTX parity obligations for all four presentation deliverables."""
from __future__ import annotations

import copy
import importlib.util
import json
import re
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.oxml.ns import qn
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
KINDS = ("executive_presentation", "five_c_presentation", "four_d_presentation", "three_e_presentation")


def normalized(text):
    return " ".join(re.sub(r"\[[^]]+\]", "", text).replace("•", "").split())


def slide_text(slide):
    parts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            parts.append(shape.text)
        elif shape.has_table:
            parts.extend(cell.text for row in shape.table.rows for cell in row.cells)
    return " ".join(parts)


class PptxParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("render_pptx_parity", ROOT / "_DESIGN_SYSTEM/scripts/render.py")
        cls.renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.renderer)
        cls.tokens = json.loads((ROOT / "_DESIGN_SYSTEM/tokens.json").read_text())
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.presentations, cls.contents = {}, {}
        for kind in KINDS:
            content = json.loads((ROOT / "_SAMPLES_ENTREGAVEIS" / kind / "input.json").read_text())
            path = Path(cls.temporary.name) / f"{kind}.pptx"
            cls.renderer.render_pptx(content, cls.tokens, path)
            cls.presentations[kind], cls.contents[kind] = Presentation(path), content

    def test_four_samples_preserve_slide_content_and_order(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                pdf = PdfReader(next((ROOT / "_SAMPLES_ENTREGAVEIS" / kind).glob("*.pdf")))
                prs = self.presentations[kind]
                self.assertEqual(len(prs.slides), len(pdf.pages))
                for page, slide in zip(pdf.pages, prs.slides):
                    # Compare word multiplicity, not only substring presence: duplicated or
                    # omitted blocks must fail even when the slide still has its title.
                    self.assertEqual(Counter(normalized(page.extract_text()).split()),
                                     Counter(normalized(slide_text(slide)).split()))

    def test_four_samples_remain_editable(self):
        for kind, prs in self.presentations.items():
            with self.subTest(kind=kind):
                self.assertTrue(any(shape.has_text_frame and shape.text.strip()
                                    for slide in prs.slides for shape in slide.shapes))
                for slide in prs.slides:
                    pictures = [shape for shape in slide.shapes if shape.shape_type == MSO_SHAPE_TYPE.PICTURE]
                    self.assertEqual(len(pictures), 1, "only the logo is rasterized")
                    self.assertLess(pictures[0].width, prs.slide_width / 4)
                    self.assertTrue(any(shape.has_text_frame and shape.text for shape in slide.shapes))

    def test_all_sample_fonts_and_cover_geometry(self):
        for kind, prs in self.presentations.items():
            with self.subTest(kind=kind):
                content = self.contents[kind]
                layout = self.renderer.load_pptx_layout(kind)
                self.assertAlmostEqual(prs.slide_width / 914400, layout["width_in"], places=4)
                self.assertAlmostEqual(prs.slide_height / 914400, layout["height_in"], places=4)
                title = content["blocks"][0]["data"]["text"]
                run = next(run for shape in prs.slides[1].shapes if shape.has_text_frame
                           for para in shape.text_frame.paragraphs for run in para.runs if run.text == title)
                self.assertEqual(run.font.size.pt, 24)
                self.assertEqual(run.font.name, self.tokens["typography"]["font_brand"])
                self.assertEqual(str(run.font.color.rgb), self.tokens["color"]["document_primary"].lstrip("#"))
                self.assertAlmostEqual(next(s for s in prs.slides[1].shapes
                                           if s.has_text_frame and s.text == title).left / 914400,
                                       layout["slots"]["titulo_slide"]["x"], places=4)
                bar = next(s for s in prs.slides[0].shapes if s.shape_type == MSO_SHAPE_TYPE.LINE)
                self.assertAlmostEqual(bar.line.width.pt, 6 * 72 / 25.4, places=3)
                self.assertEqual(bar.top, 0)
                self.assertEqual(bar.height, prs.slide_height)

    def test_all_sample_identity_numbering_and_superscripts(self):
        found = 0
        for kind, prs in self.presentations.items():
            with self.subTest(kind=kind):
                identity = self.renderer.identity_line(self.contents[kind])
                for n, slide in enumerate(prs.slides, 1):
                    self.assertIn(identity + "\t" + f"{n} / {len(prs.slides)}", slide_text(slide))
                    for shape in slide.shapes:
                        if shape.has_text_frame:
                            for p in shape.text_frame.paragraphs:
                                for run in p.runs:
                                    if re.fullmatch(r"(?:\[[^]]+\])+", run.text):
                                        self.assertEqual(run._r.get_or_add_rPr().get("baseline"), "30000")
                                        found += 1
        self.assertGreater(found, 0)

    def test_cards_callout_and_table_are_native_and_use_pdf_colors(self):
        # One card per tone holds the complete tone mapping, including neutral.
        colors = self.tokens["color"]
        tones = {"blue": (colors["document_accent_soft"], colors["document_accent"]),
                 "neutral": (colors["surface_muted"], colors["border_strong"]),
                 "red": (colors["danger_soft"], colors["danger"]),
                 "green": ("#E8F4EE", "#3F9270"), "yellow": ("#FFF4D9", "#BD8A28")}
        content = copy.deepcopy(self.contents["executive_presentation"])
        content["blocks"] = []
        for tone in tones:
            content["blocks"] += [
                {"id": f"h-{tone}", "type": "heading", "data": {"text": f"Card {tone}"}},
                {"id": f"c-{tone}", "type": "card_grid", "data": {"columns": 1, "cards": [
                    {"title": f"Título {tone}", "text": f"Texto {tone}", "tone": tone}]}}]
        content["blocks"] += [
            {"id": "h-other", "type": "heading", "data": {"text": "Destaque e tabela"}},
            {"id": "call", "type": "callout", "data": {"text": "Mensagem em destaque"}},
            {"id": "table", "type": "table", "data": {"headers": ["Campo", "Valor"], "rows": [["A", "B"]]}}]
        path = Path(self.temporary.name) / "native.pptx"
        self.renderer.render_pptx(content, self.tokens, path)
        prs = Presentation(path)
        for n, (tone, expected) in enumerate(tones.items(), 1):
            shapes = [s for s in prs.slides[n].shapes if s.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE]
            self.assertEqual([str(s.fill.fore_color.rgb) for s in shapes], [c.lstrip("#") for c in expected])
            self.assertTrue(all(s._element.find(qn("p:style")) is None for s in shapes))
            self.assertAlmostEqual(shapes[1].width.pt, 3, places=3)
            body = next(s for s in prs.slides[n].shapes if s.has_text_frame and f"Texto {tone}" in s.text)
            self.assertEqual(body.text_frame.paragraphs[-1].runs[0].font.size.pt, 17)
        slide = prs.slides[len(tones) + 1]
        fills = [str(s.fill.fore_color.rgb) for s in slide.shapes if s.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE]
        self.assertEqual(fills, [colors["document_deep"].lstrip("#"), colors["document_accent"].lstrip("#")])
        table = next(s.table for page in prs.slides for s in page.shapes if s.has_table)
        self.assertEqual([[c.text for c in row.cells] for row in table.rows], [["Campo", "Valor"], ["A", "B"]])
        self.assertEqual(str(table.cell(0, 0).fill.fore_color.rgb), colors["document_primary"].lstrip("#"))
