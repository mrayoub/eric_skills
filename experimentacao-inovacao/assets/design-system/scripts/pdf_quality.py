"""Verifica geometria, legibilidade mínima e sobreposição em PDFs gerados."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Iterator


def _chars(layout: Any) -> Iterator[Any]:
    from pdfminer.layout import LTChar

    stack = list(layout)
    while stack:
        item = stack.pop()
        if isinstance(item, LTChar):
            yield item
        elif hasattr(item, "__iter__"):
            stack.extend(item)


def check_pdf(path: Path, min_size: float = 7.5, tolerance: float = 0.5,
              overlap_ratio: float = 0.4) -> list[str]:
    from pdfminer.high_level import extract_pages

    problems: list[str] = []
    for number, page in enumerate(extract_pages(str(path)), 1):
        width, height = page.width, page.height
        chars = sorted((char for char in _chars(page) if char.get_text().strip()),
                       key=lambda char: (-char.y1, char.x0))
        outside = [char for char in chars if char.x0 < -tolerance or char.x1 > width + tolerance
                   or char.y0 < -tolerance or char.y1 > height + tolerance]
        if outside:
            sample = "".join(char.get_text() for char in outside[:20])
            problems.append(f"página {number}: texto fora da página ({sample!r})")
        small = sorted({round(char.size, 1) for char in chars if char.size < min_size - 0.05})
        if small:
            problems.append(f"página {number}: fonte abaixo de {min_size} pt ({small})")
        grid: dict[tuple[int, int], list[int]] = defaultdict(list)
        hits = 0
        for index, char in enumerate(chars):
            for gx in range(int(char.x0 // 20), int(char.x1 // 20) + 1):
                for gy in range(int(char.y0 // 20), int(char.y1 // 20) + 1):
                    for other_index in grid[(gx, gy)]:
                        other = chars[other_index]
                        # Kerning pode aproximar letras vizinhas da mesma linha.
                        if abs(other.y0 - char.y0) < 0.5 and abs(index - other_index) <= 2:
                            continue
                        overlap_width = min(char.x1, other.x1) - max(char.x0, other.x0)
                        overlap_height = min(char.y1, other.y1) - max(char.y0, other.y0)
                        smaller = min(char.width * char.height, other.width * other.height)
                        if overlap_width > 0 and overlap_height > 0 and smaller:
                            if overlap_width * overlap_height / smaller > overlap_ratio:
                                hits += 1
                    grid[(gx, gy)].append(index)
        if hits:
            problems.append(f"página {number}: {hits} pares de caracteres sobrepostos")
    return problems
