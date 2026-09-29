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
          "versao_declarada", "data_importacao", "deriva_de", "vigencia", "notas"}
TYPES = {"original", "transcricao", "adaptacao", "historico", "rubrica", "script"}
STATUS = {"confirmada", "historica", "desconhecida"}
PINNED = {
    "assets/Modelo 4D de Aprofundamento.docx": "d5071f2ab0d62e153b8f0bb7e89108a10bca6980d807dbd43c90bbd80fd115e3",
    "assets/Modelo 3E Estruturação da Solução.docx": "530cc4691c6cf5b5f093ba972b05d08649b4000a1fd077ee6020c94b00637e34",
    "assets/Playbook_Modelo_5C_Centralidade_Cliente.docx": "3b793187dccd6691e124e61b9a407e6f383513d55de255c1049deae31df4e3c7",
}


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
        if not relative_path(entry["arquivo"]):
            raise ValueError(f"{label}: arquivo deve ser caminho relativo dentro da skill")
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
    hashes: dict[tuple[str, str], str] = {}
    copies: dict[str, tuple[str, str]] = {}
    for entry in entries:
        file = entry["arquivo"]
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
             "| Fonte | Tipo | Arquivo | Deriva de | Vigência | SHA-256 (12 caracteres) | Notas |",
             "|---|---|---|---|---|---|---|"]
    for entry in selected:
        parent = lookup.get(entry["deriva_de"])
        derives = f"{parent['titulo']} ({parent['id']})" if parent else "—"
        link = f"[{cell(entry['arquivo'])}](<../{entry['arquivo']}>)"
        lines.append("| " + " | ".join([cell(entry["titulo"]), entry["tipo"], link,
                     cell(derives), entry["vigencia"], hashes[entry["id"], skill][:12], cell(entry["notas"])]) + " |")
    lines += ["", "## Vigência a confirmar", ""]
    pending = [entry for entry in selected if entry["vigencia"] == "desconhecida"]
    lines += [f"- {entry['titulo']} ({entry['id']})." for entry in pending] or ["Nenhuma fonte com vigência desconhecida no manifesto."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verifica fontes e páginas sem escrever")
    args = parser.parse_args()
    try:
        entries = load_manifest()
        hashes = validate_sources(entries)
        skills = sorted({skill for entry in entries for skill in entry["skills"]})
        pages = {ROOT / skill / "references/fontes.md": page(skill, entries, hashes) for skill in skills}
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
