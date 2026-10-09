"""Licença da CCEE, avisos de terceiros e regras do manifesto de fontes."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
import tempfile
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
IGNORE = shutil.ignore_patterns(".git", "_SAMPLE", "_OUTPUTS", "_DIST", "__pycache__", ".claude")


def run_build_sources(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(root / "_TOOLS/build_sources.py"), "--check"],
                          capture_output=True, text=True)


class RepoCopy:
    def __enter__(self) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=IGNORE)
        return self.root

    def __exit__(self, *exc) -> None:
        self.tmp.cleanup()


def edit_manifest(root: Path, change) -> None:
    path = root / "_FONTES/manifest.json"
    entries = json.loads(path.read_text(encoding="utf-8"))
    change(entries)
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ManifestoTests(unittest.TestCase):
    def test_estado_atual_passa(self) -> None:
        result = run_build_sources(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_campos_novos_sao_obrigatorios(self) -> None:
        for field in ("titular", "licenca", "distribuido"):
            with self.subTest(field=field), RepoCopy() as root:
                edit_manifest(root, lambda entries: entries[0].pop(field))
                self.assertEqual(run_build_sources(root).returncode, 1)

    def test_nao_distribuido_exige_url_https(self) -> None:
        with RepoCopy() as root:
            def change(entries):
                entry = next(e for e in entries if e["id"] == "strategyzer-test")
                entry["arquivo"] = "http://www.strategyzer.com/library/validate-your-ideas-with-the-test-card"
            edit_manifest(root, change)
            result = run_build_sources(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("https://", result.stderr)

    def test_pdf_retirado_nao_pode_voltar(self) -> None:
        with RepoCopy() as root:
            (root / "experimentacao-inovacao/assets/strategyzer-test-card-2023.pdf").write_bytes(b"%PDF-1.4")
            result = run_build_sources(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("não redistribuível", result.stderr)

    def test_nenhum_pdf_da_strategyzer_versionado(self) -> None:
        files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout
        self.assertNotRegex(files.lower(), r"strategyzer[^\n]*\.pdf")


class AvisosTests(unittest.TestCase):
    def test_referencia_4d_e_ficticia(self) -> None:
        sample = ROOT / "_SAMPLES_ENTREGAVEIS/four_d_report/sample-four-d-report-v1.0.0.pdf"
        distributed = ROOT / "relatorio-4d/assets/official-four-d-report.pdf"
        self.assertEqual(distributed.read_bytes(), sample.read_bytes())

    def test_docx_distribuidos_sem_metadados_pessoais(self) -> None:
        names = ("Modelo 4D de Aprofundamento.docx", "Modelo 3E Estruturacao da Solucao.docx",
                 "Playbook_Modelo_5C_Centralidade_Cliente.docx")
        for name in names:
            for path in ROOT.glob(f"*/assets/{name}"):
                with self.subTest(file=str(path.relative_to(ROOT))), zipfile.ZipFile(path) as docx:
                    core = ET.fromstring(docx.read("docProps/core.xml"))
                    app = ET.fromstring(docx.read("docProps/app.xml"))
                    for element in (*core.iter(), *app.iter()):
                        if element.tag.rsplit("}", 1)[-1] in {"creator", "lastModifiedBy", "Company"}:
                            self.assertFalse((element.text or "").strip())

    def test_avisos_listam_terceiros(self) -> None:
        text = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        for expected in ("Strategyzer AG", "CC BY-SA 4.0", "SIL Open Font License 1.1", "Montserrat", "Roboto"):
            self.assertIn(expected, text)

    def test_licenca_exclui_terceiros(self) -> None:
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("NÃO se aplica", text)
        self.assertIn("THIRD_PARTY_NOTICES.md", text)

    def test_nenhum_arquivo_distribuido_com_placeholder(self) -> None:
        for skill in SKILLS:
            for path in (ROOT / skill).rglob("*"):
                if path.is_file() and path.suffix in {".md", ".txt", ".json", ".yaml", ".py", ""}:
                    with self.subTest(file=str(path.relative_to(ROOT))):
                        self.assertNotIn("PREENCHER", path.read_text(encoding="utf-8", errors="ignore"))

    def test_cada_skill_leva_licenca_e_avisos(self) -> None:
        for skill in SKILLS:
            for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
                with self.subTest(skill=skill, name=name):
                    self.assertEqual((ROOT / skill / name).read_bytes(), (ROOT / name).read_bytes())

    def test_toda_fonte_tem_licenca_ofl(self) -> None:
        fonts = ROOT / "_DESIGN_SYSTEM/assets/fonts"
        licenses = {p.name.split("-")[0] for p in fonts.glob("*-OFL.txt")}
        for font in fonts.rglob("*.ttf"):
            with self.subTest(font=font.name):
                self.assertIn(font.name.split("-")[0], licenses)


if __name__ == "__main__":
    unittest.main()
