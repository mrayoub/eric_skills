# Plan 034: Gerar os 14 relatórios (A4 retrato e paisagem) em PDF com ReportLab, em nível de apresentação profissional

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 0eac9a9..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/scripts/pdf_reportlab.py _DESIGN_SYSTEM/tests/test_render.py _TOOLS/make_static_fonts.py`
> Os Planos 032 e 033 terão mudado esses arquivos. Confira que o que eles
> descrevem está presente; qualquer outra divergência dos trechos abaixo é STOP.

## Status

- **Priority**: P1
- **Effort**: L
- **Risk**: MED (código novo atrás de `--pdf-engine reportlab`; o padrão continua WeasyPrint)
- **Depends on**: `plans/032-pdf-reportlab-portatil.md` e `plans/033-verificador-de-qualidade-do-pdf.md`, ambos DONE **e** com a aprovação visual do operador registrada no 032.
- **Category**: dependências / qualidade dos entregáveis
- **Planned at**: commit `0eac9a9`, 2026-10-05

## Why this matters

O objetivo final é remover o WeasyPrint e o Pango (Plano 036). Para isso o ReportLab
precisa gerar todos os 18 tipos. Os relatórios são 14 deles e a parte mais difícil:
várias páginas, tabelas largas que atravessam páginas (a do IQB tem 40 linhas), grades
de cards e seções lado a lado. O operador pediu entregáveis em nível *state of the art*:
além de reproduzir o conteúdo, o PDF deve ter acabamento profissional — paginação
"página X de Y", marcadores de navegação, cabeçalho de tabela repetido, nenhuma faixa
de seção órfã no pé da página — e passar no portão de qualidade do Plano 033.

## Current state

### Tipos e referência de páginas

Layouts em `_DESIGN_SYSTEM/profiles.json`. Páginas dos PDFs de referência em
`_SAMPLES_ENTREGAVEIS/<tipo>/sample-*.pdf` (gerados pelo WeasyPrint):

| Layout | Tipo | Páginas ref. | Blocos na amostra |
|---|---|---|---|
| `report_portrait` | `briefing` | 1 | heading, callout, rich_text ×3, paragraph ×2 |
| `report_portrait` | `briefing_improvement_questionnaire` | 1 | paragraph, list |
| `report_portrait` | `briefing_validation` | 5 | table ×3 (IQB), callout, metric, list ×2 |
| `report_portrait` | `innovation_potential_assessment` | 2 | heading ×6, paragraph ×6, table |
| `report_portrait` | `experiment_plan` | 1 | heading ×6, paragraph ×6 |
| `report_landscape` | `four_d_workshop_record` | 2 | heading ×4, paragraph ×4, table |
| `report_landscape` | `four_d_report` | 5 | heading ×6, callout ×2, card_grid ×9, table |
| `report_landscape` | `three_e_workshop_record` | 1 | heading ×3, paragraph ×3 |
| `report_landscape` | `three_e_report` | 2 | heading ×4, paragraph ×4, table |
| `report_landscape` | `innovation_scorecard` | 1 | heading ×3, paragraph ×3, table |
| `report_landscape` | `experiment_report` | 2 | heading ×6, paragraph ×6, table |
| `report_landscape` | `evidence_recommendation` | 2 | heading ×5, paragraph ×5, table |
| `report_landscape` | `five_c_workshop_record` | 2 | heading ×5, paragraph ×5, table ×2 |
| `report_landscape` | `five_c_report` | 2 | heading ×5, paragraph ×5, table ×2 |

### Como o HTML monta um relatório (a estrutura a reproduzir)

`render.py`, `html_report_blocks` (linhas 307-340 no commit de planejamento):

```python
def html_report_blocks(blocks: list[dict[str, Any]]) -> str:
    sections: list[tuple[str, bool]] = []
    pending: list[dict[str, Any]] = []
    def flush() -> None:
        if not pending:
            return
        heading = pending[0] if pending[0]["type"] == "heading" else None
        body = pending[1:] if heading else pending[:]
        wide = any(x["type"] in ("table", "card_grid", "canvas", "chart") for x in body)
        title = html.escape(block_text(heading)) if heading else "Notas"
        inner = "".join(html_block(x) for x in body)
        sections.append((f'<section class="section-card {"wide" if wide else ""}">...', wide))
        pending.clear()
    for block in blocks:
        if block["type"] == "page_break":
            flush()
            sections.append(('<div class="page-break"></div>', True))
        elif block["type"] == "heading":
            flush()
            pending.append(block)
        else:
            pending.append(block)
    flush()
    # duas seções seguidas, ambas não "wide", ficam lado a lado (section-pair)
