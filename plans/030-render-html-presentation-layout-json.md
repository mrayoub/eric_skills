# Plan 030: `render_html` (caminho `"presentation"`) posiciona masthead/título/rodapé/conteúdo por `_DESIGN_SYSTEM/layouts/<tipo>.layout.json`

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Pré-requisito antes de abrir um worktree isolado**: `_DESIGN_SYSTEM/layouts/`
> e `_LAYOUT_STUDIO/` estavam **sem commit** no momento em que este plano foi
> escrito. Um worktree isolado só enxerga arquivos commitados — confirme
> `git log --oneline -1 -- _DESIGN_SYSTEM/layouts/executive_presentation.layout.json`
> antes de despachar um executor; se vazio, peça para o operador commitar essa
> pasta primeiro (fora do escopo deste plano decidir isso sozinho).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 063841f..HEAD -- _DESIGN_SYSTEM/scripts/render.py`
> Se o arquivo mudou desde que este plano foi escrito, compare os trechos de
> "Current state" abaixo com o código atual antes de prosseguir; em caso de
> divergência, trate como condição de STOP.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW (tem fallback idêntico ao comportamento atual quando o layout não existe)
- **Depends on**: nenhum plano anterior — independente do Plano 029 (ver "Por que
  isto importa" sobre a decisão de não compartilhar código com ele), mas
  depende de `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json`
  existir e estar commitado (ver aviso acima)
- **Category**: tech-debt
- **Planned at**: commit `063841f`, 2026-10-02

## Por que isto importa

`render_html` tem um sub-caminho só para `profile["layout"] == "presentation"`
(usado só por `executive_presentation`, que gera o PDF via WeasyPrint a partir
desse HTML) que constrói cada "slide" como uma `<section class="slide">` de
tamanho fixo, com um `masthead` (logo) e um rodapé **literalmente repetidos em
cada seção** — estruturalmente idêntico ao modelo do PPTX (Plano 029): N
elementos de posição fixa, reaplicados em toda página. Hoje essas posições são
inteiramente decididas pelo fluxo normal do HTML (sem CSS de posição
explícita) — este plano faz esse caminho também obedecer
`_DESIGN_SYSTEM/layouts/executive_presentation.layout.json`, a mesma fonte que
o Plano 029 usa para o PPTX do mesmo tipo, fechando os dois formatos deste
tipo na mesma definição visual.

**Decisão deliberada: não compartilhar código com o Plano 029.** O loader do
Plano 029 (`load_pptx_layout`) converte mm → polegadas, porque `python-pptx`
exige objetos `Inches(...)`. CSS aceita `mm` nativamente — não há conversão de
unidade a fazer aqui. Generalizar os dois loaders em um só exigiria também
tocar no Plano 029 (que ainda não foi executado) e criaria acoplamento entre
dois planos independentes só para evitar ~10 linhas de duplicação. Este plano
define seu próprio loader, independente, que só lê milímetros crus.

**Escopo deliberadamente NÃO inclui** o tamanho da página (`@page size`) — o
`presentation_16_9` já tem o tamanho hardcoded dentro da função `css()`
compartilhada (`render.py:353-355`, usada pelos 18 tipos, não só
`executive_presentation`), e mudar isso exigiria alterar uma função
compartilhada por todos os formatos — risco desproporcional ao ganho, já que
o `canvas` do `executive_presentation.layout.json` atual já equivale a
`13.333in x 7.5in` (o valor hardcoded). Este plano só reposiciona os 4
elementos dentro da página, que já tem o tamanho certo.

## Current state

`_DESIGN_SYSTEM/scripts/render.py:479-512` (o sub-caminho `"presentation"`
inteiro, dentro de `render_html`):

```python
    if profile["layout"] == "presentation":
        sections: list[tuple[str, list[dict[str, Any]]]] = []
        current_title = "Conteúdo"
        current_blocks: list[dict[str, Any]] = []
        for block in content["blocks"]:
            if block["type"] in ("heading", "page_break"):
                if current_blocks:
                    sections.append((current_title, current_blocks))
                    current_blocks = []
                if block["type"] == "heading":
                    current_title = block_text(block)
                continue
            current_blocks.append(block)
        if current_blocks:
            sections.append((current_title, current_blocks))
        masthead = f'<header class="masthead"><span class="eyebrow">{deliverable_label}</span><img src="{uri}" alt="CCEE"></header>'
        slides = [f'<section class="slide">{masthead}<h1>{title}</h1><p class="summary">{html.escape(content.get("summary", ""))}</p></section>']
        for section_title, section_blocks in sections:
            slides.append(f'<section class="slide">{masthead}<h1>{html.escape(section_title)}</h1>'
                          + "\n".join(html_block(block) for block in section_blocks) + '</section>')
        if content["citations"]:
            refs = ''.join(f'<li><strong>{html.escape(c["id"])}</strong> — {html.escape(c["source_id"])}'
                           + (f', {html.escape(c["locator"])}' if c.get("locator") else '') + '</li>'
                           for c in content["citations"])
            slides.append(f'<section class="slide">{masthead}<h1>Fontes</h1><ol>{refs}</ol></section>')
        slide_footer = f'<footer class="meta">{html.escape(identity_line(content))}</footer>'
        slides = [slide.removesuffix("</section>") + slide_footer + "</section>" for slide in slides]
        slide_css = "@media print { .slide { break-after: page; } .slide:last-child { break-after: auto; } } @media screen { .slide { min-height: 170mm; border-bottom: 1px solid #ddd; padding-bottom: 10mm; } }"
        slide_css += (f'.slide .meta {{ margin-top: 10pt; font-family: Roboto; '
                      f'font-size: {tokens["typography"]["styles"]["footer"]["size"]}pt; '
                      f'color: {tokens["color"]["text_muted"]}; }}')
        return ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
                f'<title>{title}</title><style>{css(tokens, profile["paper"])}{slide_css}</style></head>'
                f'<body><article class="document">{"".join(slides)}</article></body></html>\n')
