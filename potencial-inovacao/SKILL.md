---
name: potencial-inovacao
description: "Avalia e prioriza uma dor ou oportunidade com a rubrica interna de potencial de inovação do ERIC: impacto, viabilidade, alinhamento, urgência e novidade. Use para informar, revisar ou auditar uma decisão de prioridade em qualquer momento; exige justificativa e evidência para cada critério."
---

# Potencial de inovação

Adapta `calculate-innovation-potential` do ERIC_RC6. Esta rubrica interna de priorização **não é** o Innovation Project Scorecard da Strategyzer nem mede resultado de uma experimentação.

Leia [levantamento documental e grilling](references/levantamento-documental-e-grilling.md) e a [rubrica de potencial](references/innovation-potential-rubric.md). Defina oportunidade, público, versão, decisão de priorização e, se conhecida, fase registrada apenas como contexto. Para cada um dos cinco critérios, registre afirmação, evidência favorável/contrária, fonte/localização, limite e nota justificada entre 0 e 100. Diferencie impacto esperado de impacto medido; viabilidade percebida de recurso comprometido; urgência documentada de preferência do sponsor.

Se faltar base para qualquer nota, marque `não pontuável` e investigue a fonte ou o responsável em ordem de dependência. Não converta ausência de dados em zero e não emita `priorizar`, `monitorar` ou `arquivar` como classificação definitiva sobre entrada incompleta. Uma nota zero é uma avaliação sustentada, não um marcador de lacuna. Pergunte por dados, critérios e restrições; nunca pela prioridade desejada.

Após justificar as cinco notas, grave as cinco notas e justificativas em JSON (formato no topo de `scripts/score.py`) e execute `python3 scripts/score.py notas.json` para aplicar pesos e faixas definidos na rubrica. Não ajuste resultado calculado editorialmente. Mostre as notas, fontes, pesos, total, classe, principais sensibilidades e próximos dados capazes de mudar a leitura. Registre decisão de priorização efetivamente tomada separadamente da recomendação calculada.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative esta skill pela tarefa solicitada e pelos insumos disponíveis, em qualquer ponto da esteira ou fora dela. A fase registrada no projeto é contexto de proveniência, não condição de uso nem autorização para inventar conteúdo. Consulte o Scorecard de maturidade quando disponível para localizar evidências e lacunas, sem usá-lo como bloqueio automático. Se a pessoa chegar antes do trabalho usual, produza preparação ou versão parcial e pergunte somente pelos insumos decisivos. Se chegar depois, incorpore os materiais posteriores, preserve a cronologia e indique o que foi definido antes ou reconstruído depois; não apresente reconstrução retrospectiva como plano previamente acordado. A completude depende dos requisitos da entrega e da evidência, não do nome da fase.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `innovation_potential_assessment`. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

**Proveniência:** rubrica e algoritmo adaptados de fonte metodológica RC6 (`calculate-innovation-potential/`); o algoritmo foi revisto para preservar incompletude em vez de classificar faltas como zero.
