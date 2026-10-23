"""Verifica a CDT: campos do formulário do Jira, opções exatas, coerência entre campos, fonte por campo, pendências,
concisão, checklist do comunicado e avaliação crítica."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

OPTIONS = json.loads((Path(__file__).resolve().parent / "cdt_options.json").read_text(encoding="utf-8"))

# As cinco perguntas do comunicado, na ordem dele: a Descrição tem estas seções e nenhuma outra.
DESCRIPTION = ("problem", "audience", "current_process", "objective", "priorities")
# Campos do formulário, na ordem da tela: aba Informações Gerais e aba Benefícios da Demanda.
GENERAL = (
    "jira_title", *DESCRIPTION, "transversal_process", "family_service", "product_area", "service_area", "release",
    "attachments", "regulatory", "operation_date", "regulatory_act", "theme", "measurable_benefit", "benefits",
    "process_simplification", "process_design", "risk_if_not_done", "justification",
)
BENEFITS_TAB = (
    "demand_origin", "formal_act", "agent_benefits", "market_impact", "usage_frequency", "agent_transaction_cost",
    "corporate_risk", "risk_identification", "process_incidents", "incident_identification", "usage_frequency_score",
)
FIELDS = GENERAL + BENEFITS_TAB
# Seções de versões anteriores que saíram da CDT.
RETIRED = ("expected_results", "scope_essential", "scope_important", "scope_out", "constraints", "responsibles",
           "requester", "personal_data", "classification", "prototype", "initiative")
YES_NO = ("regulatory", "process_design", "risk_if_not_done", "agent_benefits", "agent_transaction_cost",
          "corporate_risk", "process_incidents")
SINGLE = ("product_area", "measurable_benefit", "process_simplification", "demand_origin", "market_impact",
          "usage_frequency")
TWO_LEVEL = ("transversal_process", "family_service")
# Campos que a skill nunca preenche: a pessoa escolhe no Jira ou o campo fica vazio na abertura.
ALWAYS_BLANK = ("release", "operation_date", "usage_frequency_score")
# Itens do checklist do comunicado sobre escopo, na ordem do comunicado. Os dois últimos só aparecem no checklist.
CHECKLIST = (
    "Problema e objetivo", "Públicos impactados", "Entregas essenciais",
    "Prioridades e resultados esperados", "Regras, restrições e dependências", "Responsáveis",
)
ONLY_IN_CHECKLIST = ("Regras, restrições e dependências", "Responsáveis")
STATUS = re.compile(r"\b(atendido|parcial|ausente)\b", re.IGNORECASE)
# Pendência é marcada com dois-pontos ("a confirmar: o dado (quem)"); "a confirmar na homologação" não é pendência.
PENDING = re.compile(r"\ba (confirmar|definir|levantar|obter):", re.IGNORECASE)
# Campo que não vai preenchido: a primeira linha diz o que fazer no Jira.
BLANK = re.compile(r"^(deixar vazio|selecionar no jira|escolher no jira)\b", re.IGNORECASE)
SECOND_LEVEL_TBD = "selecionar no Jira"
# O Jira não referencia fontes: os campos que vão a ele não citam fonte.
SOURCE_MENTION = re.compile(r"\bfontes?:|\[[A-Z]{1,4}-?\d{1,3}\]", re.IGNORECASE)
# Só a Descrição usa Markdown; os demais campos do Jira são texto simples.
MARKDOWN = re.compile(r"^\s*([-*+>#]\s|\d+[.)]\s)|\*\*|__|`|\[[^\]]+\]\([^)]+\)", re.MULTILINE)
MAX_WORDS = {"default": 60, "readiness": 80, "jira_title": 12,
             **{key: 150 for key in DESCRIPTION},
             **{key: 150 for key in ("publication_checklist", "quality_review", "data_to_obtain", "traceability")}}
MAX_TOTAL_WORDS = 1800
MAX_THEMES = 2


def sections(content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {block["data"]["section_key"]: block for block in content.get("blocks", [])
            if isinstance(block.get("data"), dict) and isinstance(block["data"].get("section_key"), str)
            and isinstance(block["data"].get("text"), str)}


def words(text: str) -> int:
    return len(text.split())


def first_line(text: str) -> str:
    return text.strip().splitlines()[0].strip() if text.strip() else ""


def is_blank(text: str) -> bool:
    return bool(BLANK.match(text.strip()))


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


def option_errors(key: str, value: str) -> list[str]:
    """Confere a primeira linha de um campo de lista contra as opções exatas do Jira."""
    if key in YES_NO:
        return [] if value in ("Sim", "Não") else [f"{key}: a primeira linha deve ser 'Sim' ou 'Não', não {value!r}"]
    if key in SINGLE:
        return [] if value in OPTIONS[key] else [f"{key}: {value!r} não é opção do Jira; use uma de {OPTIONS[key]}"]
    if key == "theme":
        chosen = value.split("; ")
        errors = [f"theme: {item!r} não é opção do Jira" for item in chosen if item not in OPTIONS["theme"]]
        if len(chosen) > MAX_THEMES:
            errors.append(f"theme: no máximo {MAX_THEMES} temas, separados por '; '")
        return errors
    if key in TWO_LEVEL:
        parent, _, child = value.partition(" / ")
        tree = OPTIONS[key]
        if parent not in tree:
            return [f"{key}: {parent!r} não é opção do primeiro nível; use uma de {sorted(tree)}"]
        if not child:
            return [f"{key}: escreva 'Opção / segundo nível' ou 'Opção / {SECOND_LEVEL_TBD}'"]
        if child in OPTIONS["avoid"]:
            return [f"{key}: {child!r} é opção duplicada no Jira; use a versão por extenso e sem erro"]
        if child != SECOND_LEVEL_TBD and child not in tree[parent]:
            return [f"{key}: {child!r} não é opção de {parent!r}; use uma de {tree[parent]} ou '{SECOND_LEVEL_TBD}'"]
    return []


def coherence_errors(values: dict[str, str], blank: set[str]) -> list[str]:
    """Combinações de campos que se contradizem. Campos com pendência não entram na conferência."""
    errors: list[str] = []

    def filled(key: str) -> bool:
        return key in values and key not in blank

    regulatory = values.get("regulatory")
    for act in ("regulatory_act", "formal_act"):
        if act in values:
            if regulatory == "Sim" and not filled(act):
                errors.append(f"{act}: demanda regulatória (ANEEL, MME ou CNPE) exige o ato")
            if regulatory == "Não" and filled(act):
                errors.append(f"{act}: só se preenche quando a demanda vem da ANEEL, do MME ou do CNPE; deixe vazio")
    benefit = values.get("measurable_benefit", "")
    if benefit.startswith("Elimina risco de penalidade") and values.get("risk_if_not_done") == "Não":
        errors.append("measurable_benefit: eliminar risco de multa exige 'Sim' em risk_if_not_done")
    if benefit.startswith("Benefícios direto aos Agentes") and values.get("agent_benefits") == "Não":
        errors.append("measurable_benefit: benefício direto aos agentes exige 'Sim' em agent_benefits")
    if values.get("agent_transaction_cost") == "Sim":
        if values.get("agent_benefits") == "Não":
            errors.append("agent_transaction_cost: reduzir custo do agente exige 'Sim' em agent_benefits")
        if "market_impact" in values and not filled("market_impact"):
            errors.append("market_impact: reduzir custo do agente exige ao menos uma classe de agente")
    pairs = (("corporate_risk", "risk_identification"), ("process_incidents", "incident_identification"),
             ("risk_if_not_done", "justification"))
    for flag, detail in pairs:
        if detail not in values:
            continue
        if values.get(flag) == "Sim" and not filled(detail):
            errors.append(f"{detail}: obrigatório quando {flag} é 'Sim'")
        if values.get(flag) == "Não" and filled(detail):
            errors.append(f"{detail}: deixe vazio quando {flag} é 'Não'")
    return errors


def report(content: dict[str, Any]) -> dict[str, Any]:
    """Diagnóstico da CDT em qualquer estado; `errors` impede a entrega."""
    by_key = sections(content)
    texts = {key: block["data"]["text"] for key, block in by_key.items()}
    pending = {key for key in FIELDS if key in texts and PENDING.search(texts[key])}
    blank = {key for key in FIELDS if key in texts and is_blank(texts[key])}
    unsourced = sorted(key for key in FIELDS if key in by_key and not by_key[key].get("citation_ids")
                       and key not in pending and key not in blank)
    checklist = checklist_lines(texts.get("publication_checklist", ""))
    review = texts.get("quality_review", "").casefold()
    readiness = texts.get("readiness", "").casefold()
    obtain = texts.get("data_to_obtain", "")
    long_sections = {key: words(text) for key, text in texts.items()
                     if words(text) > MAX_WORDS.get(key, MAX_WORDS["default"])}
    total = sum(words(text) for text in texts.values())

    errors: list[str] = []
    retired = [key for key in RETIRED if key in by_key]
    if retired:
        errors.append(f"seções que não fazem mais parte da CDT: {retired}; a Descrição tem só as cinco perguntas, e "
                      "regras e responsáveis vão no checklist")
    order = [key for key in (block.get("data", {}).get("section_key") for block in content.get("blocks", []))
             if key in DESCRIPTION]
    if order != [key for key in DESCRIPTION if key in order]:
        errors.append(f"Descrição fora da ordem do comunicado: {order}; use {list(DESCRIPTION)}")
    missing_description = [key for key in DESCRIPTION if key not in texts or not texts[key].strip() or key in blank]
    if missing_description:
        errors.append(f"Descrição sem resposta para {missing_description}: as cinco perguntas são obrigatórias em "
                      "qualquer versão; com dado faltando, responda o que o material sustenta e marque 'a confirmar:'")
    if unsourced:
        errors.append(f"campos sem fonte e sem pendência declarada: {unsourced}")
    formatted = [key for key in FIELDS if key not in DESCRIPTION and key in texts and MARKDOWN.search(texts[key])]
    if formatted:
        errors.append(f"formatação Markdown fora da Descrição: {formatted}; nos demais campos use texto simples, "
                      "um item por linha, sem marcador, negrito ou título")
    cited = [key for key in FIELDS if key in texts and SOURCE_MENTION.search(texts[key])]
    if cited:
        errors.append(f"fonte citada em campo do Jira: {cited}; as fontes vão só na tabela Origem dos dados")
    for key in ALWAYS_BLANK:
        if key in texts and key not in blank:
            errors.append(f"{key}: a skill não preenche este campo; escreva 'Deixar vazio', 'Selecionar no Jira' "
                          "ou 'Escolher no Jira'")
    values: dict[str, str] = {}
    for key in YES_NO + SINGLE + TWO_LEVEL + ("theme",):
        if key not in texts or key in pending or key in blank:
            continue
        value = first_line(texts[key])
        values[key] = value
        errors.extend(option_errors(key, value))
    for key in ("regulatory_act", "formal_act", "risk_identification", "incident_identification", "justification",
                "market_impact"):
        if key in texts and key not in pending:
            values.setdefault(key, first_line(texts[key]))
    errors.extend(coherence_errors(values, blank))
    priorities = texts.get("priorities", "").casefold()
    if "priorities" in texts and "priorities" not in pending:
        missing = [label for label in ("essencial", "importante", "fora do escopo") if label not in priorities]
        if missing:
            errors.append(f"priorities: separe as entregas em essencial, importante e fora do escopo; falta {missing}")
    if long_sections:
        errors.append(f"seções longas demais (palavras): {long_sections}; limites: 150 por pergunta da Descrição, "
                      "60 nos demais campos do Jira, 12 no título")
    if total > MAX_TOTAL_WORDS:
        errors.append(f"CDT com {total} palavras; limite {MAX_TOTAL_WORDS}: corte repetições e o que não responde ao comunicado")
    missing_items = [item for item in CHECKLIST if item not in checklist]
    if missing_items:
        errors.append(f"publication_checklist: itens sem status atendido, parcial ou ausente: {missing_items}")
    for item in ONLY_IN_CHECKLIST:
        status, rest = checklist.get(item, ("", ""))
        if status in ("atendido", "parcial") and not rest:
            errors.append(f"publication_checklist: '{item}' só aparece no checklist; escreva a resposta na linha")
    if "pontos fortes" not in review or "pontos fracos" not in review:
        errors.append("quality_review: exige 'Pontos fortes' e 'Pontos fracos', mesmo com todos os campos preenchidos")
    if pending and not obtain.strip():
        errors.append("data_to_obtain: há campos 'a confirmar:' sem a lista de dados a obter")
    gaps = sorted(item for item, (status, _) in checklist.items() if status != "atendido")
    return {
        "pending_fields": sorted(pending),
        "blank_fields": sorted(blank),
        "unsourced_fields": unsourced,
        "long_sections": long_sections,
        "total_words": total,
        "checklist": {item: status for item, (status, _) in checklist.items()},
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
