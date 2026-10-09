# Plan 003: Endurecer o cálculo de potencial de inovação e dar-lhe uma linha de comando

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- potencial-inovacao/scripts potencial-inovacao/references/innovation-potential-rubric.md`
> Qualquer mudança → compare com "Current state"; divergência = STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (pode rodar em paralelo ao 001; se o 001 já rodou, não há sync envolvido — `scripts/` da skill não é copiado)
- **Category**: bug
- **Planned at**: commit `967749d`, 2026-09-28

## Why this matters

A skill `potencial-inovacao` promete: "exige justificativa e evidência para cada
critério" e "não converta ausência de dados em zero". O script que faz a conta não
cumpre isso. Reproduzido em 2026-09-28:

- cinco notas `True` → `status=complete, overall_score=1.0, classification=arquivar`
  (booleano vira 1.0 via `float(True)`);
- cinco notas `80` sem justificativa → `status=complete, classification=priorizar`.

Além disso, o SKILL.md manda "execute `scripts/score.py`", mas o arquivo não tem
ponto de entrada (`if __name__ == "__main__"`): executá-lo não faz nada, e o modelo
precisa improvisar um wrapper a cada uso — fonte de variação e erro.

## Current state

- `potencial-inovacao/scripts/score.py` (98 linhas) — cálculo puro; `RUBRIC_VERSION = "1.1.0-portable"`;
  `CRITERIA` com chaves `impact` (0.30), `viability` (0.25), `strategic_alignment` (0.20),
  `urgency` (0.15), `innovation` (0.10). Trecho `score.py:44-64`:

```python
def calculate_innovation_score(scores: dict[str, Any]) -> dict[str, Any]:
    """Compute only when all criteria contain explicit valid scores."""
    ...
        raw = scores.get(key)
        if not isinstance(raw, dict) or raw.get("score") is None:
            missing.append(key)
            continue
        try:
            value = float(raw["score"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid score for {key}") from exc
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"Score for {key} must be between 0 and 100")
        normalized_score: int | float = int(value) if value.is_integer() else round(value, 1)
        normalized[key] = {
            "score": normalized_score,
            "justification": str(raw.get("justification", "")),
        }
```

  Faixas (`score.py:81-87`): `>= 70` priorizar; `>= 40` monitorar; senão arquivar.
- `potencial-inovacao/references/innovation-potential-rubric.md` — rubrica: pesos 30/25/20/15/10
  e as mesmas faixas (linhas 8–20). Linha 3: "nota faltante ou inválida não é zero; sem os
  cinco critérios sustentados o resultado permanece incompleto e sem classificação".
- `potencial-inovacao/SKILL.md:14` — "Após justificar as cinco notas, execute `scripts/score.py`..."
- Observação: a string `"0"` hoje é aceita (`float("0")`). Strings numéricas vindas de JSON
  são improváveis; o plano passa a rejeitar tudo que não seja `int`/`float` (exceto `bool`).

## Commands you will need

| Purpose | Command (na raiz) | Expected |
|---|---|---|
| Testes | `python3 -m pytest -q _TESTS/potencial-inovacao` | all pass |
| CLI | `python3 potencial-inovacao/scripts/score.py <arquivo.json>` | JSON no stdout, exit 0 |

## Scope

**In scope**: `potencial-inovacao/scripts/score.py`; `_TESTS/potencial-inovacao/test_score.py` (criar — fora da skill para não ser distribuído; veja Step 4); `potencial-inovacao/SKILL.md` somente a frase da linha 14 que cita o script.

**Out of scope**: pesos, faixas e `RUBRIC_VERSION` numérico dos critérios (não mude a
regra de negócio); `innovation-potential-assessment.schema.json` (plano 005);
qualquer outra parte do SKILL.md (plano 010).

## Git workflow

Branch `advisor/003-score`. Commit: `Endurece score.py e adiciona CLI`.

## Steps

### Step 1: Testes que falham

Crie `_TESTS/potencial-inovacao/test_score.py` (unittest), importando o módulo por
caminho com `importlib.util.spec_from_file_location` apontando para
`<raiz>/potencial-inovacao/scripts/score.py`. Casos:

1. Cinco `{"score": True, "justification":"x"}` → `ValueError`.
2. Cinco `{"score": 80, "justification": ""}` → `status == "incomplete"`, `classification is None`, e todas as cinco chaves listadas em `missing_justification`.
3. Cinco `{"score": 80, "justification": "   "}` → mesmo que 2 (só espaços não conta).
4. Cinco notas 80 com justificativa → `complete`, `overall_score == 80.0`, `priorizar`.
5. Cinco zeros com justificativa → `complete`, `arquivar` (zero sustentado é válido).
6. Critério ausente → `incomplete`, `missing_criteria == ["urgency"]`, `overall_score is None`.
7. `{"score": "80"}` → `ValueError`.
8. `{"score": 100.5}` → `ValueError`; `{"score": float("nan")}` → `ValueError`.
9. Limites: notas que dão exatamente 70.0 → `priorizar`; 40.0 → `monitorar`; 39.9 → `arquivar`.

**Verify**: `python3 -m pytest -q _TESTS/potencial-inovacao/test_score.py` → 1, 2, 3, 7 falham.

### Step 2: Corrigir o cálculo

Em `calculate_innovation_score`:
- Rejeite `bool` antes de tudo: `if isinstance(raw["score"], bool) or not isinstance(raw["score"], (int, float)): raise ValueError(f"Invalid score for {key}")`.
- Colete `missing_justification: list[str]` para critérios cuja `str(raw.get("justification") or "").strip()` seja vazia.
- Se `missing` OU `missing_justification` não vazios → retorne `status: "incomplete"`, `overall_score: None`, `classification: None`, e inclua **ambas** as listas (`missing_criteria`, `missing_justification`) no retorno. Mantenha o formato atual das demais chaves.
- No retorno `complete`, acrescente `"weighted": {key: round(score*weight, 2)}` — facilita mostrar sensibilidade no relatório. Não altere as outras chaves.
- Troque `RUBRIC_VERSION` para `"1.2.0-portable"` (mudou a regra de completude, não os pesos).

**Verify**: `python3 -m pytest -q _TESTS/potencial-inovacao/test_score.py` → todos passam.

### Step 3: Linha de comando

Acrescente ao fim de `score.py`:

```python
def main() -> None:
    import argparse, json, sys
    parser = argparse.ArgumentParser(description="Calcula o potencial de inovação a partir de um JSON com os cinco critérios.")
    parser.add_argument("input", help="arquivo JSON ou '-' para stdin")
    args = parser.parse_args()
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    try:
        result = calculate_innovation_score(json.loads(raw))
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False)); sys.exit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

