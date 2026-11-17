"""Receita oficial com cobertura determinada pela aplicação, não pela letra isolada."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def definitions() -> dict:
    return json.loads((ROOT / "official-methods.json").read_text(encoding="utf-8"))


def section_keys(content: dict) -> list[str]:
    stages = [s for session in content["metadata"]["method_application"]["sessions"] for s in session["stages"]]
    if content["deliverable_type"].endswith("report"):
        return ["purpose", "introduction", "structuring", *[f"{s['id']}_{part}" for s in stages for part in ("description", "execution", "outcome")], "conclusion", "recommendations"]
    return ["challenge_context", "structuring", *[f"execution_{s['id']}" for s in stages], "conclusion", "recommendations", *(["decision"] if content["metadata"].get("decision_required") is True else []), "call_to_action"]


def validate(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    method = content["deliverable_type"].split("_official_")[0]
    official = definitions()[method]["stages"]
    official_ids = {s["id"] for s in official}
    sessions = content["metadata"]["method_application"]["sessions"]
    seen_sessions: set[str] = set()
    seen_stages: set[str] = set()
    for session in sessions:
        sid = session["id"]
        if sid in seen_sessions:
            errors.append(f"method_application: sessão duplicada {sid}")
        seen_sessions.add(sid)
        mapped: set[str] = set()
        for stage in session["stages"]:
            if stage["id"] in seen_stages:
                errors.append(f"method_application: ID de etapa duplicado {stage['id']}")
            seen_stages.add(stage["id"])
            refs = set(stage["official_stage_ids"])
            if refs - official_ids:
                errors.append(f"{stage['id']}: correspondência oficial desconhecida {sorted(refs - official_ids)}")
            mapped |= refs
        excluded = [s["official_stage_id"] for s in session["out_of_scope_stages"]]
        if len(excluded) != len(set(excluded)):
            errors.append(f"{sid}: etapa excluída repetida")
        if set(excluded) - official_ids:
            errors.append(f"{sid}: exclusão de etapa oficial desconhecida")
        if mapped & set(excluded):
            errors.append(f"{sid}: etapa aplicada e fora do escopo simultaneamente")
        if mapped | set(excluded) != official_ids:
            errors.append(f"{sid}: cobertura incompleta do playbook; declare exclusões por desenho, não lacunas de registro")
        if session["variant"] == "standard":
            actual = [(s["label"], s["meaning"], s["official_stage_ids"]) for s in session["stages"]]
            expected = [(s["label"], s["meaning"], [s["id"]]) for s in official]
            if actual != expected or excluded:
                errors.append(f"{sid}: aplicação standard deve preservar nomes, significados e ordem do playbook")
        elif not session["adaptation_reason"].strip():
            errors.append(f"{sid}: informe o motivo da aplicação adaptada ou pocket")

    keys = section_keys(content)
    order = {key: i for i, key in enumerate(keys)}
    is_presentation = content["deliverable_type"].endswith("presentation")
    # Decisão informativa pode existir mesmo sem pedido de deliberação.
    if is_presentation and "decision" not in order:
        order = {key: i for i, key in enumerate([*keys[:-1], "decision", keys[-1]])}
    present: set[str] = set()
    last = -1
    heading_key = None
    slide_blocks = slide_words = 0

    def flush() -> None:
        if is_presentation and (slide_blocks > 4 or slide_words > 140):
            errors.append(f"{heading_key}: slide com {slide_blocks} blocos e {slide_words} palavras; limites 4 e 140")

    for block in content["blocks"]:
        data = block["data"]
        key = data.get("section_key")
        if block["type"] == "page_break":
            flush()
            heading_key = None
            slide_blocks = slide_words = 0
            continue
        if key not in order:
            errors.append(f"{block['id']}: section_key fora da receita aplicada: {key}")
            continue
        if order[key] < last:
            errors.append(f"{key}: seção fora de ordem na receita oficial")
        last = max(last, order[key])
        if block["type"] == "heading":
            flush()
            heading_key = key
            slide_blocks = slide_words = 0
            if is_presentation:
                title = str(data.get("text", "")).strip()
                if not 4 <= len(title.split()) <= 14:
                    errors.append(f"{key}: título precisa expressar um achado em 4 a 14 palavras")
            continue
        if is_presentation:
            if heading_key != key:
                errors.append(f"{key}: conteúdo precisa de título do slide com a mesma seção")
            slide_blocks += 1
            def words(value: Any) -> int:
                if isinstance(value, str):
                    return len(value.split())
                if isinstance(value, list):
                    return sum(words(v) for v in value)
                if isinstance(value, dict):
                    return sum(words(v) for k, v in value.items() if k not in ("section_key", "citation_ids"))
                return 0
            slide_words += words(data)
        if block["type"] in ("paragraph", "callout", "metric") and isinstance(data.get("text"), str) and data["text"].strip():
            present.add(key)
            if not block.get("citation_ids"):
                errors.append(f"{key}: síntese exige fonte rastreável")
    flush()
    for key in keys:
        if key not in present:
            errors.append(f"{key}: falta síntese textual visível com fonte; título ou tabela não substitui conteúdo")
    if is_presentation:
        if not content.get("summary") or len(content["summary"].split()) > 35:
            errors.append("summary: mensagem de capa obrigatória em até 35 palavras")
    return errors
