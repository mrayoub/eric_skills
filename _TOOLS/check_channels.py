#!/usr/bin/env python3
"""Confere se os três canais de update (npx skills, .skill e clone) entregam as mesmas skills e versões."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(<?([^)>\s]+)>?\)")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def npx_names(root: Path) -> list[str]:
    """Skills que o `npx skills` descobre no repositório."""
    if not shutil.which("npx"):
        raise RuntimeError("npx não encontrado; instale o Node.js ou rode com --sem-npx")
    result = subprocess.run(["npx", "-y", "skills", "add", str(root), "--list"], capture_output=True, text=True,
                            encoding="utf-8", timeout=300)
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", result.stdout + result.stderr)
    return sorted(set(re.findall(r"^│ {4}([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", text, re.M)))


def check_npx(root: Path, catalog: dict) -> list[str]:
    found, expected = npx_names(root), sorted(catalog["skills"])
    if found != expected:
        return [f"npx: descobre {found}, catálogo tem {expected}"]
    return []


def check_parity(skill: Path, tracked: list[str], distributable: list[Path]) -> list[str]:
    """O que vai no .skill é exatamente o que o git (npx e clone) entrega."""
    packaged = sorted(path.relative_to(skill).as_posix() for path in distributable)
    if packaged != sorted(tracked):
        extra = sorted(set(packaged) - set(tracked))
        missing = sorted(set(tracked) - set(packaged))
        return [f"{skill.name}: pacote difere do git (fora do git: {extra[:5]}; fora do pacote: {missing[:5]})"]
    return []


def check_links(skill: Path) -> list[str]:
    """Cada skill funciona sozinha: links relativos resolvem dentro da pasta dela."""
    problems = []
    base = skill.resolve()
    for md in sorted(skill.rglob("*.md")):
        if "design-system" in md.relative_to(skill).parts:
            continue
        for match in LINK.finditer(md.read_text(encoding="utf-8")):
            target = match.group(1).split("#")[0]
            if not target or re.match(r"^[a-z]+:", target):
                continue
            resolved = (md.parent / target).resolve()
            if base not in [resolved, *resolved.parents]:
                problems.append(f"{md.relative_to(skill.parent)}: link para fora da skill ({target})")
            elif not resolved.exists():
                problems.append(f"{md.relative_to(skill.parent)}: link quebrado ({target})")
    return problems


def check_reproducible(dist, catalog_module, skills: list[Path]) -> list[str]:
    problems = []
    with tempfile.TemporaryDirectory() as temp:
        for skill in skills:
            files = catalog_module.distributable_files(skill)
            digests = []
            for name in ("a", "b"):
                path = Path(temp) / f"{skill.name}-{name}.skill"
                dist.package(skill, files, path)
                digests.append(hashlib.sha256(path.read_bytes()).hexdigest())
            if digests[0] != digests[1]:
                problems.append(f"{skill.name}: pacote não reprodutível")
    return problems


def check_updates_report(root: Path, catalog: dict) -> list[str]:
    result = subprocess.run([sys.executable, str(root / "_DESIGN_SYSTEM/scripts/check_updates.py"),
                             "--catalog", str(root / "catalog.json"), "--path", str(root)],
                            capture_output=True, text=True, encoding="utf-8")
    lines = [line for line in result.stdout.splitlines() if ": " in line]
    updated = [line for line in lines if ": atualizada (" in line]
    if result.returncode != 0 or len(updated) != len(catalog["skills"]):
        return [f"check_updates: {len(updated)} de {len(catalog['skills'])} skills atualizadas:\n" + result.stdout]
    return []


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 também no console do Windows (cp1252)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sem-npx", action="store_true", help="pula a descoberta pelo npx (sem Node.js)")
    args = parser.parse_args()
    catalog_module = load("build_catalog", ROOT / "_TOOLS/build_catalog.py")
    dist = load("build_dist", ROOT / "_TOOLS/build_dist.py")
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    skills = catalog_module.skills()
    problems: list[str] = []
    try:
        if not args.sem_npx:
            problems += check_npx(ROOT, catalog)
        for skill in skills:
            tracked = subprocess.run(["git", "ls-files", "--", skill.name], cwd=ROOT, capture_output=True,
                                     text=True, encoding="utf-8", check=True).stdout.splitlines()
            tracked = [line.split("/", 1)[1] for line in tracked]
            problems += check_parity(skill, tracked, catalog_module.distributable_files(skill))
            problems += check_links(skill)
        problems += check_reproducible(dist, catalog_module, skills)
        problems += check_updates_report(ROOT, catalog)
    except (RuntimeError, subprocess.SubprocessError, OSError) as exc:
        problems.append(f"falha ao verificar: {exc}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"OK canais: {len(skills)} skills iguais em npx, .skill e clone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
