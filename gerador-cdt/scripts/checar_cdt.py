#!/usr/bin/env python3
"""Confere a CDT oficial e a Análise da CDT antes de renderizar.

A CDT é sempre gerada. O texto afirma o que foi decidido; o dado que falta vira lacuna "[COMPLETAR: o dado]", que
quem abre a CDT completa antes de enviar. Cada lacuna aparece na Análise da CDT, em "O que obter e analisar
primeiro", e o estado da análise diz "Com lacunas a preencher".

Uso: python3 scripts/checar_cdt.py cdt.json analise.json
Imprime um relatório JSON. Código 0: podem ser entregues; 1: corrija antes de renderizar.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

VALIDATORS = Path(__file__).resolve().parents[1] / "assets/design-system/scripts/validators"


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"{name}_validator", VALIDATORS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    cdt, analysis = (json.loads(Path(arg).read_text(encoding="utf-8")) for arg in sys.argv[1:])
    official, review = load("cdt"), load("cdt_analysis")
    cdt_report, analysis_report = official.report(cdt), review.report(analysis)
    errors = [f"CDT: {error}" for error in official.validate(cdt)]
    errors += [f"Análise: {error}" for error in analysis_report["errors"]]
    states = {name: content.get("metadata", {}).get("completeness") or "complete"
              for name, content in (("cdt", cdt), ("analise", analysis))}
    if len(set(states.values())) > 1:
        errors.append(f"os dois arquivos declaram o mesmo estado em metadata.completeness: {states}")
    gaps = cdt_report["gaps"]
    if gaps:
        if not analysis_report["readiness_says_gaps"]:
            errors.append("Análise: readiness: diga 'Com lacunas a preencher' e quais são")
        if not analysis_report["declares_pending"]:
            errors.append(f"Análise: liste as lacunas {sorted(gaps)} em 'O que obter e analisar primeiro'")
    else:
        errors += [f"Análise: {error}" for error in review.validate(analysis) if error not in analysis_report["errors"]]
    result = {
        "gaps": gaps,
        "checklist": analysis_report["checklist"],
        "checklist_gaps": analysis_report["checklist_gaps"],
        "declared_completeness": states["cdt"],
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
