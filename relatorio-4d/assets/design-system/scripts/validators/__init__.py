"""Validadores semânticos por deliverable_type: validate(content) -> list[str]."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def run(content: dict[str, Any]) -> list[str]:
    path = HERE / f"{content.get('deliverable_type', '')}.py"
    if not path.is_file():
        return []
    spec = importlib.util.spec_from_file_location(f"validators_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.validate(content))
