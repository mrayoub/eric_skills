"""Verifica o vínculo estrutural ao Test Card executado, sem julgar evidências."""
from __future__ import annotations

from typing import Any


def validate(content: dict[str, Any]) -> list[str]:
    metadata = content.get("metadata", {})
    if metadata.get("test_card_id") == metadata.get("artifact_id"):
        return ["metadata.test_card_id: o Learning Card não pode apontar para si mesmo"]
    return []
