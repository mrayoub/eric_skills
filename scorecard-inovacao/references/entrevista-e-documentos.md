# Levantamento documental e entrevista por fronteiras

## Origem e transposição

Esta rotina incorpora diretamente a lógica de [grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) e [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md), de Matt Pocock. Na versão consultada em setembro de 2026, ambas são wrappers curtos: a primeira combina [grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) e [domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md); a segunda chama `grilling`. O repositório original usa licença [MIT](https://github.com/mattpocock/skills/blob/main/LICENSE).

A variante chamada exatamente [grill-me-with-docs](https://github.com/arthur-debert/dodot/blob/main/.agents/skills/grill-me-with-docs/SKILL.md) declara sua origem no repositório de Matt Pocock. Ela acrescenta uma ordem útil: ler primeiro a especificação vigente antes de questionar decisões, e registrar no glossário apenas termos duráveis e de alto valor. Nesta skill, isso significa começar pelo documento que fixa escopo/hipótese, se existir, e depois confrontá-lo com fontes primárias. Mantemos a cadência de fronteiras da versão atual de `grilling` de Matt. O fluxo de `shipit`, o caminho fixo de Spec e a obrigação de ligar ADRs à Spec pertencem ao processo de software daquela variante e não são requisitos do Scorecard.

A rotina original conduz uma entrevista sobre plano ou design, confronta termos com o glossário e registra decisões. Ela **não especifica uma extração abrangente de documentos para pontuar um Scorecard**. A triagem e o vínculo entre afirmação, documento e dimensão abaixo são a adaptação necessária a esta skill. Não declare que essa extensão faz parte da metodologia original.

## Passagem 1: documentos antes de perguntas

1. Varra o escopo fornecido e liste arquivos e dados com caminho/ID, formato, data, fase, versão e estado de leitura. Siga o [protocolo de extração documental](extracao-documental.md). Se houver documento vigente que defina escopo, hipótese ou decisão da fase, leia-o primeiro para saber o que a avaliação precisa esclarecer; depois leia fontes primárias e versões anteriores para conferir suas afirmações. Leia glossário, decisões anteriores, propostas, atas, pesquisa, testes, métricas e relatórios relevantes. Se houver `CONTEXT.md`, `CONTEXT-MAP.md` ou ADRs, use seus termos e decisões para interpretar a documentação; não pressuponha que existam.
2. Para cada afirmação que poderia alterar uma dimensão do Scorecard, anote: afirmação, fonte e localização verificável, autor/data, população, versão, método de obtenção, observação direta ou interpretação, evidência favorável/contrária e limite. Aponte documentos contraditórios sem escolher silenciosamente um deles.
3. Marque em uma matriz por dimensão: `respondida por documento`, `documento contraditório`, `fonte citada mas ausente`, `pergunta a responsável` ou `não aplicável justificado`. Perguntas factuais resolvíveis por arquivos ou ferramentas ficam com o agente; não as transfira ao usuário.

## Passagem 2: árvore de decisões e rodadas de fronteira

A lógica do `grilling` é uma árvore: cada decisão pode liberar decisões dependentes. Sua **fronteira** contém apenas perguntas cujos pré-requisitos estão resolvidos. Em cada rodada, apresente todas as perguntas independentes dessa fronteira, numeradas e com uma recomendação justificada. Espere as respostas; atualize a árvore e forme a próxima fronteira. Perguntas dependentes entram em rodada posterior. Se o ambiente recomendar perguntas uma a uma por limite da interface, preserve a mesma ordem de dependência e o registro da rodada.

Formato sugerido, sem impor uma ferramenta específica:

> **Q1: Definição de público** · O documento F02 usa “agente”, mas F04 inclui representantes. Quem deve entrar no denominador? Proponho contar agentes com obrigação elegível e registrar representantes apenas como contato, porque a medida de pagamento é por agente. Confirma ou corrige? **Origem:** F02, seção X; F04, página Y. **Afeta:** desejabilidade e medida M01.

A recomendação serve para diminuir esforço de resposta em escolhas de método ou definição. **Não recomende uma nota, validação, resultado favorável ou decisão de gate para o usuário confirmar.** O papel do usuário é informar fatos indisponíveis, resolver termos organizacionais e tomar decisões que lhe cabem. Se disser que uma evidência existe em outro arquivo, leia esse arquivo. Se não souber, registre fonte ou responsável capaz de responder e siga para as demais perguntas independentes. Não repita a mesma pergunta sem informação nova.

Após cada resposta, registre `pergunta_id`, conteúdo, autor/data, se é fato informado ou decisão, fontes que confirmam ou contradizem e efeito nas dimensões. A resposta é evidência sobre uma definição/decisão quando o respondente tem autoridade; não é evidência empírica de efeito do projeto. Reabra ramos em caso de contradição. A entrevista chega ao fim quando a fronteira está vazia ou as perguntas restantes dependem de fonte/responsável externo identificado; nesse segundo caso, a avaliação permanece parcial nas dimensões afetadas.

## Linguagem e decisões

O `domain-modeling` confronta termos usados com o vocabulário existente, pede precisão para termos sobrecarregados e usa cenários concretos para testar limites. Faça isso nos conceitos que afetam o Scorecard, como “adoção”, “benefício”, “cliente”, “agente”, “reincidência” e “economia”. Mantenha no retrato apenas termos específicos do projeto que se repetem e cuja ambiguidade afetaria decisões futuras; deixe detalhes pontuais no registro de questões. Se o projeto usar um glossário formal, proponha a atualização nele apenas quando ela estiver no escopo autorizado; não crie documentação paralela sem necessidade.

O método original reserva ADRs para decisões simultaneamente difíceis de reverter, surpreendentes sem contexto e resultantes de uma troca real entre alternativas. Use esses três critérios antes de sugerir um ADR em projeto de software. Para a avaliação transversal, registre a decisão e sua fonte no Scorecard; criar ADR não é obrigação desta skill.

## Checagem antes de pontuar

- Cada pergunta feita ao usuário tinha lacuna e origem identificáveis? A fonte foi lida antes da pergunta?
- A árvore foi reavaliada após as respostas, sem saltar dependências?
- Termos ambíguos que alteram denominadores, população ou valor foram resolvidos ou marcados como pendentes?
- Respostas humanas foram separadas de resultados observados e de documentos?
- Cada dimensão tem evidência rastreável, contraevidência e limite, ou estado de ausência explícito?
- A decisão efetiva foi registrada só quando havia fonte, sem pedir ao usuário para escolher a conclusão analítica?
