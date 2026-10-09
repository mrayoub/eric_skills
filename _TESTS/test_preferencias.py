"""Preferências locais do usuário: precedência, alcance, reset e isolamento."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "_SHARED/preferencias.py"
SKILLS = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


class PreferencesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.env = {**os.environ, "ERIC_SKILLS_CONFIG": str(self.base / "usuario")}
        self.project = self.base / "projeto"
        self.project.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_prefs(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), *args], env=self.env, capture_output=True, text=True)

    def test_without_preferences_default_behavior(self) -> None:
        result = self.run_prefs("ler", "relatorio-4d")
        self.assertEqual(result.returncode, 0)
        self.assertIn("comportamento padrão", result.stdout)

    def test_precedence_project_skill_common(self) -> None:
        self.run_prefs("adicionar", "relatorio-4d", "Usuário, esta skill.", "--versao", "1.1.0")
        self.run_prefs("adicionar", "relatorio-4d", "Usuário, todas.", "--versao", "1.1.0", "--todas")
        self.run_prefs("adicionar", "relatorio-4d", "Projeto, esta skill.", "--versao", "1.1.0", "--projeto", str(self.project))
        out = self.run_prefs("ler", "relatorio-4d", "--projeto", str(self.project)).stdout
        order = [out.index(text) for text in ("Projeto, esta skill.", "Usuário, esta skill.", "Usuário, todas.")]
        self.assertEqual(order, sorted(order))

    def test_skill_preference_does_not_leak_to_other_skill(self) -> None:
        self.run_prefs("adicionar", "relatorio-4d", "Só no 4D.", "--versao", "1.1.0")
        self.run_prefs("adicionar", "relatorio-4d", "Em todas.", "--versao", "1.1.0", "--todas")
        out = self.run_prefs("ler", "relatorio-3e").stdout
        self.assertNotIn("Só no 4D.", out)
        self.assertIn("Em todas.", out)

    def test_reset_keeps_backup_and_restores_default(self) -> None:
        self.run_prefs("adicionar", "workshop-4d", "Preferência qualquer.", "--versao", "1.1.0")
        self.run_prefs("adicionar", "workshop-4d", "Comum.", "--versao", "1.1.0", "--todas")
        self.assertEqual(self.run_prefs("resetar", "--todas-as-skills").returncode, 0)
        folder = self.base / "usuario"
        self.assertEqual(sorted(p.name for p in folder.iterdir()), ["todas.md.bak", "workshop-4d.md.bak"])
        self.assertIn("comportamento padrão", self.run_prefs("ler", "workshop-4d").stdout)

    def test_remove_and_version_warning(self) -> None:
        self.run_prefs("adicionar", "scorecard-inovacao", "Primeira.", "--versao", "1.0.0")
        self.run_prefs("adicionar", "scorecard-inovacao", "Segunda.", "--versao", "1.1.0")
        self.assertEqual(self.run_prefs("remover", "scorecard-inovacao", "P01").returncode, 0)
        out = self.run_prefs("ler", "scorecard-inovacao", "--versao-atual", "1.2.0").stdout
        self.assertNotIn("Primeira.", out)
        self.assertIn("criada na v1.1.0", out)

    def test_never_writes_inside_a_skill_folder(self) -> None:
        env = {**self.env, "ERIC_SKILLS_CONFIG": str(ROOT / "relatorio-4d" / "prefs")}
        result = subprocess.run([sys.executable, str(SCRIPT), "adicionar", "relatorio-4d", "x", "--versao", "1.0.0"],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse((ROOT / "relatorio-4d" / "prefs").exists())


class DistributionTests(unittest.TestCase):
    def test_every_skill_ships_script_reference_and_section(self) -> None:
        script = SCRIPT.read_bytes()
        guide = (ROOT / "_SHARED/preferencias-do-usuario.md").read_bytes()
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertEqual((skill / "scripts/preferencias.py").read_bytes(), script)
                self.assertEqual((skill / "references/preferencias-do-usuario.md").read_bytes(), guide)
                self.assertIn("## Preferências do usuário", (skill / "SKILL.md").read_text(encoding="utf-8"))

    def test_script_has_no_network_access(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        for module in ("urllib", "http.client", "socket", "requests"):
            self.assertNotIn(f"import {module}", source)


if __name__ == "__main__":
    unittest.main()
