"""Obrigações dos seis oficiais, escritas a partir do plano aprovado."""
from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DS = ROOT / "_DESIGN_SYSTEM"
METHODS = {
    "four_d": [("d1", "Descongelar"), ("d2", "Diagnosticar"), ("d3", "Desenhar"), ("d4", "Decidir")],
    "three_e": [("e1", "Esclarecer"), ("e2", "Estruturar"), ("e3", "Experimentar")],
    "five_c": [("c1", "Contextualizar"), ("c2", "Compreender"), ("c3", "Confirmar"), ("c4", "Cocriar"), ("c5", "Conduzir")],
}
SKILLS = {"four_d": "relatorio-4d", "three_e": "relatorio-3e", "five_c": "relatorio-5c"}
KINDS = [f"{method}_official_{form}" for method in METHODS for form in ("report", "presentation")]


def load_renderer():
    spec = importlib.util.spec_from_file_location("official_test_render", DS / "scripts/render.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample(kind):
    return json.loads((ROOT / "_SAMPLES_ENTREGAVEIS" / kind / "input.json").read_text())


def validate(item):
    return load_renderer().validate(item, json.loads((DS / "profiles.json").read_text()))


def data_blocks(item):
    return [b for b in item["blocks"] if b["type"] not in ("heading", "page_break")]


def stages(item):
    return [stage for session in item["metadata"]["method_application"]["sessions"] for stage in session["stages"]]


def required_keys(item):
    ids = [stage["id"] for stage in stages(item)]
    if item["deliverable_type"].endswith("report"):
        return ["purpose", "introduction", "structuring", *[f"{sid}_{part}" for sid in ids for part in ("description", "execution", "outcome")], "conclusion", "recommendations"]
    return ["challenge_context", "structuring", *[f"execution_{sid}" for sid in ids], "conclusion", "recommendations", *(["decision"] if item["metadata"].get("decision_required") else []), "call_to_action"]


def keep_stages(item, keep, variant="pocket"):
    old_keys = set(required_keys(item))
    sessions = item["metadata"]["method_application"]["sessions"]
    assert len(sessions) == 1
    session = sessions[0]
    excluded = session["stages"][keep:]
    session["stages"] = session["stages"][:keep]
    session["variant"] = variant
    session["adaptation_reason"] = "Sessão curta delimitada para aprofundar a experiência atual."
    session["out_of_scope_stages"] = [{"official_stage_id": sid, "reason": "Fora do escopo por desenho da sessão curta."} for stage in excluded for sid in stage["official_stage_ids"]]
    new_keys = set(required_keys(item))
    item["blocks"] = [b for b in item["blocks"] if b["data"].get("section_key") not in old_keys - new_keys]
    return item


@pytest.mark.parametrize("method", METHODS)
def test_routing_guidance(method):
    text = (ROOT / SKILLS[method] / "SKILL.md").read_text()
    assert f"{method}_official_report" in text and f"{method}_official_presentation" in text
    assert "padrão" in text and "depreciad" in text
    renderer = load_renderer()
    for form, label in (("report", "Relatório"), ("presentation", "Apresentação")):
        assert renderer.DELIVERABLE_LABELS[f"{method}_{form}"] == f"{label} depreciad{'o' if form == 'report' else 'a'} {SKILLS[method][-2:].upper()}"


def test_gallery_catalog():
    spec = importlib.util.spec_from_file_location("official_gallery", ROOT / "_GALERIA/gerar.py")
    gallery = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gallery)
    for method, skill in SKILLS.items():
        assert gallery.SKILLS[skill][:4] == [f"{method}_official_report", f"{method}_official_presentation", f"{method}_report", f"{method}_presentation"]
    assert "test_card" in gallery.SKILLS["relatorio-3e"]


