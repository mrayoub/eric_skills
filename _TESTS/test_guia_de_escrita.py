"""O guia de escrita é a mesma fonte em todas as skills, e cada SKILL.md manda segui-lo."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_SHARED/guia-de-escrita.md"
SKILLS = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


class GuiaDeEscritaTests(unittest.TestCase):
    def test_every_skill_ships_the_same_guide(self) -> None:
        source = SOURCE.read_bytes()
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertEqual((skill / "references/guia-de-escrita.md").read_bytes(), source)

    def test_every_skill_links_the_guide(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertIn("(references/guia-de-escrita.md)", (skill / "SKILL.md").read_text(encoding="utf-8"))

    def test_language_guide_points_to_writing_guide(self) -> None:
        self.assertIn("(guia-de-escrita.md)", (ROOT / "_SHARED/linguagem-dos-entregaveis.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
