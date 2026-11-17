# Revisão editorial preliminar dos seis oficiais

Base: `e53a71c593a19df777a9cc4b9dc73f78f691fa57`, com alterações locais da feature em desenvolvimento.
Escopo: escrita, significado do método, cobertura aplicada e coerência dos exemplos; não substitui o Verifier final em HEAD.

## Referências examinadas

- Plano aprovado em `plan.md`, em especial critérios 18, 20 e 32 a 41.
- Exemplo da autora: `relatorio-5c/references/exemplos/5c-oficial-sessao-coletiva-apresentacao.md`.
- `_SHARED/tom-oficial.md` e as três cópias distribuídas.
- `SKILL.md` e `references/entregaveis-oficiais.md` de relatorio-4d, relatorio-3e e relatorio-5c.
- Os seis `input.json` oficiais, os doze JSONs adaptados/pocket e os dois JSONs 5C de sessões combinadas em `official_variants`.

## Findings

### ER-01: Capas e estruturações de variantes atribuem atividades que o inventário exclui

Gravidade: alta. Estado: corrigido na reconferência dos JSONs regenerados, conforme evidências abaixo. O texto desta seção preserva o achado da primeira leitura.

Localizadores: `summary` e bloco `structuring` dos JSONs em `_SAMPLES_ENTREGAVEIS/official_variants`.

- `five_c_official_report.pocket.json` e sua apresentação contêm na capa: "Os grupos cocriaram duas propostas; a preferência registrada...". O inventário inclui somente C1 a C3, excluindo C4 e C5 por desenho. A estruturação também diz que "os canvases organizaram a cocriação" e que a contagem de créditos foi por pessoa. O C3 desta variante foi corretamente descrito como confirmação curta por post-its, o que torna a contradição da capa mais visível.
- `four_d_official_report.pocket.json` e sua apresentação dizem "O grupo priorizou uma visão compartilhada do fluxo" e descrevem brainwriting e créditos na estruturação, embora D3 e D4 estejam fora do escopo.
- `three_e_official_report.pocket.json` e sua apresentação afirmam que foi delimitado "um teste de atualização" e que "os Test Cards organizaram testes prospectivos", embora E3 esteja excluído.
- As variantes adaptadas dos três métodos substituem a etapa final por confrontar condições, declarando "não houve distribuição de créditos nem ranking". As capas 4D e 5C preservam a preferência do grupo da aplicação integral; no 3E, a capa e a estruturação ainda afirmam o planejamento por Test Card que a etapa adaptada não realizou.
- No caso misto 5C, a estruturação distingue remoto C1 a C3 e presencial C1 a C5; as sínteses têm prefixos de sessão. A capa pode sintetizar o conjunto, mas precisa atribuir propostas e créditos à sessão presencial, sem deixar a cobertura parecer comum às duas.

Impacto: os exemplos ensinam a adaptação por metadados, mas continuam narrando a execução integral. Isso viola a distinção entre fora do escopo por desenho e atividade realizada, central no pedido do usuário e no exemplo da autora.

Correção esperada: derivar título quando afetado, capa, introdução, estruturação e fechamento do inventário e do registro efetivo. Na estruturação, distinguir ferramentas utilizadas das excluídas; não afirmar resultados de uma etapa substituída ou não realizada. Aplicar a correção tanto ao relatório quanto à apresentação e regenerar os exemplos a partir da fonte.

### ER-02: A estruturação dos exemplos não explicita o método e a razão de sua aplicação

Gravidade: média. Estado: corrigido na reconferência dos JSONs regenerados, conforme evidências abaixo. O texto desta seção preserva o achado da primeira leitura.

Localizadores: bloco `structuring` dos seis `input.json` oficiais integrais, inclusive os três pitches.

Os textos explicam a escolha de participantes e citam ferramentas, mas não dizem explicitamente o que são 4D, 3E e 5C nem por que se escolheu cada método para a pergunta daquele momento. Por exemplo, o 3E diz que o quadro de escopo separou o que precisa existir do que pode evoluir e que os Test Cards organizaram testes; a natureza do método fica inferida pelas etapas. A receita e o critério 19 pedem essa explicação no pitch.

O título comum "O formato reuniu os perfis necessários para a escuta" também é genérico para os três métodos. No 3E, o propósito central é estruturar uma solução, construção e testes. O exemplo da autora usa títulos que dão uma leitura concreta do formato, como duas sessões com profundidades diferentes.

Correção esperada: acrescentar uma explicação curta e específica do papel do método e da razão de escolha em cada estruturação, mantendo o limite do slide por divisão quando necessária. Ajustar o título de acordo com o que foi estruturado em cada aplicação; não é necessário reproduzir a tabela metodológica do exemplo da autora.

