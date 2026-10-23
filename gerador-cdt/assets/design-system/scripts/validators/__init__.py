"""Validadores semânticos por deliverable_type: validate(content) -> list[str]."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def run(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    common_path = HERE / "_common.py"
    if common_path.is_file():
        spec = importlib.util.spec_from_file_location("validators__common", common_path)
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)
        errors.extend(common.validate(content))
    path = HERE / f"{content.get('deliverable_type', '')}.py"
    if path.is_file():
        spec = importlib.util.spec_from_file_location(f"validators_{path.stem}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        errors.extend(module.validate(content))
    return errors
