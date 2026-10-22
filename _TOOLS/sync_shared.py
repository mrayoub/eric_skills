#!/usr/bin/env python3
"""Sincroniza fontes compartilhadas e limpa os pacotes das skills."""
from __future__ import annotations

import argparse
import sys
import hashlib
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {"tests", "__pycache__", ".pytest_cache"}
# Skills que só orientam e não renderizam entregáveis: não recebem o design system.
WITHOUT_DESIGN_SYSTEM = {"esteira-eric"}
GALLERY = ROOT / "_GALERIA/gerar.py"


def digest(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


def skills() -> list[Path]:
    return sorted(p for p in ROOT.iterdir() if p.is_dir()
                  and not p.name.startswith("_") and (p / "SKILL.md").is_file())


def source_tree(base: Path) -> tuple[dict[Path, Path], set[Path]]:
    files: dict[Path, Path] = {}
    dirs: set[Path] = set()
    for path in sorted(base.rglob("*")):
        rel = path.relative_to(base)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if path.is_dir():
            if path.name == "templates" and not any(path.iterdir()):
                continue
            dirs.add(rel)
        elif path.name != ".DS_Store" and path.suffix != ".pyc":
            files[rel] = path
    return files, dirs


def actions(skill: Path) -> list[tuple[str, Path, Path | None]]:
    result: list[tuple[str, Path, Path | None]] = []
    base = skill / "assets/design-system"
    files, dirs = source_tree(ROOT / "_DESIGN_SYSTEM")
    if skill.name in WITHOUT_DESIGN_SYSTEM:
        files, dirs = {}, set()
    for rel in sorted(dirs):
        if not (base / rel).exists():
            result.append(("mkdir", base / rel, None))
    for rel, src in files.items():
        dst = base / rel
        if not dst.is_file() or digest(src) != digest(dst):
            result.append(("copy", dst, src))
    removed: list[Path] = []
    for dst in sorted(base.rglob("*"), key=lambda p: (len(p.parts), str(p))):
        if any(parent in removed for parent in dst.parents):
            continue
        rel = dst.relative_to(base)
        if (dst.is_dir() and rel not in dirs) or (not dst.is_dir() and rel not in files):
            result.append(("delete", dst, None))
            removed.append(dst)
    references = [
        (ROOT / "_ERIC_CONTEXT/README.md", "eric-esteira.md", False),
        (ROOT / "_SHARED/grilling-operacional.md", "grilling-operacional.md", False),
        (ROOT / "_SHARED/linguagem-dos-entregaveis.md", "linguagem-dos-entregaveis.md", False),
        (ROOT / "_SHARED/preferencias-do-usuario.md", "preferencias-do-usuario.md", False),
    ]
    for src, name, optional in references:
        dst = skill / "references" / name
        if optional and not dst.exists():
            continue
        if not dst.is_file() or digest(src) != digest(dst):
            result.append(("copy", dst, src))
    # Script de preferências locais do usuário (plano 043): igual em todas as skills.
    prefs_src, prefs_dst = ROOT / "_SHARED/preferencias.py", skill / "scripts/preferencias.py"
    if not prefs_dst.is_file() or digest(prefs_src) != digest(prefs_dst):
        result.append(("copy", prefs_dst, prefs_src))
    updates_src, updates_dst = ROOT / "_DESIGN_SYSTEM/scripts/check_updates.py", skill / "scripts/check_updates.py"
    if not updates_dst.is_file() or digest(updates_src) != digest(updates_dst):
        result.append(("copy", updates_dst, updates_src))
    # Licença e avisos de terceiros acompanham cada skill, que pode ser instalada sem o restante do repositório.
    for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        src, dst = ROOT / name, skill / name
        if not dst.is_file() or digest(src) != digest(dst):
            result.append(("copy", dst, src))
    # Referência incorporada ao grilling no plano 010; remove só a cópia aposentada.
    retired = skill / "references/levantamento-documental-e-grilling.md"
    if retired.exists():
        result.append(("delete", retired, None))
    for dst in sorted(skill.rglob("*"), key=lambda p: (len(p.parts), str(p))):
        if base in dst.parents or dst == base:
            continue
        if any(parent in removed for parent in dst.parents):
            continue
        if dst.name in {"__pycache__", ".DS_Store"}:
            result.append(("delete", dst, None))
            removed.append(dst)
    return result


def refresh_gallery() -> None:
    """Regenera a galeria de templates; uma falha só avisa e não interrompe a sincronização."""
    if not GALLERY.is_file():
        return
    print("Gerando a galeria de templates (_GALERIA)…", flush=True)
    result = subprocess.run([sys.executable, str(GALLERY)], capture_output=True, text=True, encoding="utf-8")
    lines = (result.stdout + result.stderr).strip().splitlines()
    if result.returncode:
        print(f"AVISO: galeria não gerada ({lines[-1] if lines else 'erro'}). A sincronização foi concluída.")
    elif lines:
        print(lines[-1])


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 também no console do Windows (cp1252)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verifica sem escrever")
    mode.add_argument("--dry-run", action="store_true", help="mostra o que faria")
    parser.add_argument("--no-gallery", action="store_true",
                        help="não regenera _GALERIA ao final (ela só é gerada na sincronização que grava)")
    args = parser.parse_args()
    try:
        required = [ROOT / "_DESIGN_SYSTEM", ROOT / "_ERIC_CONTEXT/README.md",
                    ROOT / "_SHARED/grilling-operacional.md",
                    ROOT / "_SHARED/linguagem-dos-entregaveis.md", ROOT / "LICENSE",
                    ROOT / "_SHARED/preferencias.py", ROOT / "_SHARED/preferencias-do-usuario.md",
                    ROOT / "THIRD_PARTY_NOTICES.md"]
        for path in required:
            if not path.exists():
                raise FileNotFoundError(f"Fonte ausente: {path.relative_to(ROOT)}")
        pending = [action for skill in skills() for action in actions(skill)]
        if args.check:
            # Caches locais (__pycache__, .DS_Store) não são versionados nem empacotados: não contam como divergência.
            pending = [action for action in pending if action[1].name not in {"__pycache__", ".DS_Store"}]
        for kind, dst, src in pending:
            rel = dst.relative_to(ROOT)
            if args.check:
                print(f"DIVERGE {rel}")
                continue
            if args.dry_run:
                print(f"{kind.upper()} {rel}")
                continue
            if kind == "mkdir":
                dst.mkdir(parents=True, exist_ok=True)
            elif kind == "copy":
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
            elif dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
            print(f"OK {kind} {rel}")
        if not (args.check or args.dry_run or args.no_gallery):
            refresh_gallery()
        return int(args.check and bool(pending))
    except OSError as exc:
        parser.exit(1, f"Erro na sincronização: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
