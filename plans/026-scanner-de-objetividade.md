# Plan 026: Scanner determinístico de objetividade (vocabulário absoluto e números sem citação)

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat 857d0b7..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/scripts/validators`
> Se algum desses arquivos mudou desde que este plano foi escrito, compare os
> trechos de "Current state" abaixo com o código atual antes de prosseguir; em
> caso de divergência, trate como condição de STOP.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt
- **Planned at**: commit `857d0b7`, 2026-10-02

## Por que isto importa

Nenhum mecanismo hoje verifica se o texto de um entregável é objetivo — os 3
validators semânticos existentes (`briefing_validation.py`,
`innovation_potential_assessment.py`, `learning_card.py`) checam estrutura e
consistência numérica, nunca a qualidade do texto em si (confirmado por
`grep -rn "banned\|vago\|subjetiv\|hallucin\|placeholder" scripts/`: zero
ocorrências). Duas classes de problema passam sem ser pegas:
vocabulário absoluto sem suporte ("com certeza", "comprovadamente") e alegações
numéricas (`%`, `R$`, contagens) sem nenhuma citação vinculada — exatamente o
tipo de coisa que o protocolo de "Grilling" já pede para evitar na origem
(`_SHARED/grilling-operacional.md`), mas que hoje não tem nenhuma rede de
segurança automática no momento da renderização.

**Correção de design importante em relação à análise que originou este plano**:
o dispatcher `scripts/validators/__init__.py:run()` escolhe **um único arquivo**
por `deliverable_type` (`HERE / f"{deliverable_type}.py"`) — não é uma lista de
validators plugáveis. Hoje só 3 dos 18 tipos têm arquivo. Para este scanner
valer para qualquer tipo (não só os 3 que já têm validator), `run()` precisa
ser alterado para **sempre** chamar um módulo comum, além do validator
específico do tipo quando existir — não basta "adicionar um 4º arquivo" como a
análise original sugeriu.

## Current state

`_DESIGN_SYSTEM/scripts/validators/__init__.py` (arquivo inteiro, 16 linhas):

```python
"""Validadores semânticos por deliverable_type: validate(content) -> list[str]."""
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
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.validate(content))
```

`_DESIGN_SYSTEM/scripts/render.py:181-190` (onde `run()` é chamado — note que só
roda quando `effective_completeness == "complete"`, comportamento que o scanner
deve preservar: entregas `partial`/`inconclusive` não são obrigadas a já ter
citação para tudo):

```python
    if effective_completeness == "complete":
        import importlib.util

        spec = importlib.util.spec_from_file_location("deliverable_validators", ROOT / "scripts/validators/__init__.py")
        validators = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validators)
        semantic_errors = validators.run(content)
        if semantic_errors:
            raise ValueError("Inconsistência semântica: " + "; ".join(semantic_errors[:12]))
