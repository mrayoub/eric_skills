"""Pure deterministic scoring for calculate-innovation-potential."""

from __future__ import annotations

import math
from typing import Any

RUBRIC_VERSION = "1.1.0-portable"

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
    weighted_total = 0.0
    for criterion in CRITERIA:
        key = criterion["key"]
        raw = scores.get(key)
        if not isinstance(raw, dict) or raw.get("score") is None:
            missing.append(key)
            continue
        try:
            value = float(raw["score"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid score for {key}") from exc
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"Score for {key} must be between 0 and 100")
        normalized_score: int | float = int(value) if value.is_integer() else round(value, 1)
        normalized[key] = {
            "score": normalized_score,
            "justification": str(raw.get("justification", "")),
        }
        weighted_total += value * criterion["weight"]

    if missing:
        return {
            "status": "incomplete",
            "scores": normalized,
            "missing_criteria": missing,
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
        "criteria_weights": {
            criterion["key"]: criterion["weight"] for criterion in CRITERIA
        },
        "rubric_version": RUBRIC_VERSION,
    }
