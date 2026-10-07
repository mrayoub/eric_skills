# Plan 037: Distribuir as skills por `npx skills`, `.skill` e clone, com versão por skill e aviso de atualização

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat dabd0e2..HEAD -- '*/SKILL.md' '*/agents' _TOOLS _DESIGN_SYSTEM/scripts LICENSE .github`
> Qualquer mudança nesses caminhos depois do commit de planejamento precisa ser
> conferida contra a seção "Current state"; divergência que mude uma premissa é STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW (não altera instruções nem scripts de entregáveis; acrescenta ferramentas, testes, CI e documentação)
- **Depends on**: nenhum plano. Independente do 036 — se o 036 já tiver criado `.github/workflows/tests.yml`, não edite esse arquivo; este plano cria um workflow separado.
- **Category**: distribuição / DX
- **Planned at**: commit `dabd0e2`, 2026-10-07

## Why this matters

As 12 skills são independentes e atualizadas uma a uma, mas hoje os usuários não têm
como saber que a cópia deles está desatualizada, e os canais de distribuição divergem:

- `npx skills` (skills.sh) já funciona sem mudança: `npx skills add mrayoub/eric_skills --list`
  encontra as 12 skills (verificado em 2026-10-07 após o push de `dabd0e2`), e
  `npx skills update` atualiza por skill comparando o hash da pasta. Falta documentar.
- Os pacotes `.skill` (upload no Claude.ai e instalação manual) são gerados à mão em
  `_DIST/` (no `.gitignore`), estão velhos (`relatorio-4d.skill` tem 46 arquivos; a pasta
  tem 72) e não existe pacote do `relatorio-final-inovacao`.
- Não há regra que obrigue a subir `metadata.version` quando o conteúdo de uma skill muda.
  Como `_TOOLS/sync_shared.py` copia o design system para todas, uma mudança comum altera
  as 12 de uma vez — e a versão de cada uma precisa refletir isso.

Objetivo: **um único conteúdo, três canais que não quebram um ao outro** — `npx skills`,
`.skill` e clone —, com a versão de cada skill travada pelo CI e um verificador de
atualização que o usuário roda quando quiser.

## Current state (em `dabd0e2`; confira)

- Cada `SKILL.md` tem no frontmatter (padrão Agent Skills, https://agentskills.io/specification):
  ```yaml
  license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
  metadata:
    requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
    author: "GEIN-CCEE"
    version: "1.0.0"
  ```
  Os requisitos ficam em `metadata.requirements`, e não no campo `compatibility` da especificação: o ChatGPT e o
  validador do Codex aceitam só `name`, `description`, `license`, `allowed-tools` e `metadata` (o upload no ChatGPT
  recusou `compatibility` em 2026-10-07). Os dois validadores passam nas 12 skills.
- Cada skill tem `agents/openai.yaml` (só Codex) com `interface.display_name`, `short_description`,
  `brand_color: "#193C8E"` (= `color.document_primary` de `_DESIGN_SYSTEM/tokens.json`) e `default_prompt`.
- `LICENSE` na raiz; `_TOOLS/sync_shared.py` copia para `<skill>/LICENSE` (cada skill pode ser instalada sozinha).
- Formato `.skill` atual: ZIP com a pasta da skill na raiz do arquivo (`relatorio-4d/SKILL.md`, …),
  o mesmo do `package_skill.py` do skill-creator do Claude (exclui `__pycache__`, `node_modules`, `*.pyc`,
  `.DS_Store` e `evals/` na raiz da skill).
- Repositório **privado** (`mrayoub/eric_skills`). Pode ficar público depois (decisão da GEIN/jurídico);
  tudo neste plano tem de funcionar nos dois casos.
- Não há `README.md` na raiz nem `.github/`.
- O layout novo da apresentação executiva foi commitado em `28bcdb4` (com correção do logo e da cor do
  texto no PPTX); o diretório de trabalho está limpo e a suíte passa inteira.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Testes | `python3 -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` |
| Sync e fontes | `python3 _TOOLS/sync_shared.py --check && python3 _TOOLS/build_sources.py --check` | exit 0 |
| Catálogo | `python3 _TOOLS/build_catalog.py --check` | exit 0 |
| Pacotes | `python3 _TOOLS/build_dist.py` | 12 arquivos em `_DIST/`, exit 0 |
| Descoberta npx | `npx -y skills add . --list` | `Found 12 skills` |

## Scope

**In scope** (criar ou editar): `_TOOLS/build_catalog.py`, `_TOOLS/build_dist.py`, `catalog.json` (raiz),
`_DESIGN_SYSTEM/scripts/check_updates.py` (+ cópias pelo sync), `_TESTS/test_distribution.py`,
`.github/workflows/distribution.yml`, `README.md` (raiz, novo), `_TOOLS/README.md`, `plans/README.md`.

**Out of scope**: corpo dos `SKILL.md` (só a linha `version:` muda, e só pelo `--bump`), scripts de
entregáveis, `layout.json`, evals, decisão de tornar o repositório público, texto do `LICENSE`.

## Git workflow

Branch `advisor/037-distribuicao`; um commit por passo; português no imperativo; sem push/merge.

## Steps

### Step 1: `_TOOLS/build_catalog.py` — versão por skill travada pelo conteúdo

Mesmo estilo dos outros scripts de `_TOOLS` (argparse, `--check`, exit 0/1, mensagens em português).

- **Arquivos distribuíveis de uma skill** = todos os arquivos da pasta, exceto `__pycache__/`, `*.pyc`,
  `.DS_Store`, `node_modules/` e `evals/` na raiz da skill. Centralize essa regra numa função
  `distributable_files(skill_dir) -> list[Path]` que o Step 2 importa — **a mesma lista define o hash e o ZIP**.
- **Hash da skill** = sha256 de `"\n".join(f"{rel.as_posix()} {sha256(arquivo)}")` em ordem, **excluindo a linha
  `version:` do frontmatter** do `SKILL.md` (senão subir a versão muda o hash e o `--check` nunca estabiliza).
- **Versão** = `metadata.version` do frontmatter. Valide semver `X.Y.Z` entre aspas.
- `catalog.json` (raiz, commitado):
  ```json
  {"schema_version": "1.0.0", "repository": "mrayoub/eric_skills",
   "skills": {"relatorio-4d": {"version": "1.0.0", "sha256": "…", "files": 72}}}
  ```
  Ordene as chaves; JSON com `indent=2` e `\n` final, para diffs estáveis.
- Modos:
  - sem flag: regrava `catalog.json`. Recusa (exit 1) se alguma skill mudou de hash sem mudar de versão
    em relação ao `catalog.json` anterior, ou se a versão diminuiu.
  - `--check`: não escreve; exit 1 listando `"<skill>: conteúdo mudou sem subir a versão (x.y.z)"`,
    `"<skill>: versão menor que a publicada"`, `"<skill>: ausente do catálogo"` ou `"catalog.json desatualizado"`.
  - `--bump [patch|minor|major]` (padrão `patch`): para cada skill cujo hash difere do catálogo, sobe a
    versão **reescrevendo só a linha `  version: "…"`** do `SKILL.md`, e regrava o catálogo. Imprime o que subiu.
- Gere o catálogo inicial a partir do estado atual (todas em `1.0.0`).

**Verify**: `python3 _TOOLS/build_catalog.py && python3 _TOOLS/build_catalog.py --check` → exit 0;
`git diff --stat -- '*/SKILL.md'` → vazio.

### Step 2: `_TOOLS/build_dist.py` — pacotes `.skill` iguais ao que o `npx` instala

- Antes de empacotar, rode (importando ou via subprocess) `sync_shared --check`, `build_sources --check` e
  `build_catalog --check`; se algum falhar, exit 1 sem gerar nada.
- Valide cada `SKILL.md` com uma checagem própria (não dependa de validador fora do repo): `name` = nome da
  pasta e no padrão da especificação; `description` 1–1024 caracteres; nenhum campo além de `name`, `description`, `license`, `allowed-tools` e `metadata`; `metadata`
  só com valores string; `license` presente.
- Gere `_DIST/<skill>.skill` (**nome sem versão** — mantém compatível com quem já usa esses arquivos) como
  ZIP com a pasta da skill na raiz, usando `distributable_files()` do Step 1. Use datas fixas nas entradas
  do ZIP (`ZipInfo` com `date_time=(1980,1,1,0,0,0)`) para o pacote ser reprodutível.
- Gere também `_DIST/catalog.json` (cópia do da raiz) e `_DIST/SHA256SUMS`.
- Flag `--skill <nome>` para empacotar só uma.

**Verify**: `python3 _TOOLS/build_dist.py && ls _DIST/*.skill | wc -l` → 12; rodar duas vezes gera os mesmos
sha256; `unzip -l _DIST/relatorio-4d.skill | tail -1` mostra o mesmo número de arquivos do catálogo.

### Step 3: `check_updates.py` — aviso de versão, rodado pelo usuário

Crie em `_DESIGN_SYSTEM/scripts/check_updates.py` (o sync copia para todas as skills, então quem instalou
uma única skill pelo `npx` ou pelo `.skill` também tem o verificador). Rode o sync depois.

- Descobre skills instaladas: por padrão, as pastas irmãs da skill onde o script está (o diretório que
  contém `<skill>/assets/design-system/scripts/`), mais `--path DIR` repetível. Considera só pastas cujo
  `SKILL.md` tem `metadata.author: "GEIN-CCEE"`.
- Baixa o catálogo de `https://raw.githubusercontent.com/mrayoub/eric_skills/main/catalog.json`
  (`--catalog URL_OU_ARQUIVO` para sobrescrever). Usa `GITHUB_TOKEN`/`GH_TOKEN` se houver (repo privado);
  timeout de 5 s; cache em `~/.cache/eric-skills/catalog.json` por 24 h (`--refresh` ignora o cache).
- Saída, uma linha por skill: `relatorio-4d: instalada 1.0.0; disponível 1.1.0` / `atualizada` /
  `alterada localmente` (hash local ≠ hash do catálogo para a mesma versão — **nunca sugira sobrescrever**).
  No fim, o comando de atualização do canal: `npx skills update` ou "baixe o .skill na página de Releases".
- **Nunca altera arquivos** e nunca falha de forma ruidosa: sem rede ou com 404 (repo privado sem token),
  imprime uma linha explicando e sai com 0. Exit 1 só com `--strict` quando houver atualização.
- Só biblioteca padrão. Reaproveite a regra de hash do Step 1 copiando a função (o script é distribuído
  sem `_TOOLS`); um teste do Step 5 garante que as duas implementações dão o mesmo hash.
- **Não** adicione instrução nos `SKILL.md` para rodar este script automaticamente.

**Verify**: `python3 _DESIGN_SYSTEM/scripts/check_updates.py --catalog catalog.json --path .` → 12 linhas
"atualizada"; com `--catalog` apontando para uma URL inexistente → mensagem e exit 0.

### Step 4: `README.md` na raiz — os três canais

Seções curtas, em português:

1. **Instalar com `npx skills`** (Claude Code, Codex, Cursor, Copilot e outras ferramentas do padrão Agent Skills):
   `npx skills add mrayoub/eric_skills --all`, uma skill com `--skill relatorio-4d`, global com `-g`,
   ferramentas específicas com `-a`. Atualizar: `npx skills update`. Nota: enquanto o repositório for privado,
   requer acesso ao GitHub com credencial configurada no `git`.
2. **Instalar pelo arquivo `.skill`**: baixar na página de Releases; Claude.ai/app: upload em Configurações →
   Skills; instalação manual: descompactar em `~/.claude/skills/` (Claude Code) ou na pasta de skills do Codex.
   **Confirme os caminhos e o menu na documentação oficial atual de cada ferramenta antes de escrever** e
   cite a fonte num comentário HTML.
3. **Clonar o repositório** (mantenedores): clone + symlinks para a pasta de skills; `git pull` atualiza.
4. **Verificar atualizações**: `python3 <pasta-da-skill>/assets/design-system/scripts/check_updates.py`.
5. **Publicar uma nova versão** (mantenedores): editar → `sync_shared.py` → `build_catalog.py --bump` →
   commit → push; o CI gera os pacotes.
6. **Licença**: aponta para `LICENSE`.

Atualize `_TOOLS/README.md` com `build_catalog.py` e `build_dist.py`.

**Verify**: todos os comandos citados no README existem (`npx -y skills --help`, scripts do repo).

### Step 5: `_TESTS/test_distribution.py`

Use cópias temporárias do repositório (`tmp_path`) — nunca altere o repositório real nos testes.

- `build_catalog --check` passa no estado atual; falha depois de alterar um arquivo de uma skill numa cópia;
  `--bump` sobe só essa skill (`1.0.0` → `1.0.1`) e o `--check` volta a passar.
- Mudar só a linha `version:` não altera o hash.
- Versão menor que a do catálogo → exit 1.
- O ZIP de `build_dist` contém exatamente `distributable_files()` (paridade `.skill` × `npx`), com a pasta da
  skill na raiz; dois builds geram bytes idênticos.
- Hash de `check_updates.py` = hash de `build_catalog.py` para as 12 skills.
- `check_updates` com catálogo local: atualizada / desatualizada / alterada localmente; com catálogo
  inacessível → exit 0 e mensagem.
- Toda skill tem `LICENSE` igual ao da raiz, `agents/openai.yaml` com os 4 campos de `interface`, e
  `brand_color` igual a `color.document_primary` de `_DESIGN_SYSTEM/tokens.json`.
- Frontmatter de toda skill passa na checagem do Step 2.

**Verify**: suíte inteira `0 failed`.

### Step 6: `.github/workflows/distribution.yml`

- `on: push` (main) e `pull_request`. Job `check` (ubuntu, Python 3.12, Node 20): instala
  `_DESIGN_SYSTEM/requirements.txt` + pytest; roda sync `--check`, `build_sources --check`,
  `build_catalog --check`, a suíte, e `npx -y skills add . --list` conferindo `Found 12 skills`
  (derive o 12 de `catalog.json`, não fixe no YAML).
- Job `release` (só `push` em `main`, depois de `check`, `permissions: contents: write`): roda `build_dist.py`;
  para cada skill, se a tag `<skill>-v<versão>` não existir, cria a release com `gh release create` anexando
  `_DIST/<skill>.skill`, e atualiza uma release fixa `pacotes` com os 12 `.skill`, `catalog.json` e
  `SHA256SUMS` (`gh release upload --clobber`). Notas da release: `git log` da pasta da skill desde a tag anterior.
- Valide o YAML localmente (`python3 -c "import yaml; yaml.safe_load(open(...))"`); se houver `actionlint`, rode.

**Verify**: YAML válido; os comandos do job `check` passam localmente na mesma ordem.

## Test plan

Os testes do Step 5 cobrem catálogo, bump, paridade dos pacotes, verificador e consistência de
`LICENSE`/`openai.yaml`. A prova de ponta a ponta do `npx` e das releases é o CI do Step 6, no primeiro
push do operador — registre no status que ela ficou pendente.

## Done criteria

- [ ] `catalog.json` com as 12 skills em `1.0.0`; `build_catalog.py --check` → exit 0
- [ ] `build_dist.py` gera 12 `.skill` reprodutíveis, iguais ao conteúdo que o `npx` instala
- [ ] `check_updates.py` distribuído nas 12 skills pelo sync, sem rede obrigatória e sem escrever arquivos
- [ ] `README.md` com os três canais, verificação e publicação
- [ ] `_TESTS/test_distribution.py` e suíte inteira `0 failed`; sync e `build_sources --check` → exit 0
- [ ] `.github/workflows/distribution.yml` válido; nenhum `SKILL.md` alterado além da linha `version:`
- [ ] Status atualizado em `plans/README.md`

## STOP conditions

- A especificação do Agent Skills ou o `npx skills` mudaram de forma que `metadata.version` não seja mais
  aceito, ou o `npx skills add . --list` deixar de achar as 12 skills.
- Para documentar o upload no Claude.ai ou a pasta do Codex, a documentação oficial não confirma o caminho.
  Escreva "confira a documentação da ferramenta" em vez de inventar.
- O job `release` precisaria de um segredo além do `GITHUB_TOKEN` padrão.

## Maintenance notes

- Fluxo de publicação: editar → `sync_shared.py` → `build_catalog.py --bump` → commit/push. Uma mudança no
  design system sobe a versão das 12 skills — é correto, pois o pacote de cada uma mudou.
- Se o repositório ficar público, `check_updates.py` passa a funcionar sem token, sem mudar código. Antes
  disso, a GEIN/jurídico precisa decidir sobre material de terceiros no repositório (ex.: documentos da
  Strategyzer e `relatorio-final-inovacao/assets/ThePitchCanvas.pdf`) e sobre o texto do `LICENSE`
  (contato da GEIN ainda é `[PREENCHER]`).
- `openai.yaml` não é sincronizado: o teste do Step 5 acusa se `brand_color` divergir do token.
