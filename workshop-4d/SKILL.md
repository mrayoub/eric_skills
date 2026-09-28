---
name: workshop-4d
description: "Prepara, conduz ao vivo ou organiza de forma assíncrona o workshop 4D de aprofundamento de um desafio: D1 descongelar percepções, D2 diagnosticar (jornada e barco da inovação: ventos, âncoras, icebergs, porto), D3 desenhar alternativas e D4 decidir com créditos de votação. Use para montar roteiro, pauta, board colaborativo, perguntas de facilitação ou para registrar o que aconteceu em cada D. Não use para escrever o relatório consolidado depois do encontro (use relatorio-4d)."
---

# Facilitar o 4D

Leia a [transcrição integral do playbook 4D fornecido](<assets/Modelo 4D de Aprofundamento.transcricao.md>) e consulte o [DOCX original](<assets/Modelo 4D de Aprofundamento.docx>) para conferir as perguntas, dinâmicas e regras. O [registro de comparação com o RC6](references/fonte-4d-e-divergencias.md) identifica a origem e as adaptações.

Adapta `facilitate-4d-workshop` do ERIC_RC6. Leia o [playbook 4D](references/4d-workshop-playbook.md) para tempos e dinâmicas; use o [blueprint Mural](references/mural-board-4d-template.md) apenas se houver board e autorização para editá-lo. O método pode ocorrer em material físico, conversa ou ferramenta colaborativa.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative esta skill pela tarefa solicitada e pelos insumos disponíveis, em qualquer ponto da esteira ou fora dela. A fase registrada no projeto é contexto de proveniência, não condição de uso nem autorização para inventar conteúdo. Consulte o Scorecard de maturidade quando disponível para localizar evidências e lacunas, sem usá-lo como bloqueio automático. Se a pessoa chegar antes do trabalho usual, produza preparação ou versão parcial e pergunte somente pelos insumos decisivos. Se chegar depois, incorpore os materiais posteriores, preserve a cronologia e indique o que foi definido antes ou reconstruído depois; não apresente reconstrução retrospectiva como plano previamente acordado. A completude depende dos requisitos da entrega e da evidência, não do nome da fase.

## Preparação e entrevista

Leia [levantamento documental e grilling](references/levantamento-documental-e-grilling.md). Examine briefing vigente, HMW, dados, entrevistas e decisões antes de propor perguntas ao grupo. Faça uma fronteira curta de lacunas sobre objetivo, público, participantes, acesso aos materiais e restrições. Não peça ao grupo para confirmar uma causa ou proposta preferida. Diferencie dados externos, percepções internas e hipóteses.

## Condução

Quando a tarefa for conduzir o método completo, percorra D1–D4 em ordem lógica. O RC6 costuma registrar essa rodada em aprofundamento e avaliar seu relatório no BP1, conforme ADR-0037; isso descreve a esteira de origem e não restringe quando a skill pode ser usada. Se D1/D2 já existirem, retome das lacunas e confira se o diagnóstico ainda vale. Se houver resultados posteriores, use-os para atualizar o contexto sem simular uma votação antiga.

1. **D1 — Descongelar:** apresente desafio e dados com fonte; recolha anonimamente o “elefante na sala” e o sentimento dominante. Preserve divergências sem transformá-las em consenso.
2. **D2 — Diagnosticar:** mapeie jornada antes/durante/depois e barco da inovação (ventos, âncoras, icebergs e porto). Para cada afirmação, registre quem relatou, evidência disponível, casos contrários e o que deve ser verificado depois. Salve um snapshot do desafio ao concluir D2; não trate o snapshot como diagnóstico final.
3. **D3 — Desenhar:** faça brainwriting individual nas lógicas eliminar, simplificar e mudar a lógica; depois agrupe alternativas incrementais, estruturais e radicais. Ligue cada alternativa à dor que pretende resolver.
4. **D4 — Decidir:** apresente propostas, aloque créditos segundo a regra combinada antes da votação e registre ranking, razões, dissensos, riscos e responsáveis que aceitaram assumir a próxima investigação. Voto do workshop indica prioridade do grupo, não comprova efeito ou adesão de usuários.

Em cada passagem, apresente objetivo, tempo sugerido, pergunta de facilitação e registro esperado. Adapte duração ao encontro real e registre desvios. Não invente participação, votação nem saída de dinâmica que não aconteceu. Se faltarem D3/D4, entregue registro parcial, não um 4D concluído.

## Encerramento

Produza um registro por dimensão com fontes, participantes, versão, decisões e lacunas, pronto para `relatorio-4d`. Se o projeto usar BP1, ofereça o Relatório 4D concluído como insumo da avaliação; o snapshot D2 é um registro intermediário e não comprova aprovação. Em execução assíncrona, preserve a mesma ordem lógica e identifique quais dinâmicas foram substituídas por leitura documental.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

O [playbook 4D original do RC6](assets/4d-workshop-playbook-original-rc6.md) está preservado como fonte histórica imutável; a versão em `references/` contém as adaptações operacionais. Em divergência, identifique a diferença e a data; não reescreva silenciosamente o original.

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `four_d_workshop_record` para registros exportados do encontro. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

**Proveniência:** reescrita de fonte metodológica RC6 (`facilitate-4d-workshop/`). A sequência interna D1–D4 foi preservada; o vínculo do RC6 com fase e BP1 é apenas contexto histórico da fonte.
