#!/usr/bin/env python3
"""Confere a CDT oficial e a Análise da CDT antes de renderizar: os três campos do Jira, as cinco perguntas da
Descrição, pendências, checklist do comunicado, dados a obter e coerência de estado entre os dois arquivos.

Uso: python3 scripts/checar_cdt.py cdt.json analise.json
Imprime um relatório JSON. Código 0: podem ser entregues no estado declarado; 1: corrija antes de renderizar.
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
    errors = [f"CDT: {error}" for error in cdt_report["errors"]]
    errors += [f"Análise: {error}" for error in analysis_report["errors"]]
    declared = {name: content.get("metadata", {}).get("completeness") or "complete"
                for name, content in (("cdt", cdt), ("analise", analysis))}
    pending = cdt_report["pending_fields"]
    ready = not pending and not analysis_report["checklist_gaps"] and not errors
    suggested = "complete" if ready else "partial"
    if len(set(declared.values())) > 1:
        errors.append(f"os dois arquivos precisam declarar o mesmo estado em metadata.completeness: {declared}")
    if pending and not analysis_report["declares_pending"]:
        errors.append(f"Análise: a CDT tem campos 'a confirmar:' ({pending}); liste-os nos dados a obter")
    if declared["cdt"] == "complete":
        errors += [f"CDT: {error}" for error in official.validate(cdt) if error not in cdt_report["errors"]]
        errors += [f"Análise: {error}" for error in review.validate(analysis) if error not in analysis_report["errors"]]
    else:
        if not pending and not analysis_report["checklist_gaps"]:
            errors.append("versão parcial sem pendência marcada: escreva 'a confirmar: <dado> (<quem>)' no campo que "
                          "falta, ou marque os dois arquivos como completos e 'Pronta para envio'")
        if not analysis_report["readiness_says_partial"]:
            errors.append("Análise: readiness: a versão parcial deve dizer 'Parcial' e o que falta")
    result = {
        "pending_fields": pending,
        "checklist": analysis_report["checklist"],
        "checklist_gaps": analysis_report["checklist_gaps"],
        "declared_completeness": declared["cdt"],
        "suggested_completeness": suggested,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