```

Regras: cada `heading` abre uma seção (faixa com o título); blocos antes do primeiro
heading formam a seção "Notas"; seção com `table`/`card_grid`/`canvas`/`chart` é
"larga"; duas seções seguidas não largas ficam lado a lado; `page_break` força nova página.

Grade de cards — `html_card_grid` (`render.py:287-304`): `data.columns` (1–4, padrão 2),
cada card com `title`, `value` opcional (16 pt negrito), `text`, `items` (lista), `tone`
(`blue` padrão, `neutral`, `red`, `green`, `yellow`) e `citation_ids`; cards agrupados
em linhas de `columns` cards.

Tabelas — `table_views(block)` (`render.py:243-274`) devolve `[(slug, legenda, cabeçalhos, linhas)]`;
para o IQB (bloco `table` com `data.dimensions`) devolve **três** tabelas (`criterios`,
`dimensoes`, `agrupamento`) com larguras fixas em `IQB_TABLE_WIDTHS` (`render.py:44-48`):

```python
IQB_TABLE_WIDTHS = {
    "criterios": [14, 15, 10, 41, 10, 10],
    "dimensoes": [14, 7, 10, 12, 9, 10, 10, 28],
    "agrupamento": [35, 65],
}
```

Bloco com `data.status` em `missing`/`pending`/`inconclusive` (`render.py:467`): destaque
com barra esquerda 3 pt `danger` e fundo `danger_soft`.

### Aparência (CSS em `css()` e variantes, `render.py:343-429` e `577-588`)

| Elemento | Regra |
|---|---|
| Margens | `tokens.page.a4_portrait` (16 mm) / `a4_landscape` (12 mm) |
| Cabeçalho | igual ao do 032: rótulo do tipo + logo + linha 1,5 pt `document_primary` (só na 1ª página) |
| Título | `cover_title`; no retrato 25 pt, no paisagem 24 pt (variantes do CSS) |
| Faixa de seção | fundo `document_deep`, Montserrat Bold 11 pt branco, maiúsculas, padding 9 pt × 12 pt |
| Caixa de seção | borda 0,75 pt `border`, raio 6 pt, conteúdo com padding 10 pt × 11 pt, 10 pt entre seções |
| Seções lado a lado | duas colunas iguais, espaço 10 pt |
| Tabela | `table_header`/`table_body` 8 pt; cabeçalho `document_primary`/`inverse`; borda 0,75 pt `border`; linhas pares `surface_muted`; padding 6 pt × 8 pt (IQB 4 pt) |
| Grade de cards | fundo `document_accent_soft`, barra esquerda 3 pt `document_accent`; tons: neutral `surface_muted`/`border_strong`, red `danger_soft`/`danger`, green `#E8F4EE`/`#3F9270`, yellow `#FFF4D9`/`#BD8A28`; título 9 pt maiúsculas |
| Callout / metric / lista / citações / Fontes / rodapé | como no 032 |

### O que o 032 entregou (confira em `pdf_reportlab.py`)

