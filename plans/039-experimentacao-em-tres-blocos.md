# Plan 039: Organizar a `experimentacao-inovacao` em três blocos — Aprofundamento/Planejamento, Execução e Consolidação

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**: `git diff --stat a136123..HEAD -- experimentacao-inovacao _EVALS/experimentacao-inovacao`
> Qualquer mudança nesses caminhos é STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW (só instruções, referências, modelo do caderno e evals da skill; design system intocado)
- **Depends on**: nenhum
- **Category**: método / estrutura da skill
- **Planned at**: commit `a136123`, 2026-10-09

## Why this matters

O operador definiu que, **dentro da fase Experimentar da esteira ERIC**, a skill deve executar um processo
em três blocos, cada um com um entregável:

| Bloco | Atividades | Entregável |
|---|---|---|
| **Aprofundamento / Planejamento** | aprofundamento da fundamentação (Test Card); escopo da experimentação; estratégia e cronograma de execução | **Hipóteses** |
| **Execução** | construção/desenvolvimento do MVP; realização dos testes | **Implementação do MVP** |
| **Consolidação** | avaliação dos resultados, aprendizados e recomendação; avaliação do MVP | **Apresentação e direcionamento** |

Hoje a skill tem o conteúdo de planejamento e de consolidação espalhado em 8 passos, não trata a construção
do MVP (pressupõe o MVP pronto), não avalia o MVP como produto separado das hipóteses e não nomeia os três
entregáveis.

## Decisões do operador (2026-10-09)

- **A esteira ERIC não muda de forma nenhuma**: não edite `_ERIC_CONTEXT/`, `references/eric-esteira.md`
  nem nenhuma outra skill. Os três blocos são o processo interno da skill na fase Experimentar; não os
  apresente como etapas novas da esteira nem use "Materialização" como nome de etapa ERIC.
- **Reusar os tipos atuais do design system** (nenhum schema, perfil ou layout novo):
  *Hipóteses* = `experiment_plan` + um `test_card` por card; *Implementação do MVP* = `experiment_report`;
  *Apresentação e direcionamento* = `executive_presentation` + `evidence_recommendation`. Os schemas exigem só
  as seções mínimas (`experiment_plan`: hypothesis, method, population, measures, protocol, guardrails;
  `experiment_report`: scope, method, evidence, results, limits, recommendation) e aceitam seções extras.
- **Construção do MVP**: a skill planeja, acompanha e registra; quem constrói é a equipe.

## Current state

- `experimentacao-inovacao/SKILL.md` (86 linhas): "Passos" 1–8 (estado, contrato, fontes/lacunas,
  planejamento, análise, Learning Cards, recomendação/arquivos, fechamento); `metadata.version: "1.0.0"`.
- `references/entregaveis.md`: registro da rodada, Test Card, registro de execução, matriz, Learning Card,
  síntese/recomendação, gate, relatório/apresentação, passagem.
- `references/planejamento-dos-testes.md`, `references/analise-da-execucao.md`, `assets/caderno-da-rodada.md`
  (seções 1–9, com gate de início em 1).
- Evals: `_EVALS/experimentacao-inovacao/evals.json` (2 casos) e `casos-criterio-local.json`.

## Scope

**In scope**: `experimentacao-inovacao/SKILL.md`, `references/entregaveis.md`,
`references/planejamento-dos-testes.md`, novos `references/execucao-e-mvp.md` e `references/avaliacao-do-mvp.md`,
`assets/caderno-da-rodada.md`, `agents/openai.yaml`, `_EVALS/experimentacao-inovacao/` (casos e fixtures novos,
fictícios), `plans/README.md`.

**Out of scope**: `_ERIC_CONTEXT/`, `references/eric-esteira.md` (cópia gerada), design system, outras skills,
modelos `test-card.md`/`learning-card.md` (conteúdo dos cards não muda), rodar evals com modelo
(exige autorização do operador).

## Steps

### Step 1: `SKILL.md` em três blocos

- `description`: diga que a skill conduz a experimentação em três blocos — aprofundamento e planejamento
  (entregável Hipóteses), execução (construção do MVP e testes; entregável Implementação do MVP) e
  consolidação (resultados, aprendizados, avaliação do MVP; entregável Apresentação e direcionamento).
  Mantenha os gatilhos atuais (hipótese, piloto, MVP, usabilidade, sessões, Test Card, Learning Card) e as
  exclusões; ≤ 1024 caracteres.
