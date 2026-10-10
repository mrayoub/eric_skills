"""Cálculo determinístico e portátil do IQB para Entrevista Inicial ou Briefing.

Este módulo é a fonte de verdade executável da skill ``avaliacao-briefing-iqb``
(adaptada de ``validate-briefing`` do ERIC_RC6).
Ele não acessa banco, rede, LLM ou módulos do host: recebe as respostas binárias
da rubrica e devolve apenas resultados determinísticos e auditáveis.

Entrada JSON: objeto com as chaves clarity, evidence, outcomes e actionability,
cada uma contendo 10 itens com IDs CLA-01..10, EVI-01..10, OUT-01..10 ou
ACT-01..10, respectivamente. Exemplo de item:
{"criterion_id": "CLA-01", "answer": true, "evidence": "Trecho da fonte"}
Uso: python3 scripts/iqb.py respostas.json (ou '-' para ler de stdin).
"""

from __future__ import annotations

import re

IQB_RUBRIC_VERSION = "1.1.0-portable"

DIMENSION_KEYS = ["clarity", "evidence", "outcomes", "actionability"]

VETO_ITEM_IDS: dict[str, str] = {
    "clarity": "CLA-10",
    "evidence": "EVI-06",
    "outcomes": "OUT-10",
    "actionability": "ACT-10",
}

VETO_MAX_SCORES: dict[str, int] = {
    "clarity": 2,
    "evidence": 1,
    "outcomes": 2,
    "actionability": 2,
}

YES_COUNT_TO_RAW_SCORE: dict[int, int] = {
    9: 5,
    8: 5,
    7: 4,
    6: 4,
    5: 3,
    4: 3,
    3: 2,
    2: 2,
    1: 1,
    0: 1,
}

RAW_SCORE_TO_LABEL: dict[int, str] = {
    5: "Excelente",
    4: "Saudavel",
    3: "Adequado",
    2: "Fragil",
    1: "Insuficiente",
}

IQB_CLASSIFICATION: list[dict] = [
    {
        "min": 4.5,
        "max": 5.0,
        "classification": "Excelente",
        "orientation": "Pronto para execucao",
    },
    {
        "min": 3.5,
        "max": 4.4,
        "classification": "Saudavel",
        "orientation": "Ajustes rapidos antes do kick-off",
    },
    {
        "min": 2.5,
        "max": 3.4,
        "classification": "Adequado",
        "orientation": "Revisao estruturada necessaria",
    },
    {
        "min": 1.5,
        "max": 2.4,
        "classification": "Fragil",
        "orientation": "Retornar ao sponsor",
    },
    {
        "min": 1.0,
        "max": 1.4,
        "classification": "Insuficiente",
        "orientation": "Reiniciar o enquadramento",
    },
]

GAP_SEVERITY: dict[str, str] = {
    "Excelente": "info",
    "Saudavel": "info",
    "Adequado": "warning",
    "Fragil": "critical",
    "Insuficiente": "critical",
}


def calculate_dimension(
    yes_count: int,
    veto_triggered: bool,
    dimension_key: str,
) -> dict:
    """Converta a contagem binária e aplique o teto de veto da dimensão."""
    yes_count = max(0, min(9, yes_count))
    raw_score = YES_COUNT_TO_RAW_SCORE.get(yes_count, 1)
    veto_max = VETO_MAX_SCORES.get(dimension_key, 5)
    final_score = min(raw_score, veto_max) if veto_triggered else raw_score

    return {
        "yes_count": yes_count,
        "raw_score": raw_score,
        "final_score": final_score,
        "label": _score_to_label(final_score),
        "veto_triggered": veto_triggered,
        "veto_item_id": VETO_ITEM_IDS.get(dimension_key),
        "veto_max_score": veto_max,
    }


