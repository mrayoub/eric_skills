"""Verifica a Análise da CDT: estado, checklist do comunicado, dados a obter em ordem de prioridade, avaliação
crítica e origem dos dados. É o documento que fica fora do Jira."""
from __future__ import annotations

import re
from typing import Any

# Itens do checklist do comunicado sobre escopo, na ordem do comunicado. Os dois últimos não têm campo na CDT.
CHECKLIST = (
    "Problema e objetivo", "Públicos impactados", "Entregas essenciais",
    "Prioridades e resultados esperados", "Regras, restrições e dependências", "Responsáveis",
)
ONLY_IN_CHECKLIST = ("Regras, restrições e dependências", "Responsáveis")
STATUS = re.compile(r"\b(atendido|parcial|ausente)\b", re.IGNORECASE)
NOTHING_PENDING = "nenhum dado pendente"
PRIORITY_COLUMN = "Prioridade"


def sections(content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {block["data"]["section_key"]: block for block in content.get("blocks", [])
            if isinstance(block.get("data"), dict) and isinstance(block["data"].get("section_key"), str)
            and isinstance(block["data"].get("text"), str)}


def checklist_lines(text: str) -> dict[str, tuple[str, str]]:
    """Status e resto da linha de cada item do checklist, lidos da linha que começa pelo nome do item."""
    found: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        clean = line.strip().lstrip("-* ").strip()
        for item in CHECKLIST:
            if clean.casefold().startswith(item.casefold()):
                rest = clean[len(item):]
                match = STATUS.search(rest)
                if match:
                    found[item] = (match.group(1).lower(), rest[match.end():].strip(" .:;"))
    return found


def obtain_table(content: dict[str, Any]) -> dict[str, Any] | None:
    """A tabela que segue o bloco dos dados a obter."""
    blocks = content.get("blocks", [])
    for index, block in enumerate(blocks):
        if block.get("data", {}).get("section_key") == "data_to_obtain":
            following = blocks[index + 1] if index + 1 < len(blocks) else {}
            return following.get("data") if following.get("type") == "table" else None
    return None


def report(content: dict[str, Any]) -> dict[str, Any]:
    """Diagnóstico da análise em qualquer estado; `errors` impede a entrega."""
    texts = {key: block["data"]["text"] for key, block in sections(content).items()}
    checklist = checklist_lines(texts.get("publication_checklist", ""))
    review = texts.get("quality_review", "").casefold()
    readiness = texts.get("readiness", "").casefold()
    obtain = texts.get("data_to_obtain", "")
    errors: list[str] = []
    missing_items = [item for item in CHECKLIST if item not in checklist]
    if missing_items:
        errors.append(f"publication_checklist: itens sem status atendido, parcial ou ausente: {missing_items}")
    for item in ONLY_IN_CHECKLIST:
        status, rest = checklist.get(item, ("", ""))
        if status in ("atendido", "parcial") and not rest:
            errors.append(f"publication_checklist: '{item}' não tem campo na CDT; escreva a resposta na linha")
    if "pontos fortes" not in review or "pontos fracos" not in review:
        errors.append("quality_review: exige 'Pontos fortes' e 'Pontos fracos', mesmo com todos os campos preenchidos")
    pending_declared = not obtain.strip().casefold().startswith(NOTHING_PENDING)
    if "data_to_obtain" in texts and pending_declared:
        table = obtain_table(content) or {}
        headers = table.get("headers") or table.get("columns") or []
        if not headers or headers[0] != PRIORITY_COLUMN or not table.get("rows"):
            errors.append(f"data_to_obtain: liste os dados numa tabela com a coluna '{PRIORITY_COLUMN}' primeiro, "
                          "do mais importante para o menos importante")
    gaps = sorted(item for item, (status, _) in checklist.items() if status != "atendido")
    return {
        "checklist": {item: status for item, (status, _) in checklist.items()},
        "checklist_gaps": gaps,
        "declares_pending": pending_declared,
        "readiness_says_ready": "pronta para envio" in readiness,
        "readiness_says_gaps": "lacunas" in readiness,
        "errors": errors,
    }


def validate(content: dict[str, Any]) -> list[str]:
    result = report(content)
    errors = list(result["errors"])
    if result["checklist_gaps"]:
        errors.append(f"versão completa com itens do checklist não atendidos: {result['checklist_gaps']}")
    if not result["readiness_says_ready"]:
        errors.append("readiness: a versão completa deve dizer 'Pronta para envio'")
    return errors
