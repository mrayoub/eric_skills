# Plan 005: Rejeitar IQB e potencial matematicamente incoerentes antes de gerar arquivos

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/contracts/innovation-potential-assessment.schema.json _DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json _SAMPLES_ENTREGAVEIS/briefing_validation/input.json _SAMPLES_ENTREGAVEIS/innovation_potential_assessment/input.json`
> Mudanças em `render.py` vindas dos planos 002/007 são esperadas; confira que a
> função `validate` ainda tem o trecho citado abaixo. Outras divergências = STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (relatórios antigos incoerentes deixarão de renderizar — é o objetivo, mas avise)
- **Depends on**: 001 (sync), 002 (tabela `columns`/`rows` por chave, usada no bloco de notas do potencial), 003 (regra de justificativa), 004 (testes do IQB)
- **Category**: bug
- **Planned at**: commit `35c3b75`, 2026-09-28

## Why this matters

O renderizador valida o JSON só por JSON Schema, que não sabe fazer contas. Hoje ele
aceita um relatório IQB com "IQB 1 — Excelente", critérios repetidos, nota final
acima do teto de veto ou citação interna inexistente, e produz PDF/DOCX com aparência
oficial. No potencial de inovação, o schema nem exige as cinco notas, pesos, total e
classe. Este plano adiciona uma **segunda camada de validação semântica por tipo de
entregável**, executada depois do schema e antes de escrever qualquer arquivo. Ela
recalcula e compara; nunca corrige silenciosamente.

## Current state

- `_DESIGN_SYSTEM/scripts/render.py:53-103` — `validate(content, profiles)`: checa
  perfil, `artifact_id`/`content_version`, orientação, `completeness`; roda o schema
  específico **apenas quando `completeness == "complete"`** (`render.py:79`):

```python
    schema_file = profile.get("schema") if meta.get("completeness", "complete") == "complete" else None