```

Modelo de dados relevante (confirmado em `render.py:146-150` e no schema):
cada `block` tem `block["type"]`, `block["data"]`, e opcionalmente
`block["citation_ids"]` (lista de ids que devem existir em
`content["citations"]`, cada citação com campo `"id"`). `render.py` já define
uma função `block_text(block)` (linha ~194) que extrai o texto visível de um
bloco a partir de `title`/`label`/`text`/`description`/`content`/`value` em
`block["data"]` — reaproveite-a, não reimplemente extração de texto.

Exemplo de validator existente a seguir como modelo de estilo (contrato
`validate(content: dict) -> list[str]`, mensagens no formato
`"{local}: {problema}"`):
`_DESIGN_SYSTEM/scripts/validators/briefing_validation.py:13-16`.

## Commands you will need

Confirme o Python do ambiente antes de rodar qualquer teste — não assuma
`python3` do sistema:

```
PLAN_PYTHON=python3
"$PLAN_PYTHON" -c 'import jsonschema, referencing, weasyprint, docx, pptx, pypdf; print("ok: dependências locais")'
```

Se esse comando falhar, procure um ambiente virtual já criado no repositório ou
pare e reporte — não instale dependências novas sem autorização.

| Purpose | Command | Expected on success |
|---|---|---|
| Suíte de validadores | `PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest _DESIGN_SYSTEM.tests.test_validators -v` (rode a partir de `my_skills/`, com `__init__.py` ausente use `cd _DESIGN_SYSTEM && "$PLAN_PYTHON" -m unittest tests.test_validators -v`) | Nenhuma falha; novos testes do Step 3 aparecem na saída |
| Suíte completa de render | `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest tests.test_render -v` | Nenhuma falha nova (compare contagem com a baseline do `plans/README.md` antes de começar) |
| Sincronização (fora de escopo, só para confirmar que nada em `_SHARED/`/skills foi tocado) | `cd .. && python3 _TOOLS/sync_shared.py --check` | Nenhuma nova divergência além da pré-existente `__pycache__` já registrada no Plano 024 |

## Scope

**In scope**:
- `_DESIGN_SYSTEM/scripts/validators/_common.py` (novo arquivo — o scanner)
- `_DESIGN_SYSTEM/scripts/validators/__init__.py` (alterar `run()` para sempre
  chamar `_common.py` além do validator específico do tipo)
- `_DESIGN_SYSTEM/tests/test_validators.py` (novos casos de teste)

**Out of scope** (não toque, mesmo que pareça relacionado):
- Os 3 validators existentes (`briefing_validation.py`,
  `innovation_potential_assessment.py`, `learning_card.py`) — não precisam
  mudar; o `_common.py` roda **além** deles, não no lugar.
- `scripts/render.py` fora da chamada já existente a `validators.run()` — a
  mudança de comportamento vem inteiramente de dentro de `validators/`, sem
  tocar em `render.py`.
- Qualquer `SKILL.md` das 11 skills ou arquivo em `_SHARED/` — este plano é só
  do `_DESIGN_SYSTEM/`.
- Blocos do tipo `table` e `card_grid` — ver "Maintenance notes" sobre por que
  ficaram de fora da primeira versão.

## Git workflow

- Branch: `advisor/026-scanner-objetividade`
- Um commit por step (3 commits), mensagem no estilo observado em `git log`
  (ex. `Plano 026: scanner de objetividade nos validadores`).
- Não dar push nem abrir PR.

## Steps

### Step 1: Criar o módulo comum de objetividade

Crie `_DESIGN_SYSTEM/scripts/validators/_common.py` (o prefixo `_` garante que
nenhum `deliverable_type` real vai colidir com o nome do arquivo no lookup de
`run()`):

```python
"""Validações de objetividade aplicadas a todos os deliverable_types, independentemente do validator específico."""
from __future__ import annotations

import re
from typing import Any

ABSOLUTE_TERMS = (
    "com certeza", "sem dúvida", "comprovadamente", "indiscutivelmente",
    "certamente", "claramente", "obviamente", "o melhor", "a melhor",
    "garantido", "garantidamente",
)
NUMERIC_CLAIM = re.compile(r"R\$\s?\d|\d+[.,]?\d*\s?%|\b\d{2,}\b")
CLAIM_BLOCK_TYPES = {"paragraph", "callout", "metric"}


def block_text(block: dict[str, Any]) -> str:
    data = block.get("data", {})
    parts = []
    for key in ("title", "label", "text", "description", "content", "value"):
        value = data.get(key)
        if isinstance(value, str):
            parts.append(value)
    return " ".join(parts)


