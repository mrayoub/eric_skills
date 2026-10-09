# Correção do Plano 034 após revisão (05/10/2026)

> **Para o executor**: este documento complementa `plans/034-pdf-reportlab-relatorios.md`.
> Leia o plano original para contexto. Trabalhe no branch existente
> `advisor/034-pdf-reportlab-relatorios`. **Só comece depois que a correção do 033
> (`plans/033-correcao-pos-revisao.md`) estiver concluída**, porque este branch é
> construído sobre o 033. Rode cada verificação e confirme o resultado antes de seguir.
> Se uma STOP condition ocorrer, pare e reporte. Não faça push nem merge no `main`.

## O que a revisão encontrou

A estrutura está boa: os 14 relatórios renderizam, passam no portão de qualidade, têm
"página X de Y", marcadores de navegação, cabeçalho de tabela repetido e linhas alternadas.
A suíte passa (113 testes sem Pango; 119 com Pango). A comparação visual lado a lado
(`_TOOLS/compare_pdf_engines.py`) e a medição do texto extraído mostraram 4 problemas:

1. **Citações perdidas (rastreabilidade).** `_report_card_grid` em `pdf_reportlab.py` não
   renderiza o `citation_ids` do **bloco** `card_grid` — só o de cada cartão. No
   `four_d_report`, os 9 blocos `card_grid` têm `citation_ids: ["FIC-01"]`: o PDF do WeasyPrint
   mostra 12 marcas `[FIC-01]`, o do ReportLab, 3. O teste `test_report_text_is_complete` não
   pegou porque só verifica se o ID aparece em algum lugar, e ele aparece na lista "Fontes".
2. **Legenda separada da tabela.** No `four_d_report`, a legenda "O que a priorização permite
   concluir" fica no pé da página 2 e a tabela começa na página 3. Em `_report_table`, a
   legenda é seguida de um `Spacer` e nada a prende à tabela. O mesmo vale para o título de
   `card_grid` em `_report_card_grid`.
3. **Cartões desalinhados.** Em `_report_card_grid`, cada cartão é uma `Table` própria dentro
   de uma célula da linha; o fundo de cada cartão só tem a altura do próprio texto. Resultado:
   cartões da mesma linha com alturas diferentes (no `four_d_report`, "EVIDÊNCIA" fica mais
   baixo que "PERCEPÇÃO", "CAUSAS" e "LACUNA"). Além disso, o `RIGHTPADDING` de `gap` na
   última coluna faz a linha terminar antes da borda direita da faixa da seção.
4. **Passo 9 do plano não executado.** As cópias nas 11 skills não foram sincronizadas
   (`python3 _TOOLS/sync_shared.py --check` acusa `DIVERGE` em `pdf_reportlab.py`, `render.py`
   e nas fontes); o `_DESIGN_SYSTEM/README.md` não foi atualizado; a ajuda de `--pdf-engine`
   em `render.py` ainda diz "(prova: cards e one-page)"; a docstring de `pdf_reportlab.py`
   ainda diz "para cards e resumo do briefing em uma página".