```

  Depois checa IDs de bloco únicos e citações de `block.citation_ids` e de
  `card_grid.cards[].citation_ids`. **Não** olha citações aninhadas em outros lugares
  de `data` (ex.: `data.dimensions.*.items[].citation_id` do IQB). Retorna `profile`.
- `ROOT = Path(__file__).resolve().parents[1]` (a pasta do design system). O módulo não
  é pacote (sem `__init__.py` em `scripts/`).
- Schema IQB `_DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json`:
  bloco `scores` (type `table`, `data.section_key="scores"`) com
  `data.dimensions.{clarity,evidence,outcomes,actionability}` — cada um com `items`
  (10 × `{criterion_id, answer:bool, evidence, evidence_source, citation_id?}`),
  `veto_item_id`, `veto_max_score`, `veto_triggered`, `veto_detail`, `yes_count`,
  `raw_score`, `final_score`, `label`, `justification`; e `data.anti_clustering`
  `{triggered, original_scores, span, re_evaluation_notes}`. Bloco `iqb`
  (type `metric`, `data.section_key="iqb"`) com `score` (1–5), `classification`,
  `diagnosis`.
- Regras do IQB (copie destes valores, que vêm de `avaliacao-briefing-iqb/scripts/iqb.py`):

```python
YES_COUNT_TO_RAW_SCORE = {9:5, 8:5, 7:4, 6:4, 5:3, 4:3, 3:2, 2:2, 1:1, 0:1}
RAW_SCORE_TO_LABEL = {5:"Excelente", 4:"Saudavel", 3:"Adequado", 2:"Fragil", 1:"Insuficiente"}
VETO_ITEM_IDS = {"clarity":"CLA-10","evidence":"EVI-06","outcomes":"OUT-10","actionability":"ACT-10"}
VETO_MAX_SCORES = {"clarity":2,"evidence":1,"outcomes":2,"actionability":2}
PREFIX = {"clarity":"CLA","evidence":"EVI","outcomes":"OUT","actionability":"ACT"}
# faixas do IQB (após round(média, 1)):
# 4.5–5.0 Excelente; 3.5–4.4 Saudavel; 2.5–3.4 Adequado; 1.5–2.4 Fragil; 1.0–1.4 Insuficiente
```

  Semântica: `yes_count` conta respostas `True` dos 9 itens que **não** são o veto;
  `veto_triggered = (resposta do item de veto) is not True`; `final = min(raw, teto)` se
  veto; `iqb = round(soma(finais)/4, 1)`; `span = max(finais) - min(finais)`;
  `anti_clustering.triggered = span <= 1`.
- Schema do potencial `_DESIGN_SYSTEM/contracts/innovation-potential-assessment.schema.json`:
  exige apenas blocos com `section_key` `impact`, `feasibility`, `alignment`, `urgency`,
  `novelty`, `recommendation` (cada um com `text`). **Não** exige notas estruturadas.
- Regras do potencial (de `potencial-inovacao/scripts/score.py`): chaves e pesos
  `impact` 0.30, `viability` 0.25, `strategic_alignment` 0.20, `urgency` 0.15,
  `innovation` 0.10; total = `round(Σ nota×peso, 1)`; `>=70` priorizar, `>=40` monitorar,
  senão arquivar. Mapeamento para os `section_key` narrativos do schema:
  `viability→feasibility`, `strategic_alignment→alignment`, `innovation→novelty`.
- Amostras (fictícias, `metadata.sample: true`): `_SAMPLES_ENTREGAVEIS/briefing_validation/input.json`
  (completa; clarity: yes_count 6 → raw 4 → final 4) e
  `_SAMPLES_ENTREGAVEIS/innovation_potential_assessment/input.json`, cujo bloco de notas hoje é:

```json
{"id": "scores", "type": "table", "data": {"title": "Pontuação ilustrativa, sem avaliação real", "headers": ["Critério", "Nota simulada"], "rows": [["Impacto", "60"], ["Viabilidade", "45"], ["Alinhamento", "70"], ["Urgência", "40"], ["Novidade", "55"]]}, "citation_ids": ["FIC-02"], "export": {"csv": true, "variant_key": "pontuacoes"}}
```

- Testes: `_DESIGN_SYSTEM/tests/test_render.py` (unittest; helper `content(kind, artifact)`
  cria um JSON mínimo; `self.render(item, formats, folder)` roda o script por subprocess).

## Commands you will need

| Purpose | Command (na raiz) | Expected |
|---|---|---|
| Testes DS | `python3 -m pytest -q _DESIGN_SYSTEM/tests` | all pass (exceto falhas só de `pango`, se o plano 007 não rodou) |
| Render amostra | `python3 _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/briefing_validation/input.json --out-dir "$TMPDIR/bv" --formats md` | exit 0 |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |

## Scope

**In scope**:
- `_DESIGN_SYSTEM/scripts/render.py` (só `validate` + constante `RENDERER_VERSION`)
- `_DESIGN_SYSTEM/scripts/validators/__init__.py`, `briefing_validation.py`, `innovation_potential_assessment.py` (criar)
- `_DESIGN_SYSTEM/contracts/innovation-potential-assessment.schema.json`
- `_DESIGN_SYSTEM/tests/test_validators.py` (criar)
- `_DESIGN_SYSTEM/README.md` (1 parágrafo)
- `_SAMPLES_ENTREGAVEIS/innovation_potential_assessment/input.json` (bloco `scores`) e regeneração dos derivados dessa pasta
- cópias via sync

**Out of scope**: `iqb.py` e `score.py` (não importe deles em tempo de execução — as
skills precisam continuar independentes; o design system não pode depender da pasta
de outra skill); schemas dos outros 16 tipos; `table_rows` (planos 002/006).

## Git workflow

Branch `advisor/005-validador`. Commits: (1) gancho + citações aninhadas; (2) IQB; (3) potencial + schema + amostra.

## Steps

### Step 1: Gancho de validadores por tipo + citações aninhadas

1. Crie `_DESIGN_SYSTEM/scripts/validators/__init__.py` com:

```python
"""Validadores semânticos por deliverable_type. Cada módulo expõe validate(content) -> list[str]."""
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent

