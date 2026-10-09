"""Verifica notas, pesos, total e classe do potencial de inovação."""
from __future__ import annotations

import math
from collections import Counter
from typing import Any

WEIGHTS = {"impact": 0.30, "viability": 0.25, "strategic_alignment": 0.20, "urgency": 0.15, "innovation": 0.10}


def classify(score: float) -> str:
    return "priorizar" if score >= 70 else "monitorar" if score >= 40 else "arquivar"


def validate(content: dict[str, Any]) -> list[str]:
    blocks = [block["data"] for block in content["blocks"] if block["data"].get("section_key") == "scores"]
    if len(blocks) != 1:
        return ["scores: exige exatamente um bloco de notas"]
    data = blocks[0]
    errors: list[str] = []
    rows = data.get("rows", [])
    criteria = [row.get("criterion", "") for row in rows]
    duplicates = sorted(key for key, count in Counter(criteria).items() if count > 1)
    missing = sorted(set(WEIGHTS) - set(criteria))
    extra = sorted(set(criteria) - set(WEIGHTS))
    if duplicates or missing or extra or len(rows) != 5:
        errors.append(f"scores.rows.criterion: duplicados {duplicates}, faltantes {missing}, inesperados {extra}; {len(rows)} critérios")
    numeric_scores: dict[str, float] = {}
    for index, row in enumerate(rows):
        key = row.get("criterion")
        path = f"scores.rows[{index}]"
        if key in WEIGHTS and row.get("weight") != WEIGHTS[key]:
            errors.append(f"{path}.weight: informado {row.get('weight')!r}, esperado {WEIGHTS[key]}")
        if not str(row.get("justification") or "").strip():
            errors.append(f"{path}.justification: justificativa vazia")
        value = row.get("score")
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
            errors.append(f"{path}.score: nota deve ser número finito entre 0 e 100")
        else:
            numeric_scores[key] = float(value)
    if not duplicates and not missing and not extra and len(numeric_scores) == 5:
        # Acumula na mesma ordem e forma de score.py; sum() de floats (Python 3.12+) arredonda diferente.
        weighted_total = 0.0
        for key, weight in WEIGHTS.items():
            weighted_total += numeric_scores[key] * weight
        total = round(weighted_total, 1)
        if data.get("overall_score") != total:
            errors.append(f"scores.overall_score: informado {data.get('overall_score')!r}, calculado {total}")
        classification = classify(total)
        if data.get("classification") != classification:
            errors.append(f"scores.classification: informado {data.get('classification')!r}, calculado {classification!r}")
    return errors
