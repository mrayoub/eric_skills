#!/usr/bin/env python3
"""Confere se a proteção remota de main corresponde à política versionada."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".github/main-protection.json"
ENDPOINT = "repos/mrayoub/eric_skills/branches/main/protection"


def problems(actual: dict, policy: dict) -> list[str]:
    errors = []
    checks = actual.get("required_status_checks") or {}
    wanted = policy["required_status_checks"]
    if checks.get("strict") is not wanted["strict"]:
        errors.append("checks devem exigir branch atualizado")
    if sorted(checks.get("contexts") or []) != sorted(wanted["contexts"]):
        errors.append("checks obrigatórios diferem de versionamento e testes")
    reviews = actual.get("required_pull_request_reviews")
    if reviews is None:
        errors.append("pull request não obrigatório")
    elif reviews.get("required_approving_review_count") != policy["required_pull_request_reviews"]["required_approving_review_count"]:
        errors.append("quantidade de aprovações obrigatórias divergente")
    if (actual.get("enforce_admins") or {}).get("enabled") is not policy["enforce_admins"]:
        errors.append("administradores não estão sujeitos à proteção")
    for field, label in (("allow_force_pushes", "force push"), ("allow_deletions", "exclusão")):
        if (actual.get(field) or {}).get("enabled") is not policy[field]:
            errors.append(f"{label} não está bloqueado")
    return errors


def main() -> int:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    result = subprocess.run(["gh", "api", ENDPOINT], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr.strip() or "falha ao consultar proteção de main", file=sys.stderr)
        return 1
    errors = problems(json.loads(result.stdout), policy)
    if errors:
        print("Proteção de main divergente: " + "; ".join(errors), file=sys.stderr)
        return 1
    print("OK main: PR, versionamento, testes e administradores protegidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
