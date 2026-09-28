---
name: avaliacao-briefing-iqb
description: "Valida um briefing de inovação pela rubrica IQB do ERIC: quatro dimensões, 40 critérios, vetos e cálculo auditável. Use para avaliar um briefing preenchido ou uma transcrição estruturável e comparar versões sem escolher a nota por impressão geral."
---

# Avaliação de briefing pelo IQB

Esta skill reescreve `validate-briefing` do ERIC_RC6. O IQB é uma rubrica interna de **qualidade do briefing**, distinta do Innovation Project Scorecard da Strategyzer, que avalia maturidade da evidência do projeto.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative esta skill pela tarefa solicitada e pelos insumos disponíveis, em qualquer ponto da esteira ou fora dela. A fase registrada no projeto é contexto de proveniência, não condição de uso nem autorização para inventar conteúdo. Consulte o Scorecard de maturidade quando disponível para localizar evidências e lacunas, sem usá-lo como bloqueio automático. Se a pessoa chegar antes do trabalho usual, produza preparação ou versão parcial e pergunte somente pelos insumos decisivos. Se chegar depois, incorpore os materiais posteriores, preserve a cronologia e indique o que foi definido antes ou reconstruído depois; não apresente reconstrução retrospectiva como plano previamente acordado. A completude depende dos requisitos da entrega e da evidência, não do nome da fase.

## Evidência antes de nota

Leia [levantamento documental e grilling](references/levantamento-documental-e-grilling.md) e a [rubrica IQB](references/iqb-rubric.md). Identifique briefing, versão, HMW, sete campos e fontes. Quando a entrada for transcrição, explicite que é uma reconstrução e não um briefing aprovado. Marque para cada critério `yes` ou `no`, fonte e localização; ausência ou ambiguidade contam `no`, com lacuna específica. Não peça ao usuário qual nota deseja. Pergunte em fronteiras apenas para identificar fontes, versões ou definições que possam alterar a avaliação; resposta sobre intenção não substitui evidência documental.

## Avalie e calcule

Responda exatamente os 10 itens de cada família `CLA`, `EVI`, `OUT` e `ACT`, inclusive o veto de cada uma. A nota de cada dimensão vem dos nove itens pontuáveis, com teto de veto; o IQB é a média das quatro notas. Grave as 40 respostas em JSON (formato no topo de `scripts/iqb.py`) e rode `python3 scripts/iqb.py respostas.json` para contagens, vetos, média e classificação; copie os números do resultado, sem recalcular à mão. O script exige os 40 itens, IDs corretos, resposta booleana e justificativa; não complete avaliações faltantes com valores inventados. O [schema do relatório](references/briefing-validation-report.schema.json) é uma opção de saída estruturada, não dependência de infraestrutura externa.

Se o intervalo entre as quatro notas finais for até 1, reaudite manualmente as evidências de cada resposta antes de finalizar. Notas próximas podem ser corretas; não force dispersão. Não altere a classificação calculada por julgamento editorial. Oriente a melhoria pelos critérios não atendidos e pelos vetos, sem tratar IQB alto como aprovação automática do projeto ou do experimento.

## Entregue

Mostre versão e recorte avaliados, matriz de 40 respostas com citações, notas brutas e finais, veto aplicado, IQB, classificação, pontos fortes, lacunas priorizadas e até três provocações úteis ao sponsor. Se fontes decisivas estiverem inacessíveis, entregue diagnóstico parcial e identifique o que falta antes de calcular nota final. Em comparação de versões, calcule cada uma separadamente com sua própria base e explique mudanças por critério.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `briefing_validation`. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

**Proveniência:** rubrica, schema e cálculo adaptados de fonte metodológica RC6 (`validate-briefing/`); o cálculo foi endurecido para impedir pontuação com itens ausentes.
