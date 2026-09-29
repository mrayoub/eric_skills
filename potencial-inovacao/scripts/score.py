"""Calcula o potencial de inovação de forma determinística.

Entrada JSON com cinco notas e suas justificativas:
{"impact": {"score": 60, "justification": "Evidência de impacto"},
 "viability": {"score": 60, "justification": "Evidência de viabilidade"},
 "strategic_alignment": {"score": 60, "justification": "Objetivo documentado"},
 "urgency": {"score": 60, "justification": "Prazo documentado"},
 "innovation": {"score": 60, "justification": "Diferenciação documentada"}}
"""

from __future__ import annotations

import math
from typing import Any

RUBRIC_VERSION = "1.2.0-portable"

CRITERIA = [
    {
        "key": "impact",
        "name": "Impacto",
        "weight": 0.30,
        "description": "Magnitude do impacto positivo esperado",
    },
    {
        "key": "viability",
        "name": "Viabilidade",
        "weight": 0.25,
        "description": "Facilidade de implementação com recursos disponíveis",
    },
    {
        "key": "strategic_alignment",
        "name": "Alinhamento Estratégico",
        "weight": 0.20,
        "description": "Convergência com metas e objetivos da CCEE",
    },
    {
        "key": "urgency",
        "name": "Urgência",
        "weight": 0.15,
        "description": "Necessidade de ação no curto prazo",
    },
    {
        "key": "innovation",
        "name": "Inovação",
        "weight": 0.10,
        "description": "Grau de novidade e diferenciação",
    },
]


def calculate_innovation_score(scores: dict[str, Any]) -> dict[str, Any]:
    """Compute only when all criteria contain explicit valid scores."""
    normalized: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    missing_justification: list[str] = []
    weighted_total = 0.0
    for criterion in CRITERIA:
        key = criterion["key"]
        raw = scores.get(key)
        if not isinstance(raw, dict) or raw.get("score") is None:
            missing.append(key)
            continue
        if isinstance(raw["score"], bool) or not isinstance(raw["score"], (int, float)):
            raise ValueError(f"Invalid score for {key}")
        value = float(raw["score"])
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"Score for {key} must be between 0 and 100")
        normalized_score: int | float = int(value) if value.is_integer() else round(value, 1)
        if not str(raw.get("justification") or "").strip():
            missing_justification.append(key)
        normalized[key] = {
            "score": normalized_score,
            "justification": str(raw.get("justification", "")),
        }
        weighted_total += normalized_score * criterion["weight"]

    if missing or missing_justification:
        return {
            "status": "incomplete",
            "scores": normalized,
            "missing_criteria": missing,
            "missing_justification": missing_justification,
            "overall_score": None,
            "classification": None,
            "criteria_weights": {
                criterion["key"]: criterion["weight"] for criterion in CRITERIA
            },
            "rubric_version": RUBRIC_VERSION,
        }

    overall_score = round(weighted_total, 1)
    if overall_score >= 70:
        classification = "priorizar"
    elif overall_score >= 40:
        classification = "monitorar"
    else:
        classification = "arquivar"

    return {
        "status": "complete",
        "scores": normalized,
        "overall_score": overall_score,
        "classification": classification,
        "weighted": {
            criterion["key"]: round(normalized[criterion["key"]]["score"] * criterion["weight"], 2)
            for criterion in CRITERIA
        },
        "criteria_weights": {
            criterion["key"]: criterion["weight"] for criterion in CRITERIA
        },
        "rubric_version": RUBRIC_VERSION,
    }


def main() -> None:
    import argparse
    import json
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Calcula o potencial de inovação a partir de um JSON com os cinco critérios.")
    parser.add_argument("input", help="arquivo JSON ou '-' para stdin")
    args = parser.parse_args()
    raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
    try:
        result = calculate_innovation_score(json.loads(raw))
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        sys.exit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
