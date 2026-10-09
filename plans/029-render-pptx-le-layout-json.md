# Plan 029: `render_pptx` lê posição de `_DESIGN_SYSTEM/layouts/<deliverable_type>.layout.json`

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Pré-requisito antes de abrir um worktree isolado**: `_DESIGN_SYSTEM/layouts/`
> e `_LAYOUT_STUDIO/` estavam **sem commit** no momento em que este plano foi
> escrito (`git status --short` mostrava `?? _DESIGN_SYSTEM/layouts/` e
> `?? _LAYOUT_STUDIO/`). Um worktree isolado só enxerga arquivos commitados —
> se `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` não estiver
> commitado na branch de onde o worktree é criado, o Step 1 vai falhar por
> arquivo ausente. Confirme com `git log --oneline -1 -- _DESIGN_SYSTEM/layouts/executive_presentation.layout.json`
> antes de despachar um executor; se vazio, peça para o operador commitar essa
> pasta primeiro (fora do escopo deste plano decidir isso sozinho).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 063841f..HEAD -- _DESIGN_SYSTEM/scripts/render.py`
> Se o arquivo mudou desde que este plano foi escrito, compare o trecho de
> "Current state" abaixo com o código atual antes de prosseguir; em caso de
> divergência, trate como condição de STOP.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW (tem fallback idêntico ao comportamento atual quando o layout não existe)
- **Depends on**: nenhum plano anterior — mas depende de
  `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` existir e estar
  commitado (ver aviso acima)
- **Category**: tech-debt
- **Planned at**: commit `063841f`, 2026-10-02

## Por que isto importa

`render_pptx` (a única função que gera `.pptx` — só o tipo `executive_presentation`
usa esse formato, conforme `profiles.json`) tem 4 elementos visuais com posição
100% hardcoded em polegadas no código Python: logo, caixa de título, caixa de
corpo e rodapé, reaplicados identicamente em todo slide gerado. Para mudar
onde qualquer um desses elementos aparece, hoje é preciso editar `render.py`
diretamente.

Nesta sessão foi construída uma ferramenta de autoria visual (`_LAYOUT_STUDIO/`,
fora do escopo deste plano) que já extraiu essas 4 posições para
`_DESIGN_SYSTEM/layouts/executive_presentation.layout.json`, em milímetros.
Este plano é o primeiro passo para o renderizador realmente obedecer esse
arquivo em vez do valor fixo no código — escolhido como piloto porque é o
único formato com posição absoluta hoje (HTML/PDF/DOCX são renderizados em
fluxo, sem posição fixa, e exigiriam uma mudança muito maior — fora de escopo
aqui, de propósito).

## Current state

`_DESIGN_SYSTEM/scripts/render.py:740-809` (função inteira, citada por trechos
relevantes):

```python
def render_pptx(content: dict[str, Any], tokens: dict[str, Any], path: Path) -> None:
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.shapes import MSO_SHAPE
    except ImportError as exc:
        raise RuntimeError("PPTX requer python-pptx: pip install python-pptx") from exc
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    primary = RGBColor.from_string(tokens["color"]["document_primary"].lstrip("#"))
    logo = ROOT / "assets" / "logo_ccee.png"

    def slide(title: str, body: str) -> None:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.shapes.add_picture(str(logo), Inches(11.1), Inches(0.35), width=Inches(1.7))
        title_box = s.shapes.add_textbox(Inches(.5), Inches(.5), Inches(10.3), Inches(.8))
        run = title_box.text_frame.paragraphs[0].add_run()
        run.text, run.font.name, run.font.size, run.font.color.rgb = title, tokens["typography"]["font_brand"], Pt(28), primary
        body_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(.6), Inches(1.55), Inches(12.1), Inches(5.35))
        body_box.fill.solid()
        body_box.fill.fore_color.rgb = RGBColor.from_string(tokens["color"]["document_accent_soft"].lstrip("#"))
        body_box.line.color.rgb = RGBColor.from_string(tokens["color"]["border"].lstrip("#"))
        body_box.text_frame.margin_left = Inches(.2)
        body_box.text_frame.margin_top = Inches(.2)
        body_box.text_frame.word_wrap = True
        for line in body.splitlines() or [""]:
            para = body_box.text_frame.paragraphs[0] if not body_box.text_frame.text else body_box.text_frame.add_paragraph()
            para.text = line
            para.font.name, para.font.size = tokens["typography"]["font_body"], Pt(17)
        footer = s.shapes.add_textbox(Inches(.6), Inches(7.02), Inches(12.1), Inches(.33))
        footer.text_frame.word_wrap = True
        paragraph = footer.text_frame.paragraphs[0]
        paragraph.text = identity_line(content)
        paragraph.font.name = tokens["typography"]["font_body"]
        paragraph.font.size = Pt(10)
        paragraph.font.color.rgb = RGBColor.from_string(tokens["color"]["text_muted"].lstrip("#"))

    slide(content["title"], content.get("summary", ""))
    ... (resto da função itera content["blocks"], chama slide() de novo por heading/page_break — não precisa mudar)
    prs.save(path)
