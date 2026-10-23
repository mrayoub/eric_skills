"""Verifica a CDT oficial: os quatro campos que vão ao Jira (Rótulo Epic, Descrição, Justificativa e Benefícios), com
título tecnológico, a Descrição respondendo às cinco perguntas do comunicado, sem fonte citada e com Markdown só na
Descrição."""
from __future__ import annotations

import re
from typing import Any

FIELDS = ("jira_title", "description", "justification", "benefits")
# As cinco perguntas do comunicado, na ordem dele, como subtítulos em negrito dentro da Descrição.
QUESTIONS = (
    "Qual problema queremos resolver?",
    "Quem é impactado?",
    "Como o processo funciona hoje?",
    "Qual resultado esperamos alcançar?",
    "O que é prioridade neste momento?",
)
PRIORITY_GROUPS = ("essencial", "importante", "fora do escopo")
# O Rótulo Epic é o título do ticket: nomeia o que será construído, como tecnologia, e não sugere uma pessoa.
TECH_TERMS = re.compile(
    r"\b(plataforma|sistema|ferramenta|m[óo]dulo|aplica[çc][ãa]o|aplicativo|app|portal|painel|dashboard|formul[áa]rio|"
    r"integra[çc][ãa]o|api|automa[çc][ãa]o|automatiza[çc][ãa]o|interface|chatbot|software|base de dados|banco de dados|"
    r"servi[çc]o digital|funcionalidade|relat[óo]rio automatizado|rob[ôo]|rpa|workflow|fluxo automatizado|"
    r"motor|algoritmo|modelo de ia|intelig[êe]ncia artificial|ia)\b", re.IGNORECASE)
PERSON_LIKE = re.compile(r"\b(assistente|atendente|analista|consultor|secret[áa]ri[oa]|ajudante|colaborador)\b",
                         re.IGNORECASE)
MAX_TITLE_WORDS = 16
# Pendência é marcada com dois-pontos ("a confirmar: o dado (quem)"); "a confirmar na homologação" não é pendência.
PENDING = re.compile(r"\ba (confirmar|definir|levantar|obter):", re.IGNORECASE)
# Justificativa sem risco concreto fica vazia no Jira.
BLANK = re.compile(r"^deixar vazio\b", re.IGNORECASE)
# O Jira não referencia fontes.
SOURCE_MENTION = re.compile(r"\bfontes?:|\[[A-Z]{1,4}-?\d{1,3}\]", re.IGNORECASE)
# Só a Descrição usa Markdown; Justificativa e Benefícios são texto simples.
MARKDOWN = re.compile(r"^\s*([-*+>#]\s|\d+[.)]\s)|\*\*|__|`|\[[^\]]+\]\([^)]+\)", re.MULTILINE)
MAX_WORDS_PER_QUESTION = 150
MAX_WORDS = {"justification": 80, "benefits": 80}


