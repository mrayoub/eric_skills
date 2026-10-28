#!/usr/bin/env python3
"""Compare editable sample DOCX files with their canonical PDF counterparts.

Requires the design-system Python dependencies, LibreOffice and pdftoppm. The
comparison images and machine-readable report are kept outside the samples.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageStat
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTContainer
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "_SAMPLES_ENTREGAVEIS"
RENDER = ROOT / "_DESIGN_SYSTEM/scripts/render.py"
FONTS = ROOT / "_DESIGN_SYSTEM/assets/fonts/static"


def _chars(item: object):
    if isinstance(item, LTChar):
        yield item
    elif isinstance(item, LTContainer):
        for child in item:
            yield from _chars(child)


def clipped_characters(path: Path) -> int:
    count = 0
    for page in extract_pages(str(path)):
        for char in _chars(page):
            if char.x0 < -1 or char.y0 < -1 or char.x1 > page.width + 1 or char.y1 > page.height + 1:
                count += 1
    return count


def fontconfig(out: Path) -> Path:
    config = out / "fonts.conf"
    dirs = [FONTS, Path("/System/Library/Fonts"), Path("/usr/share/fonts")]
    rows = [f"<dir>{folder}</dir>" for folder in dirs if folder.is_dir()]
    config.write_text("<?xml version='1.0'?><!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>"
                      "<fontconfig>" + "".join(rows) + f"<cachedir>{out / 'font-cache'}</cachedir></fontconfig>",
                      encoding="utf-8")
    return config


def raster(pdf: Path, page: int, out: Path) -> Image.Image:
    target = out.with_suffix("")
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile",
                    "-r", "96", "-png", str(pdf), str(target)],
                   check=True, capture_output=True)
    return Image.open(str(target) + ".png").convert("RGB")


def _blue(pixel: tuple[int, int, int]) -> bool:
    r, g, b = pixel
    return b > 80 and b > r * 1.45 and b > g * 1.12 and r < 130


def compare_image(reference: Image.Image, editable: Image.Image, out: Path) -> dict[str, float]:
    if editable.size != reference.size:
        editable = editable.resize(reference.size)
    difference = ImageChops.difference(reference, editable)
    difference.save(out.with_name(out.stem + "-diff.png"))
    width, height = reference.size
    side = Image.new("RGB", (width * 2, height), "white")
    side.paste(reference, (0, 0))
    side.paste(editable, (width, 0))
    side.save(out)
    ref_pixels = reference.load()
    edit_pixels = editable.load()
    intersection = union = 0
    # Blue regions carry the main composition: mastheads, section bands and cards.
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            a, b = _blue(ref_pixels[x, y]), _blue(edit_pixels[x, y])
            intersection += a and b
            union += a or b
    return {"mean_rgb_difference": round(sum(ImageStat.Stat(difference).mean) / 3, 3),
            "blue_region_iou": round(intersection / union, 4) if union else 1.0}


def comparison_failures(reference_sizes: list[list[float]], editable_sizes: list[list[float]],
                        clipped: int) -> list[str]:
    failures = []
    if len(reference_sizes) != len(editable_sizes):
        failures.append("page_count")
    if len(reference_sizes) != len(editable_sizes) or any(
            round(abs(a - b), 2) > .2 for ref_size, edit_size in zip(reference_sizes, editable_sizes)
            for a, b in zip(ref_size, edit_size)):
        failures.append("page_size")
    if clipped:
        failures.append("clipped_text")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, help="Comparison artifacts (default: temporary directory)")
    parser.add_argument("--only", nargs="*", help="Deliverable types to compare")
    args = parser.parse_args()
    soffice = shutil.which("soffice")
    if not soffice or not shutil.which("pdftoppm"):
        parser.error("LibreOffice (soffice) e pdftoppm são necessários para comparar DOCX/PDF")
    temporary = tempfile.TemporaryDirectory(prefix="eric-docx-parity-") if args.out_dir is None else None
    out = args.out_dir or Path(temporary.name)
    out.mkdir(parents=True, exist_ok=True)
    generated, converted, pictures = (out / name for name in ("generated", "converted", "pictures"))
    for directory in (generated, converted, pictures):
        directory.mkdir(exist_ok=True)
    # The DOCX has a versioned filename; the input itself does not.
    samples = [p for p in sorted(SAMPLES.glob("*/input.json"))
               if list(p.parent.glob("sample-*.docx")) and (not args.only or p.parent.name in args.only)]
    if not samples:
        parser.error("Nenhuma amostra DOCX encontrada")
    docx_files: list[Path] = []
    for sample in samples:
        folder = generated / sample.parent.name
        subprocess.run([sys.executable, str(RENDER), str(sample), "--out-dir", str(folder),
                        "--formats", "docx"], check=True, capture_output=True, text=True)
        docx_files.extend(folder.glob("*.docx"))
    env = os.environ.copy()
    env["FONTCONFIG_FILE"] = str(fontconfig(out))
    subprocess.run([soffice, f"-env:UserInstallation={((out / 'lo-profile').resolve()).as_uri()}",
                    "--headless", "--convert-to", "pdf", "--outdir", str(converted),
                    *(str(file) for file in docx_files)], check=True, capture_output=True, text=True, env=env)
    results = []
    for sample in samples:
        kind = sample.parent.name
        reference = next(sample.parent.glob("sample-*.pdf"))
        converted_pdf = converted / reference.name
        if not converted_pdf.is_file():
            raise RuntimeError(f"LibreOffice não gerou {converted_pdf.name}")
        original, editable = PdfReader(reference), PdfReader(converted_pdf)
        page_count = min(len(original.pages), len(editable.pages))
        images = []
        for page in range(1, page_count + 1):
            ref_image = raster(reference, page, pictures / f"{kind}-{page}-reference.png")
            doc_image = raster(converted_pdf, page, pictures / f"{kind}-{page}-docx.png")
            images.append(compare_image(ref_image, doc_image, pictures / f"{kind}-{page}-side-by-side.png"))
        reference_sizes = [[round(float(p.mediabox.width), 2), round(float(p.mediabox.height), 2)] for p in original.pages]
        editable_sizes = [[round(float(p.mediabox.width), 2), round(float(p.mediabox.height), 2)] for p in editable.pages]
        clipped = clipped_characters(converted_pdf)
        failures = comparison_failures(reference_sizes, editable_sizes, clipped)
        results.append({"type": kind, "reference_pages": len(original.pages), "docx_pages": len(editable.pages),
                        "reference_sizes_pt": reference_sizes, "docx_sizes_pt": editable_sizes,
                        "clipped_characters": clipped, "pages": images, "failures": failures})
    report = {"sample_count": len(results), "failures": sum(bool(row["failures"]) for row in results),
              "results": results}
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(out / "report.json"), "samples": report["sample_count"],
                      "failures": report["failures"]}, ensure_ascii=False))
    if temporary is not None:
        temporary.cleanup()
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
