"""Regras de narrativa e densidade para a apresentação de devolutiva do 5C.

A apresentação nasce da mesma análise do Relatório 5C, mas organiza o conteúdo por insight: cada slide abre com
um título que diz a conclusão e traz poucas evidências. Mapas de dores e propostas usam cards, por isso o limite
de palavras é maior que o da apresentação executiva; o verificador de PDF continua recusando slide que não cabe.
"""
from __future__ import annotations

import unicodedata
from typing import Any

MAX_SUMMARY_WORDS = 35
TITLE_WORDS = (4, 14)
MAX_BLOCKS = 4
MAX_WORDS = 140
GENERIC_TITLES = {
    "contexto", "metodo", "formato", "achados", "resultados", "dores", "mapa das dores", "propostas", "ideias",
    "priorizacao", "proximos passos", "conclusao", "introducao", "resumo", "fontes", "conteudo", "c1", "c2",
    "c3", "c4", "c5",
}


def _normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.casefold().strip())
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn")


def _words(value: Any) -> int:
    if isinstance(value, str):
        return len(value.split())
    if isinstance(value, list):
        return sum(_words(item) for item in value)
    if isinstance(value, dict):
        return sum(_words(item) for item in value.values())
    return 0


def _block_words(block: dict[str, Any]) -> int:
    data = block.get("data", {})
    return sum(_words(data.get(key)) for key in
               ("text", "title", "description", "value", "content", "items", "headers", "columns", "rows", "cards"))


def validate(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not content.get("summary") or _words(content["summary"]) > MAX_SUMMARY_WORDS:
        errors.append(f"summary: a capa precisa da mensagem principal em até {MAX_SUMMARY_WORDS} palavras")

    heading: dict[str, Any] | None = None
    block_count = word_count = 0

    def flush() -> None:
        if heading is not None and (block_count > MAX_BLOCKS or word_count > MAX_WORDS):
            errors.append(f"{heading.get('id', 'heading')}: slide com {word_count} palavras/{block_count} blocos "
                          f"(limite {MAX_WORDS}/{MAX_BLOCKS}); divida em mais slides")

    for block in content.get("blocks", []):
        if block.get("type") in ("heading", "page_break"):
            flush()
            heading = block if block.get("type") == "heading" else None
            block_count = word_count = 0
            if heading is not None:
                title = str(heading.get("data", {}).get("text", "")).strip()
                low, high = TITLE_WORDS
                if not low <= _words(title) <= high or _normalize(title) in GENERIC_TITLES:
                    errors.append(f"{heading.get('id', 'heading')}: título de slide deve dizer a conclusão do slide "
                                  f"({low} a {high} palavras), não só o tema ou a etapa")
        elif heading is not None:
            block_count += 1
            word_count += _block_words(block)
    flush()
    return errors
