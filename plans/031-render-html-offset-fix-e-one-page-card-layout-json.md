# Plan 031: Corrige offset de `@page margin` no caminho "presentation" e estende leitura de `layout.json` para `executive_one_page` e `card_portrait`

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**: `git diff --stat 4ab1a7c..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/layouts/`
> Se algum arquivo no escopo mudou desde que este plano foi escrito, compare
> os trechos de "Estado atual" abaixo contra o código real antes de prosseguir;
> em caso de divergência, trate como condição de STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED
- **Depends on**: none (os planos 029 e 030 já estão mesclados em `main`; este plano corrige um defeito no que o plano 030 entregou e estende a mesma técnica)
- **Category**: bug + direction
- **Planned at**: commit `4ab1a7c`, 2026-10-05

## Por que isso importa

O plano 030 (já mesclado) fez `render_html`'s branch `profile["layout"] == "presentation"` (usado só por `executive_presentation`) ler posições de `_DESIGN_SYSTEM/layouts/<tipo>.layout.json` via `position: absolute; left: Xmm; top: Ymm`. A intenção declarada era "fechar os dois formatos desse tipo com a mesma fonte de verdade" (mesmo arquivo que o PPTX usa).

**Isso não está acontecendo de verdade.** `css()` define `@page { margin: 0.4in }` para `presentation_16_9` (`render.py:353-355`). Em CSS Paged Media, um elemento `position: absolute` dentro de um ancestral `position: relative` (`.slide`) é posicionado relativo à área de conteúdo da página — que já está deslocada da borda física pela margem do `@page`. O PPTX (via `render_pptx`/`python-pptx`) posiciona formas em coordenadas absolutas da página inteira, sem esse deslocamento. Resultado: todo slot renderizado em PDF/HTML está sistematicamente ~10,16mm (0,4in) deslocado para a direita/baixo em relação à mesma coordenada no PPTX — o oposto do que o plano 030 afirmou entregar.

**Prova empírica** (feita nesta sessão, não é suposição): um HTML mínimo com `@page { size: 100mm 100mm; margin: 10mm; }` e uma `<div>` com `position:absolute; left:5mm; top:5mm` dentro de um container `position:relative` renderiza, via WeasyPrint, em `x0=15mm, top=15mm` no PDF final (10mm de margem + 5mm do CSS) — não em `5mm,5mm`. Adicionar uma segunda regra `@page { margin: 0; }` depois da primeira corrige isso: o mesmo teste passa a renderizar exatamente em `5mm,5mm`. CSS aceita múltiplas regras `@page` no mesmo stylesheet; a última declaração de uma propriedade vence (cascata normal), confirmado por teste direto nesta sessão.

Depois de corrigir isso, a mesma técnica (ler `layout.json`, posicionar via `position:absolute` dentro de um container sem margem de página) pode ser estendida com segurança para mais 3 tipos: `briefing_one_page` (perfil `executive_one_page`) e `test_card`/`learning_card` (perfil `card_portrait`). Esses 3 tipos compartilham uma garantia que os outros 14 tipos fluidos/multi-página não têm: **o próprio `render.py` já rejeita o PDF com erro se ele não couber em exatamente 1 página** (`render.py:946-954`, verificado nesta sessão: conta páginas do PDF gerado via `pypdf.PdfReader`, deleta o arquivo e levanta `ValueError` se `count != 1`). Isso elimina o risco que motivou deixar os outros 14 tipos fora do escopo nos planos 029/030 (conteúdo que não cabe vira erro, não corrupção silenciosa).

Já existem rascunhos de `layout.json` para os 3 tipos em `_DESIGN_SYSTEM/layouts/` (gerados em sessão anterior, **ainda não lidos por `render.py`**), com um slot por `section_key` real do schema de cada tipo — não só os 4 slots estruturais que o plano 030 usou. Isso é intencional: ao contrário de `executive_presentation` (onde o conteúdo de cada slide continua fluindo dentro de uma caixa), estes 3 tipos têm um número fixo e conhecido de seções (confirmado abaixo), então cada seção pode ganhar sua própria posição.

## Estado atual

### 1. O bug do offset (`_DESIGN_SYSTEM/scripts/render.py`)