def run(content: dict[str, Any]) -> list[str]:
    path = HERE / f"{content.get('deliverable_type', '')}.py"
    if not path.is_file():
        return []
    spec = importlib.util.spec_from_file_location(f"validators_{path.stem}", path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return list(module.validate(content))
```

2. Em `render.py`, função `validate`, depois do laço de blocos existente e antes de `return profile`:
   - **Citações aninhadas (sempre, inclusive parciais):** percorra recursivamente
     `block["data"]` coletando strings em chaves `citation_id` e listas em chaves
     `citation_ids`; qualquer ID fora de `citation_ids` do documento →
     `ValueError(f"{block['id']}: citações aninhadas inexistentes: {sorted(unknown)}")`.
   - **Semântica (só se `completeness` for `complete` ou ausente):** carregue
     `validators/__init__.py` por caminho (`ROOT / "scripts" / "validators" / "__init__.py"`, com
     `importlib.util`, pois `scripts/` não é pacote), chame `run(content)`; se a lista não
     for vazia → `ValueError("Inconsistência semântica: " + "; ".join(erros[:12]))`.
3. `RENDERER_VERSION = "1.3.0"`.

**Verify**: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py` → sem falhas novas.

### Step 2: Validador do IQB — `validators/briefing_validation.py`

Implemente `validate(content) -> list[str]` usando as constantes de "Current state".
Localize o bloco com `data.section_key == "scores"` e o bloco com `data.section_key == "iqb"`.
Para cada dimensão, produza mensagens com caminho preciso (ex.: `"scores.evidence.final_score: informado 3, calculado 1"`):

1. IDs dos 10 itens = exatamente `{PREFIX-01..PREFIX-10}`, sem repetição (reporte duplicados e faltantes).
2. `veto_item_id` e `veto_max_score` iguais às constantes.
3. `yes_count`, `raw_score`, `veto_triggered`, `final_score`, `label` iguais ao recalculado.
4. `iqb.score == round(média dos finais, 1)` e `iqb.classification` igual à faixa.
5. `anti_clustering.span` e `.triggered` iguais ao recalculado. **Não** compare
   `original_scores` nem `re_evaluation_notes` (reauditoria manual pode tê-los alterado).

Não altere o conteúdo; só retorne mensagens.

### Step 3: Testes do IQB — `_DESIGN_SYSTEM/tests/test_validators.py`

Base: carregue `_SAMPLES_ENTREGAVEIS/briefing_validation/input.json` (caminho
`ROOT.parent / "_SAMPLES_ENTREGAVEIS" / ...`; se o arquivo não existir, `skipTest`).
1. Amostra original → `run()` retorna `[]`.
2. `iqb.score = 1`, `classification = "Excelente"` → erros citando `iqb`.
3. Duplicar `CLA-01` no lugar de `CLA-02` → erro de ID (o schema aceita; o validador não).
4. Veto disparado com `final_score` acima do teto → erro.
5. `yes_count` adulterado → erro.
6. Via subprocess no `render.py`: amostra com `iqb.score` adulterado → exit ≠ 0 e stderr contém `Inconsistência semântica`.
7. Citação aninhada inexistente (`items[0].citation_id = "NAO-EXISTE"`) com `completeness: "partial"` → exit ≠ 0 e `citações aninhadas`.
8. **Paridade** (só no repositório de manutenção): carregue `ROOT.parent / "avaliacao-briefing-iqb/scripts/iqb.py"` por caminho (skip se ausente) e afirme que suas constantes `YES_COUNT_TO_RAW_SCORE`, `VETO_ITEM_IDS`, `VETO_MAX_SCORES`, `RAW_SCORE_TO_LABEL` são iguais às do validador.

**Verify**: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_validators.py` → 8 passed.

Se o caso 1 falhar, a amostra fictícia tem incoerência real: corrija **a amostra**
(`_SAMPLES_ENTREGAVEIS/briefing_validation/input.json`) para os valores calculados,
registre no commit qual campo mudou e regenere os derivados daquela pasta (ver Step 6).

### Step 4: Notas estruturadas do potencial — schema

Em `innovation-potential-assessment.schema.json`, dentro de `blocks.allOf`, acrescente
um `contains` exigindo exatamente um bloco:

- `type: "table"`, `data.section_key: "scores"`,
- `data.columns`: array (livre),
- `data.rows`: array de 5 objetos, cada um com `criterion` ∈ {`impact`,`viability`,`strategic_alignment`,`urgency`,`innovation`}, `score` (number 0–100, não boolean — JSON Schema `"type":"number"` já rejeita `true`), `weight` (number), `justification` (string minLength 1),
- `data.overall_score`: number 0–100, `data.classification` ∈ {`priorizar`,`monitorar`,`arquivar`}.

Mantenha as seis seções narrativas já exigidas.

### Step 5: Validador do potencial — `validators/innovation_potential_assessment.py`

Com o bloco `scores`: cinco critérios distintos; `weight` igual à tabela de pesos;
`overall_score == round(Σ score×peso, 1)`; `classification` igual à faixa;
`justification.strip()` não vazia. Adicione em `test_validators.py`: amostra nova
válida → `[]`; classe trocada → erro; peso trocado → erro; critério repetido → erro;
paridade de pesos e faixas com `potencial-inovacao/scripts/score.py` (`CRITERIA`), com skip se ausente.

### Step 6: Atualizar a amostra do potencial e regenerar

Substitua o bloco `scores` de `_SAMPLES_ENTREGAVEIS/innovation_potential_assessment/input.json` por:

```json
{"id": "scores", "type": "table", "data": {"section_key": "scores", "title": "Pontuação ilustrativa, sem avaliação real",
 "columns": [{"key": "label", "label": "Critério"}, {"key": "score", "label": "Nota"}, {"key": "weight", "label": "Peso"}, {"key": "justification", "label": "Justificativa"}],
 "rows": [
  {"criterion": "impact", "label": "Impacto", "score": 60, "weight": 0.30, "justification": "Retrabalho relatado; magnitude ainda não medida (exemplo)."},
  {"criterion": "viability", "label": "Viabilidade", "score": 45, "weight": 0.25, "justification": "Integração, responsáveis e custo são hipóteses (exemplo)."},
  {"criterion": "strategic_alignment", "label": "Alinhamento", "score": 70, "weight": 0.20, "justification": "Reduz esforço de atendimento (exemplo)."},
  {"criterion": "urgency", "label": "Urgência", "score": 40, "weight": 0.15, "justification": "Prioridade moderada, não comprovada (exemplo)."},
  {"criterion": "innovation", "label": "Novidade", "score": 55, "weight": 0.10, "justification": "Novidade relativa não comparada (exemplo)."}],
 "overall_score": 54.8, "classification": "monitorar"},
 "citation_ids": ["FIC-02"], "export": {"csv": true, "variant_key": "pontuacoes"}}
```

(Conta conferida pelo advisor em Python 3.12: `round(60*.30+45*.25+70*.20+40*.15+55*.10, 1)` → `54.8`. O validador deve calcular exatamente assim — soma na ordem dos critérios, depois `round(…, 1)` — igual a `score.py`.)

Regenere os derivados: `python3 _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/innovation_potential_assessment/input.json --out-dir _SAMPLES_ENTREGAVEIS/innovation_potential_assessment --formats html,pdf,docx,md,txt,csv`
(o nome `sample-innovation-potential-assessment-v1.0.0.*` é mantido; se o PDF falhar por `pango`, gere sem `pdf` e anote no status).

**Verify**: o `.md` gerado contém `Justificativa` e `Impacto | 60`.

### Step 7: Documentar e sincronizar

Acrescente ao `_DESIGN_SYSTEM/README.md`, seção "Uso pelas skills", item novo:
"5. Para `briefing_validation` e `innovation_potential_assessment` completos, o renderizador recalcula notas, vetos, totais e classes e rejeita o JSON se algum número divergir. Corrija o conteúdo com o resultado do script da skill (`iqb.py` ou `score.py`); não edite números à mão."

Rode o sync.

**Verify**: `python3 _TOOLS/sync_shared.py --check; echo $?` → `0`; `ls potencial-inovacao/assets/design-system/scripts/validators/` → 3 arquivos `.py`.

## Test plan

`_DESIGN_SYSTEM/tests/test_validators.py`: 8 casos IQB + 5 casos potencial, descritos acima. Padrão estrutural: `RenderTests` em `test_render.py`.

## Done criteria

- [ ] `python3 -m pytest -q _DESIGN_SYSTEM/tests` → todos os novos passam; nenhuma falha nova
- [ ] As duas amostras renderizam (`--formats md`) com exit 0
- [ ] IQB "1 — Excelente" renderiza com exit ≠ 0
- [ ] `sync_shared.py --check` → 0
- [ ] `grep -rn "avaliacao-briefing-iqb\|potencial-inovacao" _DESIGN_SYSTEM/scripts` → vazio (sem dependência de runtime entre skills; só os testes referenciam)
- [ ] `plans/README.md` atualizado

## STOP conditions

- `_OUTPUTS/` ou alguma pasta de projeto real contiver JSON de `briefing_validation`/`innovation_potential_assessment` que passaria a falhar: liste-os e pergunte antes (não os altere; o histórico não deve ser recalculado silenciosamente). Cheque: `grep -rl '"deliverable_type": "briefing_validation"\|"deliverable_type": "innovation_potential_assessment"' --include=*.json . | grep -v _SAMPLES_ENTREGAVEIS | grep -v /assets/`.
- A amostra IQB tiver mais de 3 campos incoerentes (sinal de que a regra entendida aqui difere da usada para gerá-la).
- O teste de paridade falhar (as regras copiadas divergem de `iqb.py`/`score.py`).

## Maintenance notes

- Duas cópias das regras (script da skill + validador) são intencionais, para manter
  as skills independentes; o teste de paridade é a trava. Mudança de rubrica = mudar
  os dois + versão de rubrica.
- Novos tipos ganham validação semântica criando `validators/<deliverable_type>.py`.
- O plano 011 usa este mesmo gancho para `learning_card`.
- Revisor: confirme que nenhum validador altera `content` (só lê).