```

Chamada de `render_pptx` (`render.py:904`): `render_pptx(content, tokens, path)` —
só recebe `content`, `tokens`, `path`; `content["deliverable_type"]` já está
disponível dentro da função via `content`.

`ROOT` já está definido em `render.py:17` como `Path(__file__).resolve().parents[1]`
— ou seja, `ROOT / "layouts" / f"{tipo}.layout.json"` aponta certo para
`_DESIGN_SYSTEM/layouts/<tipo>.layout.json`. `json` já está importado no topo
do arquivo (`render.py:11`) — não precisa de import novo.

Conteúdo atual de `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json`
(arquivo inteiro — observe que os valores em mm, convertidos para polegadas
(mm ÷ 25.4), reproduzem exatamente os números hardcoded acima):

```json
{
  "schema_version": "1.2.0",
  "deliverable_type": "executive_presentation",
  "canvas": { "unit": "mm", "width": 338.66, "height": 190.5 },
  "grid_mm": 5,
  "slots": [
    { "id": "s1", "name": "logo", "x": 281.94, "y": 8.89, "width": 43.18, "height": 16.19, "z": 2, "section_key": "logo", "display_mode": "" },
    { "id": "s2", "name": "titulo_slide", "x": 12.7, "y": 12.7, "width": 261.62, "height": 20.32, "z": 1, "section_key": "titulo_documento", "display_mode": "title_and_content" },
    { "id": "s3", "name": "corpo_slide", "x": 15.24, "y": 39.37, "width": 307.34, "height": 135.89, "z": 1, "section_key": "", "display_mode": "content_only" },
    { "id": "s4", "name": "rodape_slide", "x": 15.24, "y": 178.31, "width": 307.34, "height": 8.38, "z": 1, "section_key": "identificacao_versao", "display_mode": "content_only" }
  ]
}
```

338.66mm ÷ 25.4 = 13.3331... pol (≈ 13.333, o valor hardcoded); 190.5mm ÷ 25.4 =
7.5 pol exatos — confirma que o arquivo já é fiel ao código atual.

## Commands you will need

```
PLAN_PYTHON=python3
"$PLAN_PYTHON" -c "import docx, pptx; print('ok')"
```

| Purpose | Command | Expected on success |
|---|---|---|
| Suíte de render completa | `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" tests/test_render.py` (rodar o arquivo diretamente — `python3 -m unittest tests.test_render` colide com um pacote `tests` de terceiros em alguns ambientes Anaconda, já documentado nos Planos 027/028) | `OK` (skips só de PDF sem `pango`, sem falha nova) |
| Só o contrato de tokens (Plano 027, deve continuar passando sem mudança) | `cd _DESIGN_SYSTEM && "$PLAN_PYTHON" tests/test_render.py -v VisualTokenContractTests` | `OK` |
| Só os testes novos deste plano | `cd _DESIGN_SYSTEM && "$PLAN_PYTHON" tests/test_render.py -v PptxLayoutJsonTests` | `OK` |

## Scope

**In scope**:
- `_DESIGN_SYSTEM/scripts/render.py` — só dentro de `render_pptx` (adicionar a
  função auxiliar de carregar o layout + trocar os 4 `Inches(...)` fixos por
  valores vindos dela, com fallback).
- `_DESIGN_SYSTEM/tests/test_render.py` (novos casos de teste).

**Out of scope** (não toque, mesmo que pareça relacionado):
- `render_docx`, `render_html`, `render_md`, `write_csv_tables` — formatos de
  fluxo, não fazem parte deste piloto.
- Qualquer schema em `contracts/`, `profiles.json`, `response-sections.json`.
- `_LAYOUT_STUDIO/` — é só a ferramenta de autoria, não precisa mudar.
- Os outros 17 arquivos `*.layout.json` em `_DESIGN_SYSTEM/layouts/` — nenhum
  outro tipo usa PPTX hoje; não crie lógica para eles.
