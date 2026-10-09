#!/usr/bin/env python3
"""Compara as skills GEIN-CCEE instaladas com o catálogo publicado e avisa o que tem versão nova.

Só lê: nunca altera arquivos. Sem rede ou sem acesso ao catálogo, explica e sai com 0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

CATALOG_URL = "https://raw.githubusercontent.com/mrayoub/eric_skills/main/catalog.json"
CACHE = Path.home() / ".cache" / "eric-skills" / "catalog.json"
CACHE_SECONDS = 24 * 3600
VERSION_LINE = re.compile(r'^  version: "(\d+)\.(\d+)\.(\d+)"$', re.M)
AUTHOR = re.compile(r'^  author: "GEIN-CCEE"$', re.M)
EXCLUDED_DIRS = {"__pycache__", "node_modules"}
EXCLUDED_FILES = {".DS_Store"}
TOKEN_HOSTS = {"raw.githubusercontent.com", "api.github.com"}


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old = urllib.parse.urlsplit(req.full_url)
        new = urllib.parse.urlsplit(newurl)
        if new.scheme != "https":
            raise ValueError("redirecionamento do catálogo para URL sem HTTPS recusado")
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None and new.hostname != old.hostname:
            redirected.remove_header("Authorization")
        return redirected


# Mesma regra de _TOOLS/build_catalog.py (este script é distribuído sem _TOOLS).
def distributable_files(skill_dir: Path) -> list[Path]:
    files = []
    # Ordena pelas partes do caminho, com maiúsculas distintas: o Windows compara caminhos sem diferenciar
    # maiúsculas, o que mudaria a ordem e o hash. Assim a ordem é a mesma em qualquer sistema.
    for path in sorted(skill_dir.rglob("*"), key=lambda item: item.relative_to(skill_dir).parts):
        rel = path.relative_to(skill_dir)
        if not path.is_file() or path.name in EXCLUDED_FILES or path.suffix == ".pyc":
            continue
        if any(part in EXCLUDED_DIRS for part in rel.parts) or rel.parts[0] == "evals":
            continue
        files.append(path)
    return files


def skill_hash(skill_dir: Path) -> str:
    lines = []
    for path in distributable_files(skill_dir):
        data = path.read_bytes()
        if path == skill_dir / "SKILL.md":
            data = VERSION_LINE.sub("  version: \"\"", data.decode("utf-8")).encode("utf-8")
        lines.append(f"{path.relative_to(skill_dir).as_posix()} {hashlib.sha256(data).hexdigest()}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def installed(paths: list[Path]) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for base in paths:
        for skill in sorted(p.resolve() for p in base.iterdir() if (p / "SKILL.md").is_file()):
            try:
                text = (skill / "SKILL.md").read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if AUTHOR.search(text) and VERSION_LINE.search(text):
                found.setdefault(skill.name, skill)
    return found


def load_catalog(source: str, refresh: bool) -> dict:
    if source.startswith("http://"):
        raise ValueError("catálogo remoto exige HTTPS")
    if not source.startswith("https://"):
        return json.loads(Path(source).read_text(encoding="utf-8"))
    if source == CATALOG_URL and not refresh and CACHE.is_file() and time.time() - CACHE.stat().st_mtime < CACHE_SECONDS:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    request = urllib.request.Request(source, headers={"User-Agent": "eric-skills-check"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    host = urllib.parse.urlsplit(source).hostname
    if token and host in TOKEN_HOSTS:
        request.add_header("Authorization", f"Bearer {token}")
    opener = urllib.request.build_opener(SafeRedirectHandler())
    with opener.open(request, timeout=5) as response:
        data = response.read()
    catalog = json.loads(data)
    if source == CATALOG_URL:
        try:
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_bytes(data)
        except OSError:
            pass
    return catalog


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 também no console do Windows (cp1252)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", action="append", type=Path, default=[],
                        help="pasta com skills instaladas (pode repetir); padrão: a pasta desta skill")
    parser.add_argument("--catalog", default=CATALOG_URL, help="URL ou arquivo do catálogo")
    parser.add_argument("--refresh", action="store_true", help="ignora o cache de 24 h")
    parser.add_argument("--strict", action="store_true", help="sai com 1 se houver atualização")
    args = parser.parse_args()
    here = Path(__file__).resolve()
    if here.parent.name == "scripts" and (here.parent.parent / "SKILL.md").is_file():
        default_path = here.parent.parent.parent
    else:
        default_path = here.parents[4] if len(here.parents) > 4 else Path.cwd()
    paths = args.path or [default_path]
    skills = installed([path for path in paths if path.is_dir()])
    if not skills:
        print("Nenhuma skill GEIN-CCEE encontrada nas pastas informadas.")
        return 0
    try:
        catalog = load_catalog(args.catalog, args.refresh)["skills"]
    except Exception as exc:  # rede, 404 de repositório privado sem token, JSON inválido
        print(f"Não foi possível ler o catálogo ({type(exc).__name__}: {exc}). "
              "Sem acesso ao repositório, defina GITHUB_TOKEN ou consulte quem mantém as skills.")
        return 0
    outdated = 0
    for name, skill in sorted(skills.items()):
        try:
            local = ".".join(VERSION_LINE.search((skill / "SKILL.md").read_text(encoding="utf-8")).groups())
            entry = catalog.get(name)
            if entry is None:
                print(f"{name}: instalada {local}; fora do catálogo")
            elif as_tuple(entry["version"]) > as_tuple(local):
                outdated += 1
                print(f"{name}: instalada {local}; disponível {entry['version']}")
            elif entry["version"] == local and entry["sha256"] != skill_hash(skill):
                print(f"{name}: {local} alterada localmente (difere da versão publicada)")
            else:
                print(f"{name}: atualizada ({local})")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"{name}: não foi possível ler esta skill ({type(exc).__name__}); ignorada")
    if outdated:
        print("Para atualizar: `npx skills update` (instalação por npx) ou baixe os .skill na página de Releases.")
    return 1 if outdated and args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
