# Plan 042: Skill-mestra `esteira-eric` — porta de entrada que diagnostica o projeto e encaminha para a skill certa

> **Executor instructions**: Siga este plano passo a passo; rode cada verificação; pare nas STOP conditions;
> ao terminar, atualize `plans/README.md`.
>
> **Drift check**: `git diff --stat 3323738..HEAD -- _TOOLS/sync_shared.py _FONTES/manifest.json _TESTS _EVALS`

## Status

- **Priority**: P1 · **Effort**: M · **Risk**: LOW (skill nova; as 12 skills não mudam de comportamento)
- **Depends on**: 037 (catálogo e pacotes)
- **Category**: experiência de uso
- **Planned at**: commit `3323738`, 2026-10-09 — item C1 da lista de boas práticas aprovada pelo operador

## Why this matters

O usuário precisa saber qual das 12 skills usar. As skills mais instaladas do ecossistema resolvem isso com uma skill
de entrada (`find-skills`, `using-superpowers`). O operador pediu uma skill-mestra que oriente pedidos gerais e
**mantenha o acionamento direto** das skills específicas (ex.: `relatorio-4d`).

## Decisões

- Nome `esteira-eric`; versão `1.0.0`; autor `GEIN-CCEE`.
- **Não produz entregáveis.** Diagnostica a etapa pelos arquivos e decisões disponíveis, mostra o que existe e o que
  falta, e indica a próxima skill (até duas alternativas) com o motivo e o insumo necessário. Com o aceite do usuário,
  segue a skill indicada por completo.
- **Acionamento direto preservado**: a descrição diz para não usá-la quando o pedido já indica o entregável ou a skill.
- A esteira ERIC não muda: o mapa usa as etapas de `_ERIC_CONTEXT/README.md` sem editá-lo. 5C é transversal.
- Sem design system (não renderiza): `sync_shared.py` não copia `assets/design-system/` para ela, mas copia
  `LICENSE`, `THIRD_PARTY_NOTICES.md`, `eric-esteira.md`, `grilling-operacional.md` e `linguagem-dos-entregaveis.md`.

## Steps

1. **Skill**: `esteira-eric/SKILL.md` (frontmatter só com campos aceitos por ChatGPT/Codex), `references/mapa-das-skills.md`
   (etapa → skill → entregável → quando usar), `agents/openai.yaml` (4 campos, `brand_color` = token).
2. **Ferramentas**: `sync_shared.py` com o conjunto de skills sem design system; `_FONTES/manifest.json` inclui a skill
   na fonte `eric-esteira`; `build_sources.py`; catálogo com a skill nova.
3. **Testes**: o teste de frontmatter só exige `metadata.requirements` mencionando `requirements.txt` em skills com design
   system; teste novo garante que a `esteira-eric` cita todas as outras skills no mapa e que a descrição exclui pedidos
   diretos; contagens de 12 → 13 onde forem contagem de skills.
4. **Evals** (sem rodar com modelo): `_EVALS/esteira-eric/` com 2 casos (projeto com briefing e 4D → indica 3E;
   pedido ambíguo sem arquivos → pergunta o mínimo e orienta o início); `_EVALS/triggers/esteira-eric.json` com pedidos
   gerais (acionar) e pedidos diretos como "faça o relatório 4D" (não acionar).
5. **Documentação**: `README.md` da raiz (13 skills; entrada pela `esteira-eric`).
6. **Fechamento**: sync, fontes, catálogo, suíte completa nos dois ambientes, validadores Claude e Codex, `build_dist.py`,
   merge, push, instalação local (links em `~/.claude/skills` e `~/.agents/skills`).

## Done criteria

- [ ] `esteira-eric` válida nos dois validadores, sem design system, com mapa cobrindo as 12 skills
- [ ] Acionamento direto preservado (descrição + caso de trigger negativo)
- [ ] Suíte `0 failed`; sync, fontes e catálogo em dia; 13 pacotes em `_DIST/`

## STOP conditions

- Exigir edição de `_ERIC_CONTEXT/` ou de outra skill além de referências de contagem.
- Algum teste das 12 skills mudar de resultado.