Formato de entrada (documente no docstring do módulo):

```json
{"impact": {"score": 60, "justification": "…"}, "viability": {...}, "strategic_alignment": {...}, "urgency": {...}, "innovation": {...}}
```

Adicione teste 10: CLI via `subprocess` com um arquivo temporário válido → exit 0 e `"status": "complete"` no stdout; com `true` como nota → exit 2 e `"status": "error"`.

**Verify**: `echo '{"impact":{"score":80,"justification":"a"},"viability":{"score":80,"justification":"a"},"strategic_alignment":{"score":80,"justification":"a"},"urgency":{"score":80,"justification":"a"},"innovation":{"score":80,"justification":"a"}}' | python3 potencial-inovacao/scripts/score.py -` → JSON com `"classification": "priorizar"`.

### Step 4: Atualizar a instrução no SKILL.md

Em `potencial-inovacao/SKILL.md:14`, troque "execute `scripts/score.py`" por:
"grave as cinco notas e justificativas em JSON (formato no topo de `scripts/score.py`) e execute `python3 scripts/score.py notas.json`" — sem alterar o resto da frase.

Crie `_TESTS/README.md` (1 parágrafo): "testes de manutenção dos scripts das skills; ficam fora das pastas das skills para não serem distribuídos. Rodar: `python3 -m pytest -q _TESTS`."

**Verify**: `grep -c "python3 scripts/score.py" potencial-inovacao/SKILL.md` → `1`; `python3 /Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py potencial-inovacao` → `Skill is valid!`.

## Test plan

Os 10 casos acima em `_TESTS/potencial-inovacao/test_score.py`.

## Done criteria

- [ ] `python3 -m pytest -q _TESTS/potencial-inovacao` → 10+ passed
- [ ] booleanos e strings rejeitados; justificativa vazia → `incomplete`
- [ ] `python3 potencial-inovacao/scripts/score.py -` funciona com stdin
- [ ] pesos e faixas inalterados: `git diff potencial-inovacao/scripts/score.py | grep -E '^[-+].*"weight"'` → vazio
- [ ] `plans/README.md` atualizado

## STOP conditions

- A rubrica em `innovation-potential-rubric.md` mostrar pesos/faixas diferentes dos do script.
- Algum arquivo fora do escopo importar `score.py` (`grep -rn "score import\|import score" --include=*.py .` retornar algo além dos testes).

## Maintenance notes

- O plano 005 (validador semântico) recalcula o total a partir do JSON do entregável
  usando os mesmos pesos; se mudar pesos aqui, mude lá (há teste de paridade no 005).
- Chaves do script (`viability`, `strategic_alignment`, `innovation`) diferem das
  `section_key` do schema do entregável (`feasibility`, `alignment`, `novelty`). O
  mapeamento fica no plano 005; não renomeie aqui.
