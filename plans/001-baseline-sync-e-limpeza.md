# Plan 001: Versionar a pasta, criar sincronização verificável do design system e limpar os pacotes

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- _DESIGN_SYSTEM _ERIC_CONTEXT '*/assets/design-system' '*/references'`
> Se algum arquivo em escopo mudou desde a linha de base, compare os trechos de
> "Current state" com o arquivo vivo; divergência = STOP.

## Status

- **Priority**: P1 (pré-requisito de todos os outros planos)
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `967749d` (tag `improve-baseline-2026-09-28`), 2026-09-28

## Why this matters

A pasta `my_skills` contém 11 skills que carregam, cada uma, uma cópia idêntica do
design system (`<skill>/assets/design-system/`) e de três referências comuns. Hoje a
sincronização dessas cópias é manual: qualquer correção em `_DESIGN_SYSTEM/scripts/render.py`
(planos 002, 005, 006, 007) precisa ser copiada 11 vezes, sem ferramenta que detecte
esquecimento. Além disso, não há git — nenhuma mudança é reversível — e os pacotes
distribuídos levam lixo (`__pycache__`, `.DS_Store`) e a pasta `tests/`, que só
serve para manutenção. Este plano cria a linha de base que torna os demais planos
seguros.

## Current state

- `/Users/mayoub/Desktop/workspaces/my_skills/` — raiz. Repositório git criado em 2026-09-28 (commit `967749d`, tag `improve-baseline-2026-09-28`), com `.gitignore` excluindo `_SAMPLE/`, `_OUTPUTS/`, `__pycache__/`, `.DS_Store`.
- Skills (pastas com `SKILL.md`): `avaliacao-briefing-iqb`, `briefing-inovacao`,
  `experimentacao-inovacao`, `potencial-inovacao`, `relatorio-3e`, `relatorio-4d`,
  `relatorio-5c`, `scorecard-inovacao`, `workshop-3e`, `workshop-4d`, `workshop-5c`.
- Pastas de manutenção (prefixo `_`, NÃO são skills): `_DESIGN_SYSTEM/` (fonte do
  design system), `_ERIC_CONTEXT/` (fonte do contexto ERIC), `_SAMPLE/` (~500 MB,
  material real de um projeto do cliente, inclui `.mp4`), `_SAMPLES_ENTREGAVEIS/`
  (amostras renderizadas, ~31 MB), `_OUTPUTS/` (saídas de execuções reais).
- `_DESIGN_SYSTEM/` contém: `README.md`, `profiles.json`, `tokens.json`,
  `response-sections.json`, `requirements.txt`, `contracts/*.schema.json` (19),
  `scripts/render.py`, `tests/test_render.py`, `assets/logo_ccee.png`,
  `assets/fonts/` (Montserrat/Roboto + licenças OFL), `templates/` (vazia).
- Cada `<skill>/assets/design-system/` é hoje byte-idêntica a `_DESIGN_SYSTEM/`
  (verificado em 2026-09-28), incluindo `tests/`.
- Referências comuns copiadas em `<skill>/references/`:
  - `eric-esteira.md` — idêntica nas 11 skills; é a cópia de `_ERIC_CONTEXT/README.md`
    (mesmo conteúdo). Ambas dizem "referência metodológica comum das **nove** skills"
    na linha 3 — hoje são onze.
  - `grilling-operacional.md` — idêntica nas 11 skills; NÃO existe fonte em pasta `_`.
  - `levantamento-documental-e-grilling.md` — idêntica em 9 skills; ausente de
    propósito em `experimentacao-inovacao` e `scorecard-inovacao`.
- Lixo encontrado: 65 ocorrências de `__pycache__`/`.DS_Store` fora de `_SAMPLE`
  (ex.: `potencial-inovacao/scripts/__pycache__/score.cpython-313.pyc`).
- Nenhum script de sincronização existe (`grep -rn "sync" _DESIGN_SYSTEM/README.md` → vazio).

Convenção do repo: scripts Python 3 com `from __future__ import annotations`,
`argparse`, `pathlib.Path`, mensagens de erro em português. Exemplo:
`_DESIGN_SYSTEM/scripts/render.py:655-661`:

```python
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
```

## Commands you will need

| Purpose | Command (rodar na raiz) | Expected on success |
|---|---|---|
| Python | `python3 --version` | 3.10+ (recon: 3.12.12) |
| Testes do DS | `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py` | 3 passed; 2 podem falhar por falta de `pango` (ver plano 007) — aceitável aqui |
| Validador de skill | `python3 /Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py <skill>` | `Skill is valid!` |

## Scope

**In scope**:
- `_TOOLS/sync_shared.py` (criar)
- `_TOOLS/README.md` (criar)
- `_SHARED/grilling-operacional.md` (criar, cópia da versão atual)
- `_SHARED/levantamento-documental-e-grilling.md` (criar, cópia da versão atual)
- `_ERIC_CONTEXT/README.md` (só a palavra "nove" → "onze" na linha 3)
- Remoção de `tests/`, `__pycache__/`, `.DS_Store` DENTRO das 11 skills (via script)

**Out of scope**:
- `_SAMPLE/`, `_OUTPUTS/`, `_SAMPLES_ENTREGAVEIS/` — não mover nem apagar nada.
- Qualquer conteúdo de `render.py`, schemas, SKILL.md (outros planos cuidam disso).
- `_DESIGN_SYSTEM/tests/` — permanece na fonte; só sai das cópias.

## Git workflow

- Branch: `advisor/001-sync` a partir de `main`/`master`.
- Commits em português, imperativo curto (ex.: `Cria sincronização do design system`).
- Não faça push.

## Steps

### Step 1: Repositório git — JÁ CONCLUÍDO pelo advisor

`.gitignore`, `git init`, commit `967749d` e tag `improve-baseline-2026-09-28` já existem.
Apenas confirme.

**Verify**: `git tag` → contém `improve-baseline-2026-09-28`; `git ls-files | grep -c "^_SAMPLE/"` → `0`.

### Step 2: Criar as fontes compartilhadas que faltam

- Copie `potencial-inovacao/references/grilling-operacional.md` para `_SHARED/grilling-operacional.md`.
- Copie `potencial-inovacao/references/levantamento-documental-e-grilling.md` para `_SHARED/levantamento-documental-e-grilling.md`.
- Em `_ERIC_CONTEXT/README.md` linha 3, troque "das nove skills" por "das onze skills".

**Verify**: `shasum _SHARED/*.md` → os dois hashes iguais aos das cópias em `potencial-inovacao/references/`; `grep -c "onze skills" _ERIC_CONTEXT/README.md` → `1`.

### Step 3: Escrever `_TOOLS/sync_shared.py`

Comportamento exigido:

- Descobre skills = subpastas diretas da raiz que contêm `SKILL.md` e cujo nome não começa com `_`.
- Mapa de sincronização (fonte → destino relativo à skill):
  - `_DESIGN_SYSTEM/` → `assets/design-system/` (espelho de diretório)
  - `_ERIC_CONTEXT/README.md` → `references/eric-esteira.md`
  - `_SHARED/grilling-operacional.md` → `references/grilling-operacional.md`
  - `_SHARED/levantamento-documental-e-grilling.md` → `references/levantamento-documental-e-grilling.md`
    **somente** se o destino já existir (preserva a ausência intencional em
    `experimentacao-inovacao` e `scorecard-inovacao`).
- Exclusões ao espelhar `_DESIGN_SYSTEM/`: diretórios `tests/`, `__pycache__/`,
  `.pytest_cache/`, `templates/` se vazia; arquivos `.DS_Store`, `*.pyc`.
- Espelho = copiar arquivos novos/alterados (comparando sha256) e **apagar** no
  destino arquivos que não existem na fonte (inclusive a pasta `tests/`).
- Também apaga `__pycache__/` e `.DS_Store` em qualquer lugar dentro das skills.
- Flags: `--check` (não escreve nada; imprime cada divergência como
  `DIVERGE <caminho>` e sai com código 1 se houver alguma; 0 caso contrário) e
  `--dry-run` (imprime o que faria).
- Sem dependências fora da biblioteca padrão (`hashlib`, `shutil`, `pathlib`, `argparse`).
- Raiz = `Path(__file__).resolve().parents[1]`.

**Verify**: `python3 _TOOLS/sync_shared.py --check; echo $?` → lista `DIVERGE` para
`tests/`, `__pycache__`, `.DS_Store` nas skills e sai `1` (ainda não sincronizado).

### Step 4: Sincronizar

`python3 _TOOLS/sync_shared.py`

**Verify**:
- `python3 _TOOLS/sync_shared.py --check; echo $?` → `0`
- `find . -path ./_SAMPLE -prune -o \( -name __pycache__ -o -name .DS_Store \) -print | grep -v "^./_" | wc -l` → `0`
- `ls */assets/design-system/tests 2>/dev/null | wc -l` → `0`
- `ls experimentacao-inovacao/references/levantamento-documental-e-grilling.md 2>&1` → "No such file"
- Para cada skill: `quick_validate.py <skill>` → `Skill is valid!`

### Step 5: Documentar

Crie `_TOOLS/README.md` (curto, português): o que é fonte (`_DESIGN_SYSTEM`,
`_ERIC_CONTEXT`, `_SHARED`), o que é cópia gerada, e a regra "edite só a fonte e
rode `python3 _TOOLS/sync_shared.py`; antes de distribuir rode `--check`". Acrescente
uma linha equivalente ao fim de `_DESIGN_SYSTEM/README.md`? **Não** — esse README é
copiado para dentro das skills e não deve falar da estrutura de manutenção.

**Verify**: `test -f _TOOLS/README.md && echo ok` → `ok`.

## Test plan

- Teste manual do `--check`: altere um byte em `workshop-4d/assets/design-system/tokens.json`,
  rode `--check` → deve listar esse arquivo e sair 1; rode o sync → `--check` volta a 0.
- Rode `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py` → mesmo resultado de antes (3 passed; falhas só por `pango`).

## Done criteria

- [ ] `python3 _TOOLS/sync_shared.py --check` sai 0
- [ ] nenhuma skill contém `assets/design-system/tests/`, `__pycache__/` ou `.DS_Store`
- [ ] as 11 skills passam em `quick_validate.py`
- [ ] `_SHARED/` tem os 2 arquivos; `_ERIC_CONTEXT/README.md` diz "onze skills"
- [ ] `plans/README.md` atualizado

## STOP conditions

- `--check` antes do sync mostrar divergência em arquivos que NÃO sejam `tests/`,
  `__pycache__`, `.DS_Store` ou `eric-esteira.md` (significa que alguém editou uma
  cópia e o sync apagaria trabalho) — reporte a lista.
- `git status` mostrar algo de `_SAMPLE/` ou `_OUTPUTS/` para commitar.
- Alguma skill deixar de passar em `quick_validate.py` após o sync.

## Maintenance notes

- A partir daqui, toda mudança em `render.py`, schemas, tokens, ERIC ou grilling é
  feita na fonte + `sync_shared.py`. Os planos 002–012 assumem isso.
- Se uma skill precisar de referência própria diferente da comum, renomeie o
  arquivo local (não use o mesmo nome), senão o sync sobrescreve.
- Quando houver empacotamento `.skill`/zip, rode `--check` antes.
