# Plan 004: Dar ao cálculo do IQB uma linha de comando e testes de regressão

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- avaliacao-briefing-iqb/scripts avaliacao-briefing-iqb/SKILL.md`
> Mudança → compare com "Current state"; divergência = STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (usa `_TESTS/` criado no plano 003; crie a pasta se não existir)
- **Category**: dx
- **Planned at**: commit `35c3b75`, 2026-09-28

## Why this matters

A skill `avaliacao-briefing-iqb` diz "Use `scripts/iqb.py` para contagens, vetos,
média e classificação", mas o módulo não tem ponto de entrada: rodá-lo não faz nada.
O modelo precisa escrever um wrapper Python a cada uso para chamar
`calculate_iqb_from_evaluations`, o que gera variação e erros (ex.: usar
`calculate_iqb` direto e pular a validação dos 40 itens). Uma CLI determinística
transforma o cálculo num passo único e auditável. O cálculo em si está correto e
não deve mudar.

## Current state

- `avaliacao-briefing-iqb/scripts/iqb.py` (316 linhas). Docstring (linhas 1–6) ainda
  cita o nome antigo: "fonte de verdade executável da skill ``validate-briefing``".
- Função pública principal `calculate_iqb_from_evaluations(evaluations)` (linha 160):
  entrada `{"clarity":[10 itens], "evidence":[...], "outcomes":[...], "actionability":[...]}`,
  cada item `{"criterion_id":"CLA-01","answer":true,"evidence":"…"}`. Valida via
  `_validate_complete_evaluations` (linha 194): exatamente 10 itens, IDs `PREFIX-01..10`,
  `answer` booleano, `evidence` não vazia. Levanta `ValueError` em qualquer falha.
- Vetos: `VETO_ITEM_IDS = {"clarity":"CLA-10","evidence":"EVI-06","outcomes":"OUT-10","actionability":"ACT-10"}`;
  tetos `VETO_MAX_SCORES = {"clarity":2,"evidence":1,"outcomes":2,"actionability":2}`.
  Veto dispara quando a resposta do item de veto **não** é `True`.
- Retorno: `scores` (por dimensão: `yes_count`, `raw_score`, `final_score`, `label`,
  `veto_triggered`, `veto_item_id`, `veto_max_score`), `iqb_score`, `classification`,
  `orientation`, `diagnosis`, `anti_clustering`, `span`, `tags`.
- Registro anterior (`VALIDACAO_ERIC_RC6.md`) afirma: 40 `no` → IQB 1; 40 `yes` → IQB 5;
  item ausente → erro. Use como casos de regressão.
- `avaliacao-briefing-iqb/SKILL.md:24` — "Use `scripts/iqb.py` para contagens, vetos, média e classificação."
- Exemplo de convenção de CLI: plano 003 (`score.py`) — mesmo formato: arquivo ou `-`,
  JSON no stdout, erro como `{"status":"error","error":...}` com exit 2.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Testes | `python3 -m pytest -q _TESTS/avaliacao-briefing-iqb` | all pass |
| CLI | `python3 avaliacao-briefing-iqb/scripts/iqb.py respostas.json` | JSON, exit 0 |

## Scope

**In scope**: `avaliacao-briefing-iqb/scripts/iqb.py` (docstring + `main()`);
`_TESTS/avaliacao-briefing-iqb/test_iqb.py` (criar); `avaliacao-briefing-iqb/SKILL.md` só a frase da linha 24 que cita o script.

**Out of scope**: tabelas de conversão, vetos, faixas e diagnósticos em `iqb.py`
(regra de negócio); `iqb-rubric.md`; schema do relatório.

## Git workflow

Branch `advisor/004-iqb-cli`. Commit: `Adiciona CLI ao iqb.py`.

## Steps

### Step 1: Testes de caracterização (antes de tocar no código)

Crie `_TESTS/avaliacao-briefing-iqb/test_iqb.py` (unittest, import por caminho com
`importlib.util`). Helper `answers(value)` que gera os 40 itens com `evidence="x"`.
Casos:
1. Todos `False` → `iqb_score == 1.0`, `classification == "Insuficiente"`.
2. Todos `True` → `iqb_score == 5.0`, `classification == "Excelente"`.
3. Remover `EVI-03` → `ValueError`.
4. `answer: "yes"` → `ValueError`.
5. `evidence: ""` → `ValueError`.
6. Veto: tudo `True` exceto `EVI-06=False` → `scores["evidence"]["final_score"] == 1`, `veto_triggered is True`.
7. Anti-agrupamento: todos `True` → `anti_clustering["triggered"] is True` (span 0).

**Verify**: `python3 -m pytest -q _TESTS/avaliacao-briefing-iqb` → 7 passed (caracteriza o comportamento atual; se algum falhar, STOP).

### Step 2: CLI e docstring

- Docstring: troque "da skill ``validate-briefing``" por "da skill ``avaliacao-briefing-iqb`` (adaptada de ``validate-briefing`` do ERIC_RC6)" e documente o formato de entrada com um exemplo de item.
- Acrescente `main()` e o guarda `if __name__ == "__main__": main()` no mesmo formato do plano 003: argumento `input` (arquivo ou `-`), chama `calculate_iqb_from_evaluations`, imprime JSON (`ensure_ascii=False, indent=2`); em `ValueError` imprime `{"status":"error","error":...}` e sai com 2. No sucesso, inclua `"status": "complete"` e `"rubric_version": IQB_RUBRIC_VERSION` no JSON impresso (sem alterar o dict retornado pela função).
- Teste 8: CLI via subprocess com o caso 2 → exit 0 e `"iqb_score": 5.0`; com o caso 3 → exit 2.

**Verify**: `python3 -m pytest -q _TESTS/avaliacao-briefing-iqb` → 8 passed.

### Step 3: Atualizar a instrução

Em `avaliacao-briefing-iqb/SKILL.md:24`, troque "Use `scripts/iqb.py` para contagens, vetos, média e classificação." por "Grave as 40 respostas em JSON (formato no topo de `scripts/iqb.py`) e rode `python3 scripts/iqb.py respostas.json` para contagens, vetos, média e classificação; copie os números do resultado, sem recalcular à mão."

**Verify**: `grep -c "python3 scripts/iqb.py" avaliacao-briefing-iqb/SKILL.md` → `1`; `quick_validate.py avaliacao-briefing-iqb` → `Skill is valid!`.

## Test plan

8 casos em `_TESTS/avaliacao-briefing-iqb/test_iqb.py`.

## Done criteria

- [ ] `python3 -m pytest -q _TESTS/avaliacao-briefing-iqb` → 8 passed
- [ ] `grep -n "validate-briefing" avaliacao-briefing-iqb/scripts/iqb.py` só aparece como origem ("adaptada de")
- [ ] `git diff avaliacao-briefing-iqb/scripts/iqb.py` não altera linhas das tabelas (`YES_COUNT_TO_RAW_SCORE`, `VETO_*`, `IQB_CLASSIFICATION`)
- [ ] `plans/README.md` atualizado

## STOP conditions

- Algum teste de caracterização do Step 1 falhar — o cálculo não é o que o plano supõe.

## Maintenance notes

- O plano 005 replica as tabelas do IQB num validador do design system e adiciona um
  teste de paridade contra este arquivo; mudanças na rubrica exigem mudar ambos.
