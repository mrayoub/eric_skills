"""Frontmatter dos SKILL.md aceito por Claude, Codex e ChatGPT."""
from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
# O ChatGPT e o validador do Codex recusam qualquer outro campo (inclusive `compatibility`).
ALLOWED = {"name", "description", "license", "allowed-tools", "metadata"}


def frontmatter(skill: Path) -> dict:
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n", 2)[1])


class FrontmatterTests(unittest.TestCase):
    def test_campos_aceitos_em_todas_as_ferramentas(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertLessEqual(set(frontmatter(skill)), ALLOWED)

    def test_metadados_obrigatorios(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                data = frontmatter(skill)
                self.assertEqual(data["name"], skill.name)
                self.assertTrue(data["license"])
                metadata = data["metadata"]
                self.assertTrue(all(isinstance(value, str) for value in metadata.values()))
                self.assertEqual(metadata["author"], "GEIN-CCEE")
                self.assertRegex(metadata["version"], r"^\d+\.\d+\.\d+$")
                self.assertTrue(metadata["requirements"].strip())
                if (skill / "assets/design-system").is_dir():
                    self.assertIn("requirements.txt", metadata["requirements"])


if __name__ == "__main__":
    unittest.main()