```

`ROOT` (`render.py:17`) e `json` (import no topo, `render.py:11`) já estão
disponíveis, igual descrito no Plano 029.

Conteúdo de `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` (igual
ao citado no Plano 029 — já em milímetros, sem conversão necessária aqui):

```json
{
  "slots": [
    { "id": "s1", "name": "logo", "x": 281.94, "y": 8.89, "width": 43.18, "height": 16.19, ... },
    { "id": "s2", "name": "titulo_slide", "x": 12.7, "y": 12.7, "width": 261.62, "height": 20.32, ... },
    { "id": "s3", "name": "corpo_slide", "x": 15.24, "y": 39.37, "width": 307.34, "height": 135.89, ... },
    { "id": "s4", "name": "rodape_slide", "x": 15.24, "y": 178.31, "width": 307.34, "height": 8.38, ... }
  ]
}
```

## Commands you will need

```
PLAN_PYTHON=python3
"$PLAN_PYTHON" -c "import jsonschema, referencing; print('ok')"
```

Este plano **não precisa de WeasyPrint/`pango`** para ser testado — os testes
chamam `render_html(...)` diretamente em Python e inspecionam a string HTML
retornada, sem converter para PDF. Isso funciona mesmo nesta máquina, que não
tem `pango` instalado (confirmado nos Planos 007/028).

| Purpose | Command | Expected on success |
|---|---|---|
| Suíte de render completa | `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" tests/test_render.py` | `OK` (mesmos skips de PDF sem `pango` de sempre, sem falha nova) |
| Só os testes novos deste plano | `cd _DESIGN_SYSTEM && "$PLAN_PYTHON" tests/test_render.py -v PresentationLayoutJsonTests` | `OK` |

## Scope

**In scope**:
- `_DESIGN_SYSTEM/scripts/render.py` — só dentro do bloco
  `if profile["layout"] == "presentation":` de `render_html` (linhas 479-512
  hoje), mais uma função auxiliar nova de carregamento.
- `_DESIGN_SYSTEM/tests/test_render.py` (novos casos de teste).

