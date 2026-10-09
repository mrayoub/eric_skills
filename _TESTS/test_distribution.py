"""Catálogo de versões, pacotes .skill e verificador de atualizações."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CATALOG = load("build_catalog", ROOT / "_TOOLS/build_catalog.py")
DIST = load("build_dist", ROOT / "_TOOLS/build_dist.py")
CHECK = load("check_updates", ROOT / "_DESIGN_SYSTEM/scripts/check_updates.py")
SKILLS = CATALOG.skills()


class RepoCopy:
    """Cópia mínima: pastas das skills, _TOOLS e catalog.json."""

    def __enter__(self) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / "repo"
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
        for skill in SKILLS:
            shutil.copytree(skill, root / skill.name, ignore=ignore)
        shutil.copytree(ROOT / "_TOOLS", root / "_TOOLS", ignore=ignore)
        shutil.copyfile(ROOT / "catalog.json", root / "catalog.json")
        return root

    def __exit__(self, *exc) -> None:
        self.tmp.cleanup()


def version(skill: Path) -> str:
    return CATALOG.read_version(skill)


def next_patch(value: str) -> str:
    major, minor, patch = (int(part) for part in value.split("."))
    return f"{major}.{minor}.{patch + 1}"


def run_catalog(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(root / "_TOOLS/build_catalog.py"), *args], capture_output=True, text=True)


class CatalogTests(unittest.TestCase):
    def test_current_catalog_is_up_to_date(self) -> None:
        result = run_catalog(ROOT, "--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_changed_content_requires_bump(self) -> None:
        with RepoCopy() as root:
            current = version(root / "relatorio-4d")
            reference = root / "relatorio-4d/references/relatorio-4d-layout.md"
            reference.write_text(reference.read_text(encoding="utf-8") + "\nAlteração de teste.\n", encoding="utf-8", newline="")
            result = run_catalog(root, "--check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("relatorio-4d: conteúdo mudou sem subir a versão", result.stderr)
            bumped = run_catalog(root, "--bump")
            self.assertEqual(bumped.returncode, 0, bumped.stderr)
            self.assertEqual(bumped.stdout.count("OK versão"), 1)
            self.assertEqual(version(root / "relatorio-4d"), next_patch(current))
            self.assertEqual(run_catalog(root, "--check").returncode, 0)

    def test_new_skill_is_added_by_write_but_flagged_by_check(self) -> None:
        with RepoCopy() as root:
            catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
            catalog["skills"].pop("workshop-3e")
            (root / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8", newline="")
            check = run_catalog(root, "--check")
            self.assertEqual(check.returncode, 1)
            self.assertIn("workshop-3e: ausente do catálogo", check.stderr)
            self.assertEqual(run_catalog(root).returncode, 0)
            self.assertEqual(run_catalog(root, "--check").returncode, 0)

    def test_version_line_does_not_change_hash(self) -> None:
        with RepoCopy() as root:
            skill = root / "workshop-4d"
            before = CATALOG.skill_hash(skill)
            path = skill / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace(f'version: "{version(skill)}"', 'version: "9.9.9"'), encoding="utf-8", newline="")
            self.assertEqual(version(skill), "9.9.9")
            self.assertEqual(CATALOG.skill_hash(skill), before)

    def test_lower_version_fails(self) -> None:
        with RepoCopy() as root:
            path = root / "experimentacao-inovacao/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                f'version: "{version(root / "experimentacao-inovacao")}"', 'version: "0.0.1"'), encoding="utf-8")
            result = run_catalog(root, "--check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("versão menor que a publicada", result.stderr)


class PackageTests(unittest.TestCase):
    def test_package_matches_distributable_files_and_is_reproducible(self) -> None:
        skill = ROOT / "relatorio-4d"
        files = CATALOG.distributable_files(skill)
        with tempfile.TemporaryDirectory() as temp:
            first, second = Path(temp) / "a.skill", Path(temp) / "b.skill"
            DIST.package(skill, files, first)
            DIST.package(skill, files, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                names = archive.namelist()
        self.assertEqual(names, [f"relatorio-4d/{p.relative_to(skill).as_posix()}" for p in files])

    def test_every_skill_passes_frontmatter_check(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertEqual(DIST.validate_skill(skill), [])


class CheckUpdatesTests(unittest.TestCase):
    def test_hash_matches_catalog_tool(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertEqual(CHECK.skill_hash(skill), CATALOG.skill_hash(skill))

    def run_check(self, root: Path, catalog: Path | str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(ROOT / "_DESIGN_SYSTEM/scripts/check_updates.py"),
                               "--catalog", str(catalog), "--path", str(root)], capture_output=True, text=True)

    def test_reports_updated_outdated_and_local_changes(self) -> None:
        with RepoCopy() as root:
            catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
            installed_5c = version(root / "relatorio-5c")
            newer = next_patch(installed_5c)
            catalog["skills"]["relatorio-5c"]["version"] = newer
            changed = root / "workshop-5c/references/metodo-5c.md"
            changed.write_text(changed.read_text(encoding="utf-8") + "\nNota local.\n", encoding="utf-8", newline="")
            path = root / "custom.json"
            path.write_text(json.dumps(catalog), encoding="utf-8", newline="")
            result = self.run_check(root, path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"relatorio-5c: instalada {installed_5c}; disponível {newer}", result.stdout)
            self.assertIn(f"workshop-5c: {version(root / 'workshop-5c')} alterada localmente", result.stdout)
            self.assertIn(f"relatorio-4d: atualizada ({version(root / 'relatorio-4d')})", result.stdout)
            self.assertIn("npx skills update", result.stdout)

    def test_unreachable_catalog_is_not_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = self.run_check(ROOT, Path(temp) / "ausente.json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Não foi possível ler o catálogo", result.stdout)


class PackageContentTests(unittest.TestCase):
    def test_license_and_codex_interface_in_every_skill(self) -> None:
        primary = json.loads((ROOT / "_DESIGN_SYSTEM/tokens.json").read_text(encoding="utf-8"))["color"]["document_primary"]
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertEqual((skill / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
                interface = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
                self.assertEqual(set(interface), {"display_name", "short_description", "brand_color", "default_prompt"})
                self.assertEqual(interface["brand_color"], primary)



CHANNELS = load("check_channels", ROOT / "_TOOLS/check_channels.py")
PUBLISH = load("publish_releases", ROOT / "_TOOLS/publish_releases.py")


class ReleaseSafetyTests(unittest.TestCase):
    def test_remote_tags_drive_dry_run(self) -> None:
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        tags = {f"{skill}-v{entry['version']}" for skill, entry in catalog["skills"].items()}
        remote = "\n".join(f"abc123\trefs/tags/{tag}" for tag in tags)
        with mock.patch.object(PUBLISH, "run", return_value=subprocess.CompletedProcess([], 0, remote, "")):
            self.assertEqual(PUBLISH.existing_tags(), tags)
        self.assertEqual(PUBLISH.plan(catalog, tags), [])

    def test_rolling_removes_stale_assets_and_moves_tag(self) -> None:
        head = "a" * 40
        files = [Path("_DIST/briefing-inovacao.skill"), Path("_DIST/catalog.json"), Path("_DIST/SHA256SUMS")]
        calls = []

        def fake_run(*args, **kwargs):
            calls.append(args)
            if args[:3] == ("gh", "release", "view"):
                return subprocess.CompletedProcess(args, 0, json.dumps({"assets": [
                    {"name": "old.skill"}, {"name": "briefing-inovacao.skill"}]}), "")
            if args[:3] == ("git", "ls-remote", "--tags"):
                return subprocess.CompletedProcess(args, 0, f"{head}\trefs/tags/pacotes\n", "")
            return subprocess.CompletedProcess(args, 0, "", "")

        with mock.patch.object(PUBLISH, "run", side_effect=fake_run):
            PUBLISH.publish_rolling({"skills": {"briefing-inovacao": {}}}, files, head)
        self.assertIn(("gh", "release", "delete-asset", "pacotes", "old.skill", "--yes"), calls)
        self.assertTrue(any(call[:4] == ("gh", "api", "-X", "PATCH") for call in calls))
        self.assertTrue(any(call[:3] == ("gh", "release", "upload") for call in calls))

    def test_gh_failure_includes_stderr(self) -> None:
        with mock.patch.object(PUBLISH.subprocess, "run", return_value=subprocess.CompletedProcess(
                ["gh"], 1, "", "permissão negada")):
            with self.assertRaisesRegex(RuntimeError, "permissão negada"):
                PUBLISH.run("gh", "release", "view", "pacotes")

    def test_empty_npx_parse_is_a_diagnostic(self) -> None:
        with mock.patch.object(CHANNELS.shutil, "which", return_value="/usr/bin/npx"), mock.patch.object(
                CHANNELS.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "Available Skills", "")):
            with self.assertRaisesRegex(RuntimeError, "não foi possível ler a saída"):
                CHANNELS.npx_names(ROOT)

    def test_release_workflow_waits_for_successful_push_tests(self) -> None:
        release = yaml.load((ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        tests = yaml.load((ROOT / ".github/workflows/tests.yml").read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        self.assertEqual(release["on"]["workflow_run"]["workflows"], ["Testes"])
        self.assertIn("workflow_run.conclusion == 'success'", release["jobs"]["publicar"]["if"])
        self.assertIn("workflow_run.event == 'push'", release["jobs"]["publicar"]["if"])
        self.assertEqual(release["permissions"]["contents"], "read")
        self.assertEqual(release["jobs"]["publicar"]["permissions"]["contents"], "write")
        self.assertIn("github.event_name", tests["concurrency"]["group"])
        node_step = next(step for step in tests["jobs"]["versionamento"]["steps"]
                         if step.get("uses", "").startswith("actions/setup-node@"))
        self.assertEqual(node_step["with"]["node-version"], "22.20.0")


class ChannelTests(unittest.TestCase):
    def test_link_outside_skill_is_flagged(self) -> None:
        with RepoCopy() as root:
            guide = root / "relatorio-4d/references/relatorio-4d-layout.md"
            guide.write_text(guide.read_text(encoding="utf-8") + "\n[fora](../../_SHARED/x.md)\n", encoding="utf-8", newline="")
            problems = CHANNELS.check_links(root / "relatorio-4d")
            self.assertTrue(any("link para fora da skill" in problem for problem in problems), problems)

    def test_untracked_file_breaks_parity(self) -> None:
        with RepoCopy() as root:
            skill = root / "workshop-4d"
            tracked = [path.relative_to(skill).as_posix() for path in CATALOG.distributable_files(skill)]
            (skill / "rascunho-local.md").write_text("não versionado", encoding="utf-8", newline="")
            problems = CHANNELS.check_parity(skill, tracked, CATALOG.distributable_files(skill))
            self.assertTrue(problems)
            self.assertIn("rascunho-local.md", problems[0])

    def test_npx_mismatch_is_flagged(self) -> None:
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        catalog["skills"]["skill-inexistente"] = {"version": "1.0.0", "sha256": "x", "files": 1}
        from unittest import mock
        with mock.patch.object(CHANNELS, "npx_names", return_value=sorted(s.name for s in SKILLS)):
            problems = CHANNELS.check_npx(ROOT, catalog)
        self.assertTrue(problems)
        self.assertIn("skill-inexistente", problems[0])


if __name__ == "__main__":
    unittest.main()