```python
# render.py:343-358 (função css(), compartilhada por TODOS os tipos — não mexer nela diretamente)
def css(tokens: dict[str, Any], paper: str) -> str:
    ...
    if paper == "presentation_16_9":
        size = "13.333in 7.5in"
        margins = "0.4in"
    else:
        size = f"{page['width']}mm {page['height']}mm"
        margins = f"{page['margin_top']}mm {page['margin_right']}mm {page['margin_bottom']}mm {page['margin_left']}mm"
    ...
    return f"""
...
@page {{ size: {size}; margin: {margins}; }}
...
.document {{ padding: 0; }}
"""
```

```python
# render.py:505-536 (branch "presentation" de render_html, já existente, plano 030)
layout_slots = load_presentation_layout(content["deliverable_type"])

def slot_css(selector: str, slot_name: str) -> str:
    slot = layout_slots.get(slot_name) if layout_slots else None
    if not slot or not all(k in slot for k in ("x", "y", "width", "height")):
        return ""
    return (f"{selector} {{ position: absolute; left: {slot['x']}mm; top: {slot['y']}mm; "
             f"width: {slot['width']}mm; height: {slot['height']}mm; }} ")
...
if layout_slots:
    slide_css += " .slide { position: relative; }"
    slide_css += slot_css(".slide .masthead", "logo")
    slide_css += slot_css(".slide h1", "titulo_slide")
    slide_css += slot_css(".slide .slide-content", "corpo_slide")
    slide_css += slot_css(".slide .meta", "rodape_slide")
```

`slide_css` acaba sendo concatenado depois de `css(tokens, profile["paper"])` no `<style>` final (linha ~542: `f'<style>{css(tokens, profile["paper"])}{slide_css}</style>'`). Isso significa que **já existe um ponto de injeção depois do `@page` original** — basta adicionar `@page { margin: 0; }` a `slide_css` quando `layout_slots` existir.

### 2. A verificação de página única (não mexer — só ler)

```python
# render.py:946-954
if profile["layout"] in ("executive_one_page", "card_portrait"):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Verificação de página única requer pypdf: pip install pypdf") from exc
    count = len(PdfReader(str(path)).pages)
    if count != 1:
        path.unlink(missing_ok=True)
        raise ValueError(f"{profile['layout']} excedeu uma página ({count}); revise ou divida o conteúdo sem reduzir a fonte")
```

### 3. `CARD_LABELS` e o branch de card (`test_card`, `learning_card`)

```python
# render.py:49-62
CARD_LABELS = {
    "test_card": {
        "hypothesis": "1. Acreditamos que — hipótese",
        "test": "2. Para verificar, vamos — teste",
        "measure": "3. Vamos medir — medida",
        "criteria": "4. Estaremos certos se — critério",
    },
    "learning_card": {
        "hypothesis": "1. Acreditávamos que — hipótese testada",
        "observations": "2. Observamos que — observações",
        "learning": "3. Aprendemos que — inferência",
        "action": "4. Portanto, vamos — ação",
    },
}
```

```python
# render.py:544-557 (dentro de render_html, branch não-"presentation", ainda não lido por layout.json)
if content["deliverable_type"] in CARD_LABELS:
    fields = CARD_LABELS[content["deliverable_type"]]
    rendered = []
    for block in content["blocks"]:
        key = block.get("data", {}).get("section_key")
        if key in fields:
            value = html.escape(block_text(block)).replace("\n", "<br>")
            refs = ''.join(f'<sup>[{html.escape(x)}]</sup>' for x in block.get("citation_ids", []))
            rendered.append(f'<section class="card-field"><h2>{html.escape(fields[key])}</h2><p>{value}{refs}</p></section>')
        else:
            rendered.append(html_block(block))
    blocks = "\n".join(rendered)
else:
    blocks = html_report_blocks(content["blocks"])
```

Cada `<section class="card-field">` não carrega hoje nenhum atributo que identifique seu `section_key` (sem `data-section-key`) — precisa ser adicionado para o CSS conseguir mirar nele individualmente.

### 4. `briefing_one_page` não usa `CARD_LABELS` — cai em `html_report_blocks` (agrupamento por heading, ignora `section_key`)

```python
# render.py:307-340 (função html_report_blocks, usada por briefing_one_page HOJE)
def html_report_blocks(blocks: list[dict[str, Any]]) -> str:
    sections: list[tuple[str, bool]] = []
    pending: list[dict[str, Any]] = []
    def flush() -> None:
        if not pending:
            return
        heading = pending[0] if pending[0]["type"] == "heading" else None
        ...
    for block in blocks:
        if block["type"] == "page_break":
            flush()
            ...
        elif block["type"] == "heading":
            flush()
            pending.append(block)
        else:
            pending.append(block)
    flush()
    ...
    return '<div class="section-grid">' + ''.join(rendered) + '</div>'
```