**Out of scope** (não toque, mesmo que pareça relacionado):
- A função `css()` (linhas 343+) — compartilhada por todos os 18 tipos; não
  mude `@page size`/margens por causa deste plano (ver "Por que isto importa").
- O resto de `render_html` (os outros `profile["layout"]`: `report_portrait`,
  `report_landscape`, `executive_one_page`, `card_portrait`) — ficam para um
  plano futuro separado, que precisa resolver a aproximação por caixa de
  margem CSS (`@top-right` etc.), não posição livre.
- `render_pptx`, `render_docx`, `render_md` — não mexer.
- `load_pptx_layout` do Plano 029 (se já existir) — não reutilizar nem
  modificar; este plano define seu próprio loader independente.
- Os outros 17 arquivos `*.layout.json` — nenhum outro tipo usa
  `profile["layout"] == "presentation"`.

## Git workflow

- Branch: `advisor/030-html-presentation-layout-json`
- Dois commits: (1) loader + reposicionamento; (2) testes.
- Não dar push nem abrir PR.

## Steps

### Step 1: Função de carregamento (em mm, sem conversão)

Adicione, antes de `def render_html(...)`:

```python
def load_presentation_layout(deliverable_type: str) -> dict[str, dict[str, Any]] | None:
    """Lê _DESIGN_SYSTEM/layouts/<tipo>.layout.json e devolve os slots por nome,
    em milímetros (CSS aceita mm nativamente — sem conversão de unidade).
    None se o arquivo não existir."""
    path = ROOT / "layouts" / f"{deliverable_type}.layout.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return {s["name"]: s for s in data.get("slots", []) if s.get("name")}
```

**Verify**: `"$PLAN_PYTHON" -c "
import sys; sys.path.insert(0, '_DESIGN_SYSTEM/scripts')
import render
slots = render.load_presentation_layout('executive_presentation')
print(slots['logo']['x'], slots['titulo_slide']['y'])
"` (rode a partir de `my_skills/`) → imprime `281.94 12.7`.

### Step 2: Reposicionar masthead/título/rodapé/conteúdo dentro do bloco `"presentation"`

Dentro do `if profile["layout"] == "presentation":`, logo após a linha que
calcula `current_blocks` (antes de montar `masthead`), adicione:

```python
        layout_slots = load_presentation_layout(content["deliverable_type"])

        def slot_css(selector: str, slot_name: str) -> str:
            slot = layout_slots.get(slot_name) if layout_slots else None
            if not slot or not all(k in slot for k in ("x", "y", "width", "height")):
                return ""
            return (f"{selector} {{ position: absolute; left: {slot['x']}mm; top: {slot['y']}mm; "
                     f"width: {slot['width']}mm; height: {slot['height']}mm; }} ")

        def wrap_slide_content(inner_html: str) -> str:
            return f'<div class="slide-content">{inner_html}</div>' if layout_slots else inner_html
```

Troque a linha do primeiro slide:
```python
        slides = [f'<section class="slide">{masthead}<h1>{title}</h1><p class="summary">{html.escape(content.get("summary", ""))}</p></section>']
```
por:
```python
        first_summary = f'<p class="summary">{html.escape(content.get("summary", ""))}</p>'
        slides = [f'<section class="slide">{masthead}<h1>{title}</h1>{wrap_slide_content(first_summary)}</section>']
```

Troque o loop de seções:
```python
        for section_title, section_blocks in sections:
            slides.append(f'<section class="slide">{masthead}<h1>{html.escape(section_title)}</h1>'
                          + "\n".join(html_block(block) for block in section_blocks) + '</section>')
```
por:
```python
        for section_title, section_blocks in sections:
            body_html = "\n".join(html_block(block) for block in section_blocks)
            slides.append(f'<section class="slide">{masthead}<h1>{html.escape(section_title)}</h1>'
                          + wrap_slide_content(body_html) + '</section>')
```

Troque o slide de fontes:
```python
            slides.append(f'<section class="slide">{masthead}<h1>Fontes</h1><ol>{refs}</ol></section>')
```
por:
```python
            slides.append(f'<section class="slide">{masthead}<h1>Fontes</h1>' + wrap_slide_content(f'<ol>{refs}</ol>') + '</section>')
```

