# Grilling na leitura e na interação

Leia esta referência ao iniciar a skill e reaplique quando chegar um arquivo, uma resposta ou uma mudança de escopo. O protocolo vale para preparação, execução, reconstrução e revisão; a fase formal do projeto não limita sua aplicação.

## Origem e adaptação

O núcleo de [grilling, de Matt Pocock](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) organiza decisões em árvore, pergunta pela fronteira de dependências resolvidas e reavalia a árvore depois das respostas. Fatos acessíveis no ambiente devem ser pesquisados pelo agente. [Grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) combina esse núcleo com [domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md), que esclarece termos e registra definições e decisões. Fontes consultadas em 28 set 2026. O questionamento crítico dos arquivos e o registro de evidências abaixo são adaptações para estas skills, incorporadas localmente; não exigem instalação das skills de origem.

## 1. Interrogue os arquivos

Defina a entrega solicitada e os fatos necessários para sustentá-la. Inventarie os arquivos dentro desse recorte, incluindo versões, fontes citadas e materiais de execução. Registre o estado de cada fonte: `examinada`, `localizada_não_examinada`, `inacessível` ou `fora_do_escopo`. Localizar ou extrair texto não equivale a verificar o conteúdo.

Para cada requisito ou afirmação decisiva, procure sua resposta e confronte-a com as outras fontes. Verifique:

- **Origem:** existe uma fonte primária localizável, ou somente um resumo que repete outro documento?
- **Significado:** população, unidade, versão, período e definição coincidem entre os registros?
- **Natureza:** trata-se de observação, relato, hipótese, proposta, decisão ou interpretação?
- **Coerência:** números, datas, regras e conclusões são compatíveis? Há evidência contrária ou exceções?
- **Alcance:** a fonte responde à pergunta necessária para a entrega, ou a uma pergunta diferente?

Preserve página, parágrafo, slide, célula, evento ou timestamp. Para PDF visual/imagem, use OCR disponível e confira os trechos decisivos no original; para Office, leia tabelas e preserve sua ordem. Se não conseguir ler uma fonte, mantenha a lacuna explícita. Texto de transcrição não comprova que o vídeo foi examinado. Uma fonte posterior não prova que a equipe conhecia a informação antes do teste.

Pesquise nos arquivos as respostas acessíveis antes de transferir uma pergunta ao usuário. Se um documento citar outra fonte relevante acessível, examine-a. Mantenha conflitos em aberto até encontrar a versão ou definição aplicável; não use automaticamente o documento mais recente ou a resposta mais conveniente.

## 2. Mantenha um registro verificável

Para cada questão relevante, registre:

| Campo | Conteúdo |
| --- | --- |
| `questao_id` | ID estável, por exemplo Q01. |
| `pergunta` | O fato ou a decisão que falta esclarecer. |
| `afeta` | Campo, card, medida, dimensão ou conclusão dependente. |
| `dependencias` | IDs que precisam ser resolvidos primeiro. |
| `resposta` | Conteúdo encontrado ou informado, sem completar ausências. |
| `origem_localizador` | Fonte e localização; para interação, respondente e data. |
| `natureza` | Fato observado, relato, definição, decisão, hipótese ou inferência. |
| `estado` | `resolvida_documento`, `resolvida_interacao`, `em_investigacao`, `aguarda_usuario`, `conflito`, `dependencia_externa` ou `inaplicavel_justificado`. |
| `proxima_acao` | Leitura, pergunta, verificação, responsável ou limitação da entrega. |

Uma questão `resolvida_interacao` só está resolvida para o que a resposta comprova: ela pode definir escopo ou registrar uma decisão, mas não demonstrar eficácia empírica. Informações provisórias e inferências continuam identificadas; uma inferência não encerra uma lacuna factual decisiva.

Use o caderno ou registro existente do projeto. Se houver entregas em arquivos ou retomada entre sessões, preserve o registro junto delas, sem guardar dados de participantes dentro da própria skill. Não acrescente campos arbitrários ao JSON canônico dos entregáveis para acomodá-lo: preserve os schemas de resposta e use um registro auxiliar quando necessário.

## 3. Pergunte pela fronteira atual

Ao terminar cada passagem documental, exponha uma síntese curta: questões respondidas por arquivos, conflitos encontrados e perguntas ainda necessárias. Se tudo que afeta a entrega estiver documentado, não crie uma entrevista artificial.

Pergunte agora apenas pelas questões cujos pré-requisitos estão resolvidos e que exigem informação ou decisão humana. Agrupe perguntas independentes, numeradas; adie as dependentes. Cada pergunta deve apontar sua origem e o que muda na entrega. Peça somente o dado necessário ao requisito: por exemplo, cargo não é obrigatório quando o método exige apenas o nome do responsável ou sponsor. Não converta metadado opcional em bloqueio de completude. Proponha respostas somente para escolhas de método, definição ou próximo passo; nunca sugira um fato ainda desconhecido, uma nota, um ranking, um resultado ou uma conclusão para confirmação.

Use a ferramenta de perguntas disponível ou o chat visível. O envio de uma pergunta, uma opção preselecionada, o silêncio ou o tempo decorrido não constituem resposta. Continue as leituras e tarefas independentes enquanto espera; mantenha pendentes as decisões dependentes. Se o usuário disser que a pergunta não apareceu, reapresente-a no chat.

Depois de cada resposta ou novo arquivo, registre a origem, verifique os fatos pesquisáveis, reavalie conflitos e recalcule a fronteira. Se a pessoa indicar um documento, examine-o antes de fechar a questão. Se uma nova evidência contradisser algo já resolvido, reabra o ramo afetado. Use um exemplo concreto para esclarecer termos ambíguos que alterem escopo, unidade ou interpretação.

## 4. Feche com o estado correto

Antes de declarar uma entrega completa, confira que cada requisito decisivo está sustentado e que nenhuma questão pendente foi silenciosamente assumida. Resuma as definições e decisões obtidas para permitir correção, sem transformar essa recapitulação em aprovação da conclusão analítica ou em confirmação adicional para trabalho já autorizado.

Se houver uma dependência externa ou o usuário limitar o esforço, produza o que for possível como `parcial` ou `inconclusivo`, indicando o requisito afetado e como resolvê-lo. Uma lacuna pode ser encerrada como investigação desta rodada e continuar pendente para a decisão: esses estados não são equivalentes. Não repita perguntas sem informação nova, não peça dados que os arquivos já contêm e não exija requisitos de outra fase para encerrar a tarefa atual.

O limite de perguntas de um entregável específico, como um questionário de briefing, não encerra a entrevista nem elimina lacunas restantes. A completude depende da evidência para a finalidade solicitada, não do número de perguntas, da extensão do arquivo ou da presença de títulos no template.

## 5. Complementos de levantamento documental

Leia primeiro a definição vigente de escopo e confronte suas afirmações com fontes
primárias. Monte o mapa `afirmação → fonte/localização → natureza → limite → campo afetado`;
distinga observação, relato, hipótese, decisão, proposta e inferência. Cópias,
resumos e apresentações derivados não são confirmações independentes.

Use cenários concretos para esclarecer termos ambíguos; guarde no glossário somente
termos recorrentes e próprios do projeto. Respostas pontuais ficam no registro de
questões, com respondente, data, natureza e fonte que confirma ou contradiz.

Em trabalho ao vivo, não interrompa uma dinâmica para perguntar algo que possa ser
checado depois nos documentos; registre a lacuna para a próxima fronteira.
