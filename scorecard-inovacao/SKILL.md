---
name: scorecard-inovacao
description: "Avalia a maturidade das evidências de um projeto de inovação com o Innovation Project Scorecard da Strategyzer, oficial ou em adaptação institucional declarada, gerando um retrato datado, sem média geral, com lacunas decisivas e próximos testes. Use quando o usuário perguntar quão validado ou maduro está um projeto, se há evidência suficiente para passar um gate, ou quiser comparar retratos ao longo da esteira. Não use para dar nota a um briefing (use avaliacao-briefing-iqb) nem para priorizar oportunidades novas (use potencial-inovacao)."
---

# Scorecard de evidências para inovação

Avalie o mesmo projeto em diferentes momentos da esteira — descoberta, definição, experimentação, piloto e decisão de adoção — com retratos datados da força das evidências. O objeto avaliado é a **maturidade das evidências sobre o projeto**, não a qualidade de execução da fase ou a aprovação automática de um gate.

O [Innovation Project Scorecard oficial](https://www.strategyzer.com/library/innovation-project-scorecard) foi concebido para projetos de modelo de negócio e proposta de valor. Leia [estrutura e adaptação](references/estrutura-e-adaptacao.md) antes de pontuar ou adaptar dimensões. Use o [modelo de saída](assets/scorecard-projeto.md) para produzir um retrato rastreável. Não apresente a versão adaptada como formulário oficial da Strategyzer nem reproduza seu layout gráfico.

O levantamento integra, nesta própria skill, a disciplina de [grilling ancorado em documentos](references/entrevista-e-documentos.md), derivada de `grill-with-docs`/`grill-me` e de suas skills-base `grilling`/`domain-modeling`. Leia essa referência em toda avaliação. Não invoque nem exija a instalação dessas outras skills.

Para ler PDFs, arquivos Office, HTML, tabelas e imagens, siga o [protocolo de extração documental](references/extracao-documental.md), incorporado a esta skill a partir de procedimentos publicados por skills de PDF e de conversão para Markdown. Ele é interno e independente da instalação das skills de origem.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Prepare o retrato

1. Identifique projeto, pergunta de decisão, fase, data de corte, versão da solução, público, escopo e responsáveis pela análise e pelo gate. Se houver retrato anterior, preserve-o e compare versões; não altere pontuações passadas à luz de evidência nova.
2. Inventarie os materiais de todas as fases disponíveis e classifique cada fonte como `examinada`, `localizada, não examinada`, `indisponível` ou `fora do escopo`. Leia primeiro o documento vigente que fixa escopo, hipótese ou decisão da fase, quando existir, e depois confronte-o com fontes primárias e versões anteriores; não presuma que a versão mais recente contenha a melhor evidência. Aplique o protocolo de extração por formato; preserve número de página, slide, seção, aba/célula ou tempo, registre falhas de leitura e confira no original tabelas, números e trechos decisivos. Extraia afirmações, definições, decisões, evidências e conflitos com fonte e localização. Não peça ao usuário fatos documentados. Registre o que veio de briefing, entrevistas, protótipos, Test Cards, Learning Cards, dados operacionais ou decisões. Uma entrevista de descoberta não vira observação de uso do MVP.
3. Escolha e declare a modalidade: **oficial como referência**, quando as dimensões de modelo de negócio se aplicam, ou **adaptação institucional**, quando o projeto busca serviço, eficiência, conformidade ou outro valor público/interno. Na adaptação, explicite a tradução de cada dimensão; não trate custo evitado como receita ou obrigação de uso como prova de desejabilidade.

## Entreviste apenas sobre o que os documentos não resolvem

Monte uma árvore das decisões necessárias para avaliar as dimensões e interpretar as fontes. Separe fatos pesquisáveis, conflitos documentais, termos ambíguos e decisões que dependem de responsáveis. Resolva fatos inspecionando arquivos ou ferramentas disponíveis; se uma resposta mencionar outra fonte, examine-a antes de perguntar de novo. Trabalhe por **rodadas de fronteira**: reúna as perguntas independentes cujos pré-requisitos já estão resolvidos, numere-as, explique o documento ou lacuna que motivou cada uma e ofereça uma resposta recomendada **apenas para método, definição ou próximo passo**, nunca para a nota, conclusão ou resultado desejado. Espere as respostas antes de abrir ramos dependentes. Use a ferramenta de perguntas do ambiente quando existir; caso contrário, pergunte no chat. Registre respostas, origem, conflitos e questões pendentes; atualize a árvore a cada rodada.

Quando um termo colidir com o glossário ou for vago, proponha definição precisa e teste-a com um cenário concreto. Registre no glossário apenas termos específicos do projeto, recorrentes e propensos a alterar futuras leituras; respostas pontuais ficam no registro de questões. Registre decisões duráveis quando houver escolha real, alternativas e razão; não transforme toda resposta em decisão arquitetural. Termine a entrevista quando não restar questão resolvível em aberto. Se faltarem dados externos ou o usuário encerrar a entrevista, entregue avaliação parcial com responsáveis/fontes para as pendências, sem atribuir notas que dependam delas. Antes de fechar uma interpretação decisiva da resposta do usuário, recapitule-a para correção; isso não é pedido de aprovação do resultado.

## Avalie por evidência

- Para cada dimensão aplicável, formule a afirmação examinada e associe fontes e localizações verificáveis. Registre evidências favoráveis, contrárias, data, população, versão e limitações. Diferencie evidência documental/observacional de resposta dada na entrevista: esta pode esclarecer escopo ou apontar uma fonte, mas não prova sozinha adoção, impacto ou viabilidade. Diferencie `sem evidência`, `evidência contrária`, `não aplicável` e `não avaliado`; são estados diferentes.
- Julgue força pela proximidade com comportamento real, qualidade da medida, cobertura e replicação. No instrumento oficial, o eixo de redução de riscos vai de 0 a 5 e distingue declaração, reação a artefato, ação e evidência em mercado real. Use uma nota numérica apenas quando a rubrica adotada estiver definida e o material permitir justificá-la; em adaptação institucional, identifique a rubrica como própria. Nunca complete uma nota a partir da fase do projeto ou de opinião do patrocinador. Registre `não pontuável` se não houver base para nota.
- Não transforme vários relatos em prova de adoção ou impacto. Separe evidência sobre necessidade, usabilidade, implementação, efeito operacional e custo. Quando um teste cobrir só uma parte da solução, mantenha as demais dimensões abertas.
- Não calcule média geral nem sinal verde automático. Destaque dimensões críticas com evidência fraca ou contrária, riscos de dano e dependências. Uma nota alta em uma dimensão não compensa uma falha crítica em outra.

## Entregue a leitura para o próximo gate

Produza o scorecard datado, uma mudança desde o retrato anterior, as lacunas decisivas e os próximos testes capazes de reduzi-las. Conecte cada recomendação a uma dimensão e evidência. Diferencie recomendação analítica da decisão tomada pelo responsável; registre a decisão somente se houver fonte. Antes de concluir, confira que todas as notas, estados e afirmações decisivas tenham rastreabilidade. Se faltarem dados decisivos, entregue retrato parcial e indique precisamente o que falta; não peça ao usuário qual resultado deseja ver.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `innovation_scorecard`. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

