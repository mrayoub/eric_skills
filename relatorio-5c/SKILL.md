---
name: relatorio-5c
description: "Compila ou revisa o Relatório 5C de um encontro de cocriação com clientes, ligando C1 a C5 a falas, votos com denominador, critérios de experiência, propostas, dissensos e próximos passos. Use quando houver registros de um workshop 5C (notas, mural, gravação, votos, ata) e o usuário quiser o relatório, a síntese ou a devolutiva aos participantes. Não use para preparar ou facilitar o encontro (use workshop-5c)."
---

# Compilar o Relatório 5C

Leia primeiro a [transcrição integral do DOCX 5C](assets/Playbook_Modelo_5C_Centralidade_Cliente.transcricao.md) para consultar as perguntas e dinâmicas originais, e então o [método 5C adaptado](references/metodo-5c.md) e o [protocolo de levantamento documental e grilling](references/levantamento-documental-e-grilling.md). O [DOCX original](assets/Playbook_Modelo_5C_Centralidade_Cliente.docx) e a [transcrição textual](assets/Playbook_Modelo_5C_Centralidade_Cliente.transcricao.md) descrevem o roteiro, não os resultados de uma execução. Não produza achados, votos ou consensos a partir do playbook sozinho.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative pela tarefa e pelos registros disponíveis, em qualquer ponto da esteira ou fora dela. Identifique data, versão do desafio e escopo real do encontro. Se C1–C5 não estiverem documentadas, entregue relatório parcial ou estrutura de consolidação com lacunas decisivas; não marque a rodada como concluída. Fontes posteriores são atualizações datadas, não prova de que o grupo as conhecia no workshop. O relatório pode ser revisto depois sem reescrever a versão original.

## Levantamento e fronteiras de perguntas

Inventarie briefing, diagnóstico, convites e presença, materiais exibidos, mural ou notas, gravações acessíveis, formulários, votos, canvases de proposta, ata e decisões posteriores. Registre para cada fonte seu identificador, data, versão e localização. Diferencie fala de cliente, relato de representante interno, dado operacional, proposta, inferência do facilitador e decisão institucional. Resolva primeiro as lacunas nos arquivos; pergunte somente pelo que muda a interpretação, como unidade de voto, participantes elegíveis, proposta votada, regra usada ou responsável que aprovou um encaminhamento. Não peça ao usuário a conclusão ou recomendação desejada.

## Estrutura do relatório

1. **Contexto e método:** desafio original e sua revisão, público convidado e presente, perfis cobertos e ausentes, objetivo, duração real, adaptações de agenda, regras de registro e votação. Não confunda grupo presente com população total de clientes.
2. **C1 — Contextualizar:** o que foi apresentado, que evidência sustentava o enquadramento, dúvidas e mudanças registradas no desafio.
3. **C2 — Compreender:** temas discutidos, experiência atual, situações positivas, dificuldades, episódios concretos, contradições e oportunidades. Mostre a priorização com votos, elegibilidade, denominador e regra efetiva; não trate contagem de menções como prevalência sem desenho apropriado.
4. **C3 — Confirmar:** dores escolhidas, experiência desejada, situações a evitar, necessidades e critérios observáveis de melhora. Separe critério proposto de meta já aprovada e de resultado medido.
5. **C4 — Cocriar:** ideias individuais e propostas coletivas, composição real dos grupos, vínculo de cada proposta à dor, funcionamento, benefícios alegados, dependências, riscos e alternativas não selecionadas. Guarde a origem das ideias quando disponível.
6. **C5 — Conduzir:** pitches, regra de créditos, votos por proposta, ranking reproduzível, razões, objeções e aprendizados. Distinga preferência dos participantes, recomendação analítica e decisão institucional efetivamente tomada.
7. **Síntese e próximos passos:** achados sustentados, limites da evidência, suposições que exigem Test Cards ou outro método, responsáveis e devolutiva acordada. Recomendação proporcional ao que o workshop permite concluir.

Cada afirmação relevante deve apontar para trecho, página, célula, mural, voto ou tempo de gravação verificável. Reconcilie totais entre quadros e narrativa. Preserve divergências e não atribua fala ou aprovação a quem não consta da fonte. Se a votação combinada não foi executada ou não há contagem confiável, descreva essa lacuna em vez de fabricar ranking.

## Qualidade e entrega

Confira C1–C5 separadamente, denominadores, versões e distinção entre experiência relatada, critério desejado e efeito demonstrado. O produto é um relatório de cocriação, não uma validação causal nem autorização de escala. Se a pergunta decisória exigir eficácia, adesão ou viabilidade, recomende um experimento adequado sem antecipar seu resultado.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar fontes e encaminhamentos. A sequência da esteira informa a cronologia; não restringe quando o relatório pode ser preparado ou atualizado.

## Arquivos e padrão visual

Siga o [sistema visual incluído](assets/design-system/README.md). Gere um `content_json` versionado do tipo `five_c_report`, com blocos, citações e metadados. O schema comum, o perfil visual, as seções de `assets/design-system/response-sections.json` e o [schema específico do relatório](assets/design-system/contracts/five-c-report.schema.json) são obrigatórios para entrega completa; C1–C5 devem conter síntese com fonte. Valide pelo [renderizador local](assets/design-system/scripts/render.py) antes de gerar arquivos. Se faltarem etapas ou evidências, marque `metadata.completeness` como `partial` ou `inconclusive` e mantenha a validação comum; nunca preencha uma lacuna para passar no schema. Derive JSON, PDF, DOCX, MD e TXT do mesmo conteúdo validado, em A4 paisagem conforme o perfil, com fontes, cores, citações e área segura. Pagine conteúdo extenso e confira ordem, tabelas, rastreabilidade e ausência de corte.

**Proveniência:** adaptação do playbook 5C fornecido pelo usuário, preservado integralmente em `assets/`. A análise de uma execução depende de fontes adicionais daquela execução.
