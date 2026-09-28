---
name: relatorio-4d
description: "Compila o Relatório 4D após D1 a D4, com diagnóstico, alternativas, priorização, evidências e lacunas rastreáveis. Use em qualquer momento para transformar registros de workshop ou fontes equivalentes em entrega rastreável, inclusive para avaliação ou revisão posterior."
---

# Compilar o Relatório 4D

Leia a [transcrição integral do playbook 4D fornecido](<assets/Modelo 4D de Aprofundamento.transcricao.md>) e consulte o [DOCX original](<assets/Modelo 4D de Aprofundamento.docx>) para verificar o método usado. O [registro de comparação com o RC6](references/fonte-4d-e-divergencias.md) identifica a origem e as adaptações; o playbook define a condução, mas não fornece resultados de workshops.

Adapta `compile-4d-report` do ERIC_RC6. Leia [levantamento documental e grilling](references/levantamento-documental-e-grilling.md) e o [playbook 4D](references/4d-workshop-playbook.md). O [PDF de referência do relatório](assets/official-four-d-report.pdf) documenta a sequência e a qualidade visual esperadas no projeto de origem; use-o como referência, sem copiar conteúdo específico de outro projeto.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative esta skill pela tarefa solicitada e pelos insumos disponíveis, em qualquer ponto da esteira ou fora dela. A fase registrada no projeto é contexto de proveniência, não condição de uso nem autorização para inventar conteúdo. Consulte o Scorecard de maturidade quando disponível para localizar evidências e lacunas, sem usá-lo como bloqueio automático. Se a pessoa chegar antes do trabalho usual, produza preparação ou versão parcial e pergunte somente pelos insumos decisivos. Se chegar depois, incorpore os materiais posteriores, preserve a cronologia e indique o que foi definido antes ou reconstruído depois; não apresente reconstrução retrospectiva como plano previamente acordado. A completude depende dos requisitos da entrega e da evidência, não do nome da fase.

## Condição de entrada

Identifique o que existe de D1–D4, mesmo se produzido em datas ou fases diferentes. O RC6 costuma fazer os quatro D em aprofundamento e submeter o relatório ao BP1, mas isso não é pré-requisito para compilar ou revisar. O snapshot D2 ajuda a rastrear a evolução do desafio e não substitui D3/D4. Se houver apenas D1/D2, entregue síntese parcial e lacunas. Se houver fontes posteriores, use-as como atualização datada, sem atribuí-las ao workshop original. Para compilação assíncrona, declare quais materiais substituíram cada dinâmica e que decisões de grupo não podem ser inferidas.

## Compilação

1. Inventarie briefing, snapshot D2, mural, transcrições, dados, alternativas e votação; distinga original de síntese derivada. Extraia páginas, linhas, timestamps e imagens relevantes. Pergunte em fronteiras apenas por documentos e decisões que faltarem; não peça a conclusão desejada.
2. Organize a narrativa em D1 (percepções e enquadramento), D2 (jornadas e diagnóstico), D3 (alternativas ligadas a dores), D4 (ranking, regras de votação, dissensos e responsáveis), conclusão e próximos passos. Preserve contagens de participantes e votos com denominador e fonte.
3. Separe em cada achado fato observado, relato interno, hipótese de causa e interpretação do facilitador. Dado de briefing não vira evidência de eficácia de uma solução. Uma votação prioriza investigação; não valida adoção nem impacto. Mostre contraevidências e divergências entre fontes.
4. Registre a formulação atual do desafio, as suposições críticas, alternativas descartadas e razões, bem como fontes ou pessoas que podem fechar lacunas. Se houve BP1, identifique separadamente a formulação submetida naquela data. Associe as recomendações ao diagnóstico e às escolhas documentadas.

Confira sequência, coerência entre texto e números, localização das afirmações e distinção entre proposta e decisão efetiva. Entregue relatório editável conforme o formato pedido; se o usuário pedir um formato estruturado específico, adapte ao contrato informado e preserve a semântica do relatório.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

O [playbook 4D original do RC6](assets/4d-workshop-playbook-original-rc6.md) está preservado como fonte histórica imutável; a versão em `references/` contém as adaptações operacionais. Em divergência, identifique a diferença e a data; não reescreva silenciosamente o original.

Leia também a [estrutura visual de cards do Relatório 4D](references/relatorio-4d-layout.md). Organize diagnósticos, jornadas, ideias e priorização em grades de cards tabulados, com tabelas para comparações e fontes ligadas a cada achado. Use somente categorias apoiadas pelos registros do projeto; a referência visual não fornece conteúdo.

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `four_d_report`. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

**Proveniência:** reescrita de fonte metodológica RC6 (`compile-4d-report/`); a ordem interna D1–D4 foi preservada, sem transformar a fase de origem em condição de uso.
