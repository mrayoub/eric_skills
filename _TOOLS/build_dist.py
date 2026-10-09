#!/usr/bin/env python3
"""Gera os pacotes .skill em _DIST/ com o mesmo conteúdo que o npx skills instala."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "_DIST"
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


def package(skill: Path, files: list[Path], destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(f"{skill.name}/{path.relative_to(skill).as_posix()}", date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", help="empacota só esta skill")
    args = parser.parse_args()
    catalog = load_catalog_module()
    failures = run_checks()
    selected = [skill for skill in catalog.skills() if not args.skill or skill.name == args.skill]
    if args.skill and not selected:
        failures.append(f"skill desconhecida: {args.skill}")
    for skill in selected:
        failures.extend(validate_skill(skill))
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    DIST.mkdir(exist_ok=True)
    for skill in selected:
        destination = DIST / f"{skill.name}.skill"
        package(skill, catalog.distributable_files(skill), destination)
        print(f"OK {destination.relative_to(ROOT)}")
    shutil.copyfile(ROOT / "catalog.json", DIST / "catalog.json")
    sums = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
            for path in sorted(DIST.glob("*.skill")) + [DIST / "catalog.json"]]
    (DIST / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
