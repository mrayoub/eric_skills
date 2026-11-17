#!/usr/bin/env python3
"""Render all four fresh PPTX files with LibreOffice and compare every PDF page.

--capture saves the exact-scale reference and rendered pictures for independent
review. No image is resized: a white canvas absorbs subpixel PDF page rounding.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
KINDS = ("executive_presentation", "five_c_presentation", "four_d_presentation", "three_e_presentation")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", action="store_true")
    args = parser.parse_args()
    if not shutil.which("soffice"):
        raise RuntimeError("LibreOffice Impress is required; visual proof cannot be skipped")
    spec = importlib.util.spec_from_file_location("pptx_comparison", ROOT / "_TOOLS/check_docx_pdf_parity.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    captures = Path(__file__).parent / "captures"
    rows = []
    with tempfile.TemporaryDirectory(prefix="eric-pptx-proof-") as tmp:
        out = Path(tmp)
        generated, converted = out / "generated", out / "converted"
        generated.mkdir()
        converted.mkdir()
        files = []
        for kind in KINDS:
            result = subprocess.run([sys.executable, str(ROOT / "_DESIGN_SYSTEM/scripts/render.py"),
                                     str(ROOT / "_SAMPLES_ENTREGAVEIS" / kind / "input.json"),
                                     "--out-dir", str(generated / kind), "--formats", "pptx"],
                                    capture_output=True, text=True, timeout=60)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            files.append(next((generated / kind).glob("*.pptx")))
        env = os.environ.copy()
        env["FONTCONFIG_FILE"] = str(helper.fontconfig(out))
        conversion = subprocess.run([shutil.which("soffice"), f"-env:UserInstallation={(out / 'lo').as_uri()}",
                                     "--headless", "--convert-to", "pdf", "--outdir", str(converted),
                                     *map(str, files)], capture_output=True, text=True, env=env, timeout=120)
        if conversion.returncode:
            raise RuntimeError(f"LibreOffice returned {conversion.returncode}: {conversion.stdout} {conversion.stderr}")
        for kind, pptx in zip(KINDS, files):
            reference = next((ROOT / "_SAMPLES_ENTREGAVEIS" / kind).glob("*.pdf"))
            editable = converted / pptx.with_suffix(".pdf").name
            original, actual = PdfReader(reference), PdfReader(editable)
            if len(original.pages) != len(actual.pages):
                raise AssertionError(f"{kind}: page count {len(original.pages)} != {len(actual.pages)}")
            if helper.clipped_characters(editable):
                raise AssertionError(f"{kind}: text outside the page")
            with pdfium.PdfDocument(reference) as a, pdfium.PdfDocument(editable) as b:
                for n in range(len(a)):
                    ref_size = [float(original.pages[n].mediabox.width), float(original.pages[n].mediabox.height)]
                    actual_size = [float(actual.pages[n].mediabox.width), float(actual.pages[n].mediabox.height)]
                    if any(abs(x - y) > .2 for x, y in zip(ref_size, actual_size)):
                        raise AssertionError(f"{kind}/{n + 1}: page dimensions differ")
                    images = [d[n].render(scale=1).to_pil().convert("RGB") for d in (a, b)]
                    size = tuple(max(im.size[axis] for im in images) for axis in (0, 1))
                    canvases = []
                    for im in images:
                        canvas = Image.new("RGB", size, "white")
                        canvas.paste(im, (0, 0))
                        canvases.append(canvas)
                    mean = sum(ImageStat.Stat(ImageChops.difference(*canvases)).mean) / 3
                    if mean > 12:
                        raise AssertionError(f"{kind}/{n + 1}: RGB difference {mean:.3f} > 12")
                    name = f"{kind}-{n + 1:02d}"
                    rows.append({"type": kind, "page": n + 1, "source": str(reference.relative_to(ROOT)),
                                 "reference": name + ".png", "running": name + ".running.png",
                                 "size": list(size), "mean_rgb_difference": round(mean, 3),
                                 "source_sha256": hashlib.sha256(reference.read_bytes()).hexdigest()})
                    if args.capture:
                        captures.mkdir(exist_ok=True)
                        for im, suffix in zip(canvases, (".png", ".running.png")):
                            im.save(captures / (name + suffix))
        if args.capture:
            (captures / "index.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps({"types": len(KINDS), "pages": len(rows),
                      "max_mean_rgb_difference": max(row["mean_rgb_difference"] for row in rows),
                      "failures": 0}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
