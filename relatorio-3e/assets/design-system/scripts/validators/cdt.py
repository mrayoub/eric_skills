"""Verifica a CDT oficial: os quatro campos que vão ao Jira (Rótulo Epic, Descrição, Justificativa e Benefícios), com
título tecnológico, a Descrição respondendo às cinco perguntas do comunicado, sem pergunta em aberto (o que falta é
lacuna [COMPLETAR: ...] para quem abre a CDT), sem fonte citada, com Markdown só na Descrição e escrita pela gerência que abre a demanda, em primeira pessoa."""
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
# A CDT é aberta quando a decisão de seguir já foi tomada: o texto afirma, não pergunta nem deixa algo "a confirmar".
# O dado que falta vira lacuna explícita, que quem abre a CDT preenche antes de enviar.
GAP = re.compile(r"\[COMPLETAR: [^\]\n?]+\]")
PENDING = re.compile(r"\b(a (confirmar|definir|levantar|obter|validar)|tbd|pendente de definição)\b", re.IGNORECASE)
# Quem abre a CDT é a gerência que patrocinou a esteira: ela não fala de si mesma na terceira pessoa.
THIRD_PERSON = re.compile(r"\b(a (área|gerência|gestão) (solicitante|demandante|da área|responsável)|"
                          r"a gestão da área|(o|a) sponsor|(o|a) patrocinador[a]?|a área de negócio)\b", re.IGNORECASE)
# Expressões de texto gerado por IA, que deixam a CDT distante e pouco direta.
AI_TICS = re.compile(r"\b(vale (destacar|ressaltar|mencionar)|é importante (destacar|ressaltar|mencionar|notar)|"
                     r"cabe (destacar|ressaltar)|nesse sentido|neste contexto|além disso|dessa forma|desse modo|"
                     r"em suma|robust[oa]s?|abrangente|alavanc\w+|potencializ\w+|sinergia|holístic[oa]|"
                     r"de forma (eficiente|eficaz|estratégica)|no cenário atual|cada vez mais|crucial)\b",
                     re.IGNORECASE)
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


def strip_questions(text: str) -> str:
    """O texto sem os subtítulos das cinco perguntas, que são as únicas perguntas permitidas."""
    for question in QUESTIONS:
        text = text.replace(f"**{question}**", "")
    return text


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
    if title:
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
        errors.append(f"Descrição: pergunta sem resposta {empty}; responda com o material ou deixe a lacuna "
                      "'[COMPLETAR: o dado]'")
    priority = answers.get(QUESTIONS[-1], "")
    if priority:
        groups = [group for group in PRIORITY_GROUPS if group not in priority.casefold()]
        if groups:
            errors.append(f"Descrição: separe a prioridade em essencial, importante e fora do escopo; falta {groups}")

    gaps = {key: GAP.findall(texts[key]) for key in FIELDS if key in texts and GAP.search(texts[key])}
    plain = {key: GAP.sub("", text) for key, text in texts.items()}
    pending = sorted(key for key in FIELDS if key in plain and PENDING.search(plain[key]))
    if pending:
        errors.append(f"ponto em aberto na CDT: {pending}; o texto afirma o que foi decidido. O dado que falta vira "
                      "lacuna '[COMPLETAR: o dado]' para quem abre a CDT")
    asking = [key for key in FIELDS if key in plain and "?" in strip_questions(plain[key])]
    if asking:
        errors.append(f"pergunta no texto da CDT: {asking}; só os subtítulos da Descrição são perguntas, o resto "
                      "afirma o que foi decidido")
    distant = sorted({match.group(0) for key in FIELDS if key in texts for match in THIRD_PERSON.finditer(texts[key])})
    if distant:
        errors.append(f"a gerência que abre a CDT fala de si em primeira pessoa (nossa equipe, precisamos); troque "
                      f"{distant}")
    tics = sorted({match.group(0).lower() for key in FIELDS if key in texts for match in AI_TICS.finditer(texts[key])})
    if tics:
        errors.append(f"expressões que deixam o texto distante e com cara de IA: {tics}; escreva direto")
    blank = sorted(key for key in ("justification",) if key in texts and BLANK.match(texts[key].strip()))
    only_gaps = {key for key in FIELDS if key in plain and not plain[key].strip(" \n.:;")}
    unsourced = sorted(key for key in FIELDS if key in by_key and not by_key[key].get("citation_ids")
                       and key not in blank and key not in only_gaps)
    if unsourced:
        errors.append(f"campos sem fonte no JSON: {unsourced}")
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
        "gaps": gaps,
        "pending_fields": pending,
        "blank_fields": blank,
        "unsourced_fields": unsourced,
        "long_sections": long_sections,
        "errors": errors,
    }


def validate(content: dict[str, Any]) -> list[str]:
    result = report(content)
    errors = list(result["errors"])
    completeness = content.get("metadata", {}).get("completeness") or "complete"
    if result["gaps"] and completeness == "complete":
        errors.append(f"CDT com lacunas {sorted(result['gaps'])}; marque completeness partial")
    if not result["gaps"] and completeness != "complete":
        errors.append("CDT sem lacunas: marque completeness complete")
    return errors
