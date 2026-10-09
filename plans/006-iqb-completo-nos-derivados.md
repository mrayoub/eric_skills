# Plan 006: Levar notas, vetos, justificativas e auditoria do IQB a todos os formatos gerados

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- _DESIGN_SYSTEM/scripts/render.py`
> Mudanças dos planos 002/005/007 são esperadas. Confirme que `table_rows` ainda começa
> com o ramo `if isinstance(data.get("dimensions"), dict):` citado abaixo e que os 5
> chamadores existem (`grep -n "table_rows(block)" _DESIGN_SYSTEM/scripts/render.py` → 5 linhas). Senão, STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (mexe nos 5 renderizadores)
- **Depends on**: 001 (sync), 002 (mesma função; evite conflito)
- **Category**: bug
- **Planned at**: commit `967749d`, 2026-09-28

## Why this matters

O relatório de validação do briefing (IQB) é auditável no JSON: para cada dimensão ele
guarda contagem de "sim", nota bruta, veto, nota final, rótulo, justificativa, e ainda
a auditoria de agrupamento e a citação de cada critério. Mas os arquivos que a pessoa
lê (PDF, DOCX, HTML, MD, TXT, PPTX, CSV) mostram só uma matriz de 40 respostas. Quem
recebe o PDF não consegue ver por que a nota é aquela nem que um veto a limitou. O
objetivo é equivalência de conteúdo: tudo que é obrigatório no JSON aparece nos derivados.

## Current state

- `_DESIGN_SYSTEM/scripts/render.py:126-135` — ramo IQB de `table_rows`:

```python
def table_rows(block: dict[str, Any]) -> tuple[list[str], list[list[str]]]:
    data = block.get("data", {})
    if isinstance(data.get("dimensions"), dict):
        rows = []
        for dimension, detail in data["dimensions"].items():
            for item in detail.get("items", []):
                rows.append([dimension, str(item.get("criterion_id", "")),
                             str(item.get("answer", "")), str(item.get("evidence", "")),
                             str(item.get("evidence_source", ""))])
        return ["Dimensão", "Critério", "Resposta", "Evidência", "Fonte"], rows
```

  Descarta: `yes_count`, `raw_score`, `final_score`, `label`, `veto_item_id`,
  `veto_max_score`, `veto_triggered`, `veto_detail`, `justification` (por dimensão),
  `items[].citation_id` e todo `data.anti_clustering`.
- Os 5 chamadores e o que fazem com `(headers, rows)`:
  - `render.py:324` `html_block` → uma `<table>` (classe `scores` se houver `dimensions`), caption = `data.title`.
  - `render.py:460` `render_md` → tabela Markdown.
  - `render.py:537` `render_docx` → `doc.add_table` estilo "Table Grid".
  - `render.py:617` `render_pptx` → texto `" | "` fatiado em blocos de 650 caracteres.
  - `render.py:643` `write_csv_tables` → um CSV por bloco com `export.csv`, nome `{stem}-{variant_key}.csv`.
- Estrutura do bloco IQB: veja `_DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json`,
  `$defs.scoresBlock` e `$defs.dimensionAssessment`. Amostra completa real:
  `_SAMPLES_ENTREGAVEIS/briefing_validation/input.json` (bloco `id: "scores"`; sem `export`;
  `anti_clustering = {"triggered": false, "original_scores": null, "span": 2, "re_evaluation_notes": null}`).
- Rótulos amigáveis a usar: `clarity`→"Clareza", `evidence`→"Evidências",
  `outcomes`→"Resultados", `actionability`→"Acionabilidade"; `True`→"Sim", `False`→"Não".
- Testes: `_DESIGN_SYSTEM/tests/test_render.py` (unittest + subprocess; ver `RenderTests.render`).

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Testes | `python3 -m pytest -q _DESIGN_SYSTEM/tests` | all pass (falhas só de `pango` toleradas se 007 não rodou) |
| Render amostra | `python3 _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/briefing_validation/input.json --out-dir "$TMPDIR/bv" --formats html,md,txt,docx` | exit 0 |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |

## Scope

**In scope**: `_DESIGN_SYSTEM/scripts/render.py` (nova função `table_views` + 5 chamadores);
`_DESIGN_SYSTEM/tests/test_render.py`; derivados de `_SAMPLES_ENTREGAVEIS/briefing_validation/`; cópias via sync.

**Out of scope**: schemas; validação (plano 005); aparência (cores/tokens/CSS além de reaproveitar a classe `scores`); outros tipos de entregável.

## Git workflow

Branch `advisor/006-iqb-derivados`. Commits: (1) `table_views` + testes; (2) chamadores; (3) amostras regeneradas.

## Steps

### Step 1: Teste que falha

Em `test_render.py`, novo teste `test_iqb_derivatives_keep_scores_vetoes_and_audit`:
carregue a amostra `ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json"`
(skip se ausente), acrescente `"citation_id": "FIC-01"` ao item `CLA-01` (o ID `FIC-01`
existe em `citations` da amostra), grave num diretório temporário, renderize
`md,docx,html,txt` e verifique, em **cada** formato (DOCX: concatene texto de
parágrafos e de células de tabelas):

- os 40 IDs (`CLA-01` … `ACT-10`);
- a string `Nota bruta` e `Nota final`;
- a `justification` da dimensão `clarity` (texto da amostra);
- `Auditoria de agrupamento` e `Amplitude: 2` (ou o `span` da amostra);
- o texto `FIC-01` na linha do critério `CLA-01`.

**Verify**: o teste falha (hoje "Nota bruta" não aparece).