Por fim, troque a montagem de `slide_css`:
```python
        slide_css = "@media print { .slide { break-after: page; } .slide:last-child { break-after: auto; } } @media screen { .slide { min-height: 170mm; border-bottom: 1px solid #ddd; padding-bottom: 10mm; } }"
        slide_css += (f'.slide .meta {{ margin-top: 10pt; font-family: Roboto; '
                      f'font-size: {tokens["typography"]["styles"]["footer"]["size"]}pt; '
                      f'color: {tokens["color"]["text_muted"]}; }}')
```
por (mantendo as duas linhas existentes exatamente iguais, só adicionando o
bloco condicional novo depois):
```python
        slide_css = "@media print { .slide { break-after: page; } .slide:last-child { break-after: auto; } } @media screen { .slide { min-height: 170mm; border-bottom: 1px solid #ddd; padding-bottom: 10mm; } }"
        slide_css += (f'.slide .meta {{ margin-top: 10pt; font-family: Roboto; '
                      f'font-size: {tokens["typography"]["styles"]["footer"]["size"]}pt; '
                      f'color: {tokens["color"]["text_muted"]}; }}')
        if layout_slots:
            slide_css += " .slide { position: relative; }"
            slide_css += slot_css(".slide .masthead", "logo")
            slide_css += slot_css(".slide h1", "titulo_slide")
            slide_css += slot_css(".slide .slide-content", "corpo_slide")
            slide_css += slot_css(".slide .meta", "rodape_slide")
```

Nenhuma outra linha do bloco `"presentation"` muda.

**Verify**: chame `render_html` direto (sem WeasyPrint) e confirme a posição
do logo na saída:
```
cd _DESIGN_SYSTEM
"$PLAN_PYTHON" -c "
import json, sys
sys.path.insert(0, 'scripts')
import render
content = json.loads(open('../_SAMPLES_ENTREGAVEIS/executive_presentation/input.json').read())
tokens = json.loads(open('tokens.json').read())
profiles = json.loads(open('profiles.json').read())
profile = profiles['types']['executive_presentation']
out = render.render_html(content, tokens, profile)
assert 'left: 281.94mm; top: 8.89mm' in out, 'posição do logo não encontrada na saída'
assert '.slide { position: relative; }' in out
print('ok: posições do layout.json aplicadas')
"
```
→ imprime `ok: posições do layout.json aplicadas`, sem `AssertionError`.

### Step 3: Testes

Confirmado em `test_render.py:1-20`: o arquivo **não** importa `render.py`
como módulo hoje — só guarda `SCRIPT = ROOT / "scripts" / "render.py"` e
chama via `subprocess.run([sys.executable, str(SCRIPT), ...])` em todo teste
existente. `importlib.util` já está importado no topo (linha 5), igual
`test_validators.py` usa para seu próprio `load_module`. Adicione o mesmo
padrão aqui, carregando o módulo uma vez:

```python
def load_render_module():
    spec = importlib.util.spec_from_file_location("render_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PresentationLayoutJsonTests(unittest.TestCase):
    """Garante que o caminho 'presentation' de render_html usa
    _DESIGN_SYSTEM/layouts/<tipo>.layout.json quando existe, e não muda nada
    quando o arquivo não existe (fallback idêntico ao comportamento anterior).
    Chama render_html direto (sem subprocess, sem WeasyPrint) -- mais rápido e
    não depende de `pango`, ao contrário de testes que convertem para PDF de
    verdade."""

    @classmethod
    def setUpClass(cls):
        cls.render = load_render_module()

    def setUp(self):
        self.content = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/executive_presentation/input.json").read_text(encoding="utf-8"))
        self.tokens = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))
        self.profile = json.loads((ROOT / "profiles.json").read_text(encoding="utf-8"))["types"]["executive_presentation"]

    def test_uses_real_layout_positions(self):
        out = self.render.render_html(self.content, self.tokens, self.profile)
        self.assertIn("left: 281.94mm; top: 8.89mm", out)
        self.assertIn(".slide { position: relative; }", out)

    def test_falls_back_without_layout_file(self):
        content = dict(self.content, deliverable_type="__plan030_fake__")
        # __plan030_fake__ não tem layout.json -- só queremos exercitar
        # render_html diretamente com um tipo sem arquivo de layout; não passa
        # pela validação de schema (essa função não valida nada sozinha).
        out = self.render.render_html(content, self.tokens, self.profile)
        self.assertNotIn("position: absolute", out)
        self.assertNotIn(".slide { position: relative; }", out)
```

