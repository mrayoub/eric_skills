#!/usr/bin/env python3
"""Gera a galeria de templates: renderiza as amostras de todos os entregáveis com o design system atual.

Uso: python3 _GALERIA/gerar.py  (depois abra _GALERIA/index.html no navegador)
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "_GALERIA"
OUTPUT = GALLERY / "saida"
RENDER = ROOT / "_DESIGN_SYSTEM" / "scripts" / "render.py"
SAMPLES = ROOT / "_SAMPLES_ENTREGAVEIS"

# Entregáveis que cada skill gera (não os que apenas lê ou avalia).
SKILLS = {
    "esteira-eric": [],
    "potencial-inovacao": ["innovation_potential_assessment"],
    "briefing-inovacao": ["briefing", "briefing_one_page", "briefing_improvement_questionnaire"],
    "avaliacao-briefing-iqb": ["briefing_validation"],
    "workshop-4d": ["four_d_workshop_record"],
    "relatorio-4d": ["four_d_report"],
    "workshop-3e": ["three_e_workshop_record", "test_card"],
    "relatorio-3e": ["three_e_report", "test_card"],
    "workshop-5c": ["five_c_workshop_record"],
    "relatorio-5c": ["five_c_report"],
    "experimentacao-inovacao": ["experiment_plan", "test_card", "learning_card", "experiment_report",
                                "evidence_recommendation", "executive_presentation"],
    "scorecard-inovacao": ["innovation_scorecard"],
    "relatorio-final-inovacao": ["evidence_recommendation", "executive_presentation"],
    "gerador-cdt": ["cdt"],
}
LAYOUT_NAMES = {"report_portrait": "Relatório A4 retrato", "report_landscape": "Relatório A4 paisagem",
                "card_portrait": "Cartão A4 retrato", "executive_one_page": "Página única A4 paisagem",
                "presentation": "Apresentação 16:9"}


def labels() -> dict[str, str]:
    """Nomes de leitura dos tipos, os mesmos do cabeçalho dos entregáveis."""
    source = (ROOT / "_DESIGN_SYSTEM" / "scripts" / "render.py").read_text(encoding="utf-8")
    start = source.index("DELIVERABLE_LABELS = {")
    namespace: dict = {}
    exec(source[start:source.index("}", start) + 1], namespace)
    return namespace["DELIVERABLE_LABELS"]


def render(kind: str, allowed: list[str]) -> dict:
    out = OUTPUT / kind
    formats = ",".join(fmt for fmt in ("html", "pdf", "md", "docx", "pptx") if fmt == "html" or fmt in allowed)
    result = subprocess.run([sys.executable, str(RENDER), str(SAMPLES / kind / "input.json"),
                             "--out-dir", str(out), "--formats", formats], capture_output=True, text=True)
    files = {path.suffix.lstrip("."): path.relative_to(GALLERY).as_posix()
             for path in sorted(out.glob("*")) if path.suffix in (".html", ".pdf", ".md", ".docx", ".pptx")}
    error = result.stderr.strip().splitlines()[-1] if result.returncode else ""
    manifest = next(out.glob("*.manifest.json"), None)
    if manifest and not error:
        unavailable = json.loads(manifest.read_text(encoding="utf-8")).get("unavailable") or {}
        error = "; ".join(f"{fmt}: {reason}" for fmt, reason in unavailable.items())
    return {"files": files, "error": error}


def main() -> None:
    catalog = json.loads((ROOT / "_DESIGN_SYSTEM" / "profiles.json").read_text(encoding="utf-8"))
    profiles = catalog["types"]
    names = labels()
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip() or "sem git"
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "_DESIGN_SYSTEM"],
                           capture_output=True, text=True).stdout.strip()
    types = {}
    for kind in sorted({kind for kinds in SKILLS.values() for kind in kinds}):
        layout = profiles[kind]["layout"]
        print(f"Renderizando {kind}…", flush=True)
        entry = render(kind, profiles[kind].get("formats", catalog["default_formats"]))
        studio = ROOT / "_DESIGN_SYSTEM" / "layouts" / f"{kind}.layout.json"
        types[kind] = {**entry, "label": names.get(kind, kind), "layout": LAYOUT_NAMES.get(layout, layout),
                       "skills": [skill for skill, kinds in SKILLS.items() if kind in kinds],
                       "studio": studio.relative_to(ROOT).as_posix() if studio.is_file() else ""}
    data = {"generated": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "commit": commit + (" + alterações locais no design system" if dirty else ""),
            "skills": SKILLS, "types": types}
    template = (GALLERY / "modelo.html").read_text(encoding="utf-8")
    page = template.replace("/*DADOS*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    (GALLERY / "index.html").write_text(page, encoding="utf-8")
    errors = [kind for kind, entry in types.items() if entry["error"]]
    print(f"OK {GALLERY / 'index.html'} ({len(types)} entregáveis"
          + (f"; com aviso: {', '.join(errors)}" if errors else "") + ")")


if __name__ == "__main__":
    main()