def calculate_iqb(
    clarity: dict,
    evidence: dict,
    outcomes: dict,
    actionability: dict,
) -> dict:
    """Calcule o IQB global a partir das quatro dimensões já avaliadas."""
    scores = {
        "clarity": clarity,
        "evidence": evidence,
        "outcomes": outcomes,
        "actionability": actionability,
    }
    final_scores = [
        clarity["final_score"],
        evidence["final_score"],
        outcomes["final_score"],
        actionability["final_score"],
    ]
    iqb_score = round(sum(final_scores) / 4, 1)
    classification_info = _classify_iqb(iqb_score)
    classification = classification_info["classification"]
    span = max(final_scores) - min(final_scores)

    tags = {}
    for dimension_key, dimension in scores.items():
        if dimension["final_score"] <= 2:
            tags[dimension_key] = "critical"
        elif dimension["final_score"] == 3:
            tags[dimension_key] = "warning"
        else:
            tags[dimension_key] = "info"

    return {
        "scores": scores,
        "iqb_score": iqb_score,
        "classification": classification,
        "orientation": classification_info["orientation"],
        "diagnosis": _generate_diagnosis(scores, iqb_score, classification),
        "anti_clustering": _check_anti_clustering(span, final_scores),
        "span": span,
        "tags": tags,
    }


def calculate_iqb_from_evaluations(
    evaluations: dict[str, list[dict]],
) -> dict:
    """Calcule todo o IQB diretamente das 40 respostas produzidas pelo avaliador.

    O LLM pode avaliar somente os critérios e suas evidências. A contagem, os
    vetos, a média, a classificação e as tags são integralmente decididos aqui.
    """
    _validate_complete_evaluations(evaluations)
    dimension_results: dict[str, dict] = {}
    for dimension_key in DIMENSION_KEYS:
        items = evaluations.get(dimension_key, [])
        veto_id = VETO_ITEM_IDS[dimension_key]
        yes_count = sum(
            1
            for item in items
            if item.get("criterion_id") != veto_id and item.get("answer") is True
        )
        veto_items = [item for item in items if item.get("criterion_id") == veto_id]
        veto_triggered = bool(veto_items) and veto_items[0].get("answer") is not True
        dimension_results[dimension_key] = calculate_dimension(
            yes_count=yes_count,
            veto_triggered=veto_triggered,
            dimension_key=dimension_key,
        )

    return calculate_iqb(
        clarity=dimension_results["clarity"],
        evidence=dimension_results["evidence"],
        outcomes=dimension_results["outcomes"],
        actionability=dimension_results["actionability"],
    )


def _validate_complete_evaluations(evaluations: dict[str, list[dict]]) -> None:
    """Reject missing or unsupported rubric answers before any score exists."""
    prefixes = {"clarity": "CLA", "evidence": "EVI", "outcomes": "OUT", "actionability": "ACT"}
    for dimension_key, prefix in prefixes.items():
        items = evaluations.get(dimension_key)
        if not isinstance(items, list) or len(items) != 10:
            raise ValueError(f"{dimension_key}: exactly 10 criterion answers are required")
        expected = {f"{prefix}-{index:02d}" for index in range(1, 11)}
        actual = {item.get("criterion_id") for item in items if isinstance(item, dict)}
        if actual != expected:
            raise ValueError(f"{dimension_key}: criterion IDs do not match the rubric")
        for item in items:
            if type(item.get("answer")) is not bool:
                raise ValueError(f"{item['criterion_id']}: answer must be true or false")
            evidence = item.get("evidence")
            if not isinstance(evidence, str) or not evidence.strip():
                raise ValueError(f"{item['criterion_id']}: evidence or an explicit absence note is required")


def validate_criterion_ids(items: list[dict]) -> list[str]:
    """Valide quantidade, formato, unicidade e família dos critérios."""
    errors: list[str] = []
    if len(items) != 10:
        return [f"Expected 10 items, got {len(items)}"]

    criterion_ids = [str(item.get("criterion_id", "")) for item in items]
    for criterion_id in criterion_ids:
        if not re.match(r"^(CLA|EVI|OUT|ACT)-(0[1-9]|10)$", criterion_id):
            errors.append(f"Invalid criterion_id format: {criterion_id}")
    if len(set(criterion_ids)) != len(criterion_ids):
        errors.append("Criterion IDs must be unique")
    return errors


