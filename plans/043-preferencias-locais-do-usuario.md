# Plan 043: Preferências locais do usuário em cada skill (C2 local, sem envio para fora)

> **Executor instructions**: siga os passos; rode as verificações; pare nas STOP conditions; atualize `plans/README.md`.
>
> **Drift check**: `git diff --stat f41944a..HEAD -- _SHARED _TOOLS/sync_shared.py '*/SKILL.md'`

## Status

- **Priority**: P1 · **Effort**: M · **Risk**: LOW (opcional; sem arquivo de preferências, nada muda)
- **Depends on**: 042
- **Category**: experiência de uso / privacidade
- **Planned at**: commit `f41944a`, 2026-10-09 — versão local da C2, desenhada com o operador

## Why this matters

O operador quer que cada usuário ajuste o comportamento das skills ao próprio jeito de trabalhar, sem enviar nada
para fora da máquina e sem mexer nas skills distribuídas. Quando o usuário corrige um comportamento, a correção pode
virar uma preferência persistida, lida no início de cada execução.

## Decisões do operador (2026-10-09)

- **Dois níveis:** usuário (`~/.config/eric-skills/`, todos os projetos) e projeto (`<projeto>/.eric/preferencias/`,
  sobrepõe para aquele projeto). A pasta do usuário pode ser trocada pela variável `ERIC_SKILLS_CONFIG`.
- **Arquivos:** um por skill (`<skill>.md`) e um comum (`todas.md`), em cada nível.
- **Prioridade:** regras do método e do design system > projeto/skill > projeto/todas > usuário/skill > usuário/todas
  > padrão de fábrica.
- **Confirmação sempre:** a skill mostra o texto e o alcance e só grava com um "sim".
- **Reset com backup:** `resetar` volta ao padrão de fábrica guardando `.bak`; vale por skill ou para todas.
- **Nunca dentro da pasta da skill** (seria apagado em cada update e acusaria "alterada localmente").

## Furos tratados

- Preferência que contraria regra do método (critério prévio, não inventar evidência, validação do schema, crédito do
  Pitch Canvas, licença) é recusada com explicação.
- Pedido pontual não vira preferência sem confirmação.
- Cada preferência guarda a versão da skill; se a skill estiver em versão maior, ela avisa que a preferência pode
  estar desatualizada.
- Claude.ai e ChatGPT não têm armazenamento persistente: a skill orienta a colar a preferência nas instruções do
  Projeto ou na memória do app.
- Preferências descrevem comportamento; não guardam dados pessoais nem conteúdo de projeto.

## Steps

1. `_SHARED/preferencias.py` (só biblioteca padrão, sem rede): `ler`, `adicionar`, `remover`, `resetar`, `listar`,
   com `--todas`, `--projeto DIR` e `--versao X.Y.Z`; formato Markdown legível e editável à mão.
2. `_SHARED/preferencias-do-usuario.md`: quando ler, quando propor, como confirmar, o que recusar, alcance, reset,
   aviso de versão, privacidade e o caso Claude.ai/ChatGPT.
3. `sync_shared.py` copia os dois para todas as skills (`scripts/preferencias.py`, `references/preferencias-do-usuario.md`).
4. Seção curta "Preferências do usuário" em cada `SKILL.md`, apontando para a referência; versões *minor* via
   `build_catalog.py --bump minor`.
5. Testes (`_TESTS/test_preferencias.py`) em pasta temporária: precedência, `todas`, projeto sobre usuário, reset com
   `.bak`, remoção, nada gravado dentro de pasta de skill, aviso de versão.
6. Sync, fontes, catálogo, suíte nos dois ambientes, validadores, pacotes, merge, push.

## Done criteria

- [ ] Script e referência em todas as 13 skills; cada `SKILL.md` com a seção
- [ ] Testes de precedência, reset e isolamento passam; suíte `0 failed`
- [ ] Sem preferências, saídas idênticas às de antes

## STOP conditions

- Alguma ferramenta exigir rede ou gravação dentro da pasta da skill.
