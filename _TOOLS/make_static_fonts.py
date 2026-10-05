#!/usr/bin/env python3
"""Gera fontes estáticas para o PDF a partir das fontes variáveis do projeto.

fontTools é necessário somente durante a manutenção, não na instalação das skills.
"""
from __future__ import annotations

from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "_DESIGN_SYSTEM" / "assets" / "fonts"
INSTANCES = (("Montserrat", 700, "Bold"), ("Roboto", 400, "Regular"),
             ("Roboto", 500, "Medium"), ("Roboto", 700, "Bold"))


def main() -> None:
    target = FONTS / "static"
    target.mkdir(exist_ok=True)
    for family, weight, style in INSTANCES:
        variable = TTFont(FONTS / f"{family}-Variable.ttf")
        instance = instantiateVariableFont(variable, {"wght": weight}, static=True, updateFontNames=True)
        instance.recalcTimestamp = False
        instance["head"].modified = 0
        instance.save(target / f"{family}-{style}.ttf")
        print(f"OK {family}-{style}.ttf")


if __name__ == "__main__":
    main()
