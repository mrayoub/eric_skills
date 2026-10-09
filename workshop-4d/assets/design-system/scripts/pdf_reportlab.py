"""PDF portátil em ReportLab para cards, resumo do briefing e relatórios."""
from __future__ import annotations

import html
import io
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts" / "static"
SUPPORTED_LAYOUTS = ("card_portrait", "executive_one_page", "report_portrait", "report_landscape", "presentation")


class PdfOverflow(ValueError):
    """O conteúdo excede a página única exigida pelo perfil."""


def _register_fonts() -> None:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for name in ("Montserrat-Bold", "Roboto-Regular", "Roboto-Medium", "Roboto-Bold"):
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
        font = "Montserrat-Bold" if spec["family"] == "font_brand" else (
            "Roboto-Bold" if font_weight >= 600 else "Roboto-Medium" if font_weight >= 500 else "Roboto-Regular")
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
        "report_title": style("report_title", "cover_title", "document_primary",
                              size=24 if layout == "report_landscape" else 25),
        "report_section": style("report_section", "section_title", "inverse", size=11,
                                weight=700),
        "card_title": style("card_title", "section_title", "document_primary", size=9,
                            weight=700),
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


def group_sections(blocks: list[dict[str, Any]], block_text: Callable[[dict[str, Any]], str]) -> list[tuple[Any, ...]]:
    """Agrupa blocos pelas mesmas fronteiras de heading/page_break do HTML."""
    result: list[tuple[Any, ...]] = []
    title = "Notas"
    body: list[dict[str, Any]] = []

    def flush() -> None:
        nonlocal body
        if body:
            wide = any(block["type"] in ("table", "card_grid", "canvas", "chart") for block in body)
            result.append(("section", title, body, wide))
            body = []

    for block in blocks:
        if block["type"] == "heading":
            flush()
            title = block_text(block)
        elif block["type"] == "page_break":
            flush()
            result.append(("page_break",))
            title = "Notas"
        else:
            body.append(block)
    flush()
    return result


def _report_table(block: dict[str, Any], styles: dict[str, Any], width: float,
                  table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
                  table_views: Callable[[dict[str, Any]], list[tuple[str, str, list[str], list[list[str]]]]],
                  iqb_widths: dict[str, list[int]]) -> list[Any]:
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

    caption_style = ParagraphStyle("table_caption", parent=styles["card_title"], spaceAfter=4, keepWithNext=1)
    views = table_views(block) if isinstance(block.get("data", {}).get("dimensions"), dict) else [
        ("", block.get("data", {}).get("title", ""), *table_rows(block))]
    result: list[Any] = []
    palette = styles["_colors"]
    for slug, caption, headings, rows in views:
        if caption:
            result.append(Paragraph(_markup(caption), caption_style))
        ncols = max(1, len(headings))
        matrix = [[Paragraph(_markup(headings[index] if index < len(headings) else ""),
                             styles["table_header"]) for index in range(ncols)]]
        matrix.extend([Paragraph(_markup(row[index] if index < len(row) else ""),
                                 styles["table_body"]) for index in range(ncols)] for row in rows)
        proportions = iqb_widths.get(slug)
        col_widths = [width * proportion / 100 for proportion in proportions] if proportions else [width / ncols] * ncols
        table = Table(matrix, colWidths=col_widths, repeatRows=1, splitByRow=1)
        padding = 4 if proportions else 6
        commands = [
            ("BACKGROUND", (0, 0), (-1, 0), palette["document_primary"]),
            ("GRID", (0, 0), (-1, -1), 0.75, palette["border"]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), padding),
            ("RIGHTPADDING", (0, 0), (-1, -1), padding),
            ("TOPPADDING", (0, 0), (-1, -1), padding),
            ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
        ]
        if len(matrix) > 1:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [palette["surface"], palette["surface_muted"]]))
        table.setStyle(TableStyle(commands))
        result.extend([table, Spacer(1, 7)])
    if block.get("citation_ids"):
        result.append(Paragraph(_cited("", block), styles["source"]))
    return result


