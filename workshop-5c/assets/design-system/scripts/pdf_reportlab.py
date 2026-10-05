"""PDF portátil em ReportLab para cards e resumo do briefing em uma página."""
from __future__ import annotations

import html
import io
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts" / "static"
SUPPORTED_LAYOUTS = ("card_portrait", "executive_one_page")


class PdfOverflow(ValueError):
    """O conteúdo excede a página única exigida pelo perfil."""


def _register_fonts() -> None:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for name in ("Montserrat-Bold", "Roboto-Regular", "Roboto-Bold"):
        font_path = FONT_DIR / f"{name}.ttf"
        if not font_path.is_file():
            raise FileNotFoundError("Fontes estáticas ausentes em assets/fonts/static; rode _TOOLS/make_static_fonts.py")
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(font_path)))
    pdfmetrics.registerFontFamily("Roboto-Regular", normal="Roboto-Regular", bold="Roboto-Bold")


def make_styles(tokens: dict[str, Any], layout: str) -> dict[str, Any]:
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    definitions = tokens["typography"]["styles"]
    minimum = float(tokens["density"]["minimum_font_size"])
    palette = tokens["color"]

    def style(name: str, token: str, color: str, *, size: float | None = None,
              weight: int | None = None, leading: float | None = None) -> Any:
        spec = definitions[token]
        font_size = float(size if size is not None else spec["size"])
        if font_size < minimum:
            raise ValueError(f"{name}: fonte abaixo do mínimo de {minimum} pt")
        font_weight = int(weight if weight is not None else spec["weight"])
        font = "Montserrat-Bold" if spec["family"] == "font_brand" else ("Roboto-Bold" if font_weight >= 600 else "Roboto-Regular")
        return ParagraphStyle(name, fontName=font, fontSize=font_size,
                              leading=leading or font_size * float(spec["line_height"]),
                              textColor=colors.HexColor(palette[color]),
                              splitLongWords=1, spaceAfter=0, spaceBefore=0)

    result = {
        "eyebrow": style("eyebrow", "cover_eyebrow", "document_accent"),
        "title": style("title", "cover_title", "document_primary", size=24 if layout == "executive_one_page" else None),
        "summary": style("summary", "body", "text_strong", size=10.5),
        "body": style("body", "body", "text_body", size=8.5 if layout == "executive_one_page" else None),
        "body_inverse": style("body_inverse", "body", "inverse", size=8.5 if layout == "executive_one_page" else None),
        "field": style("field", "section_title", "document_primary", size=13),
        "section": style("section", "section_title", "inverse", size=9, weight=700),
        "metric": style("metric", "metric", "document_primary"),
        "table_header": style("table_header", "table_header", "inverse"),
        "table_body": style("table_body", "table_body", "text_body"),
        "source": style("source", "body_dense", "text_body"),
        "footer": style("footer", "footer", "text_muted"),
    }
    result["_colors"] = {name: colors.HexColor(value) for name, value in palette.items()}
    return result


def _markup(value: Any) -> str:
    return html.escape(str(value)).replace("\n", "<br/>")


def _cited(value: Any, block: dict[str, Any]) -> str:
    refs = "".join(f'<super size="7.5" rise="3">[{_markup(citation)}]</super>'
                   for citation in block.get("citation_ids", []))
    return _markup(value) + refs


