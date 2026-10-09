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
    result = subprocess.run(list(args), cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode:
        raise RuntimeError(f"{' '.join(args)} falhou ({result.returncode}): {result.stderr.strip() or result.stdout.strip()}")
    return result


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def existing_tags() -> set[str]:
    output = run("git", "ls-remote", "--tags", "origin").stdout
    return {line.split("refs/tags/", 1)[1].removesuffix("^{}")
            for line in output.splitlines() if "refs/tags/" in line}


def release_notes(skill: str, version: str, tags: set[str]) -> str:
    previous = sorted((tag for tag in tags if tag.startswith(f"{skill}-v")),
                      key=lambda tag: as_tuple(tag.rsplit("-v", 1)[1]))
    if not previous:
        return f"Primeira versão publicada de `{skill}` ({version})."
    if run("git", "rev-parse", "--verify", previous[-1], check=False).returncode:
        return f"Mudanças em `{skill}` desde {previous[-1]}; consulte o histórico do repositório."
    log = run("git", "log", "--format=- %s", f"{previous[-1]}..HEAD", "--", skill).stdout.strip()
    return f"Mudanças em `{skill}` desde {previous[-1]}:\n\n{log or '- (ajustes compartilhados do design system)'}"


def plan(catalog: dict, tags: set[str]) -> list[tuple[str, str]]:
    return [(skill, entry["version"]) for skill, entry in sorted(catalog["skills"].items())
            if f"{skill}-v{entry['version']}" not in tags]


def rolling_assets() -> set[str] | None:
    result = run("gh", "release", "view", ROLLING, "--json", "assets", check=False)
    if result.returncode:
        if "release not found" in result.stderr.lower() or "http 404" in result.stderr.lower():
            return None
        raise RuntimeError(f"gh release view {ROLLING} falhou: {result.stderr.strip()}")
    return {asset["name"] for asset in json.loads(result.stdout)["assets"]}


def publish_rolling(catalog: dict, files: list[Path], head: str) -> None:
    current = rolling_assets()
    notes = (f"Os {len(catalog['skills'])} pacotes .skill da versão mais recente, "
             "catalog.json e SHA256SUMS.")
    if current is None:
        run("gh", "release", "create", ROLLING, "--target", head,
            "--title", "Pacotes atuais das skills", "--notes", notes, "--latest")
    else:
        for stale in sorted(current - {path.name for path in files}):
            run("gh", "release", "delete-asset", ROLLING, stale, "--yes")
        run("gh", "release", "edit", ROLLING, "--target", head, "--notes", notes, "--latest")
    run("gh", "release", "upload", ROLLING, *(str(path) for path in files), "--clobber")
    if current is not None:
        run("gh", "api", "-X", "PATCH", f"repos/{{owner}}/{{repo}}/git/refs/tags/{ROLLING}",
            "-f", f"sha={head}", "-F", "force=true")
    remote_tag = run("git", "ls-remote", "--tags", "origin", f"refs/tags/{ROLLING}").stdout.split()
    if not remote_tag or remote_tag[0] != head:
        raise RuntimeError(f"tag remota {ROLLING} não aponta para {head}")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 também no console do Windows (cp1252)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="só mostra as tags e Releases que criaria")
    args = parser.parse_args()
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    try:
        tags = existing_tags()
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    pending = plan(catalog, tags)
    files = [DIST / f"{skill}.skill" for skill in sorted(catalog["skills"])] + [DIST / "catalog.json", DIST / "SHA256SUMS"]
    if args.dry_run:
        for skill, version in pending:
            print(f"criaria {skill}-v{version} com {skill}.skill")
        print(f"atualizaria a Release '{ROLLING}' com {len(files)} arquivos")
        return 0
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        print("pacotes ausentes; rode build_dist.py antes: " + ", ".join(missing), file=sys.stderr)
        return 1
    try:
        head = run("git", "rev-parse", "HEAD").stdout.strip()
        for skill, version in pending:
            tag = f"{skill}-v{version}"
            notes = release_notes(skill, version, tags)
            run("gh", "release", "create", tag, str(DIST / f"{skill}.skill"), "--target", head,
                "--title", f"{skill} {version}", "--notes", notes, "--latest=false")
            print(f"OK {tag}")
        publish_rolling(catalog, files, head)
    except (RuntimeError, ValueError, KeyError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"OK Release '{ROLLING}' atualizada ({len(files)} arquivos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