def sections(content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {block["data"]["section_key"]: block for block in content.get("blocks", [])
            if isinstance(block.get("data"), dict) and isinstance(block["data"].get("section_key"), str)
            and isinstance(block["data"].get("text"), str)}


def words(text: str) -> int:
    return len(text.split())


def questions(description: str) -> tuple[dict[str, str], list[str]]:
    """Resposta de cada pergunta (o texto até o próximo subtítulo) e as perguntas ausentes ou fora de ordem."""
    positions = [(description.find(f"**{question}**"), question) for question in QUESTIONS]
    missing = [question for position, question in positions if position < 0]
    found = [(position, question) for position, question in positions if position >= 0]
    ordered = sorted(found)
    if [question for _, question in ordered] != [question for _, question in found]:
        missing.append("ordem do comunicado")
    answers: dict[str, str] = {}
    for index, (position, question) in enumerate(ordered):
        start = position + len(question) + 4
        end = ordered[index + 1][0] if index + 1 < len(ordered) else len(description)
        answers[question] = description[start:end].strip()
    return answers, missing


def report(content: dict[str, Any]) -> dict[str, Any]:
    """Diagnóstico da CDT oficial em qualquer estado; `errors` impede a entrega."""
    by_key = sections(content)
    texts = {key: block["data"]["text"] for key, block in by_key.items()}
    errors: list[str] = []
    extra = sorted(key for key in by_key if key not in FIELDS and not key.endswith("_heading"))
    if extra:
        errors.append(f"a CDT oficial tem só Rótulo Epic, Descrição, Justificativa e Benefícios; tire {extra} (o que não vai ao "
                      "Jira fica na Análise da CDT)")
    order = [key for key in (block.get("data", {}).get("section_key") for block in content.get("blocks", []))
             if key in FIELDS]
    if order != [key for key in FIELDS if key in order]:
        errors.append(f"campos fora de ordem: {order}; use {list(FIELDS)}")

    title = texts.get("jira_title", "").strip()
    if title and not PENDING.search(title):
        if "\n" in title or words(title) > MAX_TITLE_WORDS:
            errors.append(f"Rótulo Epic: uma linha com até {MAX_TITLE_WORDS} palavras")
        if not TECH_TERMS.search(title):
            errors.append("Rótulo Epic: nomeie o artefato tecnológico (plataforma, sistema, ferramenta, módulo, "
                          "integração, interface, painel, automação) e o que ele faz")
        person = PERSON_LIKE.search(title)
        if person:
            errors.append(f"Rótulo Epic: '{person.group(0)}' sugere uma pessoa; descreva a tecnologia (por exemplo, "
                          "'interface conversacional com IA' em vez de 'assistente')")

    answers, missing = questions(texts.get("description", ""))
    if missing:
        errors.append(f"Descrição: as cinco perguntas do comunicado são obrigatórias, como subtítulos em negrito e na "
                      f"ordem; falta {missing}")
    empty = [question for question, answer in answers.items() if not answer]
    if empty:
        errors.append(f"Descrição: pergunta sem resposta {empty}; com dado faltando, responda o que o material "
                      "sustenta e marque 'a confirmar:'")
    priority = answers.get(QUESTIONS[-1], "")
    if priority and not PENDING.search(priority):
        groups = [group for group in PRIORITY_GROUPS if group not in priority.casefold()]
        if groups:
            errors.append(f"Descrição: separe a prioridade em essencial, importante e fora do escopo; falta {groups}")

    pending = sorted(key for key in FIELDS if key in texts and PENDING.search(texts[key]))
    blank = sorted(key for key in ("justification",) if key in texts and BLANK.match(texts[key].strip()))
    unsourced = sorted(key for key in FIELDS if key in by_key and not by_key[key].get("citation_ids")
                       and key not in pending and key not in blank)
    if unsourced:
        errors.append(f"campos sem fonte no JSON e sem pendência declarada: {unsourced}")
    cited = sorted(key for key in FIELDS if key in texts and SOURCE_MENTION.search(texts[key]))
    if cited:
        errors.append(f"fonte citada em campo do Jira: {cited}; as fontes vão só na Análise da CDT")
    formatted = sorted(key for key in ("jira_title", "justification", "benefits")
                       if key in texts and MARKDOWN.search(texts[key]))
    if formatted:
        errors.append(f"formatação Markdown fora da Descrição: {formatted}; use texto simples, um item por linha")
    long_sections = {question: words(answer) for question, answer in answers.items()
                     if words(answer) > MAX_WORDS_PER_QUESTION}
    long_sections.update({key: words(texts[key]) for key in MAX_WORDS
                          if key in texts and words(texts[key]) > MAX_WORDS[key]})
    if long_sections:
        errors.append(f"textos longos demais (palavras): {long_sections}; limites: {MAX_WORDS_PER_QUESTION} por "
                      f"pergunta da Descrição, {MAX_WORDS['justification']} na Justificativa e nos Benefícios")
    return {
        "pending_fields": pending,
        "blank_fields": blank,
        "unsourced_fields": unsourced,
        "long_sections": long_sections,
        "errors": errors,
    }


def validate(content: dict[str, Any]) -> list[str]:
    result = report(content)
    errors = list(result["errors"])
    if result["pending_fields"]:
        errors.append(f"versão completa com campos a confirmar: {result['pending_fields']}; use completeness partial")
    return errors