def _report_card_grid(block: dict[str, Any], styles: dict[str, Any], width: float) -> list[Any]:
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import KeepTogether, Paragraph, Table, TableStyle

    data = block.get("data", {})
    cards = data.get("cards", [])
    columns = max(1, min(4, int(data.get("columns", 2))))
    palette = styles["_colors"]
    tones = {
        "blue": (palette["document_accent_soft"], palette["document_accent"]),
        "neutral": (palette["surface_muted"], palette["border_strong"]),
        "red": (palette["danger_soft"], palette["danger"]),
        "green": (colors.HexColor("#E8F4EE"), colors.HexColor("#3F9270")),
        "yellow": (colors.HexColor("#FFF4D9"), colors.HexColor("#BD8A28")),
    }
    result: list[Any] = []
    if data.get("title"):
        title_style = ParagraphStyle("grid_title", parent=styles["card_title"], spaceAfter=5, keepWithNext=1)
        result.append(Paragraph(_markup(data["title"]), title_style))
    gap = 6
    card_width = (width - gap * (columns - 1)) / columns
    # Uma Table por linha, com cartões nas colunas pares e espaçadores nas ímpares: todas as
    # células da linha recebem a mesma altura e a soma das larguras é exatamente `width`.
    col_widths: list[float] = []
    for index in range(columns):
        col_widths.append(card_width)
        if index < columns - 1:
            col_widths.append(gap)
    for start in range(0, len(cards), columns):
        row = cards[start:start + columns]
        cells: list[Any] = []
        commands: list[Any] = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]
        for index in range(columns):
            column = index * 2
            if index < len(row):
                card = row[index]
                lines: list[Any] = [Paragraph(_markup(card.get("title", "")).upper(), styles["card_title"])]
                if card.get("value") is not None:
                    lines.append(Paragraph(_markup(card["value"]), styles["metric"]))
                if card.get("text"):
                    lines.append(Paragraph(_markup(card["text"]), styles["body"]))
                for item in card.get("items", []):
                    lines.append(Paragraph(_markup("• " + str(item)), styles["body"]))
                if card.get("citation_ids"):
                    lines.append(Paragraph("".join(f'<super size="7.5" rise="3">[{_markup(ref)}]</super>'
                                                   for ref in card["citation_ids"]), styles["source"]))
                background, accent = tones.get(card.get("tone", "blue"), tones["blue"])
                cells.append(lines)
                commands += [
                    ("BACKGROUND", (column, 0), (column, 0), background),
                    ("LINEBEFORE", (column, 0), (column, 0), 3, accent),
                    ("LEFTPADDING", (column, 0), (column, 0), 9), ("RIGHTPADDING", (column, 0), (column, 0), 9),
                    ("TOPPADDING", (column, 0), (column, 0), 7), ("BOTTOMPADDING", (column, 0), (column, 0), 7),
                ]
            else:
                cells.append("")
            if index < columns - 1:
                cells.append("")
        row_table = Table([cells], colWidths=col_widths, hAlign="LEFT", spaceAfter=gap)
        row_table.setStyle(TableStyle(commands))
        result.append(KeepTogether([row_table]))
    if block.get("citation_ids"):
        result.append(Paragraph(_cited("", block), styles["source"]))
    return result


def _report_block(block: dict[str, Any], styles: dict[str, Any], width: float,
                  block_text: Callable[[dict[str, Any]], str],
                  table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
                  table_views: Callable[[dict[str, Any]], list[tuple[str, str, list[str], list[list[str]]]]],
                  iqb_widths: dict[str, list[int]]) -> list[Any]:
    from reportlab.platypus import Paragraph, Table, TableStyle

    if block["type"] == "table":
        return _report_table(block, styles, width, table_rows, table_views, iqb_widths)
    if block["type"] == "card_grid":
        return _report_card_grid(block, styles, width)
    items = block_flowables(block, styles, width, block_text, table_rows)
    if block.get("data", {}).get("status") in ("missing", "pending", "inconclusive"):
        box = Table([[items]], colWidths=[width])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), styles["_colors"]["danger_soft"]),
            ("LINEBEFORE", (0, 0), (0, -1), 3, styles["_colors"]["danger"]),
            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        return [box]
    return items