- O tamanho de fonte do título/corpo (`Pt(28)`, `Pt(17)`) — isso é texto, não
  posição, e já foi tratado (parcialmente) no Plano 027; não mexa aqui.

## Git workflow

- Branch: `advisor/029-pptx-layout-json`
- Dois commits: (1) a função de carregar layout + troca dos 4 elementos; (2) os testes.
- Não dar push nem abrir PR.

## Steps

### Step 1: Função auxiliar `load_pptx_layout`

Adicione, logo antes de `def render_pptx(...)` em `render.py` (mesmo nível de
indentação de função top-level, como as outras funções `render_*`):

```python
def load_pptx_layout(deliverable_type: str) -> dict[str, Any] | None:
    """Lê _DESIGN_SYSTEM/layouts/<tipo>.layout.json, se existir, e converte mm -> polegadas.
    Retorna None quando o arquivo não existe (render_pptx usa as posições hardcoded nesse caso)."""
    path = ROOT / "layouts" / f"{deliverable_type}.layout.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    mm_to_in = 1 / 25.4
    canvas = data.get("canvas", {})
    slots = {}
    for slot in data.get("slots", []):
        name = slot.get("name")
        if not name:
            continue
        slots[name] = {k: slot[k] * mm_to_in for k in ("x", "y", "width", "height") if k in slot}
    return {
        "width_in": canvas.get("width", 0) * mm_to_in,
        "height_in": canvas.get("height", 0) * mm_to_in,
        "slots": slots,
    }
```

**Verify**: `"$PLAN_PYTHON" -c "
import sys; sys.path.insert(0, '_DESIGN_SYSTEM/scripts')
import render
layout = render.load_pptx_layout('executive_presentation')
print(round(layout['width_in'], 3), round(layout['height_in'], 3))
print(round(layout['slots']['corpo_slide']['x'], 3))
"` (rode a partir de `my_skills/`) → imprime `13.333 7.5` e depois `0.6`
(15.24mm ÷ 25.4 = 0.6 polegadas exatas).

### Step 2: Usar o layout dentro de `render_pptx`, com fallback

Dentro de `render_pptx`, logo após abrir os imports (antes de `prs = Presentation()`),
adicione:

```python
    layout = load_pptx_layout(content["deliverable_type"])

    def box(name: str, fx: float, fy: float, fw: float, fh: float) -> tuple[Any, Any, Any, Any]:
        slot = layout["slots"].get(name) if layout else None
        if slot and all(k in slot for k in ("x", "y", "width", "height")):
            return Inches(slot["x"]), Inches(slot["y"]), Inches(slot["width"]), Inches(slot["height"])
        return Inches(fx), Inches(fy), Inches(fw), Inches(fh)
```

Troque:
```python
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
```
por:
```python
    if layout:
        prs.slide_width, prs.slide_height = Inches(layout["width_in"]), Inches(layout["height_in"])
    else:
        prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
```

Dentro de `slide()`, troque as 4 linhas de posição:

```python
        s.shapes.add_picture(str(logo), Inches(11.1), Inches(0.35), width=Inches(1.7))
```
por (nota: `add_picture` aqui não recebe `height` hoje — não adicione um,
python-pptx escala a altura pela proporção real da imagem; passar height
junto distorceria o logo se a proporção do slot não bater exatamente):
```python
        logo_x, logo_y, logo_w, _ = box("logo", 11.1, 0.35, 1.7, 0)
        s.shapes.add_picture(str(logo), logo_x, logo_y, width=logo_w)
```

```python
        title_box = s.shapes.add_textbox(Inches(.5), Inches(.5), Inches(10.3), Inches(.8))
```
por:
```python
        title_x, title_y, title_w, title_h = box("titulo_slide", .5, .5, 10.3, .8)
        title_box = s.shapes.add_textbox(title_x, title_y, title_w, title_h)
```

```python
        body_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(.6), Inches(1.55), Inches(12.1), Inches(5.35))
```
por:
```python
        body_x, body_y, body_w, body_h = box("corpo_slide", .6, 1.55, 12.1, 5.35)
        body_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, body_x, body_y, body_w, body_h)
```

```python
        footer = s.shapes.add_textbox(Inches(.6), Inches(7.02), Inches(12.1), Inches(.33))
```
por:
```python
        footer_x, footer_y, footer_w, footer_h = box("rodape_slide", .6, 7.02, 12.1, .33)
        footer = s.shapes.add_textbox(footer_x, footer_y, footer_w, footer_h)
```

