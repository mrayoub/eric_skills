#!/usr/bin/env python3
"""Valida as fontes preservadas e gera páginas de proveniência por skill."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {"id", "titulo", "tipo", "arquivo", "skills", "origem", "autor",
          "versao_declarada", "data_importacao", "deriva_de", "vigencia", "notas",
          "titular", "licenca", "distribuido"}
TYPES = {"original", "transcricao", "adaptacao", "historico", "rubrica", "script"}
STATUS = {"confirmada", "historica", "desconhecida"}
PINNED = {
    "assets/Modelo 4D de Aprofundamento.docx": "4c9a71f74feeef9957ad08ed2cb354bf8dbd731540622ec4680c247f816a6716",
    "assets/Modelo 3E Estruturacao da Solucao.docx": "291155873d767ae4f04f2b4234878f7de0a9b9c3f74852e3a440e676942ad90c",
    "assets/Playbook_Modelo_5C_Centralidade_Cliente.docx": "375d70d5c6c876735ac7a8ecdc89ec112facbdd1dce31ce2724b69b93c9a55d7",
}

# Material de terceiros cuja licença não permite redistribuição; nunca pode voltar a uma skill.
RETIRED = {
    "strategyzer-test-card-2023.pdf",
    "strategyzer-learning-card-2023.pdf",
    "strategyzer-innovation-project-scorecard-2023.pdf",
}

# Fontes tipográficas distribuídas em assets/design-system/assets/fonts/ de cada skill.
FONT_NOTICES = [
    ("Montserrat", "Montserrat-OFL.txt"),
    ("Roboto", "Roboto-OFL.txt"),
]
FONTS_DIR = ROOT / "_DESIGN_SYSTEM/assets/fonts"


def relative_path(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts and bool(path.parts)


def load_manifest() -> list[dict]:
    path = ROOT / "_FONTES/manifest.json"
    entries = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path}: deve conter uma lista não vazia")
    ids: set[str] = set()
    memberships: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != FIELDS:
            raise ValueError(f"{path}: campos inválidos no manifesto")
        label = entry["id"]
        for key in ("id", "titulo", "arquivo", "origem", "notas"):
            if not isinstance(entry[key], str) or (key != "notas" and not entry[key].strip()):
                raise ValueError(f"{label}: {key} deve ser texto não vazio")
        if label in ids:
            raise ValueError(f"{label}: ID duplicado")
        ids.add(label)
        if entry["tipo"] not in TYPES or entry["vigencia"] not in STATUS:
            raise ValueError(f"{label}: tipo ou vigência inválido")
        for key in ("autor", "versao_declarada", "data_importacao", "deriva_de"):
            if entry[key] is not None and (not isinstance(entry[key], str) or not entry[key].strip()):
                raise ValueError(f"{label}: {key} deve ser texto não vazio ou null")
        if entry["titular"] is not None and (not isinstance(entry["titular"], str) or not entry["titular"].strip()):
            raise ValueError(f"{label}: titular deve ser texto não vazio ou null")
        if not isinstance(entry["licenca"], str) or not entry["licenca"].strip():
            raise ValueError(f"{label}: licenca deve ser texto não vazio")
        if not isinstance(entry["distribuido"], bool):
            raise ValueError(f"{label}: distribuido deve ser booleano")
        if entry["distribuido"]:
            if not relative_path(entry["arquivo"]):
                raise ValueError(f"{label}: arquivo deve ser caminho relativo dentro da skill")
        elif not entry["arquivo"].startswith("https://"):
            raise ValueError(f"{label}: fonte não distribuída deve apontar para uma URL https://")
        skills = entry["skills"]
        if not isinstance(skills, list) or not skills:
            raise ValueError(f"{label}: skills deve ser lista não vazia")
        for skill in skills:
            if not isinstance(skill, str) or Path(skill).name != skill or not skill or skill.startswith("."):
                raise ValueError(f"{label}: nome de skill inválido")
            if not (ROOT / skill / "SKILL.md").is_file():
                raise ValueError(f"{label}: skill ausente: {skill}/SKILL.md")
            membership = (skill, entry["arquivo"])
            if membership in memberships:
                raise ValueError(f"{label}: fonte repetida em {skill}/{entry['arquivo']}")
            memberships.add(membership)
    lookup = {entry["id"]: entry for entry in entries}
    for entry in entries:
        visited: set[str] = set()
        current = entry
        while current["deriva_de"] is not None:
            parent = current["deriva_de"]
            if parent not in ids:
                raise ValueError(f"{entry['id']}: deriva_de aponta para fonte inexistente: {parent}")
            if parent in visited or parent == entry["id"]:
                raise ValueError(f"{entry['id']}: ciclo em deriva_de")
            visited.add(parent)
            current = lookup[parent]
    declared_pins = {unicodedata.normalize("NFC", entry["arquivo"]) for entry in entries
                     if entry["tipo"] == "original"}
    if set(PINNED) - declared_pins:
        raise ValueError("Manifesto omite DOCX original fixado: " + ", ".join(sorted(set(PINNED) - declared_pins)))
    return entries


def validate_sources(entries: list[dict]) -> dict[tuple[str, str], str]:
    skill_dirs = [d for d in ROOT.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()]
    for path in sorted(p for d in skill_dirs for p in d.rglob("*")):
        if path.name in RETIRED:
            raise ValueError(f"Material de terceiros não redistribuível presente: {path.relative_to(ROOT)}")
    hashes: dict[tuple[str, str], str] = {}
    copies: dict[str, tuple[str, str]] = {}
    for entry in entries:
        file = entry["arquivo"]
        if not entry["distribuido"]:
            name = file.rstrip("/").rsplit("/", 1)[-1]
            for skill in entry["skills"]:
                present = [p for p in (ROOT / skill).rglob("*") if name and p.name == name]
                if present:
                    raise ValueError(f"Fonte não distribuída presente na skill: {present[0].relative_to(ROOT)}")
                hashes[entry["id"], skill] = "não se aplica"
            continue
        for skill in entry["skills"]:
            path = ROOT / skill / file
            if not path.is_file():
                raise ValueError(f"Fonte ausente: {skill}/{file}")
            if not path.resolve().is_relative_to((ROOT / skill).resolve()):
                raise ValueError(f"Fonte fora da skill: {skill}/{file}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            pinned = PINNED.get(unicodedata.normalize("NFC", file))
            if pinned and digest != pinned:
                raise ValueError(f"Original DOCX alterado: {skill}/{file}; esperado {pinned}, encontrado {digest}")
            if file in copies and copies[file][1] != digest:
                raise ValueError(f"Cópias divergentes: {copies[file][0]}/{file} e {skill}/{file}")
            copies[file] = (skill, digest)
            hashes[entry["id"], skill] = digest
    return hashes


def cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def page(skill: str, entries: list[dict], hashes: dict[tuple[str, str], str]) -> str:
    lookup = {entry["id"]: entry for entry in entries}
    selected = sorted((entry for entry in entries if skill in entry["skills"]), key=lambda entry: entry["id"])
    lines = ["# Fontes metodológicas", "", "Página gerada de `_FONTES/manifest.json` por `_TOOLS/build_sources.py`. Não edite manualmente.", "",
             "A vigência indica o que está confirmado sobre a fonte. Publicação oficial não equivale a adoção institucional; confira as notas.", "",
             "| Fonte | Tipo | Arquivo | Deriva de | Vigência | Titular | Licença | SHA-256 (12 caracteres) | Notas |",
             "|---|---|---|---|---|---|---|---|---|"]
    for entry in selected:
        parent = lookup.get(entry["deriva_de"])
        derives = f"{parent['titulo']} ({parent['id']})" if parent else "não se aplica"
        if entry["distribuido"]:
            link = f"[{cell(entry['arquivo'])}](<../{entry['arquivo']}>)"
        else:
            link = f"[link externo, não incluído]({entry['arquivo']})"
        lines.append("| " + " | ".join([cell(entry["titulo"]), entry["tipo"], link,
                     cell(derives), entry["vigencia"], cell(entry["titular"] or "a confirmar"),
                     cell(entry["licenca"]), hashes[entry["id"], skill][:12], cell(entry["notas"])]) + " |")
    lines += ["", "## Vigência a confirmar", ""]
    pending = [entry for entry in selected if entry["vigencia"] == "desconhecida"]
    lines += [f"- {entry['titulo']} ({entry['id']})." for entry in pending] or ["Nenhuma fonte com vigência desconhecida no manifesto."]
    return "\n".join(lines) + "\n"


def notices(entries: list[dict]) -> str:
    def skills_of(entry: dict) -> str:
        return ", ".join(f"`{skill}`" for skill in entry["skills"])

    third = sorted((e for e in entries if e["titular"] not in (None, "CCEE")
                    and not e["titular"].startswith("CCEE")), key=lambda e: e["id"])
    adapted = sorted((e for e in entries if e["titular"] and e["titular"].startswith("CCEE (")),
                     key=lambda e: e["id"])
    pending = sorted((e for e in entries if e["titular"] is None or e["licenca"].startswith("A confirmar")),
                     key=lambda e: e["id"])
    lines = ["# Avisos de material de terceiros", "",
             "Gerado de `_FONTES/manifest.json` por `_TOOLS/build_sources.py`. Não edite manualmente.", "",
             "A Licença de Uso Restrito CCEE (`LICENSE`) não se aplica aos itens abaixo, que permanecem sob a "
             "titularidade e as licenças indicadas.", "",
             "## Material de terceiros", "",
             "| Fonte | Titular | Licença | Skills | Distribuição |", "|---|---|---|---|---|"]
    for e in third:
        where = (f"arquivo `{e['arquivo']}`" if e["distribuido"]
                 else f"não incluído; referência em {e['arquivo']}")
        lines.append("| " + " | ".join([cell(e["titulo"]), cell(e["titular"]), cell(e["licenca"]),
                     skills_of(e), cell(where)]) + " |")
    lines += ["", "## Adaptações de métodos de terceiros", "",
              "Conteúdo escrito pela CCEE a partir de métodos de terceiros. Os nomes e os modelos originais "
              "pertencem aos respectivos titulares, que não endossam estas adaptações.", "",
              "| Adaptação | Titular | Licença | Skills | Arquivo |", "|---|---|---|---|---|"]
    for e in adapted:
        lines.append("| " + " | ".join([cell(e["titulo"]), cell(e["titular"]), cell(e["licenca"]),
                     skills_of(e), f"`{cell(e['arquivo'])}`"]) + " |")
    lines += ["", "## Fontes tipográficas", "",
              "Distribuídas em `assets/design-system/assets/fonts/` de cada skill, sob a SIL Open Font License 1.1, "
              "cujo texto acompanha as fontes.", ""]
    for family, license_file in FONT_NOTICES:
        path = FONTS_DIR / license_file
        if not path.is_file():
            raise ValueError(f"Licença de fonte ausente: {path.relative_to(ROOT)}")
        copyright_line = path.read_text(encoding="utf-8").splitlines()[0].strip()
        lines.append(f"- **{family}**: {copyright_line}. Licença: SIL Open Font License 1.1 (`{license_file}`).")
    lines += ["", "## Titularidade a confirmar", "",
              "Itens que a Licença de Uso Restrito CCEE não reivindica até que a titularidade seja confirmada.", ""]
    lines += [f"- {cell(e['titulo'])} ({e['id']}): licença {cell(e['licenca'])}; skills {skills_of(e)}."
              for e in pending] or ["Nenhum item pendente."]
    return "\n".join(lines) + "\n"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 também no console do Windows (cp1252)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verifica fontes e páginas sem escrever")
    args = parser.parse_args()
    try:
        entries = load_manifest()
        hashes = validate_sources(entries)
        skills = sorted({skill for entry in entries for skill in entry["skills"]})
        pages = {ROOT / skill / "references/fontes.md": page(skill, entries, hashes) for skill in skills}
        pages[ROOT / "THIRD_PARTY_NOTICES.md"] = notices(entries)
        failures = []
        for path, text in pages.items():
            if args.check:
                if not path.is_file() or path.read_text(encoding="utf-8") != text:
                    failures.append(f"Página ausente ou desatualizada: {path.relative_to(ROOT)}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
                print(f"OK {path.relative_to(ROOT)}")
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"Erro nas fontes: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
