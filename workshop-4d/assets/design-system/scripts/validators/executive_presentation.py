"""Regras de narrativa e densidade para apresentações executivas completas."""
from __future__ import annotations

import unicodedata
from typing import Any


GENERIC_TITLES = {
    "contexto", "metodo", "achados", "resultados", "recomendacao",
    "proximos passos", "conclusao", "introducao", "resumo", "fontes", "conteudo",
}


def _normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.casefold().strip())
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn")


def _words(value: Any) -> int:
    if isinstance(value, str):
        return len(value.split())
    if isinstance(value, list):
        return sum(_words(item) for item in value)
    return 0


def _block_words(block: dict[str, Any]) -> int:
    data = block.get("data", {})
    return sum(_words(data.get(key)) for key in ("text", "title", "description", "items"))


def validate(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not content.get("summary") or _words(content["summary"]) > 35:
        errors.append("summary: a capa precisa da mensagem principal em até 35 palavras")

    heading: dict[str, Any] | None = None
    block_count = word_count = 0

    def flush() -> None:
        if heading is not None and (block_count > 4 or word_count > 60):
            errors.append(f"{heading.get('id', 'heading')}: slide com {word_count} palavras/{block_count} blocos; divida em mais slides")

    for block in content.get("blocks", []):
        if block.get("type") in ("heading", "page_break"):
            flush()
            heading = block if block.get("type") == "heading" else None
            block_count = word_count = 0
            if heading is not None:
                title = str(heading.get("data", {}).get("text", "")).strip()
                if not 4 <= _words(title) <= 12 or _normalize(title) in GENERIC_TITLES:
                    errors.append(f"{heading.get('id', 'heading')}: título de slide deve dizer a conclusão do slide (4 a 12 palavras), não só o tema")
        elif heading is not None:
            block_count += 1
            word_count += _block_words(block)
    flush()
    return errors
