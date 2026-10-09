# Plan 049: Fechar pendências de documentação: índice nas referências longas, contato da licença, contagem de skills e o bloco 1 da experimentação

> **Executor instructions**: Siga passo a passo; pare nas STOP conditions; atualize `plans/README.md`.
>
> **Drift check**: `git diff --stat 595f3b0..HEAD -- LICENSE _ERIC_CONTEXT _SHARED experimentacao-inovacao workshop-3e workshop-4d relatorio-3e relatorio-4d avaliacao-briefing-iqb`

## Status

- **Priority**: P2 · **Effort**: S · **Risk**: LOW · **Depends on**: none · **Category**: docs
- **Planned at**: commit `595f3b0`, 2026-10-09 · **Requer decisões do operador** (itens 2 e 3)

## Why this matters

1. **Boa prática da Anthropic** (Skill authoring best practices): referência com mais de 100 linhas precisa de índice no
   topo. Sem índice hoje: `avaliacao-briefing-iqb/references/iqb-rubric.md` (161), `references/3e-solution-structuring-playbook.md`
   em `relatorio-3e` e `workshop-3e` (198), `references/4d-workshop-playbook.md` em `relatorio-4d` e `workshop-4d` (253),
   `workshop-3e/references/mural-board-3e-template.md` (172), `workshop-4d/references/mural-board-4d-template.md` (196).
2. **Licença:** `LICENSE:21` (e as 13 cópias) termina com "Contato para autorizações: [PREENCHER: e-mail da GEIN]".
3. **Contagem:** `_ERIC_CONTEXT/README.md:3` diz "onze skills" e é copiado como `references/eric-esteira.md` para as 13;
   `_EVALS/triggers/README.md` também diz "onze". O operador pediu em 2026-10-09 para **não alterar a esteira ERIC**;
   esta frase é contagem de skills, não etapa da esteira.
4. **Bloco 1 da experimentação:** "Hipóteses com Test Cards" promete suposições priorizadas, hipóteses e escopo, mas o
   único tipo é `test_card` (exatamente 4 campos); o resto fica num caderno "opcional", e o escopo também é seção
   obrigatória do Modelo de experimentação (bloco 2).

## Decisões do operador

- Item 2: e-mail de contato da GEIN → ______
- Item 3: pode trocar "onze skills" por "treze skills" (ou remover o número) em `_ERIC_CONTEXT/README.md`? → ______

## Steps

1. Acrescente "## Índice" com links para as seções (`- [Título](#âncora)`) no topo dos arquivos-fonte do item 1. Os
   playbooks 3E e 4D existem em duas skills: edite os dois e confira que continuam idênticos; se forem cópias geradas,
   edite a fonte. Rode `build_sources.py` (os hashes em `fontes.md` mudam).
2. Item 2: preencha o contato em `LICENSE` e rode `sync_shared.py`; acrescente em `_TESTS/test_licencas.py` um teste que
   falha se algum arquivo distribuído contiver "PREENCHER".
3. Item 3 (só com autorização): ajuste a frase e o `_EVALS/triggers/README.md`; rode o sync.
4. Item 4: em `experimentacao-inovacao/SKILL.md` e `references/planejamento-dos-testes.md`, diga que, quando o usuário
   pedir só o bloco 1, as suposições, a hipótese master e o escopo saem num `experiment_plan` parcial
   (`metadata.completeness: "partial"`, sem perfil) junto dos Test Cards, e que o escopo definido no bloco 1 é a fonte
   da seção `scope` do Modelo de experimentação (bloco 2).
5. `build_catalog.py --bump`, suíte, `check_channels.py`.

## Done criteria

- [ ] Os 7 arquivos com índice · [ ] nenhum "PREENCHER" distribuído (se decisão 2 dada) · [ ] suíte `0 failed`

## STOP conditions

- Decisões ausentes: execute só os itens 1 e 4 e registre o resto como pendente.
