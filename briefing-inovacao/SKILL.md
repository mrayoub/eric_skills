---
name: briefing-inovacao
description: "Cria ou atualiza o briefing de um desafio de inovação e, quando solicitado, gera sua síntese executiva de uma página ou perguntas para fechar lacunas. Use em qualquer momento para documentar, reconstruir ou atualizar o desafio com versão e fontes rastreáveis."
---

# Briefing de inovação

Reúne três capacidades do ERIC_RC6: `generate-briefing`, `generate-briefing-one-page` e `generate-briefing-questions`. São modos do mesmo objeto documental; escolha apenas a saída solicitada. A avaliação IQB permanece na skill `avaliacao-briefing-iqb` para que a criação não atribua nota a si própria.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative esta skill pela tarefa solicitada e pelos insumos disponíveis, em qualquer ponto da esteira ou fora dela. A fase registrada no projeto é contexto de proveniência, não condição de uso nem autorização para inventar conteúdo. Consulte o Scorecard de maturidade quando disponível para localizar evidências e lacunas, sem usá-lo como bloqueio automático. Se a pessoa chegar antes do trabalho usual, produza preparação ou versão parcial e pergunte somente pelos insumos decisivos. Se chegar depois, incorpore os materiais posteriores, preserve a cronologia e indique o que foi definido antes ou reconstruído depois; não apresente reconstrução retrospectiva como plano previamente acordado. A completude depende dos requisitos da entrega e da evidência, não do nome da fase.

## Leia e pergunte

Use [levantamento documental e grilling](references/levantamento-documental-e-grilling.md). Leia entrevistas, CDT, dados, versões do briefing e decisões disponíveis antes de perguntar. Separe descrição do problema, interpretações, causas supostas e soluções sugeridas. Pergunte apenas por lacunas que mudam os sete campos ou a saída pedida; não peça ao usuário que escolha a conclusão do projeto. Salve fontes e localizadores em cada versão.

## Modo briefing

Use a [estrutura de sete campos](references/briefing_template.md): título; desafio/HMW; descrição do problema ou oportunidade; relevância institucional; resultados esperados; responsável; sponsor. Preserve HMW original e proponha reformulação em campo separado quando necessário. Escreva resultados como mudanças esperadas, distinguindo-os de entregas e funcionalidades. Não transforme uma hipótese de causa em fato nem acrescente números sem fonte, período e unidade. Marque campos sem suporte como pendentes e indique a pessoa ou dado que poderia resolvê-los.

Se o usuário pedir melhoria, mantenha vínculo com a versão-base, registre insumos novos e produza **nova versão do mesmo briefing**. Não sobrescreva a versão anterior nem crie um tipo fictício de “briefing incrementado”. Para integração que exige JSON, use o [schema do briefing](references/briefing.schema.json); em uso conversacional, entregue os sete campos legíveis com o mesmo conteúdo e linhagem.

## Modo síntese de uma página

Use uma versão identificada do briefing como fonte principal; se ela não existir, reconstrua uma versão provisória a partir das fontes, rotule-a e registre o que precisa de validação. Condense HMW, problema, relevância, resultados, responsável e sponsor, mantendo nuances e lacunas que mudam a decisão. A one-page é derivada: não pode introduzir evidência ou prometer impacto ausente do briefing. Registre `briefing_version_id` e fontes adicionais. Para renderização, consulte o [schema da one-page](references/briefing-one-page.schema.json) e a variante compartilhada `executive_one_page`: A4 paisagem, uma página, sem reduzir a fonte abaixo do mínimo.

## Modo perguntas de melhoria

Use uma versão identificada do briefing ou uma reconstrução provisória, e, quando houver, a avaliação IQB. Priorize primeiro lacunas verificáveis que impedem compreender o problema ou agir, depois questões exploratórias. Cada pergunta aponta campo, fonte já consultada, razão e possível respondente. Elimine duplicatas e limite a lista inicial a 12 perguntas; abra novas fronteiras após as respostas se necessário. Não invente respostas nem trate nota IQB alta como proibição de investigar. Para saída estruturada, use o [schema de perguntas](references/briefing-improvement-questionnaire.schema.json).

## Checagem de entrega

Confira que a saída pedida está completa para sua finalidade ou explicitamente parcial; que todo fato decisivo volta a uma fonte; que responsáveis não foram inferidos; e que síntese e perguntas apontam para a versão correta do briefing. Não gere automaticamente as três saídas quando o pedido exigir apenas uma.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `briefing`, `briefing_one_page` ou `briefing_improvement_questionnaire`, conforme o modo solicitado. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

**Proveniência:** adaptação das três skills homônimas das fontes metodológicas do RC6, com a estrutura de briefing do ERIC_RC1 preservada nos recursos locais. Funciona sem infraestrutura da iniciativa de origem.
