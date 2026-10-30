"""Contrato esperado para a proteção de main."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_main_protection", ROOT / "_TOOLS/check_main_protection.py")
GUARD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(GUARD)
POLICY = json.loads((ROOT / ".github/main-protection.json").read_text(encoding="utf-8"))


def effective() -> dict:
    return {
        "required_status_checks": {"strict": True, "contexts": ["versionamento", "testes"]},
        "required_pull_request_reviews": {"required_approving_review_count": 0},
        "enforce_admins": {"enabled": True},
        "allow_force_pushes": {"enabled": False},
        "allow_deletions": {"enabled": False},
    }


class MainProtectionTests(unittest.TestCase):
    def test_policy_requires_pr(self) -> None:
        self.assertEqual(POLICY["required_pull_request_reviews"], {"required_approving_review_count": 0})
        actual = effective()
        actual["required_pull_request_reviews"] = None
        self.assertIn("pull request não obrigatório", GUARD.problems(actual, POLICY))

    def test_policy_requires_current_checks(self) -> None:
        self.assertEqual(POLICY["required_status_checks"], {
            "strict": True, "contexts": ["versionamento", "testes"]})
        actual = effective()
        actual["required_status_checks"] = {"strict": False, "contexts": ["versionamento"]}
        self.assertIn("checks devem exigir branch atualizado", GUARD.problems(actual, POLICY))
        self.assertIn("checks obrigatórios diferem de versionamento e testes", GUARD.problems(actual, POLICY))

    def test_policy_prevents_admin_force_delete(self) -> None:
        self.assertTrue(POLICY["enforce_admins"])
        self.assertFalse(POLICY["allow_force_pushes"])
        self.assertFalse(POLICY["allow_deletions"])
        actual = effective()
        actual["enforce_admins"]["enabled"] = False
        actual["allow_force_pushes"]["enabled"] = True
        actual["allow_deletions"]["enabled"] = True
        self.assertEqual(len(GUARD.problems(actual, POLICY)), 3)

    def test_workflow_supplies_required_checks_on_pr(self) -> None:
        workflow = yaml.load((ROOT / ".github/workflows/tests.yml").read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        self.assertIn("pull_request", workflow["on"])
        self.assertEqual(set(POLICY["required_status_checks"]["contexts"]), {"versionamento", "testes"})
        for name in POLICY["required_status_checks"]["contexts"]:
            self.assertIn(name, workflow["jobs"])
            self.assertEqual(workflow["jobs"][name].get("if"), "github.event_name != 'schedule'")
