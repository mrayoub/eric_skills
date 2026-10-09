# Plan 045: Garantir que PDF e PPTX mostrem todo o conteúdo que HTML, MD e DOCX mostram

> **Executor instructions**: Siga passo a passo; rode cada verificação; pare nas STOP conditions; atualize `plans/README.md`.
>
> **Drift check**: `git diff --stat 595f3b0..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/scripts/pdf_reportlab.py _DESIGN_SYSTEM/validators _DESIGN_SYSTEM/tests/test_render.py`

## Status

- **Priority**: P1 · **Effort**: M · **Risk**: MED (muda contagem de páginas em alguns casos) · **Depends on**: none · **Category**: bug
- **Planned at**: commit `595f3b0`, 2026-10-09

## Why this matters

A auditoria reproduziu perdas silenciosas de conteúdo, só no PDF ou no PPTX, para conteúdo válido pelo schema:

1. **One-page do briefing** (`pdf_reportlab.py`, `_render_one_page_layout`, ~linhas 720–760): o laço percorre os slots
   do `layout.json`; bloco sem slot correspondente não é desenhado; dentro do slot só saem `title`, `description`/`text`,
   `points`/`items` e tabela sem `rows` — `value` de métrica, `rows` de tabela e `cards` somem; citações só vão junto
   de `description`/`text`. Sem os slots `titulo_documento`/`identificacao_versao`, cai em silêncio no caminho antigo.
2. **Tabelas nos relatórios em PDF** (`_report_table`, `pdf_reportlab.py:198`): `ncols = max(1, len(headings))` — colunas
   além do cabeçalho somem; sem cabeçalho, só a primeira coluna aparece. Os outros formatos usam a linha mais larga
   (`block_flowables`, `render_pptx`, `render_docx`).
3. **Tabelas na apresentação**: o PPTX divide em blocos de 8 linhas, mas o PDF põe a tabela inteira num slide e aborta
   com `PdfOverflow` — e como o PDF é gerado antes de MD/DOCX/PPTX (`render.py` `main`), nenhum formato é entregue.
   O validador `validators/executive_presentation.py` não conta células de tabela; o PPTX usa altura fixa de 0,45 pol
   por linha e pode transbordar com células longas.
4. **Card com campo `heading`** em DOCX (`render_docx`, ~`render.py:753`): vira um segundo título com faixa, enquanto
   PDF/HTML/MD mostram como texto do campo.

Os testes atuais cobrem só o caminho feliz (cada amostra tem um bloco por slot; tabelas com cabeçalho do tamanho das linhas).

## Steps

1. **Teste de paridade primeiro** (`test_render.py`, nova classe `FormatParityTests`): para `briefing_one_page`,
   `four_d_report` e `executive_presentation`, acrescente à amostra blocos extras (parágrafo sem `section_key`, métrica
   só com `value`, tabela "irregular" com linhas mais largas que o cabeçalho, bloco só com `points` e `citation_ids`) e
   verifique que cada texto único aparece em HTML, MD, DOCX, PPTX (quando aplicável) e PDF. Use `completeness: partial`
   onde o validador de apresentação bloquear. **Ele deve falhar hoje** — guarde a saída.
2. **One-page:** blocos sem slot vão para uma área de continuação ou geram `PdfOverflow`/`ValueError` nomeando os
   blocos (escolha: erro explícito; documente). Use `block_text`/`table_rows` do renderizador para `value`, `content`,
   `rows`; aplique `_cited` em todo bloco com `citation_ids`. Sem os slots obrigatórios, erro em vez de fallback silencioso.
3. **Tabelas de relatório:** `ncols = max(1, len(headings), *(len(row) for row in rows))`; se `iqb_widths[slug]` não tiver
   `ncols` posições, use larguras iguais.
4. **Apresentação:** extraia uma função de paginação de linhas (8 por slide, cabeçalho repetido, título "(continuação)")
   usada pelo PPTX e pelo PDF; no PPTX, divida também quando a altura estimada (caracteres por célula ÷ largura) passar
   da área do corpo. No validador, conte as palavras das células de tabela.
5. **DOCX:** campo de card enviado como `heading` vira parágrafo sob o rótulo, como em MD.
6. Ajuste `test_page_count_and_size_match_pptx` se a contagem mudar; rode a suíte.

## Done criteria

- [x] `FormatParityTests` falhava antes e passa · [x] tabela irregular completa no PDF · [x] apresentação com 20 linhas entrega PDF e PPTX · [x] suíte `0 failed` (196 testes, 1.511 subtestes antes do último ajuste de cards; 29 testes PDF focados passaram após o ajuste) · [x] sync, fontes e catálogo em dia (`--bump`)

## STOP conditions

- Alguma amostra passa a falhar no portão de qualidade do PDF depois da mudança.
- A paginação no PDF exigiria mudar o `layout.json` da apresentação.