`render_pdf(content, tokens, profile, path, *, deliverable_label, footer_label, field_labels, block_text, table_rows)`,
`SUPPORTED_LAYOUTS`, `PdfOverflow`, `make_styles(tokens, layout)`, `block_flowables(...)`,
cabeçalho, fontes estáticas em `assets/fonts/static/`. Em `render.py`: `REPORTLAB_LAYOUTS`,
`render_pdf_reportlab(...)`, `--pdf-engine`. Do 033: `check_pdf_quality` roda em todo PDF.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Ambiente | `python3 -m venv /tmp/venv-034 && /tmp/venv-034/bin/python -m pip install -q -r _DESIGN_SYSTEM/requirements.txt fonttools==4.66.1 pypdfium2 pytest` | exit 0 |
| Testes | `/tmp/venv-034/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` |
| Comparação | `/tmp/venv-034/bin/python _TOOLS/compare_pdf_engines.py --out /tmp/cmp-034` | exit 0 |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check && python3 _TOOLS/build_sources.py --check` | exit 0 |

## Scope

**In scope**: `_DESIGN_SYSTEM/scripts/pdf_reportlab.py`, `_DESIGN_SYSTEM/scripts/render.py`
(só `REPORTLAB_LAYOUTS` e a passagem de `table_views`/`IQB_TABLE_WIDTHS` ao módulo),
`_TOOLS/make_static_fonts.py` (instância `Roboto-Medium`), `_DESIGN_SYSTEM/assets/fonts/static/Roboto-Medium.ttf`,
`_DESIGN_SYSTEM/tests/test_render.py`, `_DESIGN_SYSTEM/README.md`, cópias do sync, `plans/README.md`.

**Out of scope**: HTML/CSS e o caminho WeasyPrint; o padrão de `--pdf-engine`;
`executive_presentation` (Plano 035); `layout.json`; DOCX/PPTX; `_SAMPLES_ENTREGAVEIS/`;
`pdf_quality.py` (não afrouxe o portão).

## Git workflow

Branch `advisor/034-pdf-reportlab-relatorios`; um commit por passo; português no imperativo; sem push/merge.

## Steps

### Step 1: Peso 500 para o rodapé

Em `_TOOLS/make_static_fonts.py`, acrescente `("Roboto", 500, "Medium")` a `INSTANCES`, rode o script e registre `Roboto-Medium` no módulo. Em `make_styles`, `weight` 500 → `Roboto-Medium`; `>= 600` → `Roboto-Bold`; demais → `Roboto-Regular`.

**Verify**: nome interno `Roboto-Medium`, `usWeightClass` 500 (mesmo comando de verificação do Passo 1 do 032).

### Step 2: Estrutura de seções

Em `pdf_reportlab.py`, crie `group_sections(blocks, block_text)` que reproduz exatamente as regras de `html_report_blocks` e devolve uma lista de itens `("section", title, body_blocks, wide)` ou `("page_break",)`. Não importe nem chame `html_report_blocks`.

**Verify**: teste unitário (Passo 7, caso 1) com blocos sintéticos: `[p, h1, p, table, h2, p, page_break, h3, p]` → `Notas` (não larga), `h1` (larga), `page_break`, `h3`... e a ordem preservada.

### Step 3: Renderizar seções que atravessam páginas

Cada seção vira, em sequência (não uma única célula de tabela, que não pode quebrar entre páginas):

1. A faixa do título: `Table` de uma célula, `document_deep`, Montserrat Bold 11 pt branco, maiúsculas, com `keepWithNext=True` (a faixa nunca fica sozinha no pé da página).
2. O conteúdo: os flowables de `block_flowables` dentro de um recuo (`Indenter`) de 11 pt nos dois lados, com a moldura lateral desenhada por uma `Table` de conteúdo **somente se** a seção couber numa página; se não couber, sem moldura (ReportLab não quebra célula entre páginas).
3. Um marcador de navegação por seção: `canvas.bookmarkPage(key)` + `canvas.addOutlineEntry(title, key, level=0)` via um flowable mínimo (subclasse de `Flowable` com `draw()` que registra o marcador).
4. `Spacer(1, 10)` entre seções.

Seções lado a lado: quando duas seções seguidas são não largas, monte uma `Table` de duas colunas (largura igual, espaço 10 pt) com cada seção dentro de sua célula; meça com `table.wrap(largura_disponível, altura_do_frame)`. Se a altura passar de 90% da altura do frame, desista do par e renderize as duas em sequência.

`page_break` → `PageBreak()`.

**Verify**: `three_e_workshop_record` e `experiment_plan` renderizam com `--pdf-engine reportlab` (após o Passo 6) com exit 0.

### Step 4: Tabelas e grades de cards

- Tabelas comuns: `headers, rows = table_rows(block)`; todas as células como `Paragraph` (`table_header` em maiúsculas sobre `document_primary`; `table_body`); `repeatRows=1` (cabeçalho repetido em cada página); linhas pares `surface_muted`; `GRID` 0,75 pt `border`; larguras iguais. Legenda (`data.title`) acima, Roboto Bold 8 pt.
- IQB: para blocos `table` com `data.dimensions`, use `table_views(block)` (receba a função por parâmetro, como `table_rows`) e gere as três tabelas, cada uma com legenda, larguras de coluna proporcionais a `IQB_TABLE_WIDTHS[slug]` (receba o dicionário por parâmetro) e padding 4 pt.
- Grade de cards: uma `Table` por linha de `columns` cards; cada célula com título (9 pt maiúsculas), valor (16 pt negrito, se houver), texto, itens com "•" e citações; cores pelo `tone` conforme a tabela de aparência; linhas com `KeepTogether` individual (uma linha de cards nunca é partida ao meio).
- Bloco com `data.status` em `missing`/`pending`/`inconclusive`: `Table` de uma célula com barra esquerda 3 pt `danger` e fundo `danger_soft`.
- Textos longos sem espaço (URLs, IDs) precisam quebrar dentro da célula: mantenha `splitLongWords=1` nos estilos.

**Verify**: após o Passo 6, `briefing_validation` e `four_d_report` renderizam com exit 0 (o portão do 033 garante ausência de sobreposição e texto fora da página).

### Step 5: Página, rodapé numerado e metadados

- `BaseDocTemplate` com um `PageTemplate` de um `Frame` entre as margens do token (deixando 10 mm para o rodapé). O cabeçalho (rótulo + logo + título + resumo) é flowable no início da história, só na 1ª página.
- Rodapé em todas as páginas: `footer_label + " · página X de Y"`, `footer` (Roboto-Medium 7,5 pt) `text_muted`, à direita. Para saber `Y`, use o padrão de *canvas numerado* do ReportLab: uma subclasse de `reportlab.pdfgen.canvas.Canvas` que guarda `self._saved_page_states` em `showPage()` e, em `save()`, percorre os estados desenhando o rodapé com o total; passe-a em `doc.build(story, canvasmaker=NumberedCanvas)`. Mantenha `invariant=1`.
- Metadados: `title=content["title"]`, `subject=deliverable_label`, `creator="my_skills render.py"`.
- Transbordo: em relatórios, conteúdo longo pagina. Um único elemento maior que uma página (ex.: uma linha de tabela gigante) gera `LayoutError` → relance `PdfOverflow(f"{layout}: o bloco {block_id} não cabe numa página; divida o conteúdo")`, identificando o bloco quando possível.

### Step 6: Habilitar os layouts

`SUPPORTED_LAYOUTS` (módulo) e `REPORTLAB_LAYOUTS` (`render.py`) passam a incluir `report_portrait` e `report_landscape`. Em `render_pdf`, despache por `profile["layout"]`. Cards e one-page **não** mudam (mas ganham o peso 500 do rodapé, se usarem `footer`).

**Verify**:
```
for t in briefing briefing_improvement_questionnaire briefing_validation innovation_potential_assessment experiment_plan four_d_workshop_record four_d_report three_e_workshop_record three_e_report innovation_scorecard experiment_report evidence_recommendation five_c_workshop_record five_c_report; do
  /tmp/venv-034/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/$t/input.json --out-dir /tmp/o034 --formats pdf --pdf-engine reportlab >/dev/null || echo "FALHOU $t"
