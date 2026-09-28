---
name: workshop-3e
description: "Prepara e cofacilita o workshop 3E da esteira ERIC: esclarecer hipótese e escopo, estruturar a solução e planejar experimentos. Use em qualquer momento para planejar, revisar ou conduzir E1–E3; registra planos e resultados existentes sem declarar testes não realizados."
---

# Facilitar o 3E

Adapta `facilitate-3e-workshop` do ERIC_RC6. Leia o [playbook 3E](references/3e-solution-structuring-playbook.md) para dinâmicas e tempos. O [blueprint Mural](references/mural-board-3e-template.md) é opcional: use uma ferramenta colaborativa disponível e autorizada, ou registros manuais. Não dependa de nomes específicos de ferramentas.

Leia a [transcrição integral do playbook 3E fornecido](<assets/Modelo 3E Estruturação da Solução.transcricao.md>) e consulte o [DOCX original](<assets/Modelo 3E Estruturação da Solução.docx>) para conferir o método. O [registro de comparação com o RC6](references/fonte-3e-e-divergencias.md) explicita as adaptações dos cards e os limites da fonte.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative esta skill pela tarefa solicitada e pelos insumos disponíveis, em qualquer ponto da esteira ou fora dela. A fase registrada no projeto é contexto de proveniência, não condição de uso nem autorização para inventar conteúdo. Consulte o Scorecard de maturidade quando disponível para localizar evidências e lacunas, sem usá-lo como bloqueio automático. Se a pessoa chegar antes do trabalho usual, produza preparação ou versão parcial e pergunte somente pelos insumos decisivos. Se chegar depois, incorpore os materiais posteriores, preserve a cronologia e indique o que foi definido antes ou reconstruído depois; não apresente reconstrução retrospectiva como plano previamente acordado. A completude depende dos requisitos da entrega e da evidência, não do nome da fase.

## Preparação

Use [levantamento documental e grilling](references/levantamento-documental-e-grilling.md) para ler a hipótese disponível, registros de problema, Relatório 4D, avaliação BP1, resultados experimentais e restrições que existirem. Faça perguntas por fronteiras sobre a solução candidata, papéis, dados e prazo que não estejam documentados. A pergunta de decisão deve ser neutra; não pergunte qual resultado a equipe quer obter na experimentação.

## Condução

Conduza E1–E3 em ordem lógica ao iniciar o método. No RC6, o 3E costuma ser registrado em ideação após o BP1; essa localização não impede execução antecipada, retomada ou revisão posterior. Registre o que o grupo decidiu, o que foi apenas sugerido, quando ocorreu e quem assumiu cada dependência.

1. **E1 — Esclarecer:** explicite a hipótese de origem, a dor focal, o público e a distinção entre o que a solução é, não é e não resolve agora. Liste resultados esperados como hipóteses; critérios de sucesso devem apontar para medidas verificáveis ou lacunas a fechar.
2. **E2 — Estruturar:** classifique componentes em `precisa ter`, `pode evoluir` e `fora deste recorte`. Diferencie o que já existe do que precisa ser construído ou contratado. Registre ação, responsável, apoio, dependência e prazo estimado; nenhum nome ou prazo deve ser inventado.
3. **E3 — Experimentar:** priorize suposições pelo risco, proponha Test Cards **individuais** usando o [modelo de Test Card](assets/test-card.md), com os quatro campos da Strategyzer (hipótese, teste, medida, critério), e escolha método apropriado ao risco, não automaticamente think aloud. Feche medidas e critérios verificatórios antes de executar; marque card incompleto como rascunho. Registre que evidências futuras serão necessárias para os Learning Cards. Se a execução já ocorreu, distinga Test Cards originalmente definidos de reconstruções retrospectivas e encaminhe evidências reais para Learning Cards; antes da execução, não produza achados nem Learning Cards.

O tempo do playbook é sugestão, não prova de conclusão. Se alguma etapa não ocorrer, mantenha o registro parcial e o impacto dessa lacuna no plano. Use `relatorio-3e` para compilar a entrega; a skill `experimentacao-inovacao` pode aprofundar, executar ou analisar testes em qualquer fase, sem depender dela para que esta skill funcione.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

O [playbook 3E original do RC6](assets/3e-solution-structuring-playbook-original-rc6.md) está preservado como fonte histórica imutável; a versão em `references/` contém as adaptações operacionais. Em divergência, identifique a diferença e a data; não reescreva silenciosamente o original.

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `three_e_workshop_record` e, para cada teste, `test_card`. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

**Proveniência:** reescrita de fonte metodológica RC6 (`facilitate-3e-workshop/`). A ordem interna E1–E3 e a separação entre plano e evidência foram preservadas sem restringir a fase de uso.
