#!/usr/bin/env python3
"""Preferências locais do usuário para as skills ERIC.

Guarda, fora das pastas das skills, ajustes de comportamento pedidos pelo usuário. Nada é enviado para fora da
máquina. Níveis: usuário (~/.config/eric-skills/, ou ERIC_SKILLS_CONFIG) e projeto (<projeto>/.eric/preferencias/).
Em cada nível há um arquivo por skill (<skill>.md) e um comum (todas.md).

Prioridade na leitura, da mais forte para a mais fraca: projeto/skill, projeto/todas, usuário/skill, usuário/todas.
As regras do método e do design system sempre prevalecem sobre qualquer preferência.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

COMMON = "todas"
ENTRY = re.compile(r"^- \[(P\d+)\] (\d{4}-\d{2}-\d{2}) · v(\d+\.\d+\.\d+) · (.+)$")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HEADER = ("# Preferências — {name} ({level})\n\n"
          "Arquivo das skills ERIC, guardado só nesta máquina. Pode ser editado à mão. "
          "Não registre dados pessoais nem conteúdo de projeto: descreva apenas o comportamento desejado.\n\n")


def user_dir() -> Path:
    raw = Path(os.environ.get("ERIC_SKILLS_CONFIG") or Path.home() / ".config" / "eric-skills").expanduser()
    return raw.parent.resolve() / raw.name


def project_dir(project: str) -> Path:
    raw = Path(project).expanduser().absolute()
    return raw.parent.resolve() / raw.name / ".eric" / "preferencias"


def guard(folder: Path) -> Path:
    """Nunca grava dentro de uma pasta de skill: o update apagaria o arquivo."""
    for parent in [folder, *folder.parents]:
        if parent.is_symlink():
            raise ValueError(f"link simbólico recusado: {parent}")
    folder = folder.resolve()
    for parent in [folder, *folder.parents]:
        if (parent / "SKILL.md").is_file():
            raise ValueError(f"pasta de preferências dentro de uma skill ({parent}); use uma pasta fora das skills")
    return folder


def safe_file(path: Path) -> Path:
    guard(path.parent)
    if path.is_symlink():
        raise ValueError(f"link simbólico recusado: {path}")
    return path


def accepted_path() -> Path:
    return user_dir() / "projetos-aceitos.json"


def accepted_hashes() -> dict[str, str]:
    path = safe_file(accepted_path())
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise ValueError(f"registro de confirmações inválido: {path}")
    return data


def file_hash(path: Path) -> str:
    return hashlib.sha256(safe_file(path).read_bytes()).hexdigest()


def atomic_write(path: Path, content: str) -> None:
    safe_file(path)
    guard(path.parent).mkdir(parents=True, exist_ok=True)
    safe_file(path)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=path.parent,
                                         prefix=f".{path.name}.", delete=False) as handle:
            temp_name = handle.name
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        safe_file(path)
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def read_entries(path: Path) -> list[tuple[str, str, str, str]]:
    safe_file(path)
    if not path.is_file():
        return []
    return [match.groups() for line in path.read_text(encoding="utf-8").splitlines() if (match := ENTRY.match(line))]


def write_entries(path: Path, name: str, level: str, entries: list[tuple[str, str, str, str]]) -> None:
    lines = [f"- [{pid}] {date} · v{version} · {text}" for pid, date, version, text in entries]
    atomic_write(path, HEADER.format(name=name, level=level) + "\n".join(lines) + ("\n" if lines else ""))


def sources(skill: str, project: str | None) -> list[tuple[str, Path]]:
    result = []
    if project:
        result += [("projeto · esta skill", project_dir(project) / f"{skill}.md"),
                   ("projeto · todas as skills", project_dir(project) / f"{COMMON}.md")]
    result += [("usuário · esta skill", user_dir() / f"{skill}.md"),
               ("usuário · todas as skills", user_dir() / f"{COMMON}.md")]
    return result


def target(skill: str, everyone: bool, project: str | None) -> tuple[Path, str, str]:
    folder = guard(project_dir(project) if project else user_dir())
    name = COMMON if everyone else skill
    return folder / f"{name}.md", ("todas as skills" if everyone else skill), ("projeto" if project else "usuário")


def check_name(skill: str) -> str:
    if not NAME.match(skill) or skill == COMMON:
        raise ValueError(f"nome de skill inválido: {skill!r}")
    return skill


def command_ler(args: argparse.Namespace) -> int:
    found = False
    accepted = accepted_hashes() if args.projeto else {}
    for label, path in sources(check_name(args.skill), args.projeto):
        entries = read_entries(path)
        if not entries:
            continue
        found = True
        project_source = label.startswith("projeto")
        confirmed = not project_source or accepted.get(str(path.resolve())) == file_hash(path)
        state = "CONFIRMADA" if confirmed else "NÃO CONFIRMADA — mostre ao usuário; não aplique antes de confirmar"
        print(f"## {label} ({path}) [{state}]")
        for pid, date, version, text in entries:
            note = ""
            if args.versao_atual and as_tuple(args.versao_atual) > as_tuple(version):
                note = f" [criada na v{version}; a skill está na v{args.versao_atual}: confirme se ainda vale]"
            print(f"- [{pid}] {text}{note}")
    if not found:
        print("Nenhuma preferência registrada: use o comportamento padrão da skill.")
    return 0


def command_adicionar(args: argparse.Namespace) -> int:
    skill = check_name(args.skill)
    text = " ".join(args.texto.split())
    if not text:
        raise ValueError("texto da preferência vazio")
    path, name, level = target(skill, args.todas, args.projeto)
    entries = read_entries(path)
    number = max((int(pid[1:]) for pid, *_ in entries), default=0) + 1
    entries.append((f"P{number:02d}", datetime.date.today().isoformat(), args.versao, text))
    write_entries(path, name, level, entries)
    print(f"Preferência P{number:02d} gravada para {name} ({level}) em {path}")
    return 0


def command_remover(args: argparse.Namespace) -> int:
    path, name, level = target(check_name(args.skill), args.todas, args.projeto)
    entries = read_entries(path)
    kept = [entry for entry in entries if entry[0] != args.id]
    if len(kept) == len(entries):
        raise ValueError(f"{args.id} não existe em {path}")
    write_entries(path, name, level, kept)
    print(f"Preferência {args.id} removida de {path}")
    return 0


def command_resetar(args: argparse.Namespace) -> int:
    folder = guard(project_dir(args.projeto) if args.projeto else user_dir())
    if args.todas_as_skills:
        paths = sorted(folder.glob("*.md"))
    else:
        paths = [folder / f"{check_name(args.skill)}.md"]
    reset = 0
    for path in paths:
        safe_file(path)
        if path.is_file():
            backup = safe_file(path.with_suffix(".md.bak"))
            path.replace(backup)
            reset += 1
            print(f"Padrão de fábrica restaurado: {path.name} (cópia em {path.name}.bak)")
    if not reset:
        print("Nada a resetar: não havia preferências nesse nível.")
    return 0


def command_listar(args: argparse.Namespace) -> int:
    levels = [("usuário", user_dir())] + ([("projeto", project_dir(args.projeto))] if args.projeto else [])
    for level, folder in levels:
        files = sorted(folder.glob("*.md")) if folder.is_dir() else []
        print(f"## {level} ({folder}): {len(files)} arquivo(s)")
        for path in files:
            print(f"- {path.stem}: {len(read_entries(path))} preferência(s)")
    return 0


def command_confirmar(args: argparse.Namespace) -> int:
    folder = guard(project_dir(args.projeto))
    files = sorted(folder.glob("*.md")) if folder.is_dir() else []
    if not files:
        raise ValueError(f"nenhuma preferência de projeto em {folder}")
    accepted = accepted_hashes()
    for path in files:
        safe_file(path)
        accepted[str(path.resolve())] = file_hash(path)
    atomic_write(accepted_path(), json.dumps(accepted, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(f"Confirmadas {len(files)} preferência(s) de projeto em {folder}")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="comando", required=True)
    ler = sub.add_parser("ler", help="mostra as preferências que valem para a skill")
    ler.add_argument("skill")
    ler.add_argument("--versao-atual", help="versão da skill, para avisar preferências antigas")
    add = sub.add_parser("adicionar", help="grava uma preferência confirmada pelo usuário")
    add.add_argument("skill")
    add.add_argument("texto")
    add.add_argument("--versao", required=True, help="versão da skill em que a preferência foi criada")
    add.add_argument("--todas", action="store_true", help="vale para todas as skills (todas.md)")
    rem = sub.add_parser("remover", help="remove uma preferência pelo ID")
    rem.add_argument("skill")
    rem.add_argument("id")
    rem.add_argument("--todas", action="store_true")
    res = sub.add_parser("resetar", help="volta ao padrão de fábrica, guardando .bak")
    res.add_argument("skill", nargs="?")
    res.add_argument("--todas-as-skills", action="store_true", help="reseta todos os arquivos do nível")
    sub.add_parser("listar", help="lista os arquivos de preferências")
    confirm = sub.add_parser("confirmar", help="registra a confirmação das preferências do projeto pelo usuário")
    confirm.add_argument("--projeto", required=True, help="pasta do projeto confirmada pelo usuário")
    for command in (ler, add, rem, res, sub.choices["listar"]):
        command.add_argument("--projeto", help="pasta do projeto (usa <projeto>/.eric/preferencias/)")
    args = parser.parse_args()
    if args.comando == "resetar" and not args.skill and not args.todas_as_skills:
        parser.error("informe a skill ou --todas-as-skills")
    try:
        return {"ler": command_ler, "adicionar": command_adicionar, "remover": command_remover,
                "resetar": command_resetar, "listar": command_listar,
                "confirmar": command_confirmar}[args.comando](args)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"Erro nas preferências: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