Processo: o Plano 034 dependia da aprovação visual do operador para o 032, que não aconteceu
antes da execução. A aprovação dos dois será feita sobre o resultado desta correção.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Ambiente | `python3 -m venv /tmp/venv-034c && /tmp/venv-034c/bin/python -m pip install -q -r _DESIGN_SYSTEM/requirements.txt pytest pypdfium2 pdfplumber` | exit 0 |
| Testes | `/tmp/venv-034c/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` |
| Comparação | `/tmp/venv-034c/bin/python _TOOLS/compare_pdf_engines.py --out /tmp/cmp-034c` | exit 0 |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check && python3 _TOOLS/build_sources.py --check` | exit 0 |

Com WeasyPrint no macOS/Homebrew, se `pango-1.0-0` não carregar, prefixe com `DYLD_LIBRARY_PATH=/opt/homebrew/lib`.

## Scope

**In scope**: `_DESIGN_SYSTEM/scripts/pdf_reportlab.py`, `_DESIGN_SYSTEM/scripts/render.py`
(só o texto de ajuda de `--pdf-engine`), `_DESIGN_SYSTEM/tests/test_render.py`,
`_DESIGN_SYSTEM/README.md`, cópias do sync.
**Out of scope**: `pdf_quality.py`; HTML/CSS; cards e one-page (`card_portrait`,
`executive_one_page`); `executive_presentation`; `_SAMPLES_ENTREGAVEIS/`.

## Steps

### Step 0: Trazer a correção do 033

```
git switch advisor/034-pdf-reportlab-relatorios
git merge --no-edit advisor/033-verificador-qualidade-pdf
```
**Verify**: `git log --oneline -6` inclui "Exige que as 18 amostras passem no portão de qualidade"; suíte completa `0 failed`. Conflito → STOP.

### Step 1: Citações do bloco nas grades de cartões

Em `_report_card_grid`, depois da última linha de cartões, se `block.get("citation_ids")`,
acrescente `Paragraph(_cited("", block), styles["source"])` — o mesmo padrão que
`_report_table` já usa no fim da tabela. Confira os demais caminhos de `_report_block` e
`block_flowables`: todo bloco com `citation_ids` precisa produzir as marcas `[ID]` no PDF.

**Verify**: renderize `_SAMPLES_ENTREGAVEIS/four_d_report/input.json` com `--formats pdf --pdf-engine reportlab` e conte: `[FIC-01]` aparece **12** vezes no texto extraído (`pypdf`), como no WeasyPrint.

### Step 2: Legenda presa à tabela e título preso à grade

- Em `_report_table`: a legenda deixa de ser seguida por `Spacer`; use um estilo de legenda com `spaceAfter=4` e `keepWithNext=True` (ou `caption.keepWithNext = True`) para que ela nunca fique sem a primeira linha da tabela.
- Em `_report_card_grid`: o mesmo para o título da grade (`data.title`) em relação à primeira linha de cartões.

**Verify**: no `four_d_report` renderizado, o texto "O que a priorização permite concluir" está na mesma página que "Dimensão", primeiro cabeçalho da tabela que vem logo depois.

### Step 3: Cartões da mesma linha com a mesma altura e alinhados à faixa

Reescreva a montagem de cada linha em `_report_card_grid`:

- **uma única `Table`** por linha, com uma linha e `2 * colunas - 1` colunas: as colunas pares (`0, 2, 4…`) são cartões e as ímpares são espaçadores vazios de largura `gap`;
- cada célula de cartão recebe a lista de flowables do cartão (título, valor, texto, itens, citações do cartão);
- `TableStyle` por célula: `BACKGROUND` e `LINEBEFORE` (3 pt, cor do `tone`) só nas colunas de cartão; padding 9/9/7/7 nelas; padding 0 e sem fundo nos espaçadores;
- larguras: `card_width = (width - gap * (colunas - 1)) / colunas`, de modo que `soma das larguras == width` (a linha termina exatamente na borda da área);
- linhas incompletas (ex.: 3 cartões numa grade de 2 colunas na última linha) recebem células vazias sem fundo;
- mantenha `KeepTogether` por linha.

Como todas as células estão na mesma linha da tabela, o ReportLab dá a elas a mesma altura e os fundos ficam iguais.

**Verify**: no `four_d_report` renderizado, com `pdfplumber`, os retângulos preenchidos das cores dos cartões (`document_accent_soft`, `surface_muted`, `danger_soft`, `#E8F4EE`, `#FFF4D9`) que começam no mesmo `top` (± 1 pt) têm a mesma altura (± 1 pt); e o maior `x1` desses retângulos fica a até 1 pt do `x1` da faixa da seção.

### Step 4: Testes mais fortes

Em `ReportLabReportTests`:

1. `test_report_citation_markers_per_block`: para cada uma das 14 amostras, conte as referências esperadas = soma de `len(block["citation_ids"])` de todos os blocos + soma de `len(card["citation_ids"])` de todos os cartões; o número de ocorrências de `"[" + id + "]"` no texto extraído (somando todos os IDs) deve ser **maior ou igual** a esse total. (A lista "Fontes" usa `ID —`, sem colchetes, e não infla a contagem.)
2. `test_caption_never_orphan`: estenda `test_section_band_never_orphan` para que a última linha de texto de cada página também não seja uma legenda de tabela (`data.title` de blocos `table`) nem título de grade (`data.title` de `card_grid`), nos tipos `four_d_report` e `briefing_validation`.
3. `test_card_rows_equal_height`: a verificação do Step 3 como teste, no `four_d_report`.

Cada teste novo precisa **falhar** no código anterior às correções (confira com `git stash` das mudanças de `pdf_reportlab.py`, rodando só o teste) e passar depois.

**Verify**: `pytest -k ReportLabReport` → sem falhas; suíte completa `0 failed`.

### Step 5: Documentação, textos e sync (Passo 9 do plano original)

- `render.py`: ajuda de `--pdf-engine` → "motor do PDF; reportlab dispensa Pango (todos os tipos, exceto apresentação executiva)".
- `pdf_reportlab.py`: docstring do módulo → "PDF portátil em ReportLab para cards, resumo do briefing e relatórios."
- `_DESIGN_SYSTEM/README.md`: `--pdf-engine reportlab` cobre todos os tipos exceto `executive_presentation`.
- Rode o sync e as checagens.

**Verify**: `sync_shared.py --check` e `build_sources.py --check` → exit 0; `grep -c "prova: cards" _DESIGN_SYSTEM/scripts/render.py` → `0`.

### Step 6: Material para a aprovação visual

`_TOOLS/compare_pdf_engines.py --out /tmp/cmp-034c` e informe o caminho de `index.html` no relatório. Não marque o plano como DONE: a aprovação é do operador.

## Done criteria

- [ ] `[FIC-01]` aparece 12 vezes no PDF ReportLab do `four_d_report`
- [ ] Legenda "O que a priorização permite concluir" na mesma página da tabela
- [ ] Cartões da mesma linha com a mesma altura e linha alinhada à faixa
- [ ] 3 testes novos, cada um comprovadamente falhando antes da correção
- [ ] Suíte `0 failed`; sync e fontes → exit 0
- [ ] `/tmp/cmp-034c/index.html` gerado e informado

## STOP conditions

- A correção do 033 não está concluída, ou o merge do Step 0 conflita.
- Algum relatório passa a ser reprovado pelo portão de qualidade.
- Algum teste novo não falha no código antigo (o teste não estaria testando o defeito).
- Corrigir exigiria mexer em `pdf_quality.py`, no HTML/CSS ou nos layouts de card/one-page.