def block_flowables(block: dict[str, Any], styles: dict[str, Any], width: float,
                    block_text: Callable[[dict[str, Any]], str],
                    table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]]) -> list[Any]:
    from reportlab.platypus import Paragraph, Table, TableStyle

    kind = block["type"]
    data = block.get("data", {})
    if kind in ("heading", "page_break"):
        return []
    if kind == "table":
        headings, rows = table_rows(block)
        ncols = max(1, len(headings), *(len(row) for row in rows)) if rows else max(1, len(headings))
        cells = [[Paragraph(_markup(headings[i] if i < len(headings) else ""), styles["table_header"]) for i in range(ncols)]]
        cells.extend([Paragraph(_markup(row[i] if i < len(row) else ""), styles["table_body"]) for i in range(ncols)] for row in rows)
        table = Table(cells, colWidths=[width / ncols] * ncols, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), styles["_colors"]["document_primary"]),
            ("GRID", (0, 0), (-1, -1), 0.75, styles["_colors"]["border"]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        result: list[Any] = [table]
        if block.get("citation_ids"):
            result.append(Paragraph(_cited("", block), styles["body"]))
        return result
    if kind == "list":
        return [Paragraph(_cited("• " + str(item), block), styles["body"]) for item in data.get("items", [])]
    if kind == "metric":
        value = Paragraph(_cited(block_text(block), block), styles["metric"])
        table = Table([[value]], colWidths=[width])
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), styles["_colors"]["document_accent_soft"]),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
        return [table]
    if kind == "callout":
        paragraph = Paragraph(_cited(block_text(block), block), styles["body_inverse"])
        table = Table([[paragraph]], colWidths=[width])
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), styles["_colors"]["document_deep"]),
                                   ("LINEBEFORE", (0, 0), (0, -1), 3, styles["_colors"]["document_accent"]),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                                   ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
        return [table]
    return [Paragraph(_cited(block_text(block), block), styles["body"])]


def _sections(blocks: list[dict[str, Any]], block_text: Callable[[dict[str, Any]], str]) -> list[tuple[str, list[dict[str, Any]]]]:
    result: list[tuple[str, list[dict[str, Any]]]] = []
    title = "Notas"
    body: list[dict[str, Any]] = []
    for block in blocks:
        if block["type"] == "heading":
            if body:
                result.append((title, body))
            title, body = block_text(block), []
        elif block["type"] == "page_break":
            if body:
                result.append((title, body))
            title, body = "Notas", []
        else:
            body.append(block)
    if body:
        result.append((title, body))
    return result


