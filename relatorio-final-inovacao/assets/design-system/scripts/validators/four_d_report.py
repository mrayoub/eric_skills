"""Regras de análise e conclusão do Relatório 4D completo.

Orientação da autora do playbook 4D (10/11/2026): o relatório não para na descrição de D1 a D4. Precisa de Resumo,
temas transversais, síntese analítica, hipótese de solução em três partes e conclusão. O contrato exige os títulos;
este validador confere que cada seção tem texto e que a hipótese tem as três partes.
"""
from __future__ import annotations

import unicodedata
from typing import Any

TEXT_SECTIONS = {
    "executive_summary": "Resumo",
    "cross_themes": "temas que atravessaram o 4D",
    "analytical_synthesis": "síntese analítica",
    "solution_hypothesis": "hipótese de solução",
    "conclusion": "conclusão do aprofundamento",
}
HYPOTHESIS_PARTS = ("acreditamos que", "porque", "precisamos validar")


def _normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.casefold())
    return " ".join("".join(char for char in decomposed if unicodedata.category(char) != "Mn").split())


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(_text(item) for key, item in value.items() if key not in ("section_key", "tone", "columns"))
    return ""


def _sections(content: dict[str, Any]) -> dict[str, str]:
    """Texto de cada seção: os blocos entre um título com section_key e o título seguinte."""
    sections: dict[str, str] = {}
    current: str | None = None
    for block in content.get("blocks", []):
        data = block.get("data", {})
        if block.get("type") == "heading":
            current = data.get("section_key")
            sections.setdefault(current, "")
            continue
        if current is not None and block.get("type") != "page_break":
            sections[current] += " " + _text(data)
    return sections


def validate(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sections = _sections(content)
    for key, label in TEXT_SECTIONS.items():
        if not sections.get(key, "").strip():
            errors.append(f"{key}: a seção {label} precisa de conteúdo depois do título; o relatório não pode parar "
                          "na descrição de D1 a D4")
    hypothesis = _normalize(sections.get("solution_hypothesis", ""))
    missing = [part for part in HYPOTHESIS_PARTS if part not in hypothesis]
    if hypothesis and missing:
        errors.append("solution_hypothesis: a hipótese precisa das três partes (Acreditamos que / Porque o diagnóstico "
                      f"mostrou / Precisamos validar se); faltam: {', '.join(missing)}")
    return errors