### Step 2: Criar `table_views(block)`

Nova função logo abaixo de `table_rows`:

```python
def table_views(block: dict[str, Any]) -> list[tuple[str, str, list[str], list[list[str]]]]:
    """Retorna [(slug, legenda, cabeçalhos, linhas)]. Um item para tabelas comuns; três para o IQB."""
```

- Tabela comum (sem `dimensions`): `[("", data.get("title",""), *table_rows(block))]`.
- IQB (`dimensions` dict): três vistas, nesta ordem:
  1. `("criterios", "Critérios avaliados", ["Dimensão","Critério","Resposta","Evidência","Fonte","Citação"], …)`
     — Resposta "Sim"/"Não"; marque o item de veto com sufixo `" (veto)"` no Critério; Citação = `citation_id` ou `""`.
  2. `("dimensoes", "Notas por dimensão", ["Dimensão","Sim (de 9)","Nota bruta","Veto","Teto do veto","Nota final","Rótulo","Justificativa"], …)`
     — Veto: `"Disparado: <veto_detail>"` ou `"Não disparado"`.
  3. `("agrupamento", "Auditoria de agrupamento", ["Campo","Valor"], …)` com linhas
     `Disparada` (Sim/Não), `Amplitude` (span), `Notas originais` (lista ou "—"),
     `Notas da reavaliação` (texto ou "—").
- Mantenha `table_rows` funcionando para chamadores externos, mas faça o ramo IQB
  delegar para a vista 1 (para não haver duas lógicas).

**Verify**: `python3 -c "import importlib.util as u;s=u.spec_from_file_location('r','_DESIGN_SYSTEM/scripts/render.py');m=u.module_from_spec(s);s.loader.exec_module(m);import json;d=json.load(open('_SAMPLES_ENTREGAVEIS/briefing_validation/input.json'));b=[x for x in d['blocks'] if x['id']=='scores'][0];print([v[0] for v in m.table_views(b)], len(m.table_views(b)[0][3]))"` → `['criterios', 'dimensoes', 'agrupamento'] 40`.

### Step 3: Trocar os 5 chamadores para iterar sobre `table_views`

- HTML: uma `<table>` por vista, cada uma com `<caption>` (legenda; na primeira use `data.title` se houver). Classe `scores` nas três vistas IQB. Citações do bloco (`refs`) só depois da última tabela.
- MD: para cada vista, `### <legenda>` (se não vazia) + tabela. Escape `|` nas células (`.replace("|","\\|")`) — hoje não escapa; justificativas podem conter `|`.
- DOCX: uma tabela por vista, com um parágrafo de legenda antes (quando houver).
- PPTX: concatene as vistas no texto do bloco, cada uma precedida da legenda.
- CSV: para cada vista, arquivo `{stem}-{variant}.csv` na primeira e `{stem}-{variant}-{slug}.csv` nas demais (só se o bloco tiver `export.csv`).

**Verify**: `python3 -m pytest -q _DESIGN_SYSTEM/tests` → o teste do Step 1 passa; nenhum teste antigo quebra (inclusive os do plano 002, se já existirem).

### Step 4: Regenerar a amostra e inspecionar

`python3 _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/briefing_validation/input.json --out-dir _SAMPLES_ENTREGAVEIS/briefing_validation --formats html,pdf,docx,md,txt`
(sem `pdf` se o plano 007 não rodou e faltar `pango`; anote no status).

**Verify**:
- `grep -c "Nota final" _SAMPLES_ENTREGAVEIS/briefing_validation/sample-briefing-validation-v1.0.0.md` → `≥1`
- `grep -c "ACT-10" _SAMPLES_ENTREGAVEIS/briefing_validation/sample-briefing-validation-v1.0.0.txt` → `≥1`
- Se gerou PDF: `python3 -c "from pypdf import PdfReader;r=PdfReader('_SAMPLES_ENTREGAVEIS/briefing_validation/sample-briefing-validation-v1.0.0.pdf');t=''.join(p.extract_text() for p in r.pages);print('Nota final' in t, 'Auditoria de agrupamento' in t)"` → `True True`

### Step 5: Sync

**Verify**: `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check; echo $?` → `0`.

## Test plan

- `test_iqb_derivatives_keep_scores_vetoes_and_audit` (Step 1).
- `test_md_escapes_pipes`: tabela comum com célula `"a|b"` → a linha MD contém `a\|b`.
- Rode toda a suíte para garantir que os testes de 002 continuam verdes.

## Done criteria

- [ ] Suíte do DS sem falhas novas; 2 testes novos passam
- [ ] Amostra IQB regenerada contém "Nota bruta", "Nota final", "Auditoria de agrupamento" e os 40 IDs em MD, TXT, HTML e DOCX
- [ ] `sync_shared.py --check` → 0
- [ ] `plans/README.md` atualizado

## STOP conditions

- O PDF da amostra ficar com texto cortado ou fonte menor que 7,5 pt (abra o PDF; se a
  tabela de 8 colunas não couber em A4 retrato, reporte — pode ser preciso mudar a
  vista 2 para layout de cards, o que é decisão de design).
- Algum outro tipo de entregável usar `data.dimensions` (`grep -l '"dimensions"' _SAMPLES_ENTREGAVEIS/*/input.json` deve listar só `briefing_validation`).

## Maintenance notes

- `table_views` é o ponto único para tabelas compostas; se outro tipo precisar de mais de uma vista, adicione um ramo lá.
- O revisor deve abrir o PDF/DOCX da amostra e conferir visualmente a legibilidade da tabela de 8 colunas.
