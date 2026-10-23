"""PDF portátil em ReportLab para cards, Briefing e relatórios."""
from __future__ import annotations

import html
import io
import math
import re
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts" / "static"
SUPPORTED_LAYOUTS = ("card_portrait", "executive_one_page", "report_portrait", "report_landscape", "presentation")


class PdfOverflow(ValueError):
    """O conteúdo excede a página única exigida pelo perfil."""


def _font(tokens: dict[str, Any], family: str, weight: int) -> str:
    """Nome da instância estática para a família do token (font_brand é sempre negrito)."""
    name = tokens["typography"][family]
    if family == "font_brand" or weight >= 600:
        return f"{name}-Bold"
    return f"{name}-Medium" if weight >= 500 else f"{name}-Regular"


def _register_fonts(tokens: dict[str, Any]) -> None:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    names = {_font(tokens, "font_brand", 700)} | {_font(tokens, "font_body", weight) for weight in (400, 500, 700)}
    for name in sorted(names):
        font_path = FONT_DIR / f"{name}.ttf"
        if not font_path.is_file():
            raise FileNotFoundError("Fontes estáticas ausentes em assets/fonts/static; rode _TOOLS/make_static_fonts.py")
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(font_path)))
    regular, bold = _font(tokens, "font_body", 400), _font(tokens, "font_body", 700)
    pdfmetrics.registerFontFamily(regular, normal=regular, bold=bold)


def style_specs(tokens: dict[str, Any], layout: str) -> dict[str, dict[str, Any]]:
    """Família, peso, tamanho, entrelinha e cor de cada estilo; o HTML usa os mesmos valores do PDF."""
    definitions = tokens["typography"]["styles"]
    minimum = float(tokens["density"]["minimum_font_size"])

    def spec(name: str, token: str, color: str, *, size: float | None = None,
             weight: int | None = None, leading: float | None = None) -> dict[str, Any]:
        definition = definitions[token]
        font_size = float(size if size is not None else definition["size"])
        if font_size < minimum:
            raise ValueError(f"{name}: fonte abaixo do mínimo de {minimum} pt")
        return {"family": definition["family"],
                "weight": int(weight if weight is not None else definition["weight"]),
                "size": font_size,
                "leading": leading or font_size * float(definition["line_height"]),
                "color": color}

    return {
        "eyebrow": spec("eyebrow", "cover_eyebrow", "document_accent"),
        "title": spec("title", "cover_title", "document_primary", size=24 if layout == "executive_one_page" else None),
        "summary": spec("summary", "body", "text_strong", size=10.5),
        "body": spec("body", "body", "text_body", size=8.5 if layout == "executive_one_page" else None),
        "body_inverse": spec("body_inverse", "body", "inverse", size=8.5 if layout == "executive_one_page" else None),
        "field": spec("field", "section_title", "document_primary", size=13),
        "section": spec("section", "section_title", "inverse", size=9, weight=700),
        "metric": spec("metric", "metric", "document_primary"),
        "table_header": spec("table_header", "table_header", "inverse"),
        "table_body": spec("table_body", "table_body", "text_body"),
        "source": spec("source", "body_dense", "text_body"),
        "footer": spec("footer", "footer", "text_muted"),
        "report_title": spec("report_title", "cover_title", "document_primary",
                             size=24 if layout == "report_landscape" else 25),
        "report_section": spec("report_section", "section_title", "inverse", size=11, weight=700),
        "card_title": spec("card_title", "section_title", "document_primary", size=9, weight=700),
        "score_head": spec("score_head", "label", "text_muted"),
        "score_value": spec("score_value", "table_body", "document_accent", weight=700),
        "badge": spec("badge", "label", "document_primary"),
        "callout_label": spec("callout_label", "label", "document_accent_soft"),
    }


