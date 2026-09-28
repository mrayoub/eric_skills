# Plan 002: Fazer `table_rows` buscar valores pela chave da coluna, não pelo rótulo

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tests/test_render.py`
> Se houver mudança (esperado apenas se os planos 005/006/007 já rodaram), compare o
> trecho de "Current state" com o arquivo vivo; se a função `table_rows` não
> contiver mais as linhas citadas, STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: plans/001-baseline-sync-e-limpeza.md (usa `_TOOLS/sync_shared.py`)
- **Category**: bug
- **Planned at**: commit `35c3b75`, 2026-09-28

## Why this matters

O renderizador (`render.py`) gera PDF, HTML, DOCX, MD, TXT, PPTX e CSV a partir de um
JSON canônico. Quando uma tabela declara colunas como objetos `{key, label}` e linhas
como objetos, o código converte as colunas para o **rótulo** e depois usa esse rótulo
para buscar o valor na linha. Resultado: células vazias sem erro nenhum — perda
silenciosa de dados em todos os formatos. Reproduzido em 2026-09-28:

```
table_rows({"data":{"columns":[{"key":"count","label":"Quantidade"}],"rows":[{"count":12}]}})
→ (['Quantidade'], [['']])      # esperado: (['Quantidade'], [['12']])
```

## Current state

- `_DESIGN_SYSTEM/scripts/render.py` — renderizador; fonte da verdade (as cópias em
  `<skill>/assets/design-system/` são geradas por `_TOOLS/sync_shared.py`, plano 001).
- `_DESIGN_SYSTEM/scripts/render.py:126-153` (função `table_rows`), trecho relevante:

```python
    headers = data.get("headers") or data.get("columns") or []
    headers = [str(h.get("label", h.get("key", ""))) if isinstance(h, dict) else str(h) for h in headers]
    raw_rows = data.get("rows") or []
    if raw_rows and not headers and isinstance(raw_rows[0], dict):
        headers = list(raw_rows[0])
    rows: list[list[str]] = []
    for row in raw_rows:
        if isinstance(row, list):
            rows.append([str(x) if x is not None else "" for x in row])
        elif isinstance(row, dict):
            rows.append([str(row.get(h, "")) for h in headers] if headers else [str(v) for v in row.values()])
```

- `table_rows` é chamada em 5 lugares (`render.py:324` HTML, `:460` MD, `:537` DOCX,
  `:617` PPTX, `:643` CSV) — todos consomem `(headers, rows)`; a correção num lugar
  resolve todos.
- O ramo `if isinstance(data.get("dimensions"), dict)` no início da função (IQB) NÃO faz
  parte deste plano (plano 006).
- Testes: `_DESIGN_SYSTEM/tests/test_render.py`, estilo `unittest.TestCase` rodado via
  pytest. Os testes existentes chamam o script por subprocess; para teste unitário
  de função, importe o módulo com `importlib` (o arquivo já importa `importlib.util`,
  sem uso).

## Commands you will need

| Purpose | Command (na raiz) | Expected |
|---|---|---|
| Testes | `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py` | novos testes passam; 2 falhas pré-existentes só por `pango` são aceitáveis até o plano 007 |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |

## Scope

**In scope**: `_DESIGN_SYSTEM/scripts/render.py` (só `table_rows`, parte não-IQB);
`_DESIGN_SYSTEM/tests/test_render.py`; cópias geradas via sync.

**Out of scope**: ramo `dimensions` (IQB); qualquer schema; `block_text`.

## Git workflow

Branch `advisor/002-table-rows`. Um commit: `Corrige busca de coluna por chave em table_rows`.

## Steps

### Step 1: Escrever os testes que falham

Em `test_render.py`, adicione uma classe `TableRowsTests(unittest.TestCase)` que
carrega o módulo:

```python
spec = importlib.util.spec_from_file_location("render", SCRIPT)
render = importlib.util.module_from_spec(spec); spec.loader.exec_module(render)
```

Casos:
1. `columns=[{"key":"count","label":"Quantidade"}]`, `rows=[{"count":12}]` → headers `["Quantidade"]`, rows `[["12"]]`.
2. Colunas reordenadas: `columns=[{"key":"b","label":"B"},{"key":"a","label":"A"}]`, `rows=[{"a":1,"b":2}]` → `[["2","1"]]`.
3. Zero e falso preservados: `rows=[{"count":0}]` → `[["0"]]`; `{"count": False}` → `[["False"]]`.
4. Campo ausente: `rows=[{}]` → `[[""]]` (vazio, sem inventar valor).
5. Cabeçalhos simples continuam: `headers=["Medida","Valor"]`, `rows=[["Casos","12"]]` → inalterado.
6. Linha objeto com `headers` de strings que são as chaves: `headers=["x"]`, `rows=[{"x":"v"}]` → `[["v"]]`.
7. Coluna `{"key":"k"}` sem label → header `"k"`.

**Verify**: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py -k TableRows` → casos 1, 2 e 3 FALHAM (confirma o bug); demais passam.

### Step 2: Corrigir

Separe duas listas: `keys` (para buscar) e `headers` (para exibir):

```python
columns = data.get("headers") or data.get("columns") or []
keys = [str(h.get("key", h.get("label", ""))) if isinstance(h, dict) else str(h) for h in columns]
headers = [str(h.get("label", h.get("key", ""))) if isinstance(h, dict) else str(h) for h in columns]
```

Na linha dict use `row.get(k)` com `keys`; converta `None`/ausente em `""` e qualquer
outro valor com `str(value)` (assim `0` → `"0"`, `False` → `"False"`). Quando não há
colunas e a primeira linha é dict, `keys = headers = list(raw_rows[0])`.

**Verify**: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py -k TableRows` → todos passam.

### Step 3: Regressão e sync

**Verify**:
- `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py` → nenhuma falha nova além das de `pango`.
- `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check; echo $?` → `0`.
- `grep -c "keys = " workshop-4d/assets/design-system/scripts/render.py` → `≥1`.

## Test plan

Os 7 casos do Step 1, em `TableRowsTests` dentro de `_DESIGN_SYSTEM/tests/test_render.py`.

## Done criteria

- [ ] Os 7 testes passam
- [ ] Nenhuma falha nova na suíte
- [ ] `sync_shared.py --check` sai 0
- [ ] `git diff --stat` mostra só `render.py` (fonte + 11 cópias) e `test_render.py`
- [ ] `plans/README.md` atualizado

## STOP conditions

- A correção exigir mudar o ramo `dimensions` ou outro chamador de `table_rows`.
- Alguma amostra em `_SAMPLES_ENTREGAVEIS/*/input.json` usar `columns` como dict com
  `label` igual a um valor que dependia do comportamento antigo (verifique com
  `grep -l '"columns"' _SAMPLES_ENTREGAVEIS/*/input.json`); se existir, reporte antes
  de regenerar.

## Maintenance notes

- O plano 006 reescreve o ramo IQB desta mesma função; ele deve preservar estes testes.
- Revisor: confira que valores `0`/`False` não viram vazio.
