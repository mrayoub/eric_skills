#!/usr/bin/env python3
"""Mantém catalog.json com a versão e o hash do conteúdo distribuível de cada skill."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
REPOSITORY = "mrayoub/eric_skills"
EXCLUDED_DIRS = {"__pycache__", "node_modules"}
EXCLUDED_FILES = {".DS_Store"}
VERSION_LINE = re.compile(r'^  version: "(\d+)\.(\d+)\.(\d+)"$', re.M)


def skills() -> list[Path]:
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith("_")
                  and not p.name.startswith(".") and (p / "SKILL.md").is_file())


def distributable_files(skill_dir: Path) -> list[Path]:
    """Arquivos que vão para o pacote e para o hash: a mesma regra no catálogo e no .skill."""
    files = []
    for path in sorted(skill_dir.rglob("*")):
        rel = path.relative_to(skill_dir)
        if not path.is_file() or path.name in EXCLUDED_FILES or path.suffix == ".pyc":
            continue
        if any(part in EXCLUDED_DIRS for part in rel.parts) or rel.parts[0] == "evals":
            continue
        files.append(path)
    return files


def read_version(skill_dir: Path) -> str:
    match = VERSION_LINE.search((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{skill_dir.name}: SKILL.md sem metadata.version no formato \"X.Y.Z\"")
    return ".".join(match.groups())


def skill_hash(skill_dir: Path) -> str:
    lines = []
    for path in distributable_files(skill_dir):
        data = path.read_bytes()
        if path == skill_dir / "SKILL.md":
            # A linha da versão não entra no hash: subir a versão não muda o conteúdo.
            data = VERSION_LINE.sub("  version: \"\"", data.decode("utf-8")).encode("utf-8")
        lines.append(f"{path.relative_to(skill_dir).as_posix()} {hashlib.sha256(data).hexdigest()}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def build() -> dict:
    return {"schema_version": "1.0.0", "repository": REPOSITORY,
            "skills": {skill.name: {"version": read_version(skill), "sha256": skill_hash(skill),
                                    "files": len(distributable_files(skill))} for skill in skills()}}


def dump(catalog: dict) -> str:
    return json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def problems(current: dict, previous: dict | None, *, check: bool = False) -> list[str]:
    result = []
    published = (previous or {}).get("skills", {})
    for name, entry in current["skills"].items():
        old = published.get(name)
        if old is None:
            # Skill nova: a escrita a registra; só a verificação acusa que o catálogo não a conhece.
            if check and previous is not None:
                result.append(f"{name}: ausente do catálogo; rode python _TOOLS/build_catalog.py")
            continue
        if as_tuple(entry["version"]) < as_tuple(old["version"]):
            result.append(f"{name}: versão menor que a publicada ({entry['version']} < {old['version']})")
        elif entry["sha256"] != old["sha256"] and entry["version"] == old["version"]:
            result.append(f"{name}: conteúdo mudou sem subir a versão ({entry['version']})")
    return result


def bump(level: str, previous: dict) -> list[str]:
    changed = []
    published = previous.get("skills", {})
    for skill in skills():
        old = published.get(skill.name)
        if old is None or skill_hash(skill) == old["sha256"]:
            continue
        major, minor, patch = as_tuple(read_version(skill))
        if as_tuple(read_version(skill)) > as_tuple(old["version"]):
            continue  # já subiu à mão
        major, minor, patch = {"major": (major + 1, 0, 0), "minor": (major, minor + 1, 0),
                               "patch": (major, minor, patch + 1)}[level]
        path = skill / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(VERSION_LINE.sub(f'  version: "{major}.{minor}.{patch}"', text, count=1), encoding="utf-8")
        changed.append(f"{skill.name}: {old['version']} → {major}.{minor}.{patch}")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verifica sem escrever")
    mode.add_argument("--bump", nargs="?", const="patch", choices=("patch", "minor", "major"),
                      help="sobe a versão das skills cujo conteúdo mudou (padrão: patch)")
    args = parser.parse_args()
    try:
        previous = json.loads(CATALOG.read_text(encoding="utf-8")) if CATALOG.is_file() else None
        if args.bump:
            if previous is None:
                raise ValueError("catalog.json ausente; gere o catálogo antes de usar --bump")
            for line in bump(args.bump, previous):
                print(f"OK versão {line}")
        current = build()
        issues = problems(current, previous, check=args.check)
        if args.check:
            if previous is None:
                issues.append("catalog.json ausente")
            elif not issues and dump(current) != CATALOG.read_text(encoding="utf-8"):
                issues.append("catalog.json desatualizado")
            if issues:
                print("\n".join(issues), file=sys.stderr)
                return 1
            return 0
        if issues:
            print("\n".join(issues), file=sys.stderr)
            print("Suba a versão com --bump ou corrija o conteúdo.", file=sys.stderr)
            return 1
        CATALOG.write_text(dump(current), encoding="utf-8")
        print(f"OK catalog.json ({len(current['skills'])} skills)")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Erro no catálogo: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
