"""Validações de objetividade aplicadas a todos os deliverable_types, independentemente do validator específico."""
from __future__ import annotations

import re
from typing import Any

ABSOLUTE_TERMS = (
    "com certeza", "sem dúvida", "comprovadamente", "indiscutivelmente",
    "certamente", "claramente", "obviamente", "o melhor", "a melhor",
    "garantido", "garantidamente",
)
_ABSOLUTE_PATTERNS = {term: re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)") for term in ABSOLUTE_TERMS}
NUMERIC_CLAIM = re.compile(r"R\$\s?\d|\d+[.,]?\d*\s?%|\b\d{2,}\b")
CLAIM_BLOCK_TYPES = {"paragraph", "callout", "metric"}


def block_text(block: dict[str, Any]) -> str:
    data = block.get("data", {})
    parts = []
    for key in ("title", "label", "text", "description", "content", "value"):
        value = data.get(key)
        if isinstance(value, str):
            parts.append(value)
    return " ".join(parts)


def validate(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for block in content.get("blocks", []):
        text = block_text(block)
        lowered = text.lower()
        for term, pattern in _ABSOLUTE_PATTERNS.items():
            if pattern.search(lowered):
                errors.append(f"{block['id']}: vocabulário absoluto sem suporte ({term!r})")
        if block.get("type") in CLAIM_BLOCK_TYPES and NUMERIC_CLAIM.search(text):
            if not block.get("citation_ids"):
                errors.append(f"{block['id']}: alegação numérica sem citation_ids")
    return errors