def validate(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for block in content.get("blocks", []):
        text = block_text(block)
        lowered = text.lower()
        for term in ABSOLUTE_TERMS:
            if term in lowered:
                errors.append(f"{block['id']}: vocabulário absoluto sem suporte ({term!r})")
        if block.get("type") in CLAIM_BLOCK_TYPES and NUMERIC_CLAIM.search(text):
            if not block.get("citation_ids"):
                errors.append(f"{block['id']}: alegação numérica sem citation_ids")
    return errors
```

**Verify**: `"$PLAN_PYTHON" -c "
import sys; sys.path.insert(0, '_DESIGN_SYSTEM/scripts/validators')
import _common
print(_common.validate({'blocks': [{'id': 'b1', 'type': 'paragraph', 'data': {'text': 'Isso com certeza reduz custos em 30%'}}]}))
"` (rode a partir de `my_skills/`) → deve imprimir uma lista com 2 erros para
`b1` (vocabulário absoluto E número sem citação).

### Step 2: Fazer `run()` sempre chamar o módulo comum

Em `_DESIGN_SYSTEM/scripts/validators/__init__.py`, substitua a função `run`
inteira por:

```python
def run(content: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    common_path = HERE / "_common.py"
    if common_path.is_file():
        spec = importlib.util.spec_from_file_location("validators__common", common_path)
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)
        errors.extend(common.validate(content))
    path = HERE / f"{content.get('deliverable_type', '')}.py"
    if path.is_file():
        spec = importlib.util.spec_from_file_location(f"validators_{path.stem}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        errors.extend(module.validate(content))
    return errors
```

**Verify**: `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest tests.test_validators -v` →
os testes existentes de `briefing_validation`/`innovation_potential_assessment`/
`learning_card` continuam passando sem mudança de comportamento (o módulo comum
não deve gerar erro para as amostras atuais, que já são objetivas).

### Step 3: Testes do scanner

Em `_DESIGN_SYSTEM/tests/test_validators.py`, siga o padrão já usado no arquivo
(`load_module`, `unittest.TestCase`, fixtures via dict inline — não precisa de
arquivo de amostra novo para isto, construa o `content` mínimo direto no teste).
Adicione uma classe nova:

```python
class ObjectivityValidatorTests(unittest.TestCase):
    def test_absolute_vocabulary_flagged(self):
        content = {"deliverable_type": "x", "citations": [], "blocks": [
            {"id": "b1", "type": "paragraph", "data": {"text": "Isso comprovadamente funciona."}},
        ]}
        self.assertTrue(any("vocabulário absoluto" in e for e in validators.run(content)))

    def test_numeric_claim_without_citation_flagged(self):
        content = {"deliverable_type": "x", "citations": [], "blocks": [
            {"id": "b1", "type": "metric", "data": {"value": "Redução de 42% no tempo médio"}},
        ]}
        self.assertTrue(any("sem citation_ids" in e for e in validators.run(content)))

    def test_numeric_claim_with_citation_passes(self):
        content = {"deliverable_type": "x", "citations": [{"id": "c1", "source": "planilha.xlsx"}],
                   "blocks": [{"id": "b1", "type": "metric", "citation_ids": ["c1"],
                               "data": {"value": "Redução de 42% no tempo médio"}}]}
        self.assertEqual(validators.run(content), [])

    def test_heading_and_table_not_in_scope(self):
        content = {"deliverable_type": "x", "citations": [], "blocks": [
            {"id": "b1", "type": "heading", "data": {"text": "Resultados de 2026"}},
        ]}
        self.assertEqual(validators.run(content), [])
```

**Verify**: `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest tests.test_validators -v` →
todos os testes, incluindo os 4 novos, passam.

## Test plan

- 4 casos novos em `ObjectivityValidatorTests` (Step 3), cobrindo: vocabulário
  absoluto detectado, número sem citação detectado, número com citação passa,
  tipo fora de escopo (`heading`) não é afetado mesmo com número no texto.
- Rodar a suíte completa de `tests/test_validators.py` e `tests/test_render.py`
  para confirmar que nenhuma amostra real em `_SAMPLES_ENTREGAVEIS/` passa a
  falhar por conter, sem querer, um dos termos da lista — se alguma falhar,
  trate como STOP (ver abaixo), não ajuste a amostra para "passar".

## Done criteria

- [ ] `_DESIGN_SYSTEM/scripts/validators/_common.py` existe e implementa `validate(content) -> list[str]`
- [ ] `validators.run()` chama `_common.py` sempre, e o validator específico do tipo quando existir
- [ ] Os 4 testes novos em `ObjectivityValidatorTests` passam
- [ ] `tests/test_validators.py` e `tests/test_render.py` completos continuam passando (nenhuma regressão nas amostras existentes)
- [ ] `git status` não mostra nenhum arquivo fora da lista em "Scope"
- [ ] `plans/README.md` com a linha deste plano atualizada

## STOP conditions

Pare e reporte (não improvise) se:
- O conteúdo de `validators/__init__.py` ou o trecho de `render.py:181-190`
  não bater com "Current state" (deriva desde que este plano foi escrito).
- Alguma amostra real em `_SAMPLES_ENTREGAVEIS/` passar a falhar no scanner —
  investigue se é falso positivo da lista de termos/regex (ajuste a lista,
  nunca o conteúdo da amostra) ou um problema real de objetividade na amostra
  (reporte, não corrija a amostra sozinho).
- A regex `NUMERIC_CLAIM` gerar volume alto de falsos positivos nos testes
  existentes (ex. anos como "2026", IDs como "IQB-06") — se isso acontecer,
  pare e proponha um ajuste de regex antes de prosseguir, não apenas amplie a
  lista de exceções ad-hoc.

## Maintenance notes

- `table` e `card_grid` ficaram fora do escopo porque a citação neles é por
  célula/card, não por bloco inteiro (`render_docx` já mostra isso:
  `card.get("citation_ids")` é lido por card individual) — extensão futura
  exigiria iterar `data["cards"]`/`data["rows"]`, não só `block["citation_ids"]`
  no nível do bloco. Não force isso neste plano.
- Se o scanner gerar ruído real em uso (termos legítimos do domínio batendo na
  lista), ajuste só a lista `ABSOLUTE_TERMS`/a regex `NUMERIC_CLAIM`, nunca
  remova o módulo da cadeia de `run()`.
- Este scanner não substitui julgamento humano sobre se uma evidência
  realmente sustenta uma conclusão — ele pega só padrões estruturais
  inequívocos, na mesma filosofia que `plans/README.md` já registrou para
  rejeitar automação de rastreabilidade completa ("Achados considerados e
  rejeitados").
