"""Verifica a CDT: fonte por campo, pendências declaradas, checklist da publicação e avaliação crítica."""
from __future__ import annotations

import re
from typing import Any

# Campos que vão ao Jira e precisam de fonte ou de pendência declarada.
FIELDS = (
    "jira_title", "objective", "problem", "audience", "current_process", "expected_results",
    "scope_essential", "scope_important", "scope_out", "priorities", "constraints", "responsibles",
    "theme", "regulatory", "risk_if_not_done", "benefits", "process_simplification", "requester",
    "personal_data", "impacted_systems", "evidence", "alternatives", "change_control", "family_service",
    "product_area", "operation_date", "classification", "prototype", "attachments", "initiative",
)
# Itens do checklist da publicação sobre escopo, na ordem do comunicado.
CHECKLIST = (
    "Problema e objetivo", "Públicos impactados", "Entregas essenciais",
    "Prioridades e resultados esperados", "Regras, restrições e dependências", "Responsáveis",
)
STATUS = re.compile(r"\b(atendido|parcial|ausente)\b", re.IGNORECASE)
PENDING = re.compile(r"\ba (confirmar|definir|levantar|obter)\b", re.IGNORECASE)


def sections(content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {block["data"]["section_key"]: block for block in content.get("blocks", [])
            if isinstance(block.get("data"), dict) and isinstance(block["data"].get("section_key"), str)
            and isinstance(block["data"].get("text"), str)}


def checklist_status(text: str) -> dict[str, str]:
    """Status de cada item do checklist, lido da linha que começa pelo nome do item."""
    found: dict[str, str] = {}
    for line in text.splitlines():
        clean = line.strip().lstrip("-* ").strip()
        for item in CHECKLIST:
            if clean.casefold().startswith(item.casefold()):
                match = STATUS.search(clean[len(item):])
                if match:
                    found[item] = match.group(1).lower()
    return found


def report(content: dict[str, Any]) -> dict[str, Any]:
    """Diagnóstico da CDT em qualquer estado; `errors` impede a versão completa."""
    by_key = sections(content)
    pending = {key: by_key[key]["data"]["text"] for key in FIELDS
               if key in by_key and PENDING.search(by_key[key]["data"]["text"])}
    unsourced = sorted(key for key in FIELDS if key in by_key and not by_key[key].get("citation_ids")
                       and key not in pending)
    checklist = checklist_status(by_key.get("publication_checklist", {}).get("data", {}).get("text", ""))
    review = by_key.get("quality_review", {}).get("data", {}).get("text", "").casefold()
    readiness = by_key.get("readiness", {}).get("data", {}).get("text", "").casefold()
    obtain = by_key.get("data_to_obtain", {}).get("data", {}).get("text", "")

    errors: list[str] = []
    if unsourced:
        errors.append(f"campos sem fonte e sem pendência declarada: {unsourced}")
    missing_items = [item for item in CHECKLIST if item not in checklist]
    if missing_items:
        errors.append(f"publication_checklist: itens sem status atendido, parcial ou ausente: {missing_items}")
    if "pontos fortes" not in review or "pontos fracos" not in review:
        errors.append("quality_review: exige 'Pontos fortes' e 'Pontos fracos', mesmo com todos os campos preenchidos")
    if pending and not obtain.strip():
        errors.append("data_to_obtain: há campos 'a confirmar' sem a lista de dados a obter")
    gaps = sorted(item for item, status in checklist.items() if status != "atendido")
    return {
        "pending_fields": sorted(pending),
        "unsourced_fields": unsourced,
        "checklist": checklist,
        "checklist_gaps": gaps,
        "ready": not pending and not gaps and not errors,
        "readiness_text_ok": ("pronta para envio" in readiness) if not pending and not gaps else ("parcial" in readiness),
        "errors": errors,
    }


def validate(content: dict[str, Any]) -> list[str]:
    result = report(content)
    errors = list(result["errors"])
    if result["pending_fields"]:
        errors.append(f"versão completa com campos a confirmar: {result['pending_fields']}; use completeness partial")
    if result["checklist_gaps"]:
        errors.append(f"versão completa com itens do checklist não atendidos: {result['checklist_gaps']}")
    if not result["readiness_text_ok"]:
        errors.append("readiness: a versão completa deve dizer 'Pronta para envio'")
    return errors
