# Análise, hipótese e conclusão do Relatório 4D

O registro de D1 a D4 é necessário: preserva o mural, que pode se perder, e serve à gestão do conhecimento. Mas ele
não basta. A autora do playbook 4D avaliou um relatório gerado por esta skill (10/11/2026) e apontou que ele relatava
o que aconteceu sem analisar o que aconteceu, e terminava em ações e desejos soltos em vez de uma hipótese de solução.
Este guia transforma essa orientação em regra. A origem está registrada em
[fonte-4d-e-divergencias.md](fonte-4d-e-divergencias.md#orientação-da-autora-do-playbook-10112026).

O relatório responde a uma pergunta: **o que tudo isso, analisado em conjunto, diz sobre o problema e sobre a hipótese
de solução?**

## Duas saídas da mesma base

| | Relatório 4D | Apresentação 4D |
|---|---|---|
| Tipo no design system | `four_d_report` (documento) | `four_d_presentation` (slides 16:9) |
| Pergunta que responde | O que aconteceu em cada dinâmica, com que evidência, e o que a análise conclui | O que aprendemos sobre o problema e que hipótese segue para o 3E |
| Uso | Gestão do conhecimento, retomada do trabalho, base do BP1 e do 3E | Gerência e diretoria, devolutiva ao grupo |
| Conteúdo | Registro de D1 a D4, evidências, mural consolidado, temas transversais, síntese analítica, hipótese, limitações, conclusão | Cinco slides de conteúdo, no máximo seis: desafio, principais achados, hipótese de solução, convergência, próximos passos |

Faça a análise uma vez e derive as duas; nunca deixe uma dizer algo que a outra contradiga. Entregue a apresentação
quando o usuário pedir algo para gestores, uma devolutiva, uma apresentação ou um resumo executivo; ofereça-a ao
entregar o relatório.

### Estrutura da Apresentação 4D

Cada seção é um slide: um `heading` com o título e um `paragraph` com o mesmo `section_key`, mais cards ou tabela
quando ajudar.

| `section_key` | Slide | O que contém |
|---|---|---|
| `challenge` | Desafio | Objetivo, ponto de partida (dados e perguntas que o 4D devia responder), o que mudou desde o briefing |
| `findings` | Principais achados | Os dois ou três temas mais fortes, com onde apareceram e a força; contradição principal |
| `solution_hypothesis` | Hipótese de solução | As três partes: Acreditamos que / Porque o diagnóstico mostrou / Precisamos validar se |
| `convergence` | Convergência | Ranking do D4 com a regra, e o que o grupo concluiu na rodada final; preferência não é validação |
| `next_steps` | Próximos passos | O que o 3E precisa resolver, o que segue aberto, responsáveis ou "a definir" |

Regras: título que diz a conclusão do slide (de 4 a 14 palavras, não genérico), até 4 blocos e 140 palavras por slide,
mensagem da capa (`summary`) em até 35 palavras, **no máximo 6 slides de conteúdo**. O detalhe fica no relatório. O
renderizador recusa o que fugir disso e confere as três partes da hipótese. Tabela abre slide próprio; escreva o
parágrafo da seção para funcionar sozinho.

## Ordem do relatório completo

| `section_key` do título | Seção | O que contém |
|---|---|---|
| `cover` | Desafio e escopo | Desafio, objetivo, participantes (presentes separados de convidados), data, adaptações |
| `executive_summary` | Resumo | A acabativa em um parágrafo: problema que ficou mais claro, hipótese em uma frase, o que vai para o 3E |
| `d1_d2_diagnosis` | D1 e D2 | Registro, como hoje |
| `d2_process_journey` | Jornada | Registro, como hoje |
| `d3_strategic_consolidation` | Alternativas | Registro, com cada alternativa ligada às dores |
| `d4_prioritization` | Priorização | Registro, com regra, denominador e dissensos |
| `cross_themes` | Temas que atravessaram o 4D | Tabela de temas transversais |
| `analytical_synthesis` | Síntese analítica | Padrões, contradições, comparação com o briefing, limitações |
| `solution_hypothesis` | Hipótese de solução | As três partes, sem fechar tecnologia |
| `conclusion` | Conclusão do aprofundamento | As cinco respostas da acabativa |

As seções novas (`executive_summary`, `cross_themes`, `analytical_synthesis`, `solution_hypothesis`) e o texto da
conclusão são obrigatórios na versão completa. A skill compõe todas a partir das fontes; o grilling só pergunta o que
o material não responde.

## Temas que atravessaram o 4D

Depois do D4, deixe de seguir a ordem das dinâmicas. Cruze os registros e monte uma tabela:

| Tema | Onde apareceu | Evidências | Força |
|---|---|---|---|
| Previsibilidade | D1, jornada, barco, D3 | Ausência de cronograma; "sem previsão"; proposta de roadmap | Alta: 4 dinâmicas e 1ª proposta no D4 |
| Registro | D1, jornada, barco, D3 | "Não atualizamos"; ferramenta abandonada; cultura de registro | Alta: 4 dinâmicas |
| Centralização | Entrevistas, jornada, porto, D3 | Múltiplas fontes de informação | Média: 4 fontes, poucos créditos |
| Priorização | Entrevistas, barco | "Tudo é urgente"; falta de prioridade | Média: 2 fontes |

Exemplo ilustrativo, a partir dos temas citados pela autora; não reutilize.

**Força não é só frequência.** Um tema pesa mais quando aparece em mais dinâmicas diferentes, quando recebe créditos
no D4, quando é confirmado pelos dados do briefing e quando é dito com intensidade (elefante na sala, sentimento
dominante). Escreva o critério na coluna "Força". Um tema citado muitas vezes numa só dinâmica pesa menos do que um que
atravessa três.

Se houver fichas com ID no registro (âncoras A01, icebergs I01, etapas da jornada), cite-as em "Onde apareceu".

## Síntese analítica

Em parágrafos curtos, nesta ordem:

1. **Padrões:** o que se repete e o que isso mostra sobre a causa do problema, não só o sintoma.
2. **Temas mais fortes:** os dois ou três que sustentam a hipótese, com o critério de força.
3. **Contradições:** onde dinâmicas, participantes ou dados apontam para lados diferentes. Preserve; não force
   consenso.
4. **Do briefing ao 4D:** compare com os dados e a hipótese de partida. Use os status: corroborado, corroborado com
   ressalva, aprofundado, reorientado, integrado, transversal, emergente. Diga que os dados medem frequência histórica e
   o 4D traz percepção qualificada, e que isso não valida eficácia.
5. **Limitações:** quem não estava, que dinâmica foi encurtada, o que não foi registrado, que dado faltou.

Use afirmação calibrada ("pode", "nem sempre", "há relatos de") e separe a dor relatada do impacto a examinar.

## Hipótese de solução

Transforme o conjunto de achados numa hipótese, não numa lista de ações. Formato obrigatório, com as três partes:

> **Acreditamos que** [conceito de solução] permitirá [mudança esperada] para [público ou processo].
> **Porque o diagnóstico mostrou** [problemas X, Y e Z, com os temas ou IDs do 4D].
> **Precisamos validar se** [as suposições que o 3E e a experimentação precisam testar].

Regras:

- **Conceito, não tecnologia.** Diga a mudança e o mecanismo, não "um software" nem uma ferramenta. A hipótese fica
  ampla o bastante para o 3E materializar a solução.
- **Ações viram componentes.** "Padronizar o fluxo, criar cronograma base, criar templates, centralizar projetos,
  simplificar o registro" são ações ou desejos. Agrupe-as sob um conceito e liste-as como o que o 3E vai estruturar.

  | Antes (ações soltas) | Depois (hipótese) |
  |---|---|
  | Padronizar o fluxo; criar cronograma base; criar templates; centralizar projetos; simplificar registro | **Acreditamos que** um ponto único de acompanhamento dos projetos, com etapas padrão e registro mínimo, permitirá prever prazos e saber o estado de cada projeto para as equipes e a gestão. **Porque o diagnóstico mostrou** falta de previsibilidade, registro abandonado e informação espalhada em várias fontes. **Precisamos validar se** as equipes mantêm o registro quando ele é mínimo e se a previsão de prazos melhora. |

  Exemplo ilustrativo; não reutilize.
- **Ligada ao diagnóstico.** Cada problema citado em "Porque" aparece na tabela de temas ou no registro de D1 a D4.
- **Coerente com o D4.** Se a hipótese juntar propostas ou divergir do ranking, diga isso e explique. O ranking é
  preferência do grupo; a hipótese é a leitura integrada da análise. Rotule-a como resultado da análise, não como
  decisão do grupo, salvo se o grupo a formulou na rodada de convergência.
- **Uma hipótese principal.** Com o D4 dividido, no máximo uma alternativa, com a razão.

## Conclusão do aprofundamento (acabativa)

Feche com cinco respostas curtas:

1. **O que entendemos:** qual problema ficou mais claro.
2. **Hipótese de solução:** em uma frase, remetendo à seção.
3. **Principais limitações** da análise.
4. **O que o 3E precisa resolver:** o que estruturar e quais suposições priorizar.
5. **O que segue aberto:** perguntas sem resposta e de quem depende.

O mesmo conteúdo, condensado, abre o relatório no Resumo.

## Lacunas

Distinga **fora do escopo por desenho** (a dinâmica não estava prevista nesta execução), **lacuna de registro** (aconteceu
e não foi anotado) e **ausência de dado** (a pergunta exigia dado que não existia). As três ficam escritas; nenhuma é
preenchida com dado inventado.