def render_pdf(content: dict[str, Any], tokens: dict[str, Any], profile: dict[str, Any], path: Path, *,
               deliverable_label: str, footer_label: str, field_labels: dict[str, str] | None,
               block_text: Callable[[dict[str, Any]], str],
               table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]]) -> None:
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import (BaseDocTemplate, Frame, FrameBreak, Image, KeepInFrame,
                                   PageTemplate, Paragraph, Spacer, Table, TableStyle)
    from reportlab.platypus.doctemplate import LayoutError

    layout = profile["layout"]
    if layout not in SUPPORTED_LAYOUTS:
        raise ValueError(f"ReportLab ainda não suporta o layout {layout}")
    _register_fonts()
    page = tokens["page"][profile["paper"]]
    paper_width, paper_height = float(page["width"]) * mm, float(page["height"]) * mm
    left, right = float(page["margin_left"]) * mm, float(page["margin_right"]) * mm
    top, bottom = float(page["margin_top"]) * mm, float(page["margin_bottom"]) * mm
    usable_width = paper_width - left - right
    usable_height = paper_height - top - bottom - 10 * mm
    styles = make_styles(tokens, layout)
    palette = {name: colors.HexColor(value) for name, value in tokens["color"].items()}
    logo_path = ROOT / "assets" / "logo_ccee.png"
    logo_width, logo_height = ImageReader(str(logo_path)).getSize()
    scale = min(38 * mm / logo_width, 11 * mm / logo_height)
    logo = Image(str(logo_path), width=logo_width * scale, height=logo_height * scale)
    masthead = Table([[Paragraph(_markup(deliverable_label.upper()), styles["eyebrow"]), logo]],
                     colWidths=[usable_width - 40 * mm, 40 * mm])
    masthead.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 1.5, palette["document_primary"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    header: list[Any] = [masthead, Spacer(1, 9), Paragraph(_markup(content["title"]), styles["title"])]
    if content.get("summary"):
        header.extend([Spacer(1, 6), Paragraph(_markup(content["summary"]), styles["summary"])])
    header.append(Spacer(1, 9))

    def source_items(width: float) -> list[Any]:
        if not content["citations"]:
            return []
        result: list[Any] = [Spacer(1, 7), Paragraph("Fontes", styles["field"])]
        for citation in content["citations"]:
            line = f"<b>{_markup(citation['id'])}</b> — {_markup(citation['source_id'])}"
            if citation.get("locator"):
                line += f", {_markup(citation['locator'])}"
            result.append(Paragraph(line, styles["source"]))
        return result

    if layout == "card_portrait":
        frame = Frame(left, bottom + 10 * mm, usable_width, usable_height, leftPadding=0,
                      rightPadding=0, topPadding=0, bottomPadding=0)
        story = list(header)
        for block in content["blocks"]:
            key = block.get("data", {}).get("section_key")
            if field_labels and key in field_labels:
                inner_width = usable_width - 24
                field = Table([[Paragraph(_markup(field_labels[key]), styles["field"])],
                               [*block_flowables(block, styles, inner_width, block_text, table_rows)]],
                              colWidths=[usable_width])
                field.setStyle(TableStyle([
                    ("BOX", (0, 0), (-1, -1), 0.75, palette["border"]),
                    ("LINEBEFORE", (0, 0), (0, -1), 3, palette["document_accent"]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, 0), 10), ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
                ]))
                story.extend([field, Spacer(1, 10)])
            else:
                story.extend(block_flowables(block, styles, usable_width, block_text, table_rows))
        story.extend(source_items(usable_width))
        story = [KeepInFrame(usable_width, usable_height, story, mode="error")]
        frames = [frame]
    else:
        header_height = 40 * mm
        column_gap = 8
        column_width = (usable_width - column_gap) / 2
        column_height = usable_height - header_height
        frames = [
            Frame(left, paper_height - top - header_height, usable_width, header_height, leftPadding=0,
                  rightPadding=0, topPadding=0, bottomPadding=0),
            Frame(left, bottom + 10 * mm, column_width, column_height, leftPadding=0,
                  rightPadding=0, topPadding=0, bottomPadding=0),
            Frame(left + column_width + column_gap, bottom + 10 * mm, column_width, column_height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0),
        ]
        story = [KeepInFrame(usable_width, header_height, header, mode="error"), FrameBreak()]
        sections = _sections(content["blocks"], block_text)
        for section_title, blocks in sections:
            if len(sections) == 1 and len(blocks) > 1:
                band = Table([[Paragraph(_markup(section_title.upper()), styles["section"])]],
                             colWidths=[column_width])
                band.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), palette["document_deep"]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]))
                story.extend([band, Spacer(1, 5)])
                split = (len(blocks) + 1) // 2
                for index, block in enumerate(blocks):
                    if index == split:
                        story.append(FrameBreak())
                    story.extend(block_flowables(block, styles, column_width, block_text, table_rows))
                    story.append(Spacer(1, 7))
                continue
            inner_width = column_width - 14
            inner: list[Any] = []
            for block in blocks:
                inner.extend(block_flowables(block, styles, inner_width, block_text, table_rows))
            band = Paragraph(_markup(section_title.upper()), styles["section"])
            section = Table([[band], [inner]], colWidths=[column_width])
            section.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), palette["document_deep"]),
                ("BOX", (0, 0), (-1, -1), 0.75, palette["border"]),
                ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([section, Spacer(1, 6)])
        story.extend(source_items(column_width))

    pages: list[int] = []

    def on_page(canvas: Any, doc: Any) -> None:
        pages.append(doc.page)
        canvas.setFont("Roboto-Regular", styles["footer"].fontSize)
        canvas.setFillColor(palette["text_muted"])
        canvas.drawRightString(paper_width - right, bottom / 2, footer_label)

    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=(paper_width, paper_height),
                          leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
                          title=content["title"], invariant=1)
    doc.addPageTemplates(PageTemplate(id="one-page", frames=frames, onPage=on_page))
    try:
        doc.build(story)
    except LayoutError as exc:
        raise PdfOverflow(f"{layout} excedeu uma página; revise ou divida o conteúdo sem reduzir a fonte") from exc
    if len(pages) != 1:
        raise PdfOverflow(f"{layout} excedeu uma página; revise ou divida o conteúdo sem reduzir a fonte")
    path.write_bytes(buffer.getvalue())
