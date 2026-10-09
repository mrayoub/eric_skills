#!/usr/bin/env python3
"""Gera uma folha HTML com PDFs lado a lado para revisão visual."""
from __future__ import annotations

import argparse
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "_DESIGN_SYSTEM" / "scripts" / "render.py"
SAMPLES = ROOT / "_SAMPLES_ENTREGAVEIS"


def compare(out: Path, kinds: list[str], engines: list[str]) -> None:
    import importlib.util

    import pypdfium2
    from PIL import Image, ImageDraw

    render_spec = importlib.util.spec_from_file_location("render_labels", SCRIPT)
    render_module = importlib.util.module_from_spec(render_spec)
    render_spec.loader.exec_module(render_module)
    labels = render_module.DELIVERABLE_LABELS
    spec = importlib.util.spec_from_file_location("pdf_quality", ROOT / "_DESIGN_SYSTEM/scripts/pdf_quality.py")
    quality = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(quality)
    out.mkdir(parents=True, exist_ok=True)
    entries: list[str] = []
    for kind in kinds:
        source = SAMPLES / kind / "input.json"
        if not source.is_file():
            entries.append(f"<section><h2>{html.escape(labels.get(kind, kind))}</h2><p>Amostra não encontrada.</p></section>")
            continue
        columns: list[tuple[str, list[Image.Image], str]] = []
        for engine in engines:
            destination = out / engine / kind
            destination.mkdir(parents=True, exist_ok=True)
            process = subprocess.run([sys.executable, str(SCRIPT), str(source), "--out-dir", str(destination),
                                      "--formats", "pdf", "--pdf-engine", engine],
                                     capture_output=True, text=True)
            pdf_path = next(destination.glob("*.pdf"), None)
            pages: list[Image.Image] = []
            problems: list[str] = []
            if pdf_path is not None:
                pdf = pypdfium2.PdfDocument(str(pdf_path))
                pages = [pdf[index].render(scale=100 / 72).to_pil().convert("RGB") for index in range(len(pdf))]
                problems = quality.check_pdf(pdf_path)
            quality_status = ", ".join(problems) if problems else ("OK" if pdf_path else "PDF indisponível")
            status = f"{len(pages)} página(s); qualidade: {quality_status}"
            if process.returncode:
                status += f"; exit {process.returncode}"
            if process.stderr.strip():
                status += "; " + process.stderr.strip()[-1000:]
            columns.append((engine, pages, status))

        margin, gap, header = 20, 18, 40
        widths = [max((page.width for page in pages), default=360) for _, pages, _ in columns]
        heights = [sum(page.height + gap for page in pages) for _, pages, _ in columns]
        canvas = Image.new("RGB", (sum(widths) + gap * (len(widths) - 1) + margin * 2,
                                    max(heights, default=0) + margin * 2 + header), "#E6E9EF")
        draw = ImageDraw.Draw(canvas)
        left = margin
        for (engine, pages, _), width in zip(columns, widths):
            draw.text((left, margin), engine, fill="#17244A")
            top = margin + header
            for page in pages:
                canvas.paste(page, (left, top))
                top += page.height + gap
            left += width + gap
        image_name = f"{kind}.png"
        canvas.save(out / image_name)
        details = "".join(f"<li><strong>{html.escape(engine)}</strong>: {html.escape(status)}</li>"
                          for engine, _, status in columns)
        entries.append(f'<section><h2>{html.escape(labels.get(kind, kind))} <small>({html.escape(kind)})</small></h2><ul>{details}</ul>'
                       f'<img src="{html.escape(image_name)}" alt="Comparação de PDF para {html.escape(kind)}"></section>')
    (out / "index.html").write_text(
        '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Comparação de PDFs</title>'
        '<style>body{font:16px system-ui;max-width:1200px;margin:32px auto;color:#17244a}'
        'section{margin:36px 0;padding-bottom:32px;border-bottom:1px solid #ccd3df}'
        'img{display:block;max-width:100%;height:auto}li{overflow-wrap:anywhere}</style>'
        '<h1>Comparação de PDFs</h1>' + "".join(entries) + "</html>\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--types", help="tipos separados por vírgula; padrão: todas as amostras")
    parser.add_argument("--engines", default="reportlab", help="motores separados por vírgula (só reportlab)")
    args = parser.parse_args()
    kinds = args.types.split(",") if args.types else sorted(path.parent.name for path in SAMPLES.glob("*/input.json"))
    compare(args.out, kinds, args.engines.split(","))


if __name__ == "__main__":
    main()