## Reconferência dos JSONs regenerados

ER-01 encerrado quanto à atribuição de atividades ausentes:

- As seis pockets agora abrem com "A sessão pocket aprofundou o recorte inicial" e explicam que as etapas seguintes ficaram fora do escopo. A estruturação 4D declara que não houve alternativas ou priorização; a 3E diz que Test Cards e planejamento de experimentos não fizeram parte da rodada; a 5C informa confirmação por post-its sem experiência desejada, critérios, cocriação ou votação de propostas.
- As seis adaptadas abrem com "A aplicação adaptada confrontou condições de uma oferta existente na rodada final". O 4D e o 5C explicam a rodada final sem créditos ou ranking; o 3E explicita que não produziu Test Cards nessa rodada. Não restam as alegações anteriores de preferência ou teste planejado na capa dessas variantes.
- Nos dois casos mistos 5C, o inventário preserva `remoto_c1` a `remoto_c3` e `presencial_c1` a `presencial_c5`. A estruturação diz "C4 e C5 ocorreram apenas no presencial". O C3 remoto registra a confirmação curta e seu limite; execução e desfecho de cocriação e créditos têm prefixo `presencial:`. Na conferência final, a capa também passou a atribuir as contribuições: "O remoto confirmou temas; no presencial, os grupos cocriaram propostas e priorizaram a consulta". A separação aparece agora no inventário, na estruturação, nos blocos e no resumo.

ER-02 encerrado nos seis padrões:

- 4D: "O 4D aprofunda um desafio por percepções, diagnóstico, alternativas e priorização. Foi escolhido para investigar a demora percebida antes de assumir uma solução." O título passou a "A jornada e o barco orientaram o aprofundamento do fluxo".
- 3E: "O 3E estrutura uma hipótese de solução em escopo, construção e experimentos. Foi escolhido para detalhar a hipótese do 4D e expor as condições ainda abertas antes de construir." O título passou a "A estruturação reuniu operação e apoio técnico para delimitar a construção".
- 5C: "O 5C organiza a escuta e a cocriação com clientes, do contexto aos encaminhamentos. Foi escolhido para entender o que os clientes precisam saber sobre um pedido antes de testar propostas de acompanhamento." O título explicita a contribuição de cada sessão.

### ER-03: A conclusão das variantes continua genérica e não sintetiza seus achados

Gravidade: média. Estado: corrigido na conferência editorial final dos JSONs regenerados. O texto desta seção preserva o achado da primeira reconferência.

Localizador: bloco `conclusion` dos doze JSONs `.pocket.json` e `.adapted.json`.

Todos usam o mesmo texto: "A aplicação registrou os achados das etapas incluídas no recorte. As etapas excluídas por desenho não foram realizadas, e a mudança de dinâmica limita a comparação com o método integral. Não houve aprovação de implementação."

O limite está correto, mas a conclusão não nomeia qualquer resultado do trabalho. É um fechamento burocrático comum a três métodos diferentes, enquanto o tom da autora e a receita pedem uma síntese analítica. Nos adaptados, também se fala de etapas excluídas embora o inventário declare que não houve exclusão; isso não é uma falsa execução, mas é texto desnecessário e pouco específico.

Correção esperada: usar os achados já existentes nas etapas. Exemplos de núcleo a sintetizar: 4D pocket, registros dispersos na passagem entre áreas, sem alternativa priorizada; 3E pocket, recorte do protótipo e dependência de atualização, sem planejamento E3; 5C pocket, necessidade de estado/responsável/previsão e confirmação curta, sem propostas. Nas adaptadas, ligar esses achados às condições confrontadas e ao limite da rodada final. Não inventar resultado novo para produzir uma conclusão mais forte.

## Evidências de tom nos seis padrões

| Entregável | Trecho/localizador | Avaliação |
| --- | --- | --- |
| Relatório oficial 4D | `d2_execution`: protocolo, previsão e responsável em registros diferentes; `d2_outcome`: "não houve medição de retrabalho" | Há episódio concreto, leitura do padrão e limite próximo da afirmação. É o raciocínio do exemplo da autora, sem copiar seu contexto. |
| Apresentação oficial 4D | `execution_d4`: três créditos por pessoa, oito dos doze para a visão compartilhada; "Não houve aprovação de construção" | Regra e denominador ficam explícitos; preferência não é convertida em decisão ou eficácia. |
| Relatório oficial 3E | `e2_outcome`: "A construção está planejada, não concluída"; rota indefinida até avaliação técnica | Tom concreto e calibrado, separando plano, execução e dependência. A descrição por etapa mantém a receita sem repetir slogans. |
| Apresentação oficial 3E | `execution_e3`: simulação, atualizações e tempo de registro; "Não há resultado de uso ou eficácia" | O slide comunica o que será observado e seu limite. Critério pendente aparece antes de qualquer alegação de teste pronto. |
| Relatório oficial 5C | `c2_execution`: quatro de seis presentes; dois citaram utilidade no protocolo; `c2_outcome`: menções não são prevalência ou votos | Preserva denominador, o que funciona e o alcance qualitativo da escuta. |
| Apresentação oficial 5C | `execution_c4`: consulta e avisos ligados às necessidades; "Menos contatos ... é benefício esperado, ainda sem medição" | Liga proposta à dor e distingue benefício esperado de efeito medido, como a referência da autora. |