done; ls /tmp/o034/*.pdf | wc -l
```
→ nenhuma linha `FALHOU`; `14`.

### Step 7: Testes

Classe `ReportLabReportTests` (pula sem `reportlab`):

1. `test_group_sections_matches_html_rules` (Passo 2).
2. `test_all_report_samples_render`: os 14 tipos, exit 0; páginas ≤ páginas de referência + 1 (tabela acima).
3. `test_report_text_is_complete`: para cada amostra, todo texto não vazio de `data` (`text`, `title`, `description`, itens de `items`, células de `table_rows`, títulos e textos dos cards) e todo `citation.id` aparecem no texto extraído do PDF (normalize com `" ".join(texto.split())` dos dois lados).
4. `test_long_table_repeats_header`: `content("briefing", "BR-long")` com um bloco `table` de 3 colunas e 120 linhas → ≥ 3 páginas; o texto do cabeçalho aparece em todas as páginas que contêm linhas da tabela.
5. `test_footer_page_numbers`: no `four_d_report`, a página `i` contém `f"página {i} de {total}"` e a `identity_line`.
6. `test_outline_has_sections`: `pypdf.PdfReader(...).outline` tem uma entrada por seção do `four_d_report`, com os títulos dos headings.
7. `test_report_deterministic_bytes`: duas renderizações de `briefing_validation` → bytes idênticos.
8. `test_section_band_never_orphan`: em `four_d_report` e no caso do teste 4, nenhuma página termina com uma faixa de seção sem conteúdo depois — verifique com `pdfplumber`/`pdfminer` que o último texto de cada página não é um título de seção (os títulos estão em maiúsculas Montserrat Bold 11 pt; compare com os headings da amostra).

**Verify**: `pytest -k ReportLabReport` sem falhas; suíte completa `0 failed`.

### Step 8: Revisão visual do operador (gate)

```
/tmp/venv-034/bin/python _TOOLS/compare_pdf_engines.py --out /tmp/cmp-034
```
**Verify**: `/tmp/cmp-034/index.html` com os 18 tipos (apresentação só na coluna WeasyPrint). Informe o caminho no relatório. **Não** marque o plano como DONE antes do operador aprovar a aparência; registre a aprovação ou os ajustes pedidos na linha de status.

### Step 9: Docs e sync

`_DESIGN_SYSTEM/README.md`: `--pdf-engine reportlab` passa a cobrir todos os tipos exceto `executive_presentation`. Rode sync e checagens.

## Test plan

8 testes novos (Passo 7), no estilo de `ReportLabPdfTests` (032) e `PdfQualityTests` (033). O portão do 033 roda em cada render, então todos os testes de render também verificam fonte mínima, sobreposição e texto fora da página.

## Done criteria

- [ ] 14 relatórios gerados com `--pdf-engine reportlab`, todos aprovados pelo portão
- [ ] `pytest -k ReportLabReport` sem falhas; suíte completa `0 failed`
- [ ] `/tmp/cmp-034/index.html` entregue e **aprovado pelo operador**
- [ ] `sync_shared.py --check` e `build_sources.py --check` → exit 0
- [ ] HTML padrão inalterado (mesmo procedimento de linha de base `/tmp/h0` × `/tmp/h1` do Plano 032, com as amostras `briefing_validation` e `four_d_report`)
- [ ] `git status` só com arquivos do escopo; status atualizado em `plans/README.md`

## STOP conditions

- Plano 032 ou 033 não está DONE, ou a aprovação visual do 032 não está registrada.
- Algum relatório é reprovado pelo portão do 033 e a causa não é óbvia no seu código.
- Para passar no portão, seria preciso reduzir fonte abaixo de 7,5 pt ou afrouxar `pdf_quality.py`.
- Um tipo passa de páginas de referência + 1.
- Algum texto da amostra não aparece no PDF (teste 3) — conteúdo perdido é inaceitável.
- Um passo falha duas vezes após tentativa razoável.

## Maintenance notes

- Com este plano, o layout dos relatórios existe em dois lugares (CSS e ReportLab) até o Plano 036 remover o WeasyPrint. Revisores devem cobrar os dois.
- Melhorias deliberadamente além do HTML atual: "página X de Y", marcadores de navegação, faixa nunca órfã, cabeçalho de tabela repetido. Se o HTML ganhar recursos novos, replique no ReportLab.
- Limite conhecido: o ReportLab de código aberto não gera PDF marcado (acessível). O WeasyPrint atual também não está configurado para isso, então não há regressão; registrar como evolução.