def _render_report(content: dict[str, Any], tokens: dict[str, Any], profile: dict[str, Any],
                   path: Path, *, deliverable_label: str, footer_label: str,
                   block_text: Callable[[dict[str, Any]], str],
                   table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
                   table_views: Callable[[dict[str, Any]], list[tuple[str, str, list[str], list[list[str]]]]],
                   iqb_widths: dict[str, list[int]]) -> None:
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, Indenter, PageBreak,
                                   PageTemplate, Paragraph, Spacer, Table, TableStyle)
    from reportlab.platypus.doctemplate import LayoutError

    layout = profile["layout"]
    page = tokens["page"][profile["paper"]]
    paper_width, paper_height = float(page["width"]) * mm, float(page["height"]) * mm
    left, right = float(page["margin_left"]) * mm, float(page["margin_right"]) * mm
    top, bottom = float(page["margin_top"]) * mm, float(page["margin_bottom"]) * mm
    usable_width = paper_width - left - right
    usable_height = paper_height - top - bottom - 10 * mm
    styles = make_styles(tokens, layout)
    palette = {key: colors.HexColor(value) for key, value in tokens["color"].items()}
    logo_path = ROOT / "assets" / "logo_ccee.png"
    logo_width, logo_height = ImageReader(str(logo_path)).getSize()
    scale = min(38 * mm / logo_width, 11 * mm / logo_height)
    from reportlab.platypus import Image
    logo = Image(str(logo_path), width=logo_width * scale, height=logo_height * scale)
    masthead = Table([[Paragraph(_markup(deliverable_label.upper()), styles["eyebrow"]), logo]],
                     colWidths=[usable_width - 40 * mm, 40 * mm])
    masthead.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 1.5, palette["document_primary"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story: list[Any] = [masthead, Spacer(1, 8),
                        Paragraph(_markup(content["title"]), styles["report_title"])]
    if content.get("summary"):
        story.extend([Spacer(1, 6), Paragraph(_markup(content["summary"]), styles["summary"])])
    story.append(Spacer(1, 12))

    class SectionBookmark(Flowable):
        def __init__(self, title: str, key: str):
            super().__init__()
            self.title, self.key = title, key
            self.width = self.height = 0

        def draw(self) -> None:
            self.canv.bookmarkPage(self.key)
            self.canv.addOutlineEntry(self.title, self.key, level=0)

    def section_band(title: str, width: float) -> Any:
        band = Table([[Paragraph(_markup(title.upper()), styles["report_section"])]],
                     colWidths=[width])
        band.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), palette["document_deep"]),
            ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]))
        band.keepWithNext = True
        return band

    sections = group_sections(content["blocks"], block_text)
    section_number = 0
    position = 0
    while position < len(sections):
        item = sections[position]
        if item[0] == "page_break":
            story.append(PageBreak())
            position += 1
            continue
        if (not item[3] and position + 1 < len(sections)
                and sections[position + 1][0] == "section" and not sections[position + 1][3]):
            pair = sections[position:position + 2]
            column_width = (usable_width - 10) / 2
            cells: list[list[Any]] = []
            for offset, (_, title, blocks, _) in enumerate(pair, 1):
                contents: list[Any] = [SectionBookmark(title, f"section-{section_number + offset}"),
                                       section_band(title, column_width), Spacer(1, 7)]
                for block in blocks:
                    contents.extend(_report_block(block, styles, column_width - 22, block_text,
                                                  table_rows, table_views, iqb_widths))
                    contents.append(Spacer(1, 7))
                cells.append(contents)
            table = Table([[cells[0], "", cells[1]]], colWidths=[column_width, 10, column_width])
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
            _, pair_height = table.wrap(usable_width, usable_height)
            if pair_height <= 0.9 * usable_height:
                story.extend([table, Spacer(1, 10)])
                section_number += 2
                position += 2
                continue
        _, title, blocks, _wide = item
        section_number += 1
        story.extend([CondPageBreak(110), SectionBookmark(title, f"section-{section_number}"),
                      section_band(title, usable_width), Spacer(1, 7), Indenter(left=11, right=11)])
        for block in blocks:
            story.extend(_report_block(block, styles, usable_width - 22, block_text,
                                       table_rows, table_views, iqb_widths))
            story.append(Spacer(1, 7))
        story.extend([Indenter(left=-11, right=-11), Spacer(1, 10)])
        position += 1
    if content["citations"]:
        story.extend([Paragraph("Fontes", styles["field"]), Spacer(1, 4)])
        for citation in content["citations"]:
            line = f"<b>{_markup(citation['id'])}</b> — {_markup(citation['source_id'])}"
            if citation.get("locator"):
                line += f", {_markup(citation['locator'])}"
            story.append(Paragraph(line, styles["source"]))

    class NumberedCanvas(Canvas):
        def __init__(self, *args: Any, **kwargs: Any):
            super().__init__(*args, **kwargs)
            self.saved_pages: list[dict[str, Any]] = []

        def showPage(self) -> None:
            self.saved_pages.append(dict(self.__dict__))
            self._startPage()

        def save(self) -> None:
            total = len(self.saved_pages)
            for state in self.saved_pages:
                self.__dict__.update(state)
                self.setFont("Roboto-Medium", styles["footer"].fontSize)
                self.setFillColor(palette["text_muted"])
                self.drawRightString(paper_width - right, bottom / 2,
                                     f"{footer_label} · página {self._pageNumber} de {total}")
                super().showPage()
            super().save()

    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=(paper_width, paper_height),
                          leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
                          title=content["title"], subject=deliverable_label,
                          creator="my_skills render.py", invariant=1)
    frame = Frame(left, bottom + 10 * mm, usable_width, usable_height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="report", frames=[frame]))
    try:
        doc.build(story, canvasmaker=NumberedCanvas)
    except LayoutError as exc:
        raise PdfOverflow(f"{layout}: um bloco não cabe numa página; divida o conteúdo") from exc
    path.write_bytes(buffer.getvalue())


