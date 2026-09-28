# Planos de implementação — skills de inovação

Gerados pela skill `improve` em 2026-09-28, contra o commit `35c3b75` (tag
`improve-baseline-2026-09-28`). Base: auditoria das 11 skills e revisão crítica de
`MELHORIAS_SKILLS.md`. Execute na ordem abaixo, salvo o que as dependências permitirem
paralelizar. Cada executor: leia o plano inteiro antes de começar, respeite as STOP
conditions e atualize sua linha aqui ao terminar.

Convenções comuns a todos os planos:
- **Fonte x cópia:** edite só `_DESIGN_SYSTEM/`, `_ERIC_CONTEXT/`, `_SHARED/`; as cópias dentro das skills são geradas por `python3 _TOOLS/sync_shared.py` (plano 001).
- **Testes de manutenção** ficam fora das skills: `_DESIGN_SYSTEM/tests/` e `_TESTS/`. **Evals** em `_EVALS/`.
- **Nunca** use nada de `_SAMPLE/` (material real, fora do git) em fixtures, testes ou amostras.
- Planos 008, 009 e 010 têm passos que gastam chamadas de modelo (evals): peça autorização ao operador antes.

## Ordem de execução e status

| Plano | Título | Prioridade | Esforço | Depende de | Status |
|---|---|---|---|---|---|
| 001 | [Sync do design system, limpeza dos pacotes](001-baseline-sync-e-limpeza.md) (git já criado) | P1 | M | — | DONE (sync verificado; 11 skills válidas; 5 testes passaram) |
| 002 | [`table_rows` busca por chave, não rótulo](002-table-rows-chave-rotulo.md) (T03) | P1 | S | 001 | DONE (7 casos novos e suíte com 12 testes passaram; sync verificado) |
| 003 | [Endurecer `score.py` + CLI](003-score-py-endurecer-e-cli.md) (T04) | P1 | S | — | DONE (12 testes passaram; CLI e skill validadas) |
| 004 | [CLI e testes do `iqb.py`](004-iqb-cli.md) | P1 | S | — | DONE (8 testes passaram; CLI e skill validadas; cálculo preservado) |
| 005 | [Validador semântico por tipo: IQB, potencial, citações aninhadas](005-validador-semantico-por-tipo.md) (T02 + parte de T04) | P1 | M | 001, 002, 003, 004 | DONE (51 testes passaram; amostras regeneradas; sync verificado) |
| 006 | [IQB completo nos derivados](006-iqb-completo-nos-derivados.md) (T01) | P1 | M | 001, 002 | TODO |
| 007 | [PDF sem pango: entregar o resto e avisar](007-fallback-pdf-sem-pango.md) | P2 | S | 001 | TODO |
| 008 | [Descriptions + eval de acionamento](008-descriptions-e-eval-de-acionamento.md) | P1 | M | — | TODO |
| 009 | [Evals comportamentais (2 por skill)](009-evals-comportamentais.md) | P1 | M | — | TODO |
| 010 | [Enxugar os SKILL.md (piloto → rollout)](010-enxugar-skill-md.md) | P2 | L | 001, 003, 004, 007, 008, 009 | TODO |
| 011 | [Learning Card ligado ao Test Card](011-learning-card-ligado-ao-test-card.md) | P3 | S | 001, 005 | TODO |
| 012 | [Manifesto de fontes e vigência](012-manifesto-de-fontes.md) | P3 | S | 001 | TODO |

Status: TODO | IN PROGRESS | DONE | BLOCKED (motivo em uma linha) | REJECTED (motivo em uma linha)

## Notas de dependência

- **001 antes de tudo que toca o design system** (002, 005, 006, 007, 011): sem o script de sync, cada correção teria de ser copiada à mão para 11 pastas.
- **002 antes de 005 e 006**: 005 usa tabela `columns`/`rows` com `{key,label}` no bloco de notas do potencial; 006 reescreve a mesma função `table_rows`.
- **003 e 004 antes de 005**: o validador copia as regras dos scripts e tem teste de paridade contra eles.
- **009 antes de 010**: as evals são a rede de segurança da reescrita dos SKILL.md. 010 também usa o frontmatter do 008 e as frases de CLI de 003/004, e remete ao fallback de PDF do 007 no README do design system.
- Paralelizáveis desde já: 003, 004, 008, 009 (e 001).

## Relação com `MELHORIAS_SKILLS.md`

| Item de MELHORIAS | Plano |
|---|---|
| 4.1 IQB nos derivados | 006 |
| 4.2 Consistência matemática do IQB | 005 |
| 4.3 Chave × rótulo | 002 |
| 4.4 Potencial sustentado | 003 (script) + 005 (contrato/validador) |
| 5 Rastreabilidade verificável | reduzido: citações aninhadas (005) + Learning↔Test Card (011) |
| 6 Testes comportamentais | 009 (+ acionamento em 008) |
| 7 Proveniência | 012 (manifesto único, não 11 registros) |
| 8 Equivalência entre formatos | 006 para o IQB; demais tipos adiados (ver abaixo) |
| 9 Organização da implementação | 001 (sync + git) |
| 10 Comandos de verificação | corrigidos nos planos: validador do skill-creator da Anthropic (não o do Codex); testes pulam sem pango (007) |

Achados novos, fora de MELHORIAS: scripts sem CLI (003, 004), descriptions/acionamento (008), SKILL.md prolixos e repetidos (010), `levantamento-documental` sobreposto ao grilling (010), lixo nos pacotes e `tests/` distribuído (001), PDF quebrando todos os formatos sem pango (007), chaves do `score.py` diferentes das `section_key` do schema do potencial (tratado em 005), "nove skills" no contexto ERIC (001).

## Achados considerados e rejeitados

- **Rastreabilidade executável completa** (afirmação → fonte → evidência → teste → aprendizado → recomendação, para os 18 tipos; MELHORIAS §5): custo alto e sobreposição com julgamento que só o modelo faz ("a evidência sustenta a conclusão?"). Automatizamos só o que é estrutural e inequívoco (005, 011).
- **Registro de proveniência copiado em cada skill** (MELHORIAS §7.1): 11 cópias para manter; substituído por manifesto único + página gerada (012).
- **Comparar hash binário de PDF/DOCX/PPTX entre renderizações**: bibliotecas gravam metadados variáveis; o próprio README do design system já descarta isso. A equivalência é checada por conteúdo (006).
- **Teste de equivalência de conteúdo para os 18 tipos agora** (MELHORIAS §8): só o IQB tinha perda de dados comprovada. Reavaliar depois de 006, se aparecer outro tipo com estrutura composta em `data`.
- **Tirar o design system de dentro das skills para evitar 11 cópias**: rejeitado — a independência de cada skill é requisito explícito do mantenedor. O custo das cópias é resolvido pelo sync (001).
- **Traduzir SKILL.md para inglês**: os usuários e as fontes são em português; as descriptions em português acionam melhor para pedidos em português.