def test_studio_application():
    # Execute the same pure configuration helpers called by the Studio controls.
    script = ROOT / "_LAYOUT_STUDIO/official-methods.js"
    result = subprocess.run(["node", "--input-type=commonjs", "-e", "const assert=require('assert'); const m=require(process.argv[1]); for(const type of m.types){ const initial=m.sections(type); assert(initial.includes('structuring')); const applied=[{id:'remote_x',label:'Explorar',meaning:'Ouvir experiências',official_stage_ids:[]}]; const changed=m.sections(type,applied); assert(changed.includes(type.endsWith('report')?'remote_x_outcome':'execution_remote_x')); assert(!changed.includes('execution_c5')); const saved=JSON.parse(JSON.stringify({applied_stages:applied})); assert.deepStrictEqual(m.sections(type,saved.applied_stages),changed); }", str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    page = (ROOT / "_LAYOUT_STUDIO/index.html").read_text()
    assert "OfficialMethods.sections" in page and "applied_stages" in page


@pytest.mark.parametrize("kind", [k for k in KINDS if k.endswith("report")])
def test_report_recipe(kind):
    item = sample(kind)
    validate(item)
    assert [b["data"]["section_key"] for b in data_blocks(item)] == required_keys(item)
    for key in required_keys(item):
        for replacement in (None, " ", "heading", "uncited"):
            bad = copy.deepcopy(item)
            target = next(b for b in data_blocks(bad) if b["data"]["section_key"] == key)
            if replacement is None:
                bad["blocks"].remove(target)
            elif replacement == "heading":
                target["type"] = "heading"
            elif replacement == "uncited":
                target["citation_ids"] = []
            else:
                target["data"]["text"] = replacement
            with pytest.raises(ValueError):
                validate(bad)


@pytest.mark.parametrize("kind", KINDS)
def test_standard_methods(kind):
    item = sample(kind)
    method = kind.split("_official_")[0]
    assert [(s["official_stage_ids"][0], s["label"].split(" ", 1)[-1]) for s in stages(item)] == METHODS[method]
    assert item["metadata"]["method_application"]["sessions"][0]["variant"] == "standard"
    validate(item)
    bad = copy.deepcopy(item)
    bad["metadata"]["method_application"]["sessions"][0]["stages"].reverse()
    with pytest.raises(ValueError):
        validate(bad)


@pytest.mark.parametrize("kind", [k for k in KINDS if k.endswith("presentation")])
def test_presentation_recipe(kind):
    item = sample(kind)
    validate(item)
    assert [b["data"]["section_key"] for b in data_blocks(item)] == required_keys(item)
    for key in required_keys(item):
        bad = copy.deepcopy(item)
        bad["blocks"] = [b for b in bad["blocks"] if b["data"].get("section_key") != key]
        with pytest.raises(ValueError):
            validate(bad)
    bad = copy.deepcopy(item)
    bad["blocks"][2:4], bad["blocks"][4:6] = bad["blocks"][4:6], bad["blocks"][2:4]
    with pytest.raises(ValueError):
        validate(bad)


@pytest.mark.parametrize("method", METHODS)
def test_conditional_decision(method):
    item = sample(f"{method}_official_presentation")
    item["metadata"]["decision_required"] = True
    assert any(b["data"].get("section_key") == "decision" for b in data_blocks(item))
    validate(item)
    missing = copy.deepcopy(item)
    missing["blocks"] = [b for b in missing["blocks"] if b["data"].get("section_key") != "decision"]
    with pytest.raises(ValueError):
        validate(missing)
    missing["metadata"]["decision_required"] = False
    validate(missing)
    for value in (None, "false", 0):
        bad = copy.deepcopy(missing)
        bad["metadata"]["decision_required"] = value
        with pytest.raises(ValueError):
            validate(bad)
    missing["metadata"].pop("decision_required")
    with pytest.raises(ValueError):
        validate(missing)
    missing["metadata"]["completeness"] = "partial"
    validate(missing)


def test_slide_density():
    item = sample("five_c_official_presentation")
    assert sum(b["type"] == "heading" for b in item["blocks"]) > 6
    validate(item)
    for title in ("Conclusão", " ".join(["Achado"] * 15)):
        bad = copy.deepcopy(item)
        bad["blocks"][0]["data"]["text"] = title
        with pytest.raises(ValueError):
            validate(bad)
    bad = copy.deepcopy(item)
    data_blocks(bad)[0]["data"]["text"] = " ".join(["relato"] * 141)
    with pytest.raises(ValueError):
        validate(bad)


@pytest.mark.parametrize("kind", KINDS)
def test_pocket_scopes(kind):
    keep = 3 if kind.startswith("five_c") else 2
    item = keep_stages(sample(kind), keep)
    validate(item)
    bad = copy.deepcopy(item)
    key = required_keys(bad)[-3] if kind.endswith("presentation") else f"{stages(bad)[-1]['id']}_outcome"
    bad["blocks"] = [b for b in bad["blocks"] if b["data"].get("section_key") != key]
    with pytest.raises(ValueError):
        validate(bad)
    bad["metadata"]["completeness"] = "partial"
    validate(bad)


@pytest.mark.parametrize("kind", KINDS)
def test_adapted_and_mixed(kind):
    item = sample(kind)
    session = item["metadata"]["method_application"]["sessions"][0]
    session["variant"] = "adapted"
    session["adaptation_reason"] = "A sessão confrontou uma oferta existente em vez de gerar propostas."
    session["stages"][-1]["label"] = "Confrontar"
    session["stages"][-1]["meaning"] = "Examinar condições de adoção da oferta apresentada."
    validate(item)
    mixed = ROOT / "_SAMPLES_ENTREGAVEIS/official_variants" / f"{kind}.mixed.json"
    if kind.startswith("five_c"):
        content = json.loads(mixed.read_text())
        validate(content)
        sessions = content["metadata"]["method_application"]["sessions"]
        assert [len(s["stages"]) for s in sessions] == [3, 5]
        assert len({s["id"] for s in stages(content)}) == 8
    for variant in ("adapted", "pocket"):
        fixture = ROOT / "_SAMPLES_ENTREGAVEIS/official_variants" / f"{kind}.{variant}.json"
        validate(json.loads(fixture.read_text()))


@pytest.mark.parametrize("kind", KINDS)
def test_application_validation(kind):
    for mutate in ("missing_inventory", "duplicate", "unknown_mapping", "uncovered", "contradictory", "unexplained", "meaning", "empty", "wrong_variant"):
        bad = sample(kind)
        application = bad["metadata"]["method_application"]
        session = application["sessions"][0]
        if mutate == "missing_inventory":
            bad["metadata"].pop("method_application")
        elif mutate == "duplicate":
            session["stages"][1]["id"] = session["stages"][0]["id"]
        elif mutate == "unknown_mapping":
            session["stages"][0]["official_stage_ids"] = ["z99"]
        elif mutate == "uncovered":
            session["stages"].pop()
        elif mutate == "contradictory":
            session["out_of_scope_stages"] = [{"official_stage_id": session["stages"][0]["official_stage_ids"][0], "reason": "Excluída"}]
        elif mutate == "unexplained":
            session["variant"] = "adapted"
            session["adaptation_reason"] = " "
        elif mutate == "meaning":
            session["stages"][0]["meaning"] = " "
        elif mutate == "empty":
            application["sessions"] = []
        else:
            session["variant"] = "unknown"
        with pytest.raises(ValueError):
            validate(bad)


@pytest.mark.parametrize("kind", KINDS)
def test_render_formats(kind, tmp_path):
    from pypdf import PdfReader
    from docx import Document
    from pptx import Presentation
    source = ROOT / "_SAMPLES_ENTREGAVEIS" / kind / "input.json"
    form = "docx" if kind.endswith("report") else "pptx"
    result = subprocess.run([sys.executable, str(DS / "scripts/render.py"), str(source), "--out-dir", str(tmp_path), "--formats", f"json,html,pdf,{form},md"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    manifest = json.loads(next(tmp_path.glob("*.manifest.json")).read_text())
    assert not manifest["unavailable"]
    reader = PdfReader(next(tmp_path.glob("*.pdf")))
    pdf_text = " ".join(page.extract_text() for page in reader.pages)
    html_text = next(tmp_path.glob("*.html")).read_text()
    if form == "docx":
        doc = Document(next(tmp_path.glob("*.docx")))
        editable_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])
        assert float(reader.pages[0].mediabox.width) > float(reader.pages[0].mediabox.height)
    else:
        deck = Presentation(next(tmp_path.glob("*.pptx")))
        editable_text = " ".join(shape.text for slide in deck.slides for shape in slide.shapes if shape.has_text_frame)
        assert abs(deck.slide_width / deck.slide_height - 16 / 9) < .01
    for block in data_blocks(sample(kind)):
        text = block["data"]["text"]
        # PDF wraps words; compare normalized whitespace.
        assert " ".join(text.split()) in " ".join(pdf_text.split())
        assert text in html_text
        assert " ".join(text.split()) in " ".join(editable_text.split())
    assert "fictíc" in sample(kind)["summary"].lower()


def test_legacy_compatibility():
    for method in METHODS:
        for form in ("report", "presentation"):
            kind = f"{method}_{form}"
            item = sample(kind)
            validate(item)
            assert "depreciad" in load_renderer().header_label(item)


def test_editorial_guidance():
    for skill in SKILLS.values():
        guide = ROOT / skill / "references/entregaveis-oficiais.md"
        tone = ROOT / skill / "references/tom-oficial.md"
        assert guide.is_file() and tone.is_file()
        text = tone.read_text()
        assert "autora" in text and "denominador" in text and "evidências" in text
        assert "tom-oficial.md" in guide.read_text()
        assert tone.read_bytes() == (ROOT / "_SHARED/tom-oficial.md").read_bytes()
    for kind in KINDS:
        item = sample(kind)
        assert len(item["summary"].split()) <= 35
        assert item["citations"]
        assert all(b.get("citation_ids") for b in data_blocks(item))


def test_invalid_cli(tmp_path):
    item = sample("five_c_official_report")
    item["blocks"] = [b for b in item["blocks"] if b["data"].get("section_key") != "conclusion"]
    source = tmp_path / "input.json"
    source.write_text(json.dumps(item))
    dest = tmp_path / "output"
    result = subprocess.run([sys.executable, str(DS / "scripts/render.py"), str(source), "--out-dir", str(dest)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "conclusion" in result.stderr
    assert not dest.exists()


def test_distribution():
    for script in ("sync_shared.py", "build_catalog.py", "build_dist.py"):
        result = subprocess.run([sys.executable, str(ROOT / "_TOOLS" / script), "--check"], capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
