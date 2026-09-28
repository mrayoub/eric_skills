---
name: workshop-5c
description: "Prepara, facilita ou reconstrói um workshop 5C de cocriação com clientes: C1 contextualizar, C2 compreender a experiência atual, C3 confirmar a experiência desejada, C4 cocriar propostas e C5 conduzir com pitches e créditos de votação. Use para montar roteiro, convite, regras de voto, dinâmicas ou o registro de um encontro com clientes ou agentes. Não use para escrever o relatório consolidado depois do encontro (use relatorio-5c)."
---

# Facilitar o workshop 5C

Leia primeiro a [transcrição integral do DOCX 5C](assets/Playbook_Modelo_5C_Centralidade_Cliente.transcricao.md) para consultar as perguntas e dinâmicas originais; use o [método 5C adaptado](references/metodo-5c.md) para conduzir C1–C5. O [playbook original em DOCX](assets/Playbook_Modelo_5C_Centralidade_Cliente.docx) e sua [transcrição textual](assets/Playbook_Modelo_5C_Centralidade_Cliente.transcricao.md) preservam a fonte fornecida. O documento descreve um encontro específico; não trate serviço, empresas, participantes, responsáveis ou agenda como requisitos de outros projetos.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative pela tarefa e pelos materiais disponíveis, em qualquer ponto da esteira ou fora dela. A etapa formal é contexto de proveniência, não condição de uso. Se o encontro ainda não ocorreu, prepare roteiro, materiais, plano de registro e perguntas pendentes; não declare achados. Se apenas parte ocorreu, registre cada C realizada e a lacuna das demais. Se a análise for posterior, preserve datas, versões, falas, decisões e alterações de método; não transforme reconstrução em deliberação ocorrida.

## Preparação e grilling

Leia [levantamento documental e entrevista por fronteiras](references/levantamento-documental-e-grilling.md). Inventarie briefing, diagnóstico, entrevistas, dados de jornada e decisões disponíveis. Extraia o desafio e suas evidências, identifique perfis de clientes afetados e temas a discutir sem copiar automaticamente os blocos da aplicação de origem. Resolva nos documentos o que já estiver respondido; pergunte por fronteiras apenas sobre público, acesso, objetivo, facilitadores, tempo, forma de registro, condições de participação e decisões que mudam o desenho do encontro. Nunca pergunte que resultado ou ranking o usuário deseja obter.

Planeje uma amostra de perspectivas relevantes, não uma alegação automática de representatividade. Combine antes as regras de voto e crédito, o registro de participantes e a forma de preservar falas, ideias individuais e dissensos. Os 3 votos de C2 e 10 créditos de C5 do playbook são valores de referência, adaptáveis com regra e data explícitas. Confirme a agenda: a duração declarada no DOCX não coincide com todos os intervalos do cronograma.

## Condução

1. **C1 — Contextualizar:** apresente o desafio como formulação atual, sua origem e as dúvidas ainda abertas. Explique a agenda e dê espaço para correções. Registre versão do enquadramento, fontes apresentadas e dúvidas do grupo.
2. **C2 — Compreender:** investigue a experiência atual por temas pertinentes ao projeto. Peça episódios concretos, condições, consequências, pontos que funcionam, fricções e oportunidades. Registre quem relata, perfil, tema e evidência disponível. Priorize temas conforme regra combinada; preserve contagem, elegibilidade, abstenções e divergências.
3. **C3 — Confirmar:** para as dores priorizadas, construa com os clientes a experiência desejada, o que não deve acontecer e como reconhecer melhora. Documente necessidades e critérios observáveis como hipóteses a verificar, inclusive desacordos.
4. **C4 — Cocriar:** recolha propostas individuais antes de formar grupos diversos. Associe cada solução à dor, funcionamento, benefícios alegados e dependências. Preserve ideias de origem, alterações na composição dos grupos e propostas não escolhidas; não force consenso retrospectivo.
5. **C5 — Conduzir:** registre os pitches e aplique a regra de distribuição de créditos definida antes da escolha. Apure ranking reproduzível, razões e objeções. Distinga prioridade expressa pelos presentes de decisão institucional e de validação experimental. Registre encaminhamentos e responsáveis somente quando efetivamente acordados.

No encerramento, devolva síntese de dores, experiência desejada, propostas e prioridades, e comunique apenas próximos passos já definidos. Se o método ocorrer de modo assíncrono, declare quais dinâmicas foram substituídas por documentos e quais decisões coletivas não puderam ser reproduzidas.

## Entrega e limites

Produza registro C1–C5 com fontes localizáveis, participantes ou perfis, versão, regras de votação, contagens, dissensos, decisões e lacunas para a skill `relatorio-5c`. Relatos e votos são evidências sobre experiências e preferências daquele grupo; não comprovam eficácia, escala, viabilidade ou impacto da solução. Encaminhe essas incertezas a testes posteriores quando relevantes.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione o 5C pela pergunta do projeto, sem bloquear seu uso por fase.

## Arquivos e padrão visual

Siga o [sistema visual incluído](assets/design-system/README.md). Gere um `content_json` versionado do tipo `five_c_workshop_record`, com blocos, citações e metadados. O schema comum, o perfil visual, as seções de `assets/design-system/response-sections.json` e o [schema específico 5C](assets/design-system/contracts/five-c-workshop-record.schema.json) são obrigatórios para uma entrega completa; C1–C5 devem ter síntese e fonte. Execute a validação pelo [renderizador local](assets/design-system/scripts/render.py) antes de gerar qualquer arquivo final. Em execução incompleta, marque `metadata.completeness` como `partial` ou `inconclusive`, preserve lacunas e continue validando o schema comum. Todos os formatos devem derivar do mesmo JSON validado; mantenha JSON, PDF, DOCX, MD e TXT quando cabíveis, orientação A4 paisagem do perfil, fontes, cores, citações e área segura. Não altere achados para fazê-los caber na página; pagine e confira ausência de corte.

**Proveniência:** adaptação metodológica do playbook 5C fornecido pelo usuário. Esta skill não atribui origem externa certificada ao método.
