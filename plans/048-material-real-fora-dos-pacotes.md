# Plan 048: Tirar dos pacotes o relatório 4D real e os metadados pessoais dos DOCX

> **Executor instructions**: Siga passo a passo; pare nas STOP conditions; **não reescreva o histórico do git** sem
> autorização expressa do operador registrada neste arquivo; atualize `plans/README.md`.
>
> **Autorização registrada (2026-10-09):** o operador escolheu 048a = substituir o PDF real, 048b = limpar os
> metadados pessoais e 048c = substituir os arquivos pelos corrigidos no histórico do git. Se a substituição
> histórica não for possível, autorizou somente limpar o histórico do cache. Essa decisão supera as STOP
> conditions relativas às escolhas 1–3; preserve um backup antes da reescrita.
>
> **Drift check**: `git diff --stat 595f3b0..HEAD -- relatorio-4d workshop-4d relatorio-3e workshop-3e relatorio-5c workshop-5c _FONTES _TOOLS/build_sources.py`

## Status

- **Priority**: P1 · **Effort**: M · **Risk**: MED (muda arquivos fixados por hash) · **Depends on**: none · **Category**: security / privacidade
- **Planned at**: commit `595f3b0`, 2026-10-09 · **Concluído em 2026-10-09**, com as decisões do operador abaixo.

## Why this matters

A regra do repositório é que material real fica em `_SAMPLE/` (fora do git e dos pacotes). Verificado:

- `relatorio-4d/assets/official-four-d-report.pdf` (6 páginas, imagem) é um **relatório 4D real**: a capa traz o nome de
  três facilitadores, a data do evento e o processo real; a página 2, números operacionais internos. Vai em todo
  `.skill` e nas Releases do GitHub. `_FONTES/manifest.json` o registra como "PDF de referência" da CCEE.
- `relatorio-4d/references/relatorio-4d-layout.md:3` cita o caminho de uma pasta real de `_SAMPLE/` (nome do projeto,
  arquivo e SHA-256).
- Os DOCX dos modelos 4D, 3E e 5C (`<skill>/assets/*.docx`, em `workshop-*` e `relatorio-*`) têm nomes de empregadas
  em `docProps/core.xml` (`dc:creator`, `cp:lastModifiedBy`); o manifesto registra `autor: null`. Esses DOCX são da
  CCEE (decisão do operador em 2026-10-07), mas os nomes pessoais nos metadados não precisam ser distribuídos.

## Decisões do operador (preencha antes de executar)

1. O PDF real deve **sair** (substituído por uma versão fictícia gerada pelo renderizador a partir de
   `_SAMPLES_ENTREGAVEIS/four_d_report/input.json`) ou **ficar** por ser material institucional autorizado? → **Substituir.**
2. Remover os nomes dos metadados dos DOCX? (muda o hash fixado em `_TOOLS/build_sources.py`, constante `PINNED`) → **Limpar.**
3. Reescrever o histórico do git para tirar o PDF real dos commits antigos (como foi feito com os PDFs da Strategyzer)? → **Substituir pelos arquivos corrigidos, se possível; caso contrário, limpar o histórico do cache.**

## Steps (conforme as decisões)

1. **PDF:** gere o PDF fictício com `python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/four_d_report/input.json --out-dir <tmp> --formats pdf`, troque `relatorio-4d/assets/official-four-d-report.pdf` por ele (mesmo nome ou novo nome, atualizando os links), e atualize a entrada `4d-pdf` no manifesto (origem fictícia, `titular: "CCEE"`).
2. **Guia:** em `relatorio-4d-layout.md:3`, troque o caminho real por "uma referência visual interna, fora do repositório".
3. **DOCX:** limpe `dc:creator`, `cp:lastModifiedBy` e `Company` de `docProps/core.xml`/`app.xml` com um script que reescreve só esses campos (sem alterar o corpo); atualize `PINNED` em `build_sources.py` com os novos hashes e explique a mudança em `notas` no manifesto.
4. Rode `build_sources.py`, `sync_shared.py`, `build_catalog.py --bump`, a suíte e `check_channels.py`.
5. Republique: o CI cria as Releases novas; apague, com o operador, as Releases antigas que contêm o PDF real (`gh release delete <tag> --cleanup-tag` só com autorização).
6. Histórico: só com a decisão 3 = sim, usando o procedimento do `git filter-repo` já aplicado em 2026-10-07 (backup antes, worktrees, force push, verificação num clone novo).

## Done criteria

- [x] `git grep -l "_SAMPLE/GEIN" -- ':!plans/**'` → vazio · [x] nenhum DOCX distribuído com nome pessoal nos metadados · [x] suíte `0 failed`; fontes e catálogo em dia

## Execução e verificação

- O PDF distribuído foi substituído byte a byte pelo exemplo fictício gerado de
  `_SAMPLES_ENTREGAVEIS/four_d_report/input.json`; o guia e o manifesto identificam essa origem.
- Os seis DOCX distribuídos tiveram `creator` e `lastModifiedBy` esvaziados; todos os membros do ZIP fora de
  `docProps/core.xml` permaneceram idênticos. Os três hashes fixados foram atualizados.
- `build_sources.py --check`, `sync_shared.py --check`, `build_catalog.py --check` e `check_channels.py` passaram;
  a suíte completa passou com 183 testes e 1.511 subtestes. Doze skills receberam versão patch.
- Antes da reescrita, foi criado backup local em `/private/tmp/plan048-before.bundle`. Um clone espelho isolado
  substituiu os quatro blobs antigos e o guia que citava a pasta real. Todos os branches e tags publicados foram
  atualizados atomicamente no GitHub. Um clone novo confirmou que os blobs antigos não são alcançáveis pelos refs
  publicados e que os DOCX da versão atual não contêm os metadados pessoais.
- As 19 Releases antigas com anexos afetados (3 versões de cada uma das seis skills 3E/4D/5C e `pacotes`)
  foram excluídas junto com os tags. O workflow `release.yml` publicou as 12 novas versões e a Release
  `pacotes` (run `37975334678`, sucesso). O arquivo `relatorio-4d.skill` baixado dessa Release foi conferido:
  contém o PDF fictício e o DOCX sem metadados pessoais.
- Os 40 refs locais antigos também foram reescritos. Os dez worktrees ligados a eles receberam apenas os oito
  arquivos corrigidos; as alterações não commitadas preexistentes de um worktree foram preservadas. Após expirar
  os reflogs e executar `git gc --prune=now`, os quatro blobs antigos não são mais acessíveis no Git local.
  Os bundles de backup temporários ainda preservam o histórico anterior. O GitHub pode reter objetos
  inalcançáveis em caches internos até sua coleta de lixo.

## STOP conditions

- Decisões 1–3 não preenchidas.
- Algum teste depende do conteúdo do PDF real.
