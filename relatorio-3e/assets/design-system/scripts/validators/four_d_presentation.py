"""Regras da Apresentação 4D: devolutiva curta para gerência e diretoria.

Orientação da autora do playbook 4D (10/11/2026): a apresentação vai direto aos insights, em cerca de cinco slides
(desafio, principais achados, hipótese de solução, convergência e próximos passos). Deriva da mesma análise do
Relatório 4D. Cada slide abre com um título que diz a conclusão.
"""
from __future__ import annotations

import unicodedata
from typing import Any

MAX_SUMMARY_WORDS = 35
TITLE_WORDS = (4, 14)
MAX_BLOCKS = 4
MAX_WORDS = 140
MAX_CONTENT_SLIDES = 6
HYPOTHESIS_PARTS = ("acreditamos que", "porque", "precisamos validar")
GENERIC_TITLES = {
    "contexto", "desafio", "achados", "principais achados", "resultados", "hipotese", "hipotese de solucao",
    "convergencia", "decisao", "priorizacao", "proximos passos", "conclusao", "resumo", "fontes", "conteudo",
    "d1", "d2", "d3", "d4",
}


def _normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.casefold())
    return " ".join("".join(char for char in decomposed if unicodedata.category(char) != "Mn").split())


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


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(_text(item) for key, item in value.items() if key not in ("section_key", "tone", "columns"))
    return ""


def check_slides(content: dict[str, Any], generic_titles: set[str]) -> list[str]:
    errors: list[str] = []
    if not content.get("summary") or _words(content["summary"]) > MAX_SUMMARY_WORDS:
        errors.append(f"summary: a capa precisa da mensagem principal em até {MAX_SUMMARY_WORDS} palavras")
    heading: dict[str, Any] | None = None
    block_count = word_count = slides = 0

    def flush() -> None:
        if heading is not None and (block_count > MAX_BLOCKS or word_count > MAX_WORDS):
            errors.append(f"{heading.get('id', 'heading')}: slide com {word_count} palavras/{block_count} blocos "
                          f"(limite {MAX_WORDS}/{MAX_BLOCKS}); condense, porque a apresentação é curta")

    for block in content.get("blocks", []):
        if block.get("type") in ("heading", "page_break"):
            flush()
            heading = block if block.get("type") == "heading" else None
            block_count = word_count = 0
            if heading is not None:
                slides += 1
                title = str(heading.get("data", {}).get("text", "")).strip()
                low, high = TITLE_WORDS
                if not low <= _words(title) <= high or _normalize(title) in generic_titles:
                    errors.append(f"{heading.get('id', 'heading')}: título de slide deve dizer a conclusão do slide "
                                  f"({low} a {high} palavras), não só o tema ou a etapa")
        elif heading is not None:
            block_count += 1
            word_count += _block_words(block)
    flush()
    if slides > MAX_CONTENT_SLIDES:
        errors.append(f"apresentação com {slides} slides de conteúdo; o limite é {MAX_CONTENT_SLIDES}. "
                      "O detalhe fica no relatório")
    return errors


def section_text(content: dict[str, Any], key: str) -> str:
    current: str | None = None
    parts: list[str] = []
    for block in content.get("blocks", []):
        data = block.get("data", {})
        if block.get("type") == "heading":
            current = str(data.get("section_key", "")).removesuffix("_heading")
            continue
        if data.get("section_key") == key or current == key:
            parts.append(_text(data))
    return _normalize(" ".join(parts))


def validate(content: dict[str, Any]) -> list[str]:
    errors = check_slides(content, GENERIC_TITLES)
    hypothesis = section_text(content, "solution_hypothesis")
    missing = [part for part in HYPOTHESIS_PARTS if part not in hypothesis]
    if missing:
        errors.append("solution_hypothesis: a hipótese precisa das três partes (Acreditamos que / Porque o diagnóstico "
                      f"mostrou / Precisamos validar se); faltam: {', '.join(missing)}")
    return errors