def _render_presentation(content: dict[str, Any], tokens: dict[str, Any], path: Path, *,
                         deliverable_label: str,
                         block_text: Callable[[dict[str, Any]], str],
                         table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
                         load_layout: Callable[[str], dict[str, dict[str, Any]] | None],
                         identity: str) -> None:
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import KeepInFrame, Paragraph, Spacer

    slots = load_layout(content["deliverable_type"]) or {}
    for name in ("logo", "titulo_slide", "corpo_slide", "rodape_slide"):
        if name not in slots or any(key not in slots[name] for key in ("x", "y", "width", "height")):
            raise ValueError(f"layout.json da apresentação sem o slot {name}")
    if float(slots["titulo_slide"]["height"]) < 19:
        raise ValueError("layout.json da apresentação: titulo_slide precisa de pelo menos 19 mm")
    page = tokens["page"]["presentation_16_9"]
    page_width, page_height = float(page["width_in"]) * inch, float(page["height_in"]) * inch
    palette = {key: colors.HexColor(value) for key, value in tokens["color"].items()}
    styles = make_styles(tokens, "presentation")
    definitions = tokens["typography"]["styles"]

    def slide_style(name: str, token: str, color: str, *, size: float | None = None) -> Any:
        spec = definitions[token]
        font_size = size or float(spec["size"])
        font = "Montserrat-Bold" if spec["family"] == "font_brand" else (
            "Roboto-Bold" if spec["weight"] >= 600 else "Roboto-Medium" if spec["weight"] >= 500 else "Roboto-Regular")
        return ParagraphStyle(name, fontName=font, fontSize=font_size,
                              leading=font_size * float(spec["line_height"]),
                              textColor=palette[color], splitLongWords=1)

    styles["cover"] = slide_style("slide_cover", "slide_cover_title", "document_primary")
    styles["slide_title"] = slide_style("slide_title", "slide_title", "document_primary")
    styles["body"] = slide_style("slide_body", "slide_body", "text_body")
    styles["body_inverse"] = slide_style("slide_body_inverse", "slide_body", "inverse")
    styles["metric"] = slide_style("slide_metric", "slide_metric", "document_primary")
    styles["source"] = slide_style("slide_source", "slide_body", "text_body", size=12)
    styles["table_header"] = slide_style("slide_table_header", "slide_body", "inverse", size=12)
    styles["table_body"] = slide_style("slide_table_body", "slide_body", "text_body", size=12)
    styles["card_title"] = slide_style("slide_card_title", "slide_body", "document_primary", size=12)
    footer = slide_style("slide_footer", "slide_footer", "text_muted")
    eyebrow = slide_style("slide_eyebrow", "cover_eyebrow", "document_accent")

    def rectangle(name: str) -> tuple[float, float, float, float]:
        slot = slots[name]
        x, y, width, height = (float(slot[key]) * mm for key in ("x", "y", "width", "height"))
        if min(x, y, width, height) < 0 or x + width > page_width + .1 or y + height > page_height + .1:
            raise ValueError(f"layout.json da apresentação: slot {name} fora da página")
        return x, page_height - y - height, width, height

    title_rect, body_rect = rectangle("titulo_slide"), rectangle("corpo_slide")
    logo_rect, footer_rect = rectangle("logo"), rectangle("rodape_slide")

    sections = _sections(content["blocks"], block_text)
    slides: list[tuple[str, Any]] = [("cover", None)]
    slides.extend(("section", section) for section in sections)
    if content["citations"]:
        # Preserve uma linha de fonte por item e abra continuação quando necessário.
        source_lines = []
        for citation in content["citations"]:
            line = f"{citation['id']} — {citation['source_id']}"
            if citation.get("locator"):
                line += f", {citation['locator']}"
            source_lines.append(line)
        current: list[str] = []
        for line in source_lines:
            candidate = current + [line]
            flow = [Paragraph(_markup(item), styles["source"]) for item in candidate]
            if current and sum(item.wrap(body_rect[2], body_rect[3])[1] + 12 for item in flow) > body_rect[3]:
                slides.append(("sources", current))
                current = [line]
            else:
                current = candidate
        if current:
            slides.append(("sources", current))

    buffer = io.BytesIO()
    canvas = Canvas(buffer, pagesize=(page_width, page_height), invariant=1,
                    pageCompression=1, bottomup=1)
    canvas.setTitle(content["title"])
    canvas.setSubject(deliverable_label)
    canvas.setCreator("my_skills render.py")
    image = ImageReader(str(ROOT / "assets" / "logo_ccee.png"))
    image_width, image_height = image.getSize()
    scale = min(logo_rect[2] / image_width, logo_rect[3] / image_height)

    def draw_frame(flowables: list[Any], rect: tuple[float, float, float, float],
                   number: int, title: str) -> None:
        x, y, width, height = rect
        if not flowables:
            return
        try:
            frame = KeepInFrame(width, height, flowables, mode="error", hAlign="LEFT", vAlign="TOP")
            frame.canv = canvas
            _, used_height = frame.wrap(width, height)
            if used_height > height + .1:
                raise ValueError("altura excedida")
            frame.drawOn(canvas, x, y + height - used_height)
        except Exception as exc:
            raise PdfOverflow(f"slide {number} ({title}) excede a área; divida o conteúdo em mais slides") from exc

    total = len(slides)
    for number, (kind, payload) in enumerate(slides, 1):
        canvas.setFillColor(palette["surface"])
        canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
        canvas.drawImage(image, logo_rect[0], logo_rect[1] + (logo_rect[3] - image_height * scale) / 2,
                         width=image_width * scale, height=image_height * scale, mask="auto")
        if kind == "cover":
            canvas.setFillColor(palette["document_accent"])
            canvas.rect(0, 0, 6 * mm, page_height, fill=1, stroke=0)
            cover_rect = (title_rect[0], title_rect[1] - 34 * mm, title_rect[2], title_rect[3] + 34 * mm)
            cover_items = [Paragraph(_markup(deliverable_label.upper()), eyebrow), Spacer(1, 16),
                           Paragraph(_markup(content["title"]), styles["cover"])]
            draw_frame(cover_items, cover_rect, number, content["title"])
            summary_rect = (body_rect[0], body_rect[1] + 20 * mm, body_rect[2], body_rect[3] - 40 * mm)
            draw_frame([Paragraph(_markup(content.get("summary", "")), styles["body"])],
                       summary_rect, number, content["title"])
        elif kind == "section":
            title, blocks = payload
            draw_frame([Paragraph(_markup(title), styles["slide_title"])], title_rect, number, title)
            items: list[Any] = []
            for block in blocks:
                data = block.get("data", {})
                if block["type"] == "metric":
                    value = data.get("value") or data.get("text") or block_text(block)
                    metric = Paragraph(_cited(value, block), styles["metric"])
                    support = data.get("description") or data.get("title")
                    items.append(metric)
                    if support:
                        items.extend([Spacer(1, 8), Paragraph(_markup(support), styles["body"])])
                elif block["type"] == "card_grid":
                    card = dict(block)
                    card["data"] = {**data, "columns": min(3, int(data.get("columns", 2)))}
                    items.extend(_report_card_grid(card, styles, body_rect[2]))
                else:
                    items.extend(block_flowables(block, styles, body_rect[2], block_text, table_rows))
                items.append(Spacer(1, 12))
            draw_frame(items, body_rect, number, title)
        else:
            title = "Fontes" if not any(item[0] == "sources" for item in slides[:number - 1]) else "Fontes (cont.)"
            draw_frame([Paragraph(title, styles["slide_title"])], title_rect, number, title)
            items = []
            for line in payload:
                items.extend([Paragraph(_markup(line), styles["source"]), Spacer(1, 12)])
            draw_frame(items, body_rect, number, title)

        x, y, width, height = footer_rect
        footer_y = y + (height - footer.fontSize) / 2
        right = f"{number} / {total}"
        if pdfmetrics.stringWidth(identity, footer.fontName, footer.fontSize) + 20 + pdfmetrics.stringWidth(
                right, footer.fontName, footer.fontSize) > width:
            raise PdfOverflow(f"slide {number} (rodapé) excede a área; reduza a identificação")
        canvas.setFont(footer.fontName, footer.fontSize)
        canvas.setFillColor(footer.textColor)
        canvas.drawString(x, footer_y, identity)
        canvas.drawRightString(x + width, footer_y, right)
        canvas.showPage()
    canvas.save()
    path.write_bytes(buffer.getvalue())