Se carregar `render.py` como módulo disparar algum efeito colateral no nível
do módulo (ex: algo fora de função/classe que roda na importação), pare e
reporte — não deveria acontecer (o arquivo só define funções e tem um
`if __name__ == "__main__": main()` no fim, que não executa ao importar), mas
confirme lendo o fim do arquivo antes de rodar.

**Verify**: `cd _DESIGN_SYSTEM && "$PLAN_PYTHON" tests/test_render.py -v PresentationLayoutJsonTests` →
2 testes, ambos passam. Depois rode a suíte completa para confirmar zero
regressão nos outros 39-40 testes existentes.

## Test plan

- `test_uses_real_layout_positions`: prova que a integração funciona de
  verdade (a posição do layout aparece na saída).
- `test_falls_back_without_layout_file`: prova que, sem arquivo de layout, a
  saída não ganha nenhum `position: absolute` novo — o comportamento visual
  observável para tipos/casos sem layout continua exatamente o de antes.
- Suíte completa de `tests/test_render.py` para garantir zero regressão.

## Done criteria

- [ ] `load_presentation_layout` existe em `render.py`, antes de `render_html`
- [ ] Os 3 pontos de construção de slide (resumo inicial, loop de seções,
      slide de fontes) usam `wrap_slide_content(...)`
- [ ] `slide_css` ganha as 4 regras de posição (`masthead`/`h1`/`.slide-content`/`.meta`)
      só quando `layout_slots` existe
- [ ] Os 2 testes novos em `PresentationLayoutJsonTests` passam
- [ ] Suíte completa de `tests/test_render.py` continua passando
- [ ] `git status` não mostra nenhum arquivo fora da lista em "Scope"
- [ ] `plans/README.md` com a linha deste plano atualizada

## STOP conditions

Pare e reporte (não improvise) se:
- O trecho de `render_html` citado em "Current state" não bater com o código
  atual (deriva desde que este plano foi escrito).
- `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` não existir no
  worktree (ver aviso de pré-requisito no topo).
- `test_render.py` importar funções de `render.py` de um jeito que torne
  `import render` (módulo inteiro) inviável sem reescrever o cabeçalho do
  arquivo de teste — nesse caso, pare e descreva o padrão de import real
  encontrado, não force um import incompatível com o resto do arquivo.
- Você perceber que `html_block`/`table_views` (chamados dentro do loop de
  seções) já fazem algum tipo de posicionamento ou paginação interna que
  colidiria com o `<div class="slide-content">` novo — investigue e reporte
  antes de prosseguir, não assuma que é seguro envolver o conteúdo.

## Maintenance notes

- Este plano cobre só o caminho `"presentation"` (1 tipo: `executive_presentation`).
  Os outros 17 tipos (documento fluido) ficam para um plano futuro que precisa
  decidir a aproximação por caixa de margem CSS — não é uma continuação
  mecânica deste plano, é uma abordagem diferente.
- Se `_LAYOUT_STUDIO/` for usada para editar `executive_presentation.layout.json`
  de novo (mover o logo, redimensionar o corpo, etc.), a próxima geração de
  PDF já reflete isso automaticamente, tanto aqui quanto no PPTX do Plano 029
  — são duas integrações independentes da mesma fonte de verdade.
- O tamanho de página (`@page size`) continua fixo em `css()`, fora do
  controle do `layout.json` — se um dia o `canvas` do layout precisar ser
  diferente de `13.333in x 7.5in`, isso exige tocar a função `css()`
  compartilhada, avaliado à parte.
