"""Verifica a consistência matemática das avaliações IQB completas."""
from __future__ import annotations

from collections import Counter
from typing import Any

YES_COUNT_TO_RAW_SCORE = {9: 5, 8: 5, 7: 4, 6: 4, 5: 3, 4: 3, 3: 2, 2: 2, 1: 1, 0: 1}
RAW_SCORE_TO_LABEL = {5: "Excelente", 4: "Saudavel", 3: "Adequado", 2: "Fragil", 1: "Insuficiente"}
VETO_ITEM_IDS = {"clarity": "CLA-10", "evidence": "EVI-06", "outcomes": "OUT-10", "actionability": "ACT-10"}
VETO_MAX_SCORES = {"clarity": 2, "evidence": 1, "outcomes": 2, "actionability": 2}
PREFIX = {"clarity": "CLA", "evidence": "EVI", "outcomes": "OUT", "actionability": "ACT"}


def validate(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sections = {block["data"].get("section_key"): block["data"] for block in content["blocks"]}
    scores = sections.get("scores")
    iqb = sections.get("iqb")
    if scores is None or iqb is None:
        return ["scores/iqb: blocos obrigatórios ausentes"]

    def compare(path: str, actual: Any, expected: Any) -> None:
        if actual != expected:
            errors.append(f"{path}: informado {actual!r}, calculado {expected!r}")

    finals: list[int] = []
    for dimension, prefix in PREFIX.items():
        detail = scores.get("dimensions", {}).get(dimension, {})
        items = detail.get("items", [])
        ids = [item.get("criterion_id", "") for item in items]
        expected_ids = {f"{prefix}-{index:02d}" for index in range(1, 11)}
        duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
        missing_ids = sorted(expected_ids - set(ids))
        extra_ids = sorted(set(ids) - expected_ids)
        path = f"scores.{dimension}"
        if duplicate_ids or missing_ids or extra_ids or len(items) != 10:
            errors.append(f"{path}.items.criterion_id: duplicados {duplicate_ids}, faltantes {missing_ids}, inesperados {extra_ids}; {len(items)} itens")
            continue
        veto_id = VETO_ITEM_IDS[dimension]
        veto_max = VETO_MAX_SCORES[dimension]
        yes_count = sum(item.get("answer") is True for item in items if item["criterion_id"] != veto_id)
        veto = next(item for item in items if item["criterion_id"] == veto_id).get("answer") is not True
        raw = YES_COUNT_TO_RAW_SCORE[yes_count]
        final = min(raw, veto_max) if veto else raw
        finals.append(final)
        for field, calculated in {
            "veto_item_id": veto_id, "veto_max_score": veto_max,
            "yes_count": yes_count, "raw_score": raw, "veto_triggered": veto,
            "final_score": final, "label": RAW_SCORE_TO_LABEL[final],
        }.items():
            compare(f"{path}.{field}", detail.get(field), calculated)
    if len(finals) == 4:
        total = round(sum(finals) / 4, 1)
        classification = next(label for lower, upper, label in [
            (4.5, 5.0, "Excelente"), (3.5, 4.4, "Saudavel"),
            (2.5, 3.4, "Adequado"), (1.5, 2.4, "Fragil"), (1.0, 1.4, "Insuficiente"),
        ] if lower <= total <= upper)
        compare("iqb.score", iqb.get("score"), total)
        compare("iqb.classification", iqb.get("classification"), classification)
        span = max(finals) - min(finals)
        anti = scores.get("anti_clustering", {})
        compare("scores.anti_clustering.span", anti.get("span"), span)
        compare("scores.anti_clustering.triggered", anti.get("triggered"), span <= 1)
    return errors
