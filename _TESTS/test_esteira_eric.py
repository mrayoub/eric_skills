"""A skill-mestra encaminha para todas as outras sem tomar o lugar delas."""
from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "esteira-eric"
OTHERS = sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file() and p != MASTER)


class EsteiraEricTests(unittest.TestCase):
    def test_map_covers_every_other_skill(self) -> None:
        mapa = (MASTER / "references/mapa-das-skills.md").read_text(encoding="utf-8")
        self.assertEqual(len(OTHERS), 12)
        for name in OTHERS:
            with self.subTest(skill=name):
                self.assertIn(f"`{name}`", mapa)

    def test_description_keeps_direct_invocation(self) -> None:
        text = (MASTER / "SKILL.md").read_text(encoding="utf-8")
        description = yaml.safe_load(text.split("---\n", 2)[1])["description"]
        self.assertIn("Não use quando o pedido já indicar o entregável ou a skill", description)

    def test_router_does_not_ship_design_system(self) -> None:
        self.assertFalse((MASTER / "assets/design-system").exists())
        for name in ("LICENSE", "THIRD_PARTY_NOTICES.md", "references/eric-esteira.md", "references/grilling-operacional.md"):
            with self.subTest(file=name):
                self.assertTrue((MASTER / name).is_file())


if __name__ == "__main__":
    unittest.main()
