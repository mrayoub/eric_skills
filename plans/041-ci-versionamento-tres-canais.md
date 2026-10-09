# Plan 041: CI que garante o versionamento das skills nos três canais de update — `npx skills`, `.skill` e clone

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 478c43a..HEAD -- .github _TOOLS catalog.json _DESIGN_SYSTEM/scripts/check_updates.py _TESTS/test_distribution.py README.md .gitattributes`
> Mudanças nesses caminhos precisam ser conferidas contra "Current state"; divergência que mude uma premissa é STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (o CI passa a bloquear pushes e PRs; a publicação de Releases é visível para quem acessa o repositório)
- **Depends on**: 037 DONE (catálogo, empacotador e verificador existem).
- **Category**: CI / distribuição
- **Planned at**: commit `478c43a`, 2026-10-09

## Why this matters

Cada skill tem versão própria (`metadata.version`) e três canais de update, que leem fontes diferentes:

| Canal | O que o usuário roda | O que ele recebe | O que precisa ser verdade |
|---|---|---|---|
| `npx skills` | `npx skills update` | a pasta da skill no `main` do GitHub, comparada pelo hash da pasta | `main` só recebe conteúdo com versão coerente; o npx descobre as 12 skills |
| `.skill` | baixa na página de Releases | o ZIP gerado por `_TOOLS/build_dist.py` | cada versão nova vira um pacote publicado, reprodutível e igual ao conteúdo do `main` |
| clone | `git pull` | o repositório inteiro, via links simbólicos | cada skill funciona sozinha (nada aponta para fora da pasta) e o `catalog.json` do `main` está em dia |

O `check_updates.py` compara a skill instalada com o `catalog.json` do `main`. Se o `main` aceitar conteúdo
alterado sem subir a versão, os três canais passam a divergir sem aviso. O CI é o único lugar que impede isso
para todos os mantenedores.

## Current state (em `478c43a`)

- `.github/workflows/tests.yml` (criado no 036): `on: workflow_dispatch` apenas; matriz 3 SO × Python 3.10/3.12;
  instala `_DESIGN_SYSTEM/requirements.txt` + `pytest pyyaml pdfplumber pypdfium2` **sem versão**; roda a suíte,
  `sync_shared.py --check` e `build_sources.py --check`.
- `_TOOLS/build_catalog.py` (`--check`, `--bump`), `_TOOLS/build_dist.py` (gera `_DIST/*.skill`, `catalog.json`,
  `SHA256SUMS`; roda as três checagens antes), `catalog.json` na raiz, `_DESIGN_SYSTEM/scripts/check_updates.py`
  copiado para as 12 skills, `_TESTS/test_distribution.py` (10 testes).
- `_DIST/` está no `.gitignore`. Não existe `.gitattributes`. Repositório privado: Actions consome minutos
  (macOS conta 10×, Windows 2×).

### Problemas encontrados na revisão do `tests.yml` (corrigir neste plano)

1. Não roda `build_catalog.py --check`: conteúdo alterado sem subir versão passa.
2. Só `workflow_dispatch`: nenhum push ou PR é verificado.
3. Dependências de teste sem versão fixa: o resultado do CI muda sozinho com novas versões do PyPI.
4. **Windows + quebras de linha**: sem `.gitattributes`, o checkout no Windows pode converter texto para CRLF;
   o hash do `build_catalog.py` muda e o `catalog.json` (gerado com LF) deixa de bater.
5. **Windows + codificação**: `build_catalog.py --bump` imprime "→" e outros scripts imprimem caracteres fora do
   cp1252; no console padrão do Windows isso gera `UnicodeEncodeError`.
6. Nenhuma verificação dos canais: descoberta pelo npx, reprodutibilidade do `.skill`, autossuficiência da pasta
   (clone/symlink), paridade entre o pacote e o que o git distribui.
7. Sem `permissions:` explícitas e sem publicação dos pacotes.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Testes | `python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` |
| Checagens | `python _TOOLS/sync_shared.py --check && python _TOOLS/build_sources.py --check && python _TOOLS/build_catalog.py --check` | exit 0 |
| Canais | `python _TOOLS/check_channels.py` (Step 3) | exit 0 |
| Pacotes | `python _TOOLS/build_dist.py` | 12 `.skill` |
| YAML | `python -c "import yaml;[yaml.safe_load(open(f)) for f in ('.github/workflows/tests.yml','.github/workflows/release.yml')]"` | sem erro |
| Lint (se houver) | `actionlint` | sem erro |

## Scope

**In scope**: `.github/workflows/tests.yml` (reescrever), `.github/workflows/release.yml` (novo), `.gitattributes`
(novo), `_TESTS/requirements-dev.txt` (novo), `_TOOLS/check_channels.py` (novo), ajustes de saída UTF-8 em
`_TOOLS/*.py` e `_DESIGN_SYSTEM/scripts/check_updates.py`, `_TESTS/test_distribution.py`, `README.md`,
`_TOOLS/README.md`, `plans/README.md`.

**Out of scope**: tornar o repositório público; regras de proteção de branch no GitHub (é configuração do
operador — o plano só documenta qual check exigir); conteúdo das skills.

## Git workflow

Branch `advisor/041-ci-versionamento`; um commit por passo; português no imperativo. **Não faça push** até o
Step 7: o push do workflow já dispara o CI.

## Steps

### Step 1: Quebras de linha e codificação estáveis em qualquer sistema

- Crie `.gitattributes`: `* text=auto eol=lf`; binários explícitos (`*.pdf *.docx *.pptx *.png *.ttf *.skill binary`).
  Rode `git add --renormalize .` e confirme que nenhum arquivo de texto mudou de conteúdo (`git diff --cached --stat`
  deve mostrar só o `.gitattributes`; se mostrar outros, STOP — havia CRLF no repositório).
- Em `_TOOLS/build_catalog.py`, `build_dist.py`, `sync_shared.py`, `build_sources.py`, `check_channels.py` e
  `check_updates.py`: no início de `main()`, `sys.stdout.reconfigure(encoding="utf-8")` e o mesmo para `stderr`
  (protegido com `hasattr`). No workflow, defina também `PYTHONUTF8: "1"`.

**Verify**: `PYTHONIOENCODING=cp1252 python _TOOLS/build_catalog.py --check` → exit 0 (sem `UnicodeEncodeError`).

### Step 2: Dependências de teste com versão fixa

`_TESTS/requirements-dev.txt` com `-r ../_DESIGN_SYSTEM/requirements.txt` e versões fixas de `pytest`, `pyyaml`,
`pdfplumber`, `pypdfium2` (use as instaladas no ambiente em que a suíte passa hoje: `pip freeze`).

**Verify**: venv limpo + `pip install -r _TESTS/requirements-dev.txt` → suíte `0 failed`.

### Step 3: `_TOOLS/check_channels.py` — o que cada canal precisa

Um script (argparse, `--check` implícito, exit 0/1, mensagens em português) que verifica:

1. **npx**: `npx -y skills add . --list` encontra exatamente as skills de `catalog.json` (compare os nomes, não só a
   contagem). Se `npx` não existir, falhe com mensagem clara (no CI ele existe).
2. **Paridade git × pacote**: para cada skill, `build_catalog.distributable_files()` num checkout limpo é igual a
   `git ls-files <skill>` (o que o npx e o clone entregam é o que o `.skill` contém).
3. **Autossuficiência (clone/symlink e `.skill`)**: nenhum link Markdown relativo em `<skill>/**/*.md` (exceto
   `assets/design-system/`) aponta para fora da pasta da skill; todo link relativo resolve para um arquivo existente.
4. **Reprodutibilidade**: gerar os pacotes duas vezes em pastas temporárias dá os mesmos sha256.
5. **Verificador**: `check_updates.py --catalog catalog.json --path .` lista as 12 skills como `atualizada`.

Teste em `_TESTS/test_distribution.py`: cada verificação falha num caso construído (link `../../fora.md`, arquivo não
versionado dentro da skill, nome a mais no catálogo).

### Step 4: `tests.yml` reescrito — verificação em todo push e PR, matriz completa sob demanda

```yaml
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: "0 9 * * 1"   # matriz completa toda segunda
permissions:
  contents: read