Nenhuma outra linha de `slide()` muda (texto, fonte, cor continuam iguais).

**Verify**: renderize a amostra real e confirme que a saída é idêntica à de
antes da mudança (já que o layout atual reproduz os valores hardcoded):
```
cd _DESIGN_SYSTEM
TMP=$(mktemp -d)
"$PLAN_PYTHON" scripts/render.py ../_SAMPLES_ENTREGAVEIS/executive_presentation/input.json --out-dir "$TMP" --formats pptx
"$PLAN_PYTHON" -c "
from pptx import Presentation
import os
f = [x for x in os.listdir('$TMP') if x.endswith('.pptx')][0]
p = Presentation('$TMP/' + f)
print(p.slide_width.inches, p.slide_height.inches)
s = p.slides[0]
print(s.shapes[1].left.inches, s.shapes[1].top.inches, s.shapes[1].width.inches, s.shapes[1].height.inches)
"
rm -rf "$TMP"
```
→ imprime `13.333... 7.5` e depois `0.5 0.5 10.3 0.8` (posição da caixa de
título, idêntica à constante hardcoded anterior, com tolerância de
arredondamento de ponto flutuante na conversão mm↔polegada).

### Step 3: Testes

Em `_DESIGN_SYSTEM/tests/test_render.py`, siga o padrão de
`VisualTokenContractTests` (linha 862 — `setUp` carregando um JSON de apoio,
subprocess chamando `render.py`, depois inspecionar o arquivo gerado com
`python-pptx`). Adicione:

```python
class PptxLayoutJsonTests(unittest.TestCase):
    """Garante que render_pptx usa _DESIGN_SYSTEM/layouts/<tipo>.layout.json quando existe,
    e cai para as posições hardcoded quando o arquivo não existe."""

    def test_existing_layout_matches_hardcoded_positions(self):
        from pptx import Presentation
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/executive_presentation/input.json"
        if not path.exists():
            self.skipTest("Amostra ausente")
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            subprocess.run([sys.executable, str(SCRIPT), str(path), "--out-dir", str(out), "--formats", "pptx"],
                           check=True, capture_output=True, text=True)
            prs = Presentation(str(next(out.glob("*.pptx"))))
            self.assertAlmostEqual(prs.slide_width.inches, 13.333, places=2)
            self.assertAlmostEqual(prs.slide_height.inches, 7.5, places=2)
            title_shape = prs.slides[0].shapes[1]
            self.assertAlmostEqual(title_shape.left.inches, 0.5, places=2)
            self.assertAlmostEqual(title_shape.top.inches, 0.5, places=2)

    def test_custom_layout_file_moves_the_title_box(self):
        from pptx import Presentation
        sample_path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/executive_presentation/input.json"
        if not sample_path.exists():
            self.skipTest("Amostra ausente")
        content = json.loads(sample_path.read_text(encoding="utf-8"))
        fake_layout = {
            "schema_version": "1.2.0", "deliverable_type": "__plan029_fake__",
            "canvas": {"unit": "mm", "width": 338.66, "height": 190.5}, "grid_mm": 5,
            "slots": [
                {"id": "s1", "name": "logo", "x": 281.94, "y": 8.89, "width": 43.18, "height": 16.19},
                {"id": "s2", "name": "titulo_slide", "x": 50.0, "y": 60.0, "width": 200.0, "height": 20.32},
                {"id": "s3", "name": "corpo_slide", "x": 15.24, "y": 39.37, "width": 307.34, "height": 135.89},
                {"id": "s4", "name": "rodape_slide", "x": 15.24, "y": 178.31, "width": 307.34, "height": 8.38},
            ],
        }
        content["deliverable_type"] = "__plan029_fake__"
        layouts_dir = ROOT / "layouts"
        fake_path = layouts_dir / "__plan029_fake__.layout.json"
        fake_path.write_text(json.dumps(fake_layout), encoding="utf-8")
        try:
            with tempfile.TemporaryDirectory() as temp:
                out = Path(temp)
                in_path = out / "input.json"
                in_path.write_text(json.dumps(content), encoding="utf-8")
                result = subprocess.run([sys.executable, str(SCRIPT), str(in_path),
                                         "--out-dir", str(out), "--formats", "pptx"],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                prs = Presentation(str(next(out.glob("*.pptx"))))
                title_shape = prs.slides[0].shapes[1]
                # 50mm / 25.4 ~= 1.9685 pol -- bem diferente dos 0.5 pol hardcoded;
                # prova que a posição veio do layout.json, não do fallback.
                self.assertAlmostEqual(title_shape.left.inches, 50.0 / 25.4, places=2)
                self.assertAlmostEqual(title_shape.top.inches, 60.0 / 25.4, places=2)
        finally:
            fake_path.unlink(missing_ok=True)
```