Os seis padrões usam fonte por bloco, linguagem simples e verbos neutros. Não encontrei reutilização de nomes, números ou achados específicos do contexto de comercializadores varejistas da referência 5C. Os cenários fictícios usam outro fluxo e preservam a distinção entre relato, proposta, preferência e decisão.

Os relatórios mantêm descrição separada da execução e do desfecho; os pitches combinam execução e leitura em um bloco por etapa. Essa síntese é compatível com a receita. Uma futura saída real pode aprofundar episódios e tabelas no relatório conforme as fontes, sem impor três evidências ou a densidade do exemplo visual.

## Orientações das skills e referência comum

As três receitas oficiais reconhecem alterações de nome, significado, ordem, dinâmica, duração e quantidade de fases. Explicitam que uma pocket pode estar completa em seu escopo e que uma etapa prevista sem registro continua lacuna. A distinção é adequada e está disponível nas três instalações.

A referência comum traduz bem a voz da autora: afirmação, evidências e leitura, títulos com achados, contagens com denominador e ressalvas locais. Não transforma três evidências em quota obrigatória. A explicação de que uma contagem de palavras não comprova tom é adequada para a revisão independente posterior.

As instruções de análise integral anteriores permanecem como referência. No 4D, a frase "somente D1/D2 exige parcial" aparece nessa seção integral, mas a seleção oficial e a receita nova prevalecem explicitamente para pockets. Não a tratei como mudança metodológica obrigatória pendente; convém manter a delimitação integral inequívoca para evitar aplicação acidental aos oficiais pocket.

## Conferência editorial final

ER-01, ER-02 e ER-03 estão fechados nos arquivos atuais. A conferência incluiu os doze JSONs adaptados/pocket e os dois casos mistos. As conclusões de relatório e apresentação são consistentes entre si para cada aplicação:

| Método e variante | Trecho da conclusão conferida | Resultado |
| --- | --- | --- |
| 4D pocket | "D1 e D2 aprofundaram a questão, sem desenhar alternativas ou registrar preferência"; relaciona demora à passagem por registros dispersos | Síntese concreta do diagnóstico, sem inventar priorização. |
| 4D adaptado | "O diagnóstico relacionou a demora a registros dispersos e o desenho gerou alternativas"; rodada final sem créditos não escolhe vencedora | Preserva achados e limite da etapa adaptada. |
| 3E pocket | "delimitou responsável, estado e previsão no primeiro recorte"; E3 fora do escopo, plano de teste ainda por elaborar | Registra construção planejada e não executada, sem atribuir Test Card ausente. |
| 3E adaptado | "a construção planejada depende da atualização entre áreas"; confronto de adoção substituiu experimentos | Conclui sobre a dependência, mantendo avaliação e teste em aberto. |
| 5C pocket | "A confirmação por post-its delimitou temas para aprofundar, sem experiência desejada, critérios, propostas ou ranking" | Síntese do alcance real da sessão curta, sem tratar exclusão como lacuna. |
| 5C adaptado | "a escuta ligou previsibilidade a estado e responsabilidade"; consulta e avisos cocriados, sem preferência formal na rodada adaptada | Liga escuta, propostas e dependências sem fabricar votação. |

No misto 5C, `summary` atribui confirmação ao remoto e cocriação/priorização ao presencial. O desfecho pode sintetizar a aplicação conjunta porque a origem dos achados está preservada nas etapas prefixadas e na estruturação. Não encontrei nova inconsistência material nos trechos alterados.

## Verdict

Revisão editorial preliminar aprovada: os seis padrões e seus exemplos adaptados, pocket e mistos seguem o tom analítico, concreto e calibrado identificado na autora. As três ocorrências registradas foram corrigidas e conferidas. Esta aprovação trata dos JSONs e orientações atuais; não substitui a validação mecânica dos derivados nem o Verifier final em HEAD.
