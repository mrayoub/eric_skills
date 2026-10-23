#!/usr/bin/env python3
"""Confere a CDT antes de renderizar: fonte por campo, pendências, checklist da publicação e avaliação crítica.

Uso: python3 scripts/checar_cdt.py cdt.json
Imprime um relatório JSON. Código 0: pode ser entregue no estado declarado; 1: corrija antes de renderizar.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "assets/design-system/scripts/validators/cdt.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("cdt_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    content = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    validator = load_validator()
    result = validator.report(content)
    declared = content.get("metadata", {}).get("completeness") or "complete"
    result["declared_completeness"] = declared
    result["suggested_completeness"] = "complete" if result["ready"] else "partial"
    if declared == "complete":
        result["errors"] = validator.validate(content)
    elif not result["readiness_text_ok"]:
        result["errors"].append("readiness: a versão parcial deve dizer 'Parcial' e o que falta")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