def slide_style_specs(tokens: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Estilos próprios dos slides, sobrepostos aos de style_specs na apresentação."""
    definitions = tokens["typography"]["styles"]

    def spec(token: str, color: str, *, size: float | None = None) -> dict[str, Any]:
        definition = definitions[token]
        font_size = size or float(definition["size"])
        return {"family": definition["family"], "weight": int(definition["weight"]), "size": font_size,
                "leading": font_size * float(definition["line_height"]), "color": color}

    return {
        "cover": spec("slide_cover_title", "document_primary"),
        "slide_title": spec("slide_title", "document_primary"),
        "body": spec("slide_body", "text_body"),
        "body_inverse": spec("slide_body", "inverse"),
        "metric": spec("slide_metric", "document_primary"),
        "source": spec("slide_body", "text_body", size=12),
        "table_header": spec("slide_body", "inverse", size=12),
        "table_body": spec("slide_body", "text_body", size=12),
        "card_title": spec("slide_body", "document_primary", size=12),
        "footer": spec("slide_footer", "text_muted"),
        "eyebrow": spec("cover_eyebrow", "document_accent"),
    }


def _paragraph_style(tokens: dict[str, Any], name: str, spec: dict[str, Any], **extra: Any) -> Any:
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    return ParagraphStyle(name, fontName=_font(tokens, spec["family"], spec["weight"]), fontSize=spec["size"],
                          leading=spec["leading"], textColor=colors.HexColor(tokens["color"][spec["color"]]),
                          splitLongWords=1, **extra)


def make_styles(tokens: dict[str, Any], layout: str) -> dict[str, Any]:
    from reportlab.lib import colors

    result: dict[str, Any] = {name: _paragraph_style(tokens, name, spec, spaceAfter=0, spaceBefore=0)
                              for name, spec in style_specs(tokens, layout).items()}
    result["_colors"] = {name: colors.HexColor(value) for name, value in tokens["color"].items()}
    return result


def _markup(value: Any) -> str:
    # Negrito em Markdown (**texto**), usado na Descrição da CDT.
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(str(value))).replace("\n", "<br/>")


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


def paginate_table_rows(headings: list[str], rows: list[list[str]], width_pt: float,
                        height_pt: float, font_pt: float = 14) -> list[tuple[list[list[str]], list[float]]]:
    """Divide linhas com um orçamento conservador comum ao PDF e ao PPTX."""
    columns = max(1, len(headings), *(len(row) for row in rows)) if rows else max(1, len(headings))
    chars_per_line = max(8, int((width_pt / columns - 16) / (font_pt * .56)))

    def row_height(cells: list[str]) -> float:
        lines = max(1, *(math.ceil(len(str(cell)) / chars_per_line) for cell in cells)) if cells else 1
        return max(27, lines * font_pt * 1.3 + 12)

    budget = height_pt - 42  # legenda e folga para bordas/medição dos dois motores
    header_height = row_height(headings)
    if header_height >= budget:
        raise PdfOverflow("tabela da apresentação: cabeçalho não cabe na área do slide")
    chunks: list[tuple[list[list[str]], list[float]]] = []
    current: list[list[str]] = []
    heights: list[float] = []
    used = header_height
    for row in rows:
        height = row_height(row)
        if height + header_height > budget:
            raise PdfOverflow("tabela da apresentação: uma linha não cabe no slide; resuma a célula")
        if current and (len(current) >= 8 or used + height > budget):
            chunks.append((current, [header_height, *heights]))
            current, heights, used = [], [], header_height
        current.append(row)
        heights.append(height)
        used += height
    if current or not chunks:
        chunks.append((current, [header_height, *heights]))
    return chunks


def group_sections(blocks: list[dict[str, Any]], block_text: Callable[[dict[str, Any]], str]) -> list[tuple[Any, ...]]:
    """Agrupa blocos pelas mesmas fronteiras de heading/page_break do HTML."""
    result: list[tuple[Any, ...]] = []
    title = "Notas"
    body: list[dict[str, Any]] = []
    titled = False  # o título veio de um heading e ainda não foi emitido

    def flush() -> None:
        nonlocal body, titled
        # Como no HTML, um heading aparece mesmo sem conteúdo até o próximo heading ou quebra.
        if body or titled:
            wide = any(block["type"] in ("table", "card_grid", "canvas", "chart") for block in body)
            result.append(("section", title, body, wide))
            body = []
        titled = False

    for block in blocks:
        if block["type"] == "heading":
            flush()
            title = block_text(block)
            titled = True
        elif block["type"] == "page_break":
            flush()
            result.append(("page_break",))
            title = "Notas"
        else:
            body.append(block)
    flush()
    return result


# Tipos cuja ordem e colunas vêm do layout.json do Layout Studio; o conteúdo continua fluindo entre páginas.
FLOW_LAYOUT_TYPES = ("innovation_potential_assessment",)
# Tipos em que cada seção ocupa a largura inteira: nunca agrupa duas seções curtas lado a lado.
SINGLE_COLUMN_TYPES = ("cdt",)
FLOW_FIXED_SLOTS = ("titulo_documento", "identificacao_versao", "logo", "rodape")
SCORE_LABELS = {"impact": "Impacto", "viability": "Viabilidade", "strategic_alignment": "Alinhamento estratégico",
                "urgency": "Urgência", "innovation": "Novidade"}
# Selo da classificação: (fundo, texto) do tokens.json; o rótulo sempre aparece por extenso.
SCORE_PANEL_SHARES = (.19, .08, .19, .14, .40)
IQB_PANEL_SHARES = (.14, .08, .08, .14, .16, .11, .29)
IQB_DIMENSION_LABELS = {"clarity": "Clareza", "evidence": "Evidências", "outcomes": "Resultados",
                        "actionability": "Acionabilidade"}
BADGE_TONES = {"priorizar": ("document_accent", "inverse"), "monitorar": ("document_accent_soft", "document_primary"),
               "arquivar": ("surface_muted", "text_muted"), "": ("surface_muted", "text_muted")}
IQB_BADGE_TONES = {"Excelente": ("document_accent", "inverse"), "Saudavel": ("document_accent", "inverse"),
                   "Adequado": ("document_accent_soft", "document_primary"), "Fragil": ("danger_soft", "danger"),
                   "Insuficiente": ("danger", "inverse")}


def plan_flow(content: dict[str, Any], slots: dict[str, dict[str, Any]]) -> tuple[list[list[dict[str, Any]]], list[dict[str, Any]]]:
    """Linhas de células na ordem do Studio (y, depois x) e os blocos sem slot, que seguem no fim.

    Slots com a mesma altura de topo formam uma linha de duas colunas; slot mais estreito que 60% do
    maior ocupa meia largura. display_mode define o componente: title_and_content (card com faixa),
    content_only (caixa escura sem título) e tabular_list (tabela ou painel de notas).
    """
    candidates = [{**slot, "key": slot.get("section_key") or name} for name, slot in slots.items()
                  if name not in FLOW_FIXED_SLOTS and (slot.get("section_key") or name) not in FLOW_FIXED_SLOTS]
    candidates.sort(key=lambda slot: (float(slot["y"]), float(slot["x"])))
    widest = max((float(slot["width"]) for slot in candidates), default=1.0)
    used: set[int] = set()
    rows: list[list[dict[str, Any]]] = []
    for slot in candidates:
        key = slot["key"]
        heading = next((block for block in content["blocks"] if block["type"] == "heading"
                        and block.get("data", {}).get("section_key") in (key, f"{key}_heading")), None)
        blocks = [block for block in content["blocks"] if block["type"] != "heading"
                  and block.get("data", {}).get("section_key") == key]
        if not blocks and heading is None:
            continue
        used.update(id(block) for block in blocks)
        if heading is not None:
            used.add(id(heading))
        cell = {"key": key, "heading": heading, "blocks": blocks, "y": float(slot["y"]),
                "mode": slot.get("display_mode") or "title_and_content",
                "half": float(slot["width"]) < .6 * widest}
        if rows and len(rows[-1]) < 2 and abs(rows[-1][0]["y"] - cell["y"]) < 3:
            rows[-1].append(cell)
        else:
            rows.append([cell])
    for row in rows:
        if len(row) == 2:
            for cell in row:
                cell["half"] = True
    return rows, [block for block in content["blocks"] if id(block) not in used]


def _number_text(value: float) -> str:
    return f"{round(float(value), 4):g}"


def score_panel_data(block: dict[str, Any]) -> dict[str, Any]:
    """Conteúdo do painel de notas: colunas, linhas (com o valor da barra), total e selo.

    Potencial: peso em %, nota de 0 a 100 e ponderado sem arredondar (a soma fecha com o total).
    IQB: notas por dimensão de 1 a 5, com veto e teto; o total é o IQB validado do bloco "iqb".
    """
    data = block.get("data", {})
    if isinstance(data.get("dimensions"), dict):
        rows = []
        for dimension, detail in data["dimensions"].items():
            final = detail.get("final_score")
            numeric = isinstance(final, (int, float)) and not isinstance(final, bool)
            ceiling = detail.get("veto_max_score")
            if detail.get("veto_triggered"):
                veto = f"Disparado (teto {ceiling}): {detail.get('veto_detail') or 'sem detalhe'}"
            else:
                veto = f"Não disparado (teto {ceiling})" if ceiling is not None else "Não disparado"
            rows.append({"cells": [IQB_DIMENSION_LABELS.get(dimension, dimension), str(detail.get("yes_count", "")),
                                   str(detail.get("raw_score", "")), _number_text(final) if numeric else "sem nota", veto,
                                   str(detail.get("label", "")), str(detail.get("justification", ""))],
                         "bar": max(0.0, min(100.0, float(final) * 20)) if numeric else None})
        summary = data.get("panel_total") or {}
        total, classification = summary.get("score"), str(summary.get("classification") or "")
        return {"title": "Notas por dimensão", "rows": rows, "total_prefix": "IQB",
                "heads": ["Dimensão", "Sim (de 9)", "Nota bruta", "Nota final (1 a 5)", "Veto", "Rótulo", "Justificativa"],
                "shares": IQB_PANEL_SHARES, "bar": 3, "strong": (0, 5), "value": 3, "badge_column": 5,
                "total_label": "IQB (média das quatro dimensões)",
                "total": _number_text(total) if isinstance(total, (int, float)) else "pendente",
                "badge": (classification or "pendente").upper(),
                "tone": IQB_BADGE_TONES.get(classification, BADGE_TONES[""])}
    rows = []
    for row in data.get("rows", []):
        score, weight = row.get("score"), row.get("weight")
        numeric = isinstance(score, (int, float)) and not isinstance(score, bool)
        rows.append({"cells": [str(row.get("label") or SCORE_LABELS.get(row.get("criterion", ""), row.get("criterion", ""))),
                               f"{_number_text(weight * 100)}%" if isinstance(weight, (int, float)) else "sem peso",
                               _number_text(score) if numeric else "sem nota",
                               _number_text(score * weight) if numeric and isinstance(weight, (int, float)) else "sem nota",
                               str(row.get("justification") or "")],
                     "bar": max(0.0, min(100.0, float(score))) if numeric else None})
    total = data.get("overall_score")
    classification = data.get("classification") if data.get("classification") in BADGE_TONES else ""
    return {"title": str(data.get("title") or "Pontuação por critério"), "rows": rows, "total_prefix": "Total",
            "heads": ["Critério", "Peso", "Nota (0 a 100)", "Ponderado", "Justificativa"],
            "shares": SCORE_PANEL_SHARES, "bar": 2, "strong": (0, 3), "value": 3, "badge_column": 4,
            "total_label": "Total ponderado",
            "total": _number_text(total) if isinstance(total, (int, float)) else "pendente",
            "badge": (classification or "pendente").upper(), "tone": BADGE_TONES[classification]}


def panel_widths(panel: dict[str, Any], styles: dict[str, Any], width: float) -> list[float]:
    """Larguras do painel: as proporções do tipo, alargando a coluna em que a palavra mais longa não cabe."""
    column_styles = ["score_value" if index == panel["bar"] else "card_title" if index in panel["strong"] else "table_body"
                     for index in range(len(panel["heads"]))]
    total = [""] * len(panel["heads"])
    total[panel["value"]], total[panel["badge_column"]] = panel["total"], panel["badge"]
    lines = [panel["heads"], *(row["cells"] for row in panel["rows"]), total]
    return _content_widths(lines, len(panel["heads"]), width, 7, styles, [share * 100 for share in panel["shares"]],
                           column_styles=column_styles, header_style="score_head")


def is_score_panel(block: dict[str, Any]) -> bool:
    data = block.get("data", {})
    return (block["type"] == "table" and data.get("section_key") == "scores" and isinstance(data.get("rows"), list)
            and all(isinstance(row, dict) and "score" in row for row in data["rows"]))


def with_panel_totals(content: dict[str, Any]) -> dict[str, Any]:
    """Leva o IQB validado (bloco "iqb") ao bloco de notas por dimensão, para o painel mostrar total e selo."""
    iqb = next((block["data"] for block in content["blocks"] if block.get("data", {}).get("section_key") == "iqb"), None)
    if iqb is None:
        return content
    blocks = [{**block, "data": {**block["data"], "panel_total": {"score": iqb.get("score"),
                                                                   "classification": iqb.get("classification")}}}
              if isinstance(block.get("data", {}).get("dimensions"), dict) else block for block in content["blocks"]]
    return {**content, "blocks": blocks}


def _score_panel(block: dict[str, Any], styles: dict[str, Any], width: float) -> list[Any]:
    """Painel de notas: faixa com título, total e selo; tabela com barra e linha de total."""
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Flowable, KeepTogether, Paragraph, Spacer, Table, TableStyle

    palette = styles["_colors"]
    panel = score_panel_data(block)

    class ScoreBar(Flowable):
        def __init__(self, value: float | None):
            super().__init__()
            self.value = value

        def wrap(self, available_width: float, available_height: float) -> tuple[float, float]:
            self.width = available_width
            return available_width, 7

        def draw(self) -> None:
            self.canv.setFillColor(palette["border"])
            self.canv.roundRect(0, 3, self.width, 4, 2, fill=1, stroke=0)
            if self.value:
                self.canv.setFillColor(palette["document_accent"])
                self.canv.roundRect(0, 3, self.width * self.value / 100, 4, 2, fill=1, stroke=0)

    background, foreground = panel["tone"]
    badge_style = ParagraphStyle("score_badge", parent=styles["badge"], textColor=palette[foreground], alignment=1)
    badge = Table([[Paragraph(_markup(panel["badge"]), badge_style)]], colWidths=[74], cornerRadii=[8, 8, 8, 8])
    badge.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), palette[background]),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    total_style = ParagraphStyle("score_total", parent=styles["section"], alignment=2)
    header = Table([[Paragraph(_markup(panel["title"].upper()), styles["section"]),
                     Paragraph(_markup(f"{panel['total_prefix']}: {panel['total']}"), total_style), badge]],
                   colWidths=[width - 172, 90, 82])
    header.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), palette["document_deep"]),
                                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                                ("RIGHTPADDING", (1, 0), (1, 0), 4), ("LEFTPADDING", (2, 0), (2, 0), 4),
                                ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    columns = len(panel["heads"])
    matrix: list[list[Any]] = [[Paragraph(_markup(head), styles["score_head"]) for head in panel["heads"]]]
    for row in panel["rows"]:
        cells: list[Any] = []
        for index, value in enumerate(row["cells"]):
            if index == panel["bar"]:
                cells.append([ScoreBar(row["bar"]), Paragraph(_markup(value), styles["score_value"])])
            else:
                style = styles["card_title"] if index in panel["strong"] else styles["table_body"]
                cells.append(Paragraph(_markup(value), style))
        matrix.append(cells)
    total_row: list[Any] = [""] * columns
    total_row[0] = Paragraph(_markup(panel["total_label"]), styles["card_title"])
    total_row[panel["value"]] = Paragraph(_markup(panel["total"]), styles["card_title"])
    total_row[panel["badge_column"]] = Paragraph(_markup(panel["badge"]), styles["score_value"])
    matrix.append(total_row)
    table = Table(matrix, colWidths=panel_widths(panel, styles, width), repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), palette["surface_muted"]),
        ("BACKGROUND", (0, -1), (-1, -1), palette["surface_muted"]),
        ("SPAN", (0, -1), (panel["value"] - 1, -1)),
        ("LINEBELOW", (0, 0), (-1, -2), .75, palette["border"]),
        ("LINEABOVE", (0, -1), (-1, -1), 1.5, palette["border_strong"]),
        ("BOX", (0, 0), (-1, -1), .75, palette["border"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    # O painel inteiro vai para a página seguinte quando não cabe; se for maior que a página, divide.
    result: list[Any] = [KeepTogether([header, table])]
    if block.get("citation_ids"):
        result.extend([Spacer(1, 3), Paragraph(_cited("", block), styles["source"])])
    return result


def _flow_row(row: list[dict[str, Any]], styles: dict[str, Any], width: float,
              block_text: Callable[[dict[str, Any]], str],
              table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
              table_views: Callable[[dict[str, Any]], list[tuple[str, str, list[str], list[list[str]]]]],
              iqb_widths: dict[str, list[int]]) -> list[Any]:
    """Uma linha do layout do Studio: card compacto, caixa escura ou painel de notas, em 1 ou 2 colunas."""
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

    palette = styles["_colors"]
    gap = 8
    half = (width - gap) / 2
    if len(row) == 1 and row[0]["mode"] == "tabular_list":
        cell = row[0]
        cell_width = half if cell["half"] else width
        result: list[Any] = []
        for block in cell["blocks"]:
            result.extend(_score_panel(block, styles, cell_width) if is_score_panel(block)
                          else _report_block(block, styles, cell_width, block_text, table_rows, table_views, iqb_widths))
        return result
    titled = any(cell["mode"] == "title_and_content" and cell["heading"] is not None for cell in row)
    columns = [half, gap, half] if row[0]["half"] else [width]
    bands: list[Any] = []
    bodies: list[Any] = []
    commands: list[Any] = [("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]
    body_row = 1 if titled else 0
    for index in range(len(columns)):
        if index % 2 == 1 or index // 2 >= len(row):
            bands.append("")
            bodies.append("")
            continue
        cell, column = row[index // 2], index
        inner_width = columns[column] - 18
        dark = cell["mode"] == "content_only"
        items: list[Any] = []
        if dark and cell["heading"] is not None:
            # Sem faixa de título: o rótulo fica dentro da caixa escura, pequeno, para o texto não se perder.
            items += [Paragraph(_markup(block_text(cell["heading"]).upper()), styles["callout_label"]), Spacer(1, 3)]
        for block in cell["blocks"]:
            if dark and block["type"] not in ("table", "card_grid"):
                items.append(Paragraph(_cited(block_text(block), block), styles["body_inverse"]))
            else:
                items.extend(_report_block(block, styles, inner_width, block_text, table_rows, table_views, iqb_widths))
            items.append(Spacer(1, 4))
        if items:
            items.pop()
        has_band = cell["mode"] == "title_and_content" and cell["heading"] is not None
        bands.append(Paragraph(_markup(block_text(cell["heading"]).upper()), styles["section"]) if has_band else "")
        bodies.append(items)
        if titled and has_band:
            commands += [("BACKGROUND", (column, 0), (column, 0), palette["document_deep"]),
                         ("LEFTPADDING", (column, 0), (column, 0), 9), ("RIGHTPADDING", (column, 0), (column, 0), 9),
                         ("TOPPADDING", (column, 0), (column, 0), 5), ("BOTTOMPADDING", (column, 0), (column, 0), 5)]
        elif titled:
            commands.append(("SPAN", (column, 0), (column, 1)))
        top = 0 if titled and not has_band else body_row
        commands += [("LEFTPADDING", (column, top), (column, body_row), 9),
                     ("RIGHTPADDING", (column, top), (column, body_row), 9),
                     ("TOPPADDING", (column, top), (column, body_row), 8),
                     ("BOTTOMPADDING", (column, top), (column, body_row), 8)]
        if dark:
            commands += [("BACKGROUND", (column, top), (column, body_row), palette["document_deep"]),
                         ("LINEBEFORE", (column, top), (column, body_row), 3, palette["document_accent"])]
        else:
            commands += [("BACKGROUND", (column, body_row), (column, body_row), palette["surface_muted"]),
                         ("BOX", (column, 0), (column, body_row), .75, palette["border"])]
    if titled:
        matrix = [bands, bodies]
        # Células escuras sem título ocupam as duas linhas: o conteúdo vai na primeira.
        for column in range(len(columns)):
            if column % 2 == 0 and column // 2 < len(row) and bands[column] == "":
                matrix[0][column], matrix[1][column] = bodies[column], ""
    else:
        matrix = [bodies]
    table = Table(matrix, colWidths=columns, hAlign="LEFT")
    table.setStyle(TableStyle(commands))
    return [table]


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
        if slug == "dimensoes":
            # Notas por dimensão do IQB no painel de notas, com o IQB e a classificação.
            result.extend([*_score_panel({**block, "citation_ids": []}, styles, width), Spacer(1, 7)])
            continue
        if caption:
            result.append(Paragraph(_markup(caption), caption_style))
        ncols = max(1, len(headings), *(len(row) for row in rows)) if rows else max(1, len(headings))
        matrix = [[Paragraph(_markup(headings[index] if index < len(headings) else ""),
                             styles["table_header"]) for index in range(ncols)]]
        matrix.extend([Paragraph(_markup(row[index] if index < len(row) else ""),
                                 styles["table_body"]) for index in range(ncols)] for row in rows)
        proportions = iqb_widths.get(slug)
        padding = 4 if proportions else 6
        col_widths = _content_widths([headings, *rows], ncols, width, padding, styles,
                                     proportions if proportions and len(proportions) == ncols else None)
        table = Table(matrix, colWidths=col_widths, repeatRows=1, splitByRow=1)
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


def _content_widths(lines: list[list[str]], ncols: int, width: float, padding: float,
                    styles: dict[str, Any], proportions: list[float] | None = None,
                    column_styles: list[str] | None = None, header_style: str = "table_header") -> list[float]:
    """Larguras em que cada coluna cabe sua palavra mais longa. Com proporções fixas, mantém-nas e
    só alarga as colunas estreitas demais, tirando a diferença das que têm folga; sem proporções,
    divide o espaço que sobra pela quantidade de texto. Sem espaço para isso, mantém a base."""
    from reportlab.pdfbase.pdfmetrics import stringWidth

    minimum, amount = [0.0] * ncols, [0.0] * ncols
    for number, line in enumerate(lines):
        for index in range(ncols):
            style = styles[header_style if number == 0 else column_styles[index] if column_styles else "table_body"]
            text = str(line[index]) if index < len(line) else ""
            words = [stringWidth(word, style.fontName, style.fontSize) for word in text.split()]
            minimum[index] = max(minimum[index], max(words, default=0) + 2 * padding + 1)
            amount[index] += sum(words)
    spare = width - sum(minimum)
    if proportions:
        base = [width * proportion / 100 for proportion in proportions]
        widths = [max(low, start) for low, start in zip(minimum, base)]
        slack = [current - low for current, low in zip(widths, minimum)]
        excess = sum(widths) - width
        if spare < 0 or excess > sum(slack):
            return base
        return [current - excess * room / sum(slack) if sum(slack) else current
                for current, room in zip(widths, slack)]
    if spare < 0 or not sum(amount):
        return [width / ncols] * ncols
    return [low + spare * share / sum(amount) for low, share in zip(minimum, amount)]


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
                   iqb_widths: dict[str, list[int]],
                   load_layout: Callable[[str], dict[str, dict[str, Any]] | None] | None = None) -> None:
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, Indenter, KeepTogether,
                                   PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)
    from reportlab.platypus.doctemplate import LayoutError

    content = with_panel_totals(content)
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

    remaining = content["blocks"]
    slots = load_layout(content["deliverable_type"]) if load_layout and content["deliverable_type"] in FLOW_LAYOUT_TYPES else None
    if slots:
        rows, remaining = plan_flow(content, slots)
        for row in rows:
            story.extend(_flow_row(row, styles, usable_width, block_text, table_rows, table_views, iqb_widths))
            story.append(Spacer(1, 8))
        story.append(Spacer(1, 4))
    sections = group_sections(remaining, block_text)
    section_number = 0
    position = 0
    while position < len(sections):
        item = sections[position]
        if item[0] == "page_break":
            story.append(PageBreak())
            position += 1
            continue
        if (not item[3] and position + 1 < len(sections) and content["deliverable_type"] not in SINGLE_COLUMN_TYPES
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
        lines = []
        for citation in content["citations"]:
            line = f"<b>{_markup(citation['id'])}</b>: {_markup(citation['source_id'])}"
            if citation.get("locator"):
                line += f", {_markup(citation['locator'])}"
            lines.append(Paragraph(line, styles["source"]))
        # O título não fica sozinho no pé da página: acompanha a primeira fonte.
        story.extend([KeepTogether([Paragraph("Fontes", styles["field"]), Spacer(1, 4), lines[0]]), *lines[1:]])

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
                self.setFont(styles["footer"].fontName, styles["footer"].fontSize)
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


def plan_slides(content: dict[str, Any], block_text: Callable[[dict[str, Any]], str],
                table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
                table_views: Callable[[dict[str, Any]], list[tuple[str, str, list[str], list[list[str]]]]] | None,
                body_width: float, body_height: float,
                sources_fit: Callable[[list[str]], bool]) -> list[tuple[str, Any]]:
    """Sequência de slides (capa, seções com tabelas paginadas e fontes), comum ao PDF e ao HTML."""
    sections = _sections(content["blocks"], block_text)
    slides: list[tuple[str, Any]] = [("cover", None)]
    for section_title, blocks in sections:
        pending: list[dict[str, Any]] = []
        for block in blocks:
            if block["type"] != "table":
                pending.append(block)
                continue
            if pending:
                slides.append(("section", (section_title, pending)))
                pending = []
            views = table_views(block) if table_views else [("", "", *table_rows(block))]
            continued = False
            for _, legend, heads, rows in views:
                for chunk, _ in paginate_table_rows(heads, rows, body_width, body_height):
                    table_block = {**block, "data": {"headers": heads, "rows": chunk,
                                                      "title": legend or block.get("data", {}).get("title", "")}}
                    slide_title = section_title + (" (continuação)" if continued else "")
                    slides.append(("section", (slide_title, [table_block])))
                    continued = True
        if pending:
            slides.append(("section", (section_title, pending)))
    if content["citations"]:
        # Preserve uma linha de fonte por item e abra continuação quando necessário.
        source_lines = []
        for citation in content["citations"]:
            line = f"{citation['id']}: {citation['source_id']}"
            if citation.get("locator"):
                line += f", {citation['locator']}"
            source_lines.append(line)
        current: list[str] = []
        for line in source_lines:
            candidate = current + [line]
            if current and not sources_fit(candidate):
                slides.append(("sources", current))
                current = [line]
            else:
                current = candidate
        if current:
            slides.append(("sources", current))
    return slides


def _render_presentation(content: dict[str, Any], tokens: dict[str, Any], path: Path, *,
                         deliverable_label: str,
                         block_text: Callable[[dict[str, Any]], str],
                         table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]],
                         table_views: Callable[[dict[str, Any]], list[tuple[str, str, list[str], list[list[str]]]]] | None,
                         load_layout: Callable[[str], dict[str, dict[str, Any]] | None],
                         identity: str) -> None:
    from reportlab.lib import colors
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
    names = {"cover": "slide_cover", "slide_title": "slide_title", "body": "slide_body",
             "body_inverse": "slide_body_inverse", "metric": "slide_metric", "source": "slide_source",
             "table_header": "slide_table_header", "table_body": "slide_table_body",
             "card_title": "slide_card_title", "footer": "slide_footer", "eyebrow": "slide_eyebrow"}
    slide_styles = {key: _paragraph_style(tokens, names[key], spec) for key, spec in slide_style_specs(tokens).items()}
    footer, eyebrow = slide_styles.pop("footer"), slide_styles.pop("eyebrow")
    styles.update(slide_styles)

    def rectangle(name: str) -> tuple[float, float, float, float]:
        slot = slots[name]
        x, y, width, height = (float(slot[key]) * mm for key in ("x", "y", "width", "height"))
        if min(x, y, width, height) < 0 or x + width > page_width + .1 or y + height > page_height + .1:
            raise ValueError(f"layout.json da apresentação: slot {name} fora da página")
        return x, page_height - y - height, width, height

    title_rect, body_rect = rectangle("titulo_slide"), rectangle("corpo_slide")
    logo_rect, footer_rect = rectangle("logo"), rectangle("rodape_slide")

    def sources_fit(lines: list[str]) -> bool:
        flow = [Paragraph(_markup(item), styles["source"]) for item in lines]
        return sum(item.wrap(body_rect[2], body_rect[3])[1] + 12 for item in flow) <= body_rect[3]

    slides = plan_slides(content, block_text, table_rows, table_views, body_rect[2], body_rect[3], sources_fit)

    buffer = io.BytesIO()
    canvas = Canvas(buffer, pagesize=(page_width, page_height), invariant=1,
                    pageCompression=1, bottomup=1)
    canvas.setTitle(content["title"])
    canvas.setSubject(deliverable_label)
    canvas.setCreator("my_skills render.py")
    image = ImageReader(str(ROOT / "assets" / "logo_ccee.png"))
    image_width, image_height = image.getSize()
    # Como no HTML e no PPTX: o logo cabe no slot e em 38 x 11 mm, alinhado à direita.
    scale = min(min(logo_rect[2], 38 * mm) / image_width, min(logo_rect[3], 11 * mm) / image_height)
    logo_x = logo_rect[0] + logo_rect[2] - image_width * scale

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
        canvas.drawImage(image, logo_x, logo_rect[1] + (logo_rect[3] - image_height * scale) / 2,
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


ONE_PAGE_SLOTS = ("titulo_documento", "identificacao_versao")


def _render_one_page_layout(content: dict[str, Any], tokens: dict[str, Any], profile: dict[str, Any], path: Path, *,
                            deliverable_label: str, slots: dict[str, dict[str, Any]],
                            block_text: Callable[[dict[str, Any]], str],
                            table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]], identity: str) -> None:
    """Resumo de uma página desenhado nos slots do layout.json do Layout Studio.

    Cada slot recebe os blocos com o mesmo section_key. O HMW aparece sem subtítulo; os
    demais blocos mostram o subtítulo (data.title) e o conteúdo. Nada fica fora dos slots.
    """
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import KeepInFrame, Paragraph, Spacer
    from reportlab.platypus.doctemplate import LayoutError

    page = tokens["page"][profile["paper"]]
    page_width, page_height = float(page["width"]) * mm, float(page["height"]) * mm
    palette = {key: colors.HexColor(value) for key, value in tokens["color"].items()}
    styles = make_styles(tokens, "executive_one_page")
    hmw_style = ParagraphStyle("one_page_hmw", parent=styles["field"], fontSize=15, leading=19,
                               textColor=palette["inverse"])
    subtitle = ParagraphStyle("one_page_subtitle", parent=styles["field"], fontSize=11, leading=14, spaceAfter=5)
    body = ParagraphStyle("one_page_body", parent=styles["body"], fontSize=10, leading=13.5, spaceAfter=4)
    small = ParagraphStyle("one_page_small", parent=styles["footer"])
    gap = 1.5 * mm

    def rectangle(name: str) -> tuple[float, float, float, float]:
        slot = slots[name]
        x, y, width, height = (float(slot[key]) * mm for key in ("x", "y", "width", "height"))
        if min(x, y, width, height) < 0 or x + width > page_width + .1 or y + height > page_height + .1:
            raise ValueError(f"layout.json do resumo: slot {name} fora da página")
        return x, page_height - y - height, width, height

    buffer = io.BytesIO()
    canvas = Canvas(buffer, pagesize=(page_width, page_height), invariant=1, pageCompression=1, bottomup=1)
    canvas.setTitle(content["title"])
    canvas.setSubject(deliverable_label)
    canvas.setCreator("my_skills render.py")
    canvas.setFillColor(palette["surface"])
    canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    def draw(flowables: list[Any], rect: tuple[float, float, float, float], name: str, *,
             background: Any = None, accent: Any = None, padding: float = 0, middle: bool = False) -> None:
        x, y, width, height = rect
        if background is not None:
            x, y, width, height = x + gap, y + gap, width - 2 * gap, height - 2 * gap
            canvas.setFillColor(background)
            canvas.rect(x, y, width, height, fill=1, stroke=0)
            if accent is not None:
                canvas.setFillColor(accent)
                canvas.rect(x, y, 3, height, fill=1, stroke=0)
        inner_width, inner_height = width - 2 * padding, height - 2 * padding
        frame = KeepInFrame(inner_width, inner_height, flowables, mode="error", hAlign="LEFT", vAlign="TOP")
        frame.canv = canvas
        try:
            _, used = frame.wrap(inner_width, inner_height)
        except LayoutError as exc:
            raise PdfOverflow(f"executive_one_page excedeu uma página: o bloco {name} não cabe na área do layout; "
                              "resuma o conteúdo sem reduzir a fonte") from exc
        if used > inner_height + .1:
            raise PdfOverflow(f"executive_one_page excedeu uma página: o bloco {name} não cabe na área do layout; "
                              "resuma o conteúdo sem reduzir a fonte")
        top_offset = (inner_height - used) / 2 if middle else 0
        frame.drawOn(canvas, x + padding, y + padding + inner_height - used - top_offset)

    # Cabeçalho na faixa acima do slot de título: rótulo do tipo à esquerda, logo à direita e
    # linha; o slot titulo_documento fica só com o título.
    tx, ty, tw, th = rectangle("titulo_documento")
    band_top = page_height - 3 * mm
    image = ImageReader(str(ROOT / "assets" / "logo_ccee.png"))
    image_width, image_height = image.getSize()
    available = band_top - (ty + th) - 2 * mm
    if available < 5 * mm:
        raise ValueError("layout.json do resumo: titulo_documento precisa de ao menos 10 mm livres acima")
    scale = min(38 * mm / image_width, min(11 * mm, available) / image_height)
    logo_width, logo_height = image_width * scale, image_height * scale
    canvas.drawImage(image, tx + tw - logo_width, band_top - logo_height, width=logo_width,
                     height=logo_height, mask="auto")
    canvas.setFont(styles["eyebrow"].fontName, styles["eyebrow"].fontSize)
    canvas.setFillColor(styles["eyebrow"].textColor)
    canvas.drawString(tx, band_top - logo_height / 2 - styles["eyebrow"].fontSize / 3, deliverable_label.upper())
    canvas.setStrokeColor(palette["document_primary"])
    canvas.setLineWidth(1.5)
    line_y = band_top - logo_height - 1.5 * mm
    canvas.line(tx, line_y, tx + tw, line_y)
    draw([Paragraph(_markup(content["title"]), styles["title"])], (tx, ty, tw, th), "titulo_documento", middle=True)

    by_key: dict[str, list[dict[str, Any]]] = {}
    for block in content["blocks"]:
        by_key.setdefault(block.get("data", {}).get("section_key"), []).append(block)
    mapped_keys = {slot.get("section_key") or name for name, slot in slots.items()
                   if name not in ONE_PAGE_SLOTS}
    unmapped = [block["id"] for block in content["blocks"]
                if block["type"] != "page_break" and block.get("data", {}).get("section_key") not in mapped_keys]
    if unmapped:
        raise ValueError("executive_one_page: blocos sem slot no layout: " + ", ".join(unmapped))
    for name, slot in slots.items():
        key = slot.get("section_key") or name
        if name in ONE_PAGE_SLOTS or key in ONE_PAGE_SLOTS or key not in by_key:
            continue
        rect = rectangle(name)
        blocks = by_key[key]
        if key == "hmw":
            items = [Paragraph(_cited(block_text(block), block), hmw_style) for block in blocks]
            draw(items, rect, name, background=palette["document_deep"], accent=palette["document_accent"],
                 padding=5 * mm, middle=True)
            continue
        items = []
        for block in blocks:
            data = block.get("data", {})
            if data.get("title"):
                items.append(Paragraph(_markup(data["title"]), subtitle))
            if block["type"] == "table" and data.get("rows"):
                headers, rows = table_rows(block)
                lines = ([" | ".join(headers)] if headers else []) + [" | ".join(row) for row in rows]
                items.extend(Paragraph(_markup(line), body) for line in lines)
            elif data.get("description") or data.get("text"):
                items.append(Paragraph(_markup(data.get("description") or data.get("text")), body))
            elif data.get("value") is not None or data.get("content"):
                items.append(Paragraph(_markup(data.get("value") if data.get("value") is not None
                                               else data["content"]), body))
            elif block["type"] == "table" or data.get("cards") or not (data.get("points") or data.get("items") or data.get("title")):
                lines = [line for line in block_text(block).splitlines() if line.strip()]
                items.extend(Paragraph(_markup(line), body) for line in lines)
            for point in data.get("points", []) or data.get("items", []):
                items.append(Paragraph(_markup("• " + str(point)), body))
            if block.get("citation_ids"):
                items.append(Paragraph(_cited("", block), body))
        draw(items, rect, name, background=palette["document_accent_soft"] if key != "people" else palette["surface_muted"],
             accent=palette["document_accent"] if key != "people" else palette["border_strong"], padding=4 * mm)

    # Rodapé: fontes e identificação.
    fx, fy, fw, fh = rectangle("identificacao_versao")
    footer_items: list[Any] = []
    if content["citations"]:
        sources = "; ".join(f"{citation['id']}: {citation['source_id']}"
                            + (f", {citation['locator']}" if citation.get("locator") else "")
                            for citation in content["citations"])
        footer_items.append(Paragraph(_markup("Fontes: " + sources), small))
    footer_items.append(Paragraph(_markup(identity), small))
    draw(footer_items, (fx, fy, fw, fh), "identificacao_versao")
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
    _register_fonts(tokens)
    if layout == "presentation":
        if load_presentation_layout is None or identity_line is None:
            raise ValueError("Apresentação requer layout e identificação")
        _render_presentation(content, tokens, path, deliverable_label=deliverable_label,
                             block_text=block_text, table_rows=table_rows, table_views=table_views,
                             load_layout=load_presentation_layout,
                             identity=identity_line(content))
        return
    if layout == "executive_one_page" and load_presentation_layout is not None and identity_line is not None:
        one_page_slots = load_presentation_layout(content["deliverable_type"]) or {}
        missing = [name for name in ONE_PAGE_SLOTS if name not in one_page_slots]
        if missing:
            raise ValueError("layout.json do resumo sem slots obrigatórios: " + ", ".join(missing))
        _render_one_page_layout(content, tokens, profile, path, deliverable_label=deliverable_label,
                                slots=one_page_slots, block_text=block_text,
                                table_rows=table_rows, identity=identity_line(content))
        return
    if layout in ("report_portrait", "report_landscape"):
        if table_views is None or iqb_widths is None:
            raise ValueError("Relatórios requerem table_views e iqb_widths")
        _render_report(content, tokens, profile, path, deliverable_label=deliverable_label,
                       footer_label=footer_label, block_text=block_text,
                       table_rows=table_rows, table_views=table_views, iqb_widths=iqb_widths,
                       load_layout=load_presentation_layout)
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
            line = f"<b>{_markup(citation['id'])}</b>: {_markup(citation['source_id'])}"
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
                # Um campo do card pode vir como heading; dentro do card ele é texto do campo.
                field_block = {**block, "type": "paragraph"} if block["type"] == "heading" else block
                field = Table([[Paragraph(_markup(field_labels[key]), styles["field"])],
                               [*block_flowables(field_block, styles, inner_width, block_text, table_rows)]],
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
        canvas.setFont(_font(tokens, "font_body", 400), styles["footer"].fontSize)
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