**Nota de isolamento**: o teste cria e remove `layouts/__plan029_fake__.layout.json`
— use esse nome exato (prefixo `__plan029_fake__`) para não colidir com nenhum
dos 18 arquivos reais, e o `finally` garante remoção mesmo se o teste falhar no
meio. Não deixe esse arquivo para trás.

**Verify**: `cd _DESIGN_SYSTEM && "$PLAN_PYTHON" tests/test_render.py -v PptxLayoutJsonTests` →
2 testes, ambos passam. Depois rode a suíte completa
(`"$PLAN_PYTHON" tests/test_render.py`) para confirmar que nada mais quebrou,
inclusive `VisualTokenContractTests` do Plano 027.

## Test plan

- `test_existing_layout_matches_hardcoded_positions`: prova que o caminho
  "layout existe e é igual ao hardcoded" não muda nada observável — a
  regressão mais importante a evitar.
- `test_custom_layout_file_moves_the_title_box`: prova que a integração
  realmente lê e aplica posições diferentes — sem isso, um bug que ignorasse
  silenciosamente o arquivo passaria despercebido.
- Suíte completa de `tests/test_render.py` (40 testes antes deste plano) para
  garantir zero regressão nos outros formatos/tipos.

## Done criteria

- [ ] `load_pptx_layout` existe em `render.py`, antes de `render_pptx`
- [ ] Os 4 elementos de `slide()` (logo, título, corpo, rodapé) e
      `prs.slide_width`/`slide_height` usam `box(...)`/`layout` em vez de
      `Inches(...)` literal
- [ ] `test_existing_layout_matches_hardcoded_positions` e
      `test_custom_layout_file_moves_the_title_box` passam
- [ ] Suíte completa de `tests/test_render.py` continua passando (incluindo
      `VisualTokenContractTests` do Plano 027, sem modificá-lo)
- [ ] Nenhum arquivo `__plan029_fake__.layout.json` sobra em
      `_DESIGN_SYSTEM/layouts/` depois dos testes
- [ ] `git status` não mostra nenhum arquivo fora da lista em "Scope"
- [ ] `plans/README.md` com a linha deste plano atualizada

## STOP conditions

Pare e reporte (não improvise) se:
- O trecho de `render_pptx` citado em "Current state" não bater com o código
  atual (deriva desde que este plano foi escrito).
- `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` não existir no
  worktree (ver aviso de pré-requisito no topo) — não invente um novo arquivo
  nem copie o conteúdo colado neste plano para criar um; reporte que falta
  commitar a pasta.
- A conversão mm→polegadas produzir uma posição visivelmente diferente da
  hardcoded para o layout real de `executive_presentation` (tolerância: até
  0.02 polegada de diferença é arredondamento aceitável; mais que isso indica
  que o arquivo não é mais fiel ao código, e a causa precisa ser investigada
  antes de prosseguir, não silenciosamente aceita).
- `add_picture` com `height` vindo do layout distorcer o logo de forma visível
  (não deveria acontecer, já que o Step 2 explicitamente não passa `height`
  para o logo — se você se pegar querendo adicionar isso, pare e confirme com
  o operador primeiro).

## Maintenance notes

- Este plano cobre só `executive_presentation`/PPTX. HTML, PDF e DOCX
  continuam com estrutura em fluxo, sem posição fixa — estender esse padrão
  para eles exige decidir como "posição absoluta" se encaixa num documento que
  cresce com o conteúdo (quebra de página, overflow de texto), o que é uma
  mudança de design maior, não uma continuação direta deste plano.
- Se `_LAYOUT_STUDIO/` for usada para editar `executive_presentation.layout.json`
  de novo depois (mudar posição de verdade, não só manter os valores atuais),
  a próxima renderização já vai refletir isso automaticamente — não precisa de
  nenhuma mudança adicional em `render.py` para isso funcionar.
- Os outros 17 arquivos `*.layout.json` (rascunho, com `_draft_note`) ficam
  sem efeito nenhum até um plano futuro decidir como/se integrar formatos de
  fluxo — não é um bug que eles "não façam nada" ainda.