def _score_to_label(score: int) -> str:
    return RAW_SCORE_TO_LABEL.get(score, "Insuficiente")


def _classify_iqb(iqb_score: float) -> dict:
    for band in IQB_CLASSIFICATION:
        if band["min"] <= iqb_score <= band["max"]:
            return {
                "classification": band["classification"],
                "orientation": band["orientation"],
            }
    return {
        "classification": "Insuficiente",
        "orientation": "Reiniciar o enquadramento",
    }


def _check_anti_clustering(span: int, final_scores: list[int]) -> dict:
    result = {
        "triggered": span <= 1,
        "original_scores": list(final_scores) if span <= 1 else None,
        "span": span,
        "re_evaluation_notes": None,
    }
    if span <= 1:
        low_dims = []
        high_dims = []
        for index, key in enumerate(DIMENSION_KEYS):
            if final_scores[index] <= 2:
                low_dims.append(key)
            elif final_scores[index] >= 4:
                high_dims.append(key)

        notes = [
            f"Auditoria de agrupamento necessária (span={span} <= 1). "
            f"As quatro dimensões ficaram a até {span} ponto(s) umas das outras."
        ]
        if low_dims:
            notes.append(f"Lower dimensions: {', '.join(low_dims)}.")
        if high_dims:
            notes.append(f"Higher dimensions: {', '.join(high_dims)}.")
        notes.append("Reexaminar manualmente cada evidência; não forçar dispersão artificial.")
        result["re_evaluation_notes"] = " ".join(notes)
    return result


def _generate_diagnosis(scores: dict, iqb_score: float, classification: str) -> str:
    dim_labels = {
        "clarity": "Clareza",
        "evidence": "Evidencias",
        "outcomes": "Resultados",
        "actionability": "Acionabilidade",
    }
    ordered = sorted(DIMENSION_KEYS, key=lambda key: scores[key]["final_score"])
    strengths = [dim_labels[key] for key in ordered if scores[key]["final_score"] >= 4]
    gaps = [dim_labels[key] for key in ordered if scores[key]["final_score"] <= 2]
    parts = [
        f"IQB {iqb_score} — {classification}. "
        f"O documento avaliado {_classification_to_verb(classification)}."
    ]
    if strengths:
        parts.append(f"Pontos fortes: {', '.join(strengths)}.")
    if gaps:
        parts.append(f"Lacunas prioritarias: {', '.join(gaps)}.")

    if classification in ("Fragil", "Insuficiente"):
        parts.append(
            "Recomenda-se retornar ao sponsor para revisao substancial antes de "
            "iniciar a descoberta."
        )
    elif classification == "Adequado":
        parts.append(
            "Recomenda-se revisao estruturada dos gaps identificados antes do kick-off."
        )
    elif classification == "Saudavel":
        parts.append("Recomendam-se ajustes rapidos nos gaps antes do kick-off.")
    elif classification == "Excelente":
        parts.append("Documento avaliado pronto para execução.")
    return " ".join(parts)


def _classification_to_verb(classification: str) -> str:
    verbs = {
        "Excelente": "esta completo e bem fundamentado",
        "Saudavel": "esta solido com oportunidades de refinamento",
        "Adequado": "atinge o minimo necessario para iniciar",
        "Fragil": "requer revisao significativa",
        "Insuficiente": "nao possui fundamentacao minima",
    }
    return verbs.get(classification, "requer atencao")


def main() -> None:
    import argparse
    import json
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Calcula o IQB a partir de um JSON com as 40 respostas da rubrica.")
    parser.add_argument("input", help="arquivo JSON ou '-' para stdin")
    args = parser.parse_args()
    raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
    try:
        result = calculate_iqb_from_evaluations(json.loads(raw))
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        sys.exit(2)
    print(json.dumps({**result, "status": "complete", "rubric_version": IQB_RUBRIC_VERSION},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