- Substitua "Passos" por: uma seção curta **"Antes de cada bloco"** (estado antes/durante/depois, decisões
  vigentes do 3E, fontes/lacunas e triagem — conteúdo dos passos 1 e 3 atuais) e **três seções de bloco**, cada
  uma com atividades numeradas e o entregável com conteúdo mínimo e tipo do design system:
  - **Bloco 1** — 1. fundamentação (contrato, suposições, Test Cards; passos 2 e 4 atuais); 2. escopo da
    experimentação (hipótese master, recorte do MVP, versão, público, fora do escopo); 3. estratégia e
    cronograma (sequência dos testes, métodos, marcos de construção e de teste, datas, responsáveis, gate de
    início, guardrails). Entregável **Hipóteses**.
  - **Bloco 2** — 4. construção/desenvolvimento do MVP (componentes "precisa ter" do 3E, critérios de pronto,
    versão, desvios datados, trabalho manual por trás, prontidão para testar); 5. realização dos testes
    (protocolo, elegibilidade, adesão, desvios, registros e livro de evidências; sem interpretar). Entregável
    **Implementação do MVP**.
  - **Bloco 3** — 6. resultados, aprendizados e recomendação (passos 5, 6 e 7 atuais); 7. avaliação do MVP
    (nova; separada das hipóteses); 8. fechamento e direcionamento (passo 8 atual + saída avançar / iterar /
    investigar / encerrar para o BP2). Entregável **Apresentação e direcionamento**.
- "Quando usar": o pedido pode cair em qualquer bloco; entregue o bloco pedido, preparação ou versão parcial,
  sem inventar o que um bloco anterior deveria ter produzido.
- Checagem final: acrescente bloco e entregável identificados; MVP construído registrado contra o escopo;
  avaliação do MVP separada da avaliação das hipóteses.
- "Entrega em arquivo": tabela entregável → `deliverable_type` (decisão acima).
- `metadata.version` → `"1.1.0"`.

**Verify**: os dois `quick_validate` (Claude e Codex) → "Skill is valid!"; `wc -l SKILL.md` ≤ 130.

### Step 2: Referências

- `references/planejamento-dos-testes.md`: seções para **escopo da experimentação** e **estratégia e
  cronograma** (sem remover o conteúdo atual).
- `references/execucao-e-mvp.md` (novo): construção do MVP (o que registrar, critérios de pronto, desvios,
  prontidão) e realização dos testes (o que registrar sem interpretar).
- `references/avaliacao-do-mvp.md` (novo): dimensões — aderência ao escopo, funcionamento, experiência de uso
  observada, viabilidade operacional e técnica, esforço e custo da construção, pendências e prontidão para
  implantação; cada uma com evidência ou `não avaliado`. Regra: MVP que funciona não valida hipótese, e
  hipótese não sustentada não implica MVP ruim.
- `references/entregaveis.md`: organize por bloco e acrescente os três entregáveis (seções mínimas e
  mapeamento para os tipos), mantendo os modelos atuais.

### Step 3: Caderno da rodada

Reorganize `assets/caderno-da-rodada.md` sob os três blocos, preservando todas as tabelas atuais e IDs, e
acrescente: escopo; estratégia e cronograma (marco, tipo construção/teste, data, responsável, dependência,
estado); construção do MVP (componente, origem no 3E, critério de pronto, estado, versão, desvio); avaliação
do MVP (dimensão, evidência, avaliação, pendência).

### Step 4: Interface e evals

- `agents/openai.yaml`: `short_description` (25–64 caracteres) e `default_prompt` refletindo os três blocos.
- `_EVALS/experimentacao-inovacao/`: dois casos novos com fixtures fictícias — (a) registro da construção e
  dos testes → *Implementação do MVP* sem interpretar resultados; (b) consolidação com avaliação do MVP
  separada das hipóteses. Não rode evals com modelo.

### Step 5: Rotinas, testes e pacotes

`sync_shared.py`, `build_sources.py`, suíte completa, validadores, commit, push e `_DIST/` regenerado.

## Done criteria

- [ ] `SKILL.md` em três blocos, com os três entregáveis e seus tipos; versão 1.1.0
- [ ] Construção do MVP e avaliação do MVP cobertas em referências próprias
- [ ] Caderno reorganizado sem perder tabelas nem IDs
- [ ] Nenhuma alteração fora do escopo (`git diff --stat` só nos caminhos listados)
- [ ] Sync/fontes → 0; suíte `0 failed`; validadores Claude e Codex passam; `_DIST/` regenerado

## STOP conditions

- Alguma mudança exigiria editar `_ERIC_CONTEXT/` ou outra skill.
- Algum entregável não couber no tipo atual sem alterar schema.
- Algum teste ou eval existente passar a contradizer a estrutura nova.