def render_pdf(content: dict[str, Any], tokens: dict[str, Any], profile: dict[str, Any], path: Path, *,
               deliverable_label: str, footer_label: str, field_labels: dict[str, str] | None,
               block_text: Callable[[dict[str, Any]], str],
               table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
               table_views: Callable[[dict[str, Any]], list[tuple[str, str, list[str], list[list[str]]]]] | None = None,
               iqb_widths: dict[str, list[int]] | None = None,
               load_presentation_layout: Callable[[str], dict[str, dict[str, Any]] | None] | None = None,
               identity_line: Callable[[dict[str, Any]], str] | None = None) -> None:
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
    if layout == "presentation":
        if load_presentation_layout is None or identity_line is None:
            raise ValueError("Apresentação requer layout e identificação")
        _render_presentation(content, tokens, path, deliverable_label=deliverable_label,
                             block_text=block_text, table_rows=table_rows,
                             load_layout=load_presentation_layout,
                             identity=identity_line(content))
        return
    if layout in ("report_portrait", "report_landscape"):
        if table_views is None or iqb_widths is None:
            raise ValueError("Relatórios requerem table_views e iqb_widths")
        _render_report(content, tokens, profile, path, deliverable_label=deliverable_label,
                       footer_label=footer_label, block_text=block_text,
                       table_rows=table_rows, table_views=table_views, iqb_widths=iqb_widths)
        return
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