concurrency:
  group: tests-${{ github.ref }}
  cancel-in-progress: true
env:
  PYTHONUTF8: "1"
```

- Job **`versionamento`** (ubuntu, Python 3.12, Node 20; em todo PR/push): instala `_TESTS/requirements-dev.txt`
  com cache do pip; roda `sync_shared --check`, `build_sources --check`, `build_catalog --check` e `check_channels.py`.
  Mensagem de falha do catálogo deve dizer "rode `python _TOOLS/build_catalog.py --bump`".
- Job **`testes`** (em todo PR/push: ubuntu + 3.12): a suíte.
- Job **`matriz`** (só `workflow_dispatch` e `schedule`): 3 SO × Python 3.10/3.12, a suíte + as três checagens.
  Comentário no YAML explicando o custo (macOS 10×, Windows 2× em repositório privado).
- Use versões fixas das actions (`actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`).

### Step 5: `release.yml` — publicar o canal `.skill` quando uma versão sobe

```yaml
on:
  push:
    branches: [main]
    paths: [catalog.json]
  workflow_dispatch:
permissions:
  contents: write
concurrency:
  group: release
  cancel-in-progress: false
```

- Depois de repetir as checagens do job `versionamento`, rode `python _TOOLS/build_dist.py`.
- Para cada skill do catálogo: se a tag `<skill>-v<versão>` não existir, crie a tag no commit atual e uma
  Release com `_DIST/<skill>.skill` anexado; notas = `git log --format='- %s' <tag anterior>..HEAD -- <skill>`
  (ou "Primeira versão publicada").
- Atualize uma Release fixa `pacotes` (crie se não existir) com os 12 `.skill`, `catalog.json` e `SHA256SUMS`
  (`gh release upload pacotes ... --clobber`). É o link estável do README.
- Só `GITHUB_TOKEN`. Use `gh` (pré-instalado no runner) com `GH_TOKEN: ${{ github.token }}`.

**Verify**: YAML válido; simule a lógica de tags localmente com um script de dry-run (`--dry-run` que só imprime
as tags que criaria) — com o catálogo atual, imprime 12 tags `*-v1.0.0`/`experimentacao-inovacao-v1.1.0`.

### Step 6: Documentação

- `README.md` (raiz): link da Release `pacotes` no canal `.skill`; seção "Publicar uma nova versão" passa a dizer
  que o CI recusa conteúdo sem `--bump` e que a Release sai sozinha após o merge.
- `_TOOLS/README.md`: `check_channels.py` e os dois workflows.
- Recomendação ao operador (no relatório final, não em código): em Settings → Branches, exigir o check
  `versionamento` antes do merge no `main`.

### Step 7: Ativação

Só depois de todos os Verify locais: push da branch, abrir PR, conferir que `versionamento` e `testes` rodam e
passam; então merge. A primeira execução do `release.yml` no `main` cria as 12 Releases iniciais.

## Test plan

Testes novos do Step 3 em `_TESTS/test_distribution.py`; suíte completa local; a prova de Windows e macOS é a
primeira execução da `matriz` (Step 4), disparada manualmente após o merge.

## Done criteria

- [ ] `.gitattributes` com LF; renormalização sem mudança de conteúdo
- [ ] Scripts não quebram com `PYTHONIOENCODING=cp1252`
- [ ] `_TESTS/requirements-dev.txt` com versões fixas
- [ ] `check_channels.py` cobre npx, paridade, autossuficiência, reprodutibilidade e verificador, com testes
- [ ] `tests.yml` com `versionamento` + `testes` em PR/push e `matriz` sob demanda/semanal; `permissions: read`
- [ ] `release.yml` cria tags `<skill>-v<versão>`, Releases por skill e a Release `pacotes`
- [ ] Primeira execução no GitHub verde; status em `plans/README.md`

## STOP conditions

- `git add --renormalize .` altera arquivos além do `.gitattributes`.
- Algum passo exigiria segredo além do `GITHUB_TOKEN`.
- O operador não autorizar o consumo de minutos do Actions no repositório privado (pergunte antes do Step 7).
- `npx skills add . --list` deixar de encontrar as skills do catálogo.

## Maintenance notes

- Fluxo do mantenedor: editar → `sync_shared.py` → `build_catalog.py --bump` → PR. O CI barra o que esquecer o bump;
  o merge publica a Release.
- Se o repositório ficar público, o Actions passa a ser gratuito: dá para levar a `matriz` para todo PR.
- Versão de Node/actions: revisar a cada semestre.
