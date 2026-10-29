#!/usr/bin/env python3
"""Gera ou verifica os pacotes .skill versionados em _SKILLS_PRONTAS/."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "_SKILLS_PRONTAS"
ALLOWED_FIELDS = {"name", "description", "license", "allowed-tools", "metadata"}
NAME = __import__("re").compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def load_catalog_module():
    spec = importlib.util.spec_from_file_location("build_catalog", ROOT / "_TOOLS/build_catalog.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frontmatter(skill: Path) -> dict:
    import yaml

    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{skill.name}: SKILL.md sem frontmatter")
    return yaml.safe_load(text.split("---\n", 2)[1]) or {}


def validate_skill(skill: Path) -> list[str]:
    data = frontmatter(skill)
    errors = []
    extra = set(data) - ALLOWED_FIELDS
    if extra:
        errors.append(f"{skill.name}: campos não aceitos pelo ChatGPT/Codex: {sorted(extra)}")
    if data.get("name") != skill.name or not NAME.match(str(data.get("name", ""))) or len(skill.name) > 64:
        errors.append(f"{skill.name}: name deve ser igual ao nome da pasta, em minúsculas e hífens")
    description = data.get("description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append(f"{skill.name}: description deve ter de 1 a 1024 caracteres")
    if not data.get("license"):
        errors.append(f"{skill.name}: license ausente")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or not all(isinstance(value, str) for value in metadata.values()):
        errors.append(f"{skill.name}: metadata deve ser um mapa de textos")
    return errors


def run_checks() -> list[str]:
    failures = []
    for script in ("sync_shared.py", "build_sources.py", "build_catalog.py"):
        result = subprocess.run([sys.executable, str(ROOT / "_TOOLS" / script), "--check"],
                                capture_output=True, text=True)
        if result.returncode != 0:
            failures.append(f"{script} --check falhou:\n{(result.stdout + result.stderr).strip()}")
    return failures


def package(skill: Path, files: list[Path], destination: Path | io.BytesIO) -> None:
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(f"{skill.name}/{path.relative_to(skill).as_posix()}", date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


def expected_files(skills: list[Path], catalog) -> dict[str, bytes]:
    expected = {}
    for skill in skills:
        buffer = io.BytesIO()
        package(skill, catalog.distributable_files(skill), buffer)
        expected[f"{skill.name}.skill"] = buffer.getvalue()
    expected["catalog.json"] = (ROOT / "catalog.json").read_bytes()
    sums = [f"{hashlib.sha256(expected[name]).hexdigest()}  {name}"
            for name in sorted(expected) if name.endswith(".skill")]
    sums.append(f"{hashlib.sha256(expected['catalog.json']).hexdigest()}  catalog.json")
    expected["SHA256SUMS"] = ("\n".join(sums) + "\n").encode("utf-8")
    return expected


def differences(expected: dict[str, bytes], directory: Path) -> list[str]:
    actual = {path.name: path for path in directory.iterdir()} if directory.is_dir() else {}
    result = [f"ausente: {name}" for name in sorted(expected.keys() - actual.keys())]
    result.extend(f"extra: {name}" for name in sorted(actual.keys() - expected.keys()))
    result.extend(f"alterado: {name}" for name in sorted(expected.keys() & actual.keys())
                  if not actual[name].is_file() or actual[name].read_bytes() != expected[name])
    return result


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 também no console do Windows (cp1252)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", help="valida a skill indicada e reconstrói o conjunto completo")
    parser.add_argument("--check", action="store_true", help="confere nomes e bytes sem escrever")
    args = parser.parse_args()
    if args.check and args.skill:
        parser.error("--check compara o conjunto completo; não use --skill")
    catalog = load_catalog_module()
    failures = run_checks()
    skills = catalog.skills()
    if args.skill and not any(skill.name == args.skill for skill in skills):
        failures.append(f"skill desconhecida: {args.skill}")
    for skill in skills:
        failures.extend(validate_skill(skill))
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    expected = expected_files(skills, catalog)
    if args.check:
        changed = differences(expected, DIST)
        if changed:
            print("_SKILLS_PRONTAS divergente; rode python3 _TOOLS/build_dist.py:\n" + "\n".join(changed), file=sys.stderr)
            return 1
        print(f"OK _SKILLS_PRONTAS: {len(expected)} arquivos idênticos às fontes")
        return 0
    DIST.mkdir(exist_ok=True)
    for path in DIST.iterdir():
        if path.name not in expected:
            if not path.is_file():
                print(f"entrada extra não é arquivo: {path}", file=sys.stderr)
                return 1
            path.unlink()
    for name, data in expected.items():
        (DIST / name).write_bytes(data)
        print(f"OK {DIST / name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
