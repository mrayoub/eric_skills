#!/usr/bin/env python3
"""Publica o canal .skill: uma Release por versão nova de skill e a Release fixa `pacotes` com tudo.

Usa o `gh` (GitHub CLI). Com --dry-run, só mostra o que faria. Pressupõe `_DIST/` gerado por build_dist.py.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "_DIST"
ROLLING = "pacotes"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(list(args), cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=check)


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def existing_tags() -> set[str]:
    return set(run("git", "tag", "--list").stdout.split())


def release_notes(skill: str, version: str, tags: set[str]) -> str:
    previous = sorted((tag for tag in tags if tag.startswith(f"{skill}-v")),
                      key=lambda tag: as_tuple(tag.rsplit("-v", 1)[1]))
    if not previous:
        return f"Primeira versão publicada de `{skill}` ({version})."
    log = run("git", "log", "--format=- %s", f"{previous[-1]}..HEAD", "--", skill).stdout.strip()
    return f"Mudanças em `{skill}` desde {previous[-1]}:\n\n{log or '- (ajustes compartilhados do design system)'}"


def plan(catalog: dict, tags: set[str]) -> list[tuple[str, str]]:
    return [(skill, entry["version"]) for skill, entry in sorted(catalog["skills"].items())
            if f"{skill}-v{entry['version']}" not in tags]


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 também no console do Windows (cp1252)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="só mostra as tags e Releases que criaria")
    args = parser.parse_args()
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    tags = existing_tags()
    pending = plan(catalog, tags)
    for skill, version in pending:
        tag = f"{skill}-v{version}"
        package = DIST / f"{skill}.skill"
        if args.dry_run:
            print(f"criaria {tag} com {package.name}")
            continue
        if not package.is_file():
            print(f"pacote ausente: {package}; rode build_dist.py antes", file=sys.stderr)
            return 1
        notes = release_notes(skill, version, tags)
        run("gh", "release", "create", tag, str(package), "--target", run("git", "rev-parse", "HEAD").stdout.strip(),
            "--title", f"{skill} {version}", "--notes", notes, "--latest=false")
        print(f"OK {tag}")
    files = sorted(str(path) for path in DIST.glob("*.skill")) + [str(DIST / "catalog.json"), str(DIST / "SHA256SUMS")]
    if args.dry_run:
        print(f"atualizaria a Release '{ROLLING}' com {len(files)} arquivos")
        return 0
    if run("gh", "release", "view", ROLLING, check=False).returncode != 0:
        run("gh", "release", "create", ROLLING, "--title", "Pacotes atuais das skills",
            "--notes", "Os 13 pacotes .skill da versão mais recente, catalog.json e SHA256SUMS.", "--latest")
    run("gh", "release", "upload", ROLLING, *files, "--clobber")
    print(f"OK Release '{ROLLING}' atualizada ({len(files)} arquivos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