Essa função agrupa blocos por **headings**, não por `section_key` — e os blocos reais de `briefing_one_page` não usam `heading` nenhum (confirmado na amostra `_SAMPLES_ENTREGAVEIS/briefing_one_page/input.json`: todos os 5 blocos são `callout`/`table` com `section_key` fixo). Ou seja, hoje essas 5 seções caem todas como "pending" sem heading e viram `.section-card` com título genérico "Notas", reorganizadas em pares de 2 colunas por `section-pair` — **a posição de cada uma não é controlável hoje**.

O schema confirma que o `section_key` é fixo e obrigatório por bloco (`contracts/briefing-one-page.schema.json`, cada `$defs` bloco tem `"section_key": { "const": "<valor>" }`): sempre `hmw`, `problem_opportunity`, `business_relevance`, `expected_outcomes`, `people`, nessa estrutura, sem variação. Isso é o que torna seguro introduzir um caminho de renderização por `section_key` dedicado para este tipo.

### 5. Tail compartilhado de `render_html` (gera o `<article class="document">` para os 4 layouts não-"presentation")

```python
# render.py:589-601
footer_label = identity_line(content)
if content["deliverable_type"] == "learning_card" and meta.get("test_card_id"):
    footer_label += f' · Test Card {meta["test_card_id"]} v{meta.get("test_card_version", "")}'
css_footer_label = json.dumps(footer_label, ensure_ascii=False).replace("<", "\\003c ")
footer_css = (f'@page {{ @bottom-right {{ content: {css_footer_label}; '
              f'font-family: Roboto; font-size: 7.5pt; color: {tokens["color"]["text_muted"]}; }} }} '
              '@media print { footer.meta { display: none; } }')
return ("<!doctype html>\n<html lang=\"pt-BR\"><head><meta charset=\"utf-8\">"
        f"<title>{title}</title><style>{css(tokens, profile['paper'])}{variant_css}{footer_css}</style></head><body><article class=\"document\">"
        f'<header class="masthead"><span class="eyebrow">{deliverable_label}</span><img src="{uri}" alt="CCEE"></header>'
        f"<h1>{title}</h1>{summary}{blocks}{refs}"
        f'<footer class="meta">{html.escape(footer_label)}</footer>'
        "</article></body></html>\n")
```

`footer_css` usa `@page { @bottom-right { ... } }` (caixa de margem de CSS Paged Media) — isso **funciona porque hoje depende da margem da página para existir** (a caixa `@bottom-right` vive dentro da margem). Se este plano zera a margem para estes 2 tipos quando `layout.json` existir, esse mecanismo de rodapé deixa de ter onde desenhar. Por isso o rodapé desses 2 tipos precisa virar uma `<footer>` posicionada via `position:absolute` (igual ao que o plano 030 já fez para `rodape_slide`), **só quando `layout.json` existir** — quando não existir, o mecanismo atual (`@bottom-right`) continua intocado.

### 6. `load_presentation_layout` (já existe, genérico o bastante para reaproveitar sem renomear)

