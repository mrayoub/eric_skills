# Plan 011: Exigir que todo Learning Card completo aponte para o Test Card executado

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- _DESIGN_SYSTEM/contracts/learning-card.schema.json _SAMPLES_ENTREGAVEIS/learning_card _DESIGN_SYSTEM/scripts/validators`
> `validators/` deve existir (plano 005). Se não existir, STOP (dependência não cumprida).

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 005 (gancho `validators/`), 001 (sync)
- **Category**: bug
- **Planned at**: commit `35c3b75`, 2026-09-28

## Why this matters

A skill `experimentacao-inovacao` exige "um Learning Card individual por Test Card
executado, **ligado ao ID e à versão do Test Card**". Mas o contrato do Learning Card não
tem campo para essa ligação: um card completo pode ser renderizado sem dizer que teste o
originou, e a cadeia hipótese → teste → aprendizado se perde nos arquivos. Esta é a
parte da "rastreabilidade executável" que vale automatizar: é estrutural, barata e
inequívoca. (O resto — se a evidência realmente sustenta a conclusão — continua sendo
julgamento do modelo; foi rejeitado automatizar, ver `plans/README.md`.)

## Current state

- `_DESIGN_SYSTEM/contracts/learning-card.schema.json`: envelope + exatamente 4 blocos em
  ordem `hypothesis`, `observations` (exige `citation_ids` ≥ 1), `learning`, `action`.
  Nenhuma exigência em `metadata`.
- Envelope `deliverable-content.schema.json`: `metadata` é objeto com `additionalProperties: true`.
- `render.py` `validate()` exige `metadata.artifact_id` e `metadata.content_version`
  (strings seguras para nome de arquivo) — Test Cards também os têm; portanto o ID e a
  versão de um Test Card são `artifact_id` e `content_version` do JSON dele.
- Amostra: `_SAMPLES_ENTREGAVEIS/learning_card/input.json`, `metadata = {"artifact_id": "sample-learning-card", "content_version": "1.0.0", "completeness": "complete", "orientation": "portrait", "sample": true}`.
  Amostra de Test Card: `_SAMPLES_ENTREGAVEIS/test_card/input.json` (`artifact_id` "sample-test-card", confira).
- Teste existente que monta Learning Card completo: `test_render.py::test_complete_cards_require_four_fields_and_learning_evidence` (usa helper `content()` cujo `metadata` não tem os campos novos — precisará ser ajustado).

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Testes | `python3 -m pytest -q _DESIGN_SYSTEM/tests` | 0 failed |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |

## Scope

**In scope**: `learning-card.schema.json`; `_DESIGN_SYSTEM/scripts/validators/learning_card.py` (criar); `_DESIGN_SYSTEM/tests/test_render.py` e `test_validators.py`; `_SAMPLES_ENTREGAVEIS/learning_card/input.json` + derivados; `_DESIGN_SYSTEM/README.md` (1 frase); `experimentacao-inovacao/assets/learning-card.md` (1 linha de cabeçalho, se o modelo tiver área de metadados); cópias via sync.

**Out of scope**: Test Card schema; outros tipos; qualquer validação de "a evidência sustenta a conclusão".

## Git workflow

Branch `advisor/011-learning-card-link`. Um commit.

## Steps

### Step 1: Schema

Em `learning-card.schema.json`, no objeto do `allOf` que já fixa `deliverable_type`,
acrescente:

```json
"metadata": {"type": "object", "required": ["test_card_id", "test_card_version"],
  "properties": {"test_card_id": {"type": "string", "minLength": 1},
                 "test_card_version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"}}}
```

(Só se aplica a cards completos, porque `render.py` só usa o schema específico quando `completeness == "complete"`.)

### Step 2: Validador

`validators/learning_card.py`: `validate(content)` retorna erro se
`metadata.test_card_id == metadata.artifact_id` (card apontando para si mesmo) e se
algum `citation_ids` do bloco `observations` não existir — este último já é coberto pelo
render; então implemente só a autorreferência. Mantenha o arquivo curto.

### Step 3: Amostra e testes

- Amostra: acrescente `"test_card_id": "<artifact_id da amostra de test_card>", "test_card_version": "1.0.0"` ao `metadata`; regenere os derivados da pasta (`--formats html,pdf,docx,md,txt`, sem `pdf` se faltar backend).
- Em `test_render.py::test_complete_cards_require_four_fields_and_learning_evidence`, acrescente os dois campos ao `learning["metadata"]` antes da renderização que deve passar, e um caso sem eles que deve falhar com `Conteúdo inválido`.
- Em `test_validators.py`: autorreferência → erro.
- Mostre a ligação nos derivados. Hoje `artifact_id`/`content_version` aparecem só no rodapé do HTML/PDF (`render.py:424` `footer_label = (f'ID {meta["artifact_id"]} · versão {meta["content_version"]} · '` e `render.py:433` `<footer class="meta">…`). Quando `deliverable_type == "learning_card"` e houver `test_card_id`, acrescente ` · Test Card {test_card_id} v{test_card_version}` nesses dois rodapés (com `html.escape` no segundo, como já é feito). Em `render_md`, logo após o título, acrescente a linha `Test Card: <id> v<versão>` + linha em branco, só para Learning Cards. No DOCX, um parágrafo com o mesmo texto logo após o título. Teste: o `.md` da amostra contém `Test Card: sample-test-card v1.0.0`.

**Verify**: `python3 -m pytest -q _DESIGN_SYSTEM/tests` → 0 failed; `grep -c "test_card_id" _SAMPLES_ENTREGAVEIS/learning_card/input.json` → `1`.

### Step 4: Documentar e sincronizar

No `_DESIGN_SYSTEM/README.md`, na frase que descreve os cards completos, acrescente:
"O Learning Card completo exige `metadata.test_card_id` e `metadata.test_card_version`, iguais ao `artifact_id` e `content_version` do Test Card executado."

**Verify**: `sync --check` → 0.

## Test plan

Casos: com ligação → passa; sem ligação (completo) → falha; parcial sem ligação → passa; autorreferência → falha.

## Done criteria

- [ ] 4 casos acima passam
- [ ] Amostra atualizada e regenerada
- [ ] README do DS atualizado; `sync --check` → 0
- [ ] `plans/README.md` atualizado

## STOP conditions

- Existirem Learning Cards completos fora das amostras (`grep -rl '"deliverable_type": "learning_card"' --include=*.json . | grep -v "_SAMPLES_ENTREGAVEIS\|/assets/"`) — eles deixariam de renderizar; liste e pergunte.

## Maintenance notes

- Se um dia houver um "índice da rodada" (experiment_report) com lista de pares Test/Learning Card, a checagem cruzada (todo Test Card executado tem Learning Card) pode ir para `validators/experiment_report.py`.
