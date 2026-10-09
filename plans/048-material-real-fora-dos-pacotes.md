# Plan 048: Tirar dos pacotes o relatório 4D real e os metadados pessoais dos DOCX

> **Executor instructions**: Siga passo a passo; pare nas STOP conditions; **não reescreva o histórico do git** sem
> autorização expressa do operador registrada neste arquivo; atualize `plans/README.md`.
>
> **Drift check**: `git diff --stat 595f3b0..HEAD -- relatorio-4d workshop-4d relatorio-3e workshop-3e relatorio-5c workshop-5c _FONTES _TOOLS/build_sources.py`

## Status

- **Priority**: P1 · **Effort**: M · **Risk**: MED (muda arquivos fixados por hash) · **Depends on**: none · **Category**: security / privacidade
- **Planned at**: commit `595f3b0`, 2026-10-09 · **Requer decisões do operador** (ver abaixo)

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
   `_SAMPLES_ENTREGAVEIS/four_d_report/input.json`) ou **ficar** por ser material institucional autorizado? → ______
2. Remover os nomes dos metadados dos DOCX? (muda o hash fixado em `_TOOLS/build_sources.py`, constante `PINNED`) → ______
3. Reescrever o histórico do git para tirar o PDF real dos commits antigos (como foi feito com os PDFs da Strategyzer)? → ______

## Steps (conforme as decisões)

1. **PDF:** gere o PDF fictício com `python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/four_d_report/input.json --out-dir <tmp> --formats pdf`, troque `relatorio-4d/assets/official-four-d-report.pdf` por ele (mesmo nome ou novo nome, atualizando os links), e atualize a entrada `4d-pdf` no manifesto (origem fictícia, `titular: "CCEE"`).
2. **Guia:** em `relatorio-4d-layout.md:3`, troque o caminho real por "uma referência visual interna, fora do repositório".
3. **DOCX:** limpe `dc:creator`, `cp:lastModifiedBy` e `Company` de `docProps/core.xml`/`app.xml` com um script que reescreve só esses campos (sem alterar o corpo); atualize `PINNED` em `build_sources.py` com os novos hashes e explique a mudança em `notas` no manifesto.
4. Rode `build_sources.py`, `sync_shared.py`, `build_catalog.py --bump`, a suíte e `check_channels.py`.
5. Republique: o CI cria as Releases novas; apague, com o operador, as Releases antigas que contêm o PDF real (`gh release delete <tag> --cleanup-tag` só com autorização).
6. Histórico: só com a decisão 3 = sim, usando o procedimento do `git filter-repo` já aplicado em 2026-10-07 (backup antes, worktrees, force push, verificação num clone novo).

## Done criteria

- [ ] `git grep -l "_SAMPLE/GEIN"` → vazio · [ ] nenhum DOCX distribuído com nome pessoal nos metadados · [ ] suíte `0 failed`; fontes e catálogo em dia

## STOP conditions

- Decisões 1–3 não preenchidas.
- Algum teste depende do conteúdo do PDF real.