```python
# render.py:471-479
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

Apesar do nome, essa função não tem nada específico de apresentação — já recebe `deliverable_type` e devolve slots por `name`. **Decisão deste plano: reaproveitar sem renomear.** Renomear exigiria atualizar o teste já mesclado `PresentationLayoutJsonTests` (que faz `patch.object(self.render, "load_presentation_layout", ...)`) sem nenhum ganho — puro custo de churn.

### 7. Layouts já existentes (rascunhos, ainda não lidos por `render.py`; **corrigidos nesta sessão antes deste plano**)

`_DESIGN_SYSTEM/layouts/briefing_one_page.layout.json` — canvas 297×210mm (`a4_landscape`, bate com `tokens.json["page"]["a4_landscape"]`), 7 slots: `titulo_documento`, `hmw`, `problem_opportunity`, `business_relevance`, `expected_outcomes`, `people`, `identificacao_versao`.

`_DESIGN_SYSTEM/layouts/test_card.layout.json` e `learning_card.layout.json` — canvas 210×297mm (`a4_portrait`, bate com `tokens.json["page"]["a4_portrait"]`; **este arquivo tinha um bug de canvas 148×210mm, corrigido nesta sessão antes deste plano ser escrito** — confirme que o canvas já está em 210×297 antes de prosseguir; se não estiver, PARE, isso significa que o arquivo mudou desde que este plano foi escrito). 6 slots cada: `titulo_documento`, 4 slots nomeados pelo rótulo completo do campo (ex: `"1. Acreditamos que — hipótese"`) com `section_key` igual às chaves de `CARD_LABELS`, e `identificacao_versao`.

Nenhum dos 3 arquivos tem slot `logo`/masthead — **a logo continua renderizando sem posicionamento controlado por `layout.json` nestes 3 tipos, como já acontece hoje.** Não é regressão: nunca houve controle de posição da logo para estes tipos antes deste plano.

### `profiles.json` dos 3 tipos (confirmado nesta sessão)

```json
"briefing_one_page": {"layout": "executive_one_page", "paper": "a4_landscape", "schema": "briefing-one-page.schema.json"}
"test_card": {"layout": "card_portrait", "paper": "a4_portrait", "schema": "test-card.schema.json"}
"learning_card": {"layout": "card_portrait", "paper": "a4_portrait", "schema": "learning-card.schema.json"}
```

## Comandos que você vai precisar

| Propósito | Comando | Esperado no sucesso |
|---|---|---|
| Testes (sem Pango/PDF) | `python3 tests/test_render.py` (rodar o arquivo direto, NÃO `python3 -m unittest tests.test_render` — colide com um pacote `tests` do Anaconda no `site-packages`) | todos passam; testes que precisam de PDF usam `pdf_available()` e são pulados se Pango faltar — isso é esperado e não é falha |
| Sync para as 11 skills | `python3 ../_TOOLS/sync_shared.py` (a partir de `_DESIGN_SYSTEM/`) depois `python3 ../_TOOLS/sync_shared.py --check` | segundo comando sai com código 0 |
| Validação de schema (opcional, sanidade) | `python3 -c "import json; json.load(open('layouts/briefing_one_page.layout.json'))"` (repita para os outros 2) | sem exceção |

Se seu ambiente tiver Pango instalado mas não encontrado pelo Python (erro `OSError: cannot load library 'pango-1.0-0'`), isso é um problema de ambiente local, não deste plano — não tente corrigir isso como parte da execução; rode os testes que puxam PDF de verdade só se eles passarem naturalmente, e não trate skips de PDF como falha.

## Escopo

**Em escopo** (únicos arquivos a modificar):
- `_DESIGN_SYSTEM/scripts/render.py` — função `render_html`, especificamente:
  - o branch `profile["layout"] == "presentation"` (linhas ~505-536): adicionar a correção do offset de `@page margin`.
  - o tail compartilhado (linhas ~544-601): adicionar lógica condicional de posicionamento só para `profile["layout"] in ("executive_one_page", "card_portrait")`.
- `_DESIGN_SYSTEM/tests/test_render.py` — novos testes.

**Fora de escopo** (não toque, mesmo parecendo relacionado):
- `profile["layout"] in ("report_portrait", "report_landscape")` — continuam fluindo exatamente como hoje, sem `layout.json`. Multi-página de verdade, decisão de uma plano futuro separado (já registrada em `plans/README.md`, seção "Planos 029-030 — origem").
- `render_pptx` e `render_docx` — nenhum dos 3 tipos deste plano usa PPTX; DOCX não tem posicionamento livre nativo (OOXML exigiria frames flutuantes manuais, fora de escopo, mesma decisão já tomada nos planos 029/030).
- `_DESIGN_SYSTEM/layouts/*.json` — os 3 arquivos já existem e já estão corretos; não regenere nem edite os valores de x/y/width/height a não ser que o passo 4 abaixo exija adicionar `data-section-key` (que é no HTML gerado, não no arquivo de layout).
- `_LAYOUT_STUDIO/` — não precisa de nenhuma mudança para este plano.
- O mecanismo `@page { @bottom-right { ... } }` para `report_portrait`/`report_landscape` — continua existindo sem alteração.
- `css()` (linhas 343-430) — função compartilhada por todos os 18 tipos; não edite o `@page` base nela. A correção de offset é uma regra `@page` **adicional**, injetada só no HTML de cada tipo afetado, depois do CSS compartilhado.

## Git workflow

- Branch: `advisor/031-html-offset-fix-one-page-card-layout`
- Um commit por etapa lógica (ex: "corrige offset de @page margin no branch presentation", "render_html: card_portrait lê layout.json por section_key", "render_html: executive_one_page lê layout.json por section_key"), seguindo o padrão observado em `git log` (mensagens curtas, imperativas, em português, sem prefixo de tipo).
- Não dê push nem abra PR a menos que instruído.

## Passos

### Passo 1: Corrige o offset de `@page margin` no branch "presentation"

Em `render_html`, dentro do bloco `if profile["layout"] == "presentation":` (linha ~505 em diante), depois de montar `slide_css` com os 4 `slot_css(...)` existentes (linhas ~535-536), adicione uma regra `@page` extra **só quando `layout_slots` existir**:

```python
if layout_slots:
    slide_css += " .slide { position: relative; }"
    slide_css += slot_css(".slide .masthead", "logo")
    slide_css += slot_css(".slide h1", "titulo_slide")
    slide_css += slot_css(".slide .slide-content", "corpo_slide")
    slide_css += slot_css(".slide .meta", "rodape_slide")
    slide_css += " @page { margin: 0; }"
```

**Verify**: rode isto a partir de `_DESIGN_SYSTEM/`:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import render, json
content = json.loads(open('../_SAMPLES_ENTREGAVEIS/executive_presentation/input.json').read())
tokens = json.loads(open('tokens.json').read())
profile = json.loads(open('profiles.json').read())['types']['executive_presentation']
out = render.render_html(content, tokens, profile)
assert '@page { margin: 0; }' in out, 'regra de override não encontrada'
assert out.count('@page { size: 13.333in 7.5in; margin: 0.4in; }') == 1, 'regra original deveria continuar presente (vem do css() compartilhado, não mexemos nela)'
print('OK: override presente, regra original intacta')
"
```
Esperado: imprime `OK: override presente, regra original intacta`, sem exceção.

### Passo 2: Teste de regressão do offset (prova que o bug existia e que foi corrigido)

Adicione em `_DESIGN_SYSTEM/tests/test_render.py`, dentro da classe `PresentationLayoutJsonTests` já existente (não crie uma classe nova para isto — é a mesma área testada):

```python
def test_page_margin_zeroed_when_layout_present(self):
    out = self.render.render_html(self.content, self.tokens, self.profile)
    # a regra @page { margin: 0.4in } vem do css() compartilhado e continua lá;
    # o que importa é que uma regra @page POSTERIOR zera a margem, porque em CSS
    # a última declaração de uma propriedade em regras @page do mesmo stylesheet
    # vence. Sem isso, as coordenadas absolutas abaixo ficam deslocadas ~10mm
    # da posição real do canvas (confirmado por teste manual com WeasyPrint
    # nesta sessão: @page margin:10mm desloca um elemento position:absolute
    # left:5mm para x0=15mm no PDF final, não 5mm).
    style_start = out.index("<style>")
    style_end = out.index("</style>")
    style = out[style_start:style_end]
    assert style.rindex("@page { margin: 0; }") > style.rindex("margin: 0.4in")
```

**Verify**: `python3 tests/test_render.py -v PresentationLayoutJsonTests` → `OK`, incluindo o novo teste.

### Passo 3: `card_portrait` (test_card, learning_card) lê `layout.json` por `section_key`

No bloco `if content["deliverable_type"] in CARD_LABELS:` (linha ~544), modifique para anexar `data-section-key` a cada `<section class="card-field">` e ao título/rodapé:

```python
if content["deliverable_type"] in CARD_LABELS:
    fields = CARD_LABELS[content["deliverable_type"]]
    rendered = []
    for block in content["blocks"]:
        key = block.get("data", {}).get("section_key")
        if key in fields:
            value = html.escape(block_text(block)).replace("\n", "<br>")
            refs = ''.join(f'<sup>[{html.escape(x)}]</sup>' for x in block.get("citation_ids", []))
            rendered.append(f'<section class="card-field" data-section-key="{html.escape(key)}"><h2>{html.escape(fields[key])}</h2><p>{value}{refs}</p></section>')
        else:
            rendered.append(html_block(block))
    blocks = "\n".join(rendered)
else:
    blocks = html_report_blocks(content["blocks"])
```

Depois, no tail compartilhado (linha ~589 em diante, onde hoje está `footer_label`/`footer_css`), adicione a lógica de posicionamento **só para os 2 layouts deste plano**, antes de montar `footer_css`:

```python
position_css = ""
if profile["layout"] in ("executive_one_page", "card_portrait"):
    layout_slots_doc = load_presentation_layout(content["deliverable_type"])
    if layout_slots_doc:
        def doc_slot_css(selector: str, slot_name: str) -> str:
            slot = layout_slots_doc.get(slot_name)
            if not slot or not all(k in slot for k in ("x", "y", "width", "height")):
                return ""
            return (f"{selector} {{ position: absolute; left: {slot['x']}mm; top: {slot['y']}mm; "
                     f"width: {slot['width']}mm; height: {slot['height']}mm; }} ")
        position_css = " .document { position: relative; } @page { margin: 0; }"
        position_css += doc_slot_css(".document h1", "titulo_documento")
        position_css += doc_slot_css(".document footer.meta", "identificacao_versao")
        if content["deliverable_type"] in CARD_LABELS:
            for key in CARD_LABELS[content["deliverable_type"]]:
                # o "name" do slot no layout.json é o rótulo completo do campo, não a chave;
                # localize o slot certo comparando section_key, não name.
                slot = next((s for s in json.loads((ROOT / "layouts" / f"{content['deliverable_type']}.layout.json").read_text(encoding="utf-8"))["slots"] if s.get("section_key") == key), None)
                if slot and all(k in slot for k in ("x", "y", "width", "height")):
                    position_css += (f'.document section.card-field[data-section-key="{key}"] {{ position: absolute; '
                                      f"left: {slot['x']}mm; top: {slot['y']}mm; width: {slot['width']}mm; height: {slot['height']}mm; }} ")
```

Note que o trecho acima relê o arquivo de layout diretamente para pegar `section_key` por slot, porque `load_presentation_layout` indexa por `name` (que para os slots de conteúdo dos cards é o rótulo completo, ex: `"1. Acreditamos que — hipótese"`, não a chave curta `hypothesis`) — **isso é deliberado, não um bug**: o `name` existe para o Layout Studio mostrar algo legível ao usuário; o `section_key` é o identificador estável que o código deve usar para casar com o conteúdo. Se achar uma forma mais limpa de fazer essa busca sem reler o arquivo (ex: estender `load_presentation_layout` para indexar por `section_key` também), pode fazer — desde que não quebre `PresentationLayoutJsonTests` (que depende de indexação por `name` continuar funcionando para `executive_presentation`).

**Verify**: rode isto a partir de `_DESIGN_SYSTEM/`:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import render, json
content = json.loads(open('../_SAMPLES_ENTREGAVEIS/test_card/input.json').read())
tokens = json.loads(open('tokens.json').read())
profile = json.loads(open('profiles.json').read())['types']['test_card']
out = render.render_html(content, tokens, profile)
assert 'data-section-key=\"hypothesis\"' in out
assert 'section.card-field[data-section-key=\"hypothesis\"] { position: absolute' in out
print('OK')
"
```
Esperado: imprime `OK`.

### Passo 4: `executive_one_page` (briefing_one_page) ganha um caminho de renderização por `section_key`

Diferente do Passo 3, aqui não existe hoje nenhum agrupamento por `section_key` — `html_report_blocks` agrupa por heading. Adicione uma função nova (ao lado de `html_report_blocks`, mesmo arquivo):

```python
def html_blocks_by_section_key(blocks: list[dict[str, Any]], layout_slots: dict[str, dict[str, Any]]) -> tuple[str, str]:
    """Renderiza um <section> por bloco, casado por section_key com um slot do
    layout.json (indexado por section_key, não por name — ver passo 4 do plano 031).
    Devolve (html, css). Blocos sem section_key correspondente em nenhum slot
    caem no html_report_blocks tradicional, anexado ao final sem posição."""
    slots_by_key = {s.get("section_key"): s for s in layout_slots.values() if s.get("section_key")}
    positioned: list[dict[str, Any]] = []
    leftover: list[dict[str, Any]] = []
    for block in blocks:
        key = block.get("data", {}).get("section_key")
        if key and key in slots_by_key and key != "titulo_documento" and key != "identificacao_versao":
            positioned.append(block)
        else:
            leftover.append(block)
    rendered = []
    css_rules = ""
    for block in positioned:
        key = block["data"]["section_key"]
        slot = slots_by_key[key]
        inner = html_block(block)
        rendered.append(f'<section class="section-card" data-section-key="{html.escape(key)}">{inner}</section>')
        if all(k in slot for k in ("x", "y", "width", "height")):
            css_rules += (f'.document section.section-card[data-section-key="{html.escape(key)}"] {{ position: absolute; '
                          f"left: {slot['x']}mm; top: {slot['y']}mm; width: {slot['width']}mm; height: {slot['height']}mm; }} ")
    html_out = '<div class="section-grid section-grid-positioned">' + ''.join(rendered) + '</div>'
    if leftover:
        html_out += html_report_blocks(leftover)
    return html_out, css_rules
```

No tail compartilhado, onde hoje está (linha ~556-557):
```python
    else:
        blocks = html_report_blocks(content["blocks"])
```

Troque por:

```python
    elif profile["layout"] == "executive_one_page" and (_layout := load_presentation_layout(content["deliverable_type"])):
        blocks, _blocks_position_css = html_blocks_by_section_key(content["blocks"], _layout)
        position_css += _blocks_position_css
    else:
        blocks = html_report_blocks(content["blocks"])
```

(isso exige que `position_css = ""` do Passo 3 seja declarado **antes** deste trecho, não depois — ajuste a ordem das linhas de forma que `position_css` exista antes de ser referenciado aqui. Decida a ordem final você mesmo, documentando no commit se mudou a ordem do que este plano descreveu.)

Por fim, troque o `<style>` final (linha ~597) de:
```python
f"<title>{title}</title><style>{css(tokens, profile['paper'])}{variant_css}{footer_css}</style></head><body><article class=\"document\">"
```
para incluir `position_css`:
```python
f"<title>{title}</title><style>{css(tokens, profile['paper'])}{variant_css}{footer_css}{position_css}</style></head><body><article class=\"document\">"
```

**Verify**:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import render, json
content = json.loads(open('../_SAMPLES_ENTREGAVEIS/briefing_one_page/input.json').read())
tokens = json.loads(open('tokens.json').read())
profile = json.loads(open('profiles.json').read())['types']['briefing_one_page']
out = render.render_html(content, tokens, profile)
for key in ('hmw', 'problem_opportunity', 'business_relevance', 'expected_outcomes', 'people'):
    assert f'data-section-key=\"{key}\"' in out, f'faltou {key}'
    assert f'section.section-card[data-section-key=\"{key}\"] {{ position: absolute' in out, f'faltou CSS de {key}'
print('OK')
"
```
Esperado: imprime `OK`.

### Passo 5: Fallback sem `layout.json` continua idêntico (teste de não-regressão)

Para cada um dos 3 tipos, confirme que remover/simular ausência do arquivo reproduz exatamente o HTML de antes deste plano — use `unittest.mock.patch.object` no módulo de render, igual ao padrão já usado em `PresentationLayoutJsonTests.test_falls_back_without_layout_file` (linhas ~1025-1035 de `test_render.py`), **não troque `deliverable_type` por um valor fictício** (isso quebra antes de chegar no código novo, porque `DELIVERABLE_LABELS[...]` e `validate()` levantam exceção para tipos desconhecidos — já documentado como pegadinha nos planos 029/030).

```python
class ExecutiveOnePageCardLayoutJsonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render = load_render_module()

    def _render(self, deliverable_type):
        content = json.loads((ROOT.parent / f"_SAMPLES_ENTREGAVEIS/{deliverable_type}/input.json").read_text(encoding="utf-8"))
        tokens = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))
        profile = json.loads((ROOT / "profiles.json").read_text(encoding="utf-8"))["types"][deliverable_type]
        return self.render.render_html(content, tokens, profile)

    def test_briefing_one_page_uses_layout(self):
        out = self._render("briefing_one_page")
        self.assertIn('data-section-key="hmw"', out)

    def test_briefing_one_page_falls_back_without_layout_file(self):
        with unittest.mock.patch.object(self.render, "load_presentation_layout", return_value=None):
            out = self._render("briefing_one_page")
        self.assertNotIn('data-section-key="hmw"', out)
        self.assertNotIn("position: absolute", out)

    def test_test_card_uses_layout(self):
        out = self._render("test_card")
        self.assertIn('data-section-key="hypothesis"', out)
        self.assertIn("position: absolute", out)

    def test_test_card_falls_back_without_layout_file(self):
        with unittest.mock.patch.object(self.render, "load_presentation_layout", return_value=None):
            out = self._render("test_card")
        self.assertIn('data-section-key="hypothesis"', out)  # o data-attribute sempre é escrito
        self.assertNotIn("position: absolute", out)  # mas sem posição quando não há layout.json

    def test_learning_card_uses_layout(self):
        out = self._render("learning_card")
        self.assertIn('data-section-key="hypothesis"', out)
        self.assertIn("position: absolute", out)
```

**Verify**: `python3 tests/test_render.py -v ExecutiveOnePageCardLayoutJsonTests` → `OK`, todos os testes passam.

### Passo 6: Suite completa + sync

```bash
cd _DESIGN_SYSTEM
python3 tests/test_render.py
python3 ../_TOOLS/sync_shared.py
python3 ../_TOOLS/sync_shared.py --check
```
**Verify**: primeiro comando sai OK (skips de PDF são aceitáveis se Pango não estiver disponível no ambiente); segundo comando roda sem erro; terceiro sai com código 0.

## Plano de testes

- `PresentationLayoutJsonTests.test_page_margin_zeroed_when_layout_present` (Passo 2) — regressão do bug de offset.
- `ExecutiveOnePageCardLayoutJsonTests` (Passo 5), modelada em `PresentationLayoutJsonTests` — 5 testes cobrindo: uso do layout para os 3 tipos, fallback sem arquivo para `briefing_one_page` (caminho novo, precisa provar que volta ao `html_report_blocks` antigo) e para `test_card` (caminho que já existia via `CARD_LABELS`, precisa provar que o `data-section-key` não quebra nada mesmo sem posição).
- Não é necessário testar `learning_card` sem layout.json separadamente — mesmo código de `test_card`, cobertura redundante.
- Verificação: `python3 tests/test_render.py` → todos os testes passam (PDF pulado se Pango ausente, não é falha).

## Done criteria

Todas devem valer:

- [ ] `python3 tests/test_render.py` sai OK (incluindo os novos testes dos Passos 2 e 5)
- [ ] `grep -c "position: absolute" <(python3 -c "...")` (Passo 3/4 verify commands) confirmam presença de posicionamento para os 3 tipos
- [ ] Renderizar `executive_presentation`, `briefing_one_page`, `test_card`, `learning_card` **sem** `layout.json` (via mock) produz HTML sem nenhuma ocorrência de `position: absolute` nos elementos antes posicionados — fallback idêntico ao comportamento pré-plano
- [ ] `python3 ../_TOOLS/sync_shared.py --check` sai com código 0
- [ ] Nenhum arquivo fora do escopo foi modificado (`git status` só mostra `_DESIGN_SYSTEM/scripts/render.py`, `_DESIGN_SYSTEM/tests/test_render.py`, e os espelhos de sync nas 11 skills após rodar `sync_shared.py`)
- [ ] `plans/README.md` com a linha de status deste plano atualizada

## STOP conditions

Pare e reporte (não improvise) se:

- O código em `render.py` nas linhas citadas não bater com os trechos de "Estado atual" (drift desde que este plano foi escrito).
- `_DESIGN_SYSTEM/layouts/test_card.layout.json` ou `learning_card.layout.json` ainda mostrarem canvas `148×210` em vez de `210×297` — significa que a correção feita antes deste plano foi revertida ou o arquivo mudou; não prossiga positionando sobre coordenadas erradas.
- Um teste de verificação falhar duas vezes após uma tentativa razoável de ajuste.
- Você descobrir que `position: absolute` dentro de `.document` se comporta diferente do testado neste plano para o papel `a4_portrait`/`a4_landscape` (o teste empírico desta sessão só cobriu um HTML mínimo de 100×100mm com margem simétrica — se o comportamento divergir com margens assimétricas ou fontes customizadas, pare e descreva o que observou em vez de compensar com valores arbitrários).
- A mudança de ordem entre `position_css` (Passo 3) e seu uso no Passo 4 causar `NameError` ou comportamento inesperado — reorganize com cuidado e documente a ordem final escolhida no commit.

## Notas de manutenção

- Se no futuro alguém adicionar um slot de `logo` aos 3 arquivos de layout deste plano, o masthead continuará sem posição controlada — este plano não cobre isso; seria um passo adicional natural (seguir o padrão de `slot_css(".slide .masthead", "logo")` do plano 030).
- Se o plano futuro que trata os 14 tipos fluidos/multi-página for escrito, ele **não pode** reusar a técnica de `@page { margin: 0; }` diretamente — esses tipos dependem da margem de página para o fluxo normal de texto funcionar em múltiplas páginas; a técnica deste plano só é segura porque `executive_one_page`/`card_portrait`/`presentation` são garantidamente uma página.
- O `_draft_note` (se existir) nos 3 arquivos de `layout.json` pode ser removido pelo usuário via Layout Studio a qualquer momento — não depende de nada deste plano.
- Revisor: confira que o Passo 1 (correção do offset) realmente se aplica também quando `layout_slots` é `None` (ou seja, SEM regressão no fallback do tipo `executive_presentation` sem `layout.json`) — a condição `if layout_slots:` já garante isso, mas vale conferir no diff.
