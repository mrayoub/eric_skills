# Triagem de lacunas e entrevista orientada a evidências

Use este fluxo quando faltar contexto para planejar, analisar ou recomendar. A completude é relativa à decisão e ao artefato solicitado: não existe obrigação de coletar todos os dados imagináveis.

## 1. Levante o que já se sabe

Leia primeiro as decisões vigentes do 3E e o plano do experimento, quando disponíveis. Consulte briefing e descoberta para entender como se chegou a esse recorte; examine também Test Cards, registros de execução, transcrições, vídeos acessíveis, planilhas e resultados já produzidos. Separe fatos observados, decisões registradas, inferências e fontes ausentes. Quando houver conflito factual ou não for possível identificar a decisão vigente, preserve as versões com data e origem até esclarecer. Não trate resumo anterior como substituto automático da fonte primária.

### Afunilamento do briefing ao 3E

O briefing apresenta o problema inicial; o 4D aprofunda o entendimento e as
alternativas; o 3E consolida a hipótese, o público, a solução escolhida e os testes.
Para esses campos, use as decisões registradas no 3E vigente como referência
principal. Uma atualização posterior documentada pode substituí-las; a data ou
o nome do arquivo, sozinhos, não comprovam que houve essa decisão.

Antes de transformar uma dúvida antiga em pergunta, confira se o 3E a resolveu,
substituiu ou deixou fora do escopo. Registre a fonte e o motivo e encerre essa
questão para a rodada atual, preservando o histórico. Não peça ao usuário para
decidir novamente algo já decidido. Um recorte mais estreito não é, por si só,
contradição com o briefing.

Exemplo: o briefing aborda obrigações financeiras em geral, o 4D discute várias
ações e o 3E escolhe testar avisos na contribuição associativa, deixando Pix
automático para depois. Planeje esse teste; não reabra o tipo de obrigação nem
exija Pix automático para completar o pacote inicial. Se o 3E não definiu a
data-limite de pagamento ou o critério de sucesso, essas lacunas continuam abertas.

A prioridade do 3E vale para decisões, não para tornar afirmações verdadeiras.
Mantenha riscos e evidências contrárias do histórico que ainda afetem o recorte
escolhido. Reabra uma questão quando aparecer evidência nova relevante, uma
contradição factual não resolvida ou dúvida sobre qual decisão vale. Preserve os
critérios registrados antes da coleta; um documento posterior não os altera
retroativamente. Se não houver 3E, trabalhe com o material disponível e identifique
as decisões ausentes, sem exigir o workshop como pré-requisito.

Mantenha um registro com: `item_id`, pergunta que afeta, resposta ou lacuna, status (`fonte examinada`, `decisão confirmada`, `inferência`, `pendente`, `inaplicável`), localização da fonte, responsável pela resposta, artefatos afetados e próxima ação. Use o [caderno da rodada](../assets/caderno-da-rodada.md) quando estiver gerando arquivos.

## 2. Monte a frente de perguntas

Ordene lacunas por dependência e consequência. Pergunte agora apenas o que pode ser respondido sem presumir uma decisão ainda aberta. Depois de cada resposta, reavalie o que ela resolve e que novas perguntas ela desbloqueia.

Perguntas típicas que exigem resposta humana, se não houver registro: quem tem responsabilidade pelo gate; quais obrigações e agentes são elegíveis; quais dados existem e quem pode acessá-los; qual risco operacional é bloqueador; qual restrição de tempo e custo existe; quem aprova o contrato de medidas e uma eventual adaptação antes da coleta. O agente pode propor uma opção metodológica e explicar seu efeito, mas não pode atribuir aprovação a alguém nem reescrever retroativamente um critério. A hipótese e os documentos de origem devem fornecer a pergunta avaliativa; não pergunte qual conclusão, recomendação ou status o usuário quer receber.

Perguntas típicas que o agente deve pesquisar antes de interromper: quais execuções ocorreram e em quais unidades; qual versão da intervenção foi usada; qual procedimento foi seguido; onde está o Test Card original; se há registro temporal, gabarito, comparação ou linha de base; como um número do relatório foi calculado. Se o arquivo não estiver acessível, peça caminho ou anexo com precisão.

## 3. Faça perguntas úteis

- Use o mecanismo de perguntas da plataforma, se existir e estiver disponível; caso contrário, pergunte diretamente na conversa. Não fixe nomes de ferramentas ou schemas de um provedor nesta skill. Em ambos os casos, espere a resposta antes de tomar a decisão dependente: o aceite de uma chamada de ferramenta não é resposta do usuário. Se o usuário disser que não viu a pergunta, reformule-a no canal visível da conversa.
- Agrupe no mesmo turno apenas perguntas independentes. Se o usuário preferir, faça uma por vez. Evite questionários genéricos ou número fixo de perguntas.
- Para cada pergunta, diga qual artefato depende dela e, quando se tratar de método ou operação, ofereça uma proposta baseada no material, claramente identificada como tal. Inclua opções curtas quando ajudarem. Não apresente `ampliar`, `iterar` ou `encerrar` como respostas a escolher antes da evidência; são possíveis saídas do gate após a análise.
- Aceite confirmação, correção, adiamento ou `não sei`. Registre respostas provisórias como provisórias; associe pendência a uma fonte, pessoa ou teste futuro, sem perguntar a mesma coisa repetidamente.
- Quando uma resposta contrariar documento anterior, peça ou procure a versão válida e registre a mudança; não escolha silenciosamente a versão mais conveniente.
- Atualize o registro imediatamente após receber uma resposta. Em trabalhos que atravessam sessões, salve-o junto aos entregáveis para permitir retomada sem refazer a entrevista.

## 4. Aplique gates proporcionais

| Artefato ou etapa | Lacunas que impedem declarar pronto | Saída possível quando faltam dados |
|---|---|---|
| Test Card verificatório | Hipótese focal, método, público, medida/critério, fonte de evidência e dono da decisão | Rascunho com questões abertas; não iniciar verificação formal como se o contrato estivesse fechado |
| Análise da execução | Registros examinados, unidades elegíveis, procedimento, fonte localizável e limites do que foi observado | Análise parcial com cobertura declarada e questões de reconciliação |
| Learning Card | Vínculo ao Test Card, evidências favoráveis/contrárias e distinção entre observação e interpretação | Aprendizado exploratório ou status formal inconclusivo |
| Síntese de evidências e recomendação | Decisão buscada, status dos testes críticos, riscos, evidências e limites relevantes | Recomendação condicionada de investigar, iterar ou testar em piloto controlado, com responsáveis, limites e condição de revisão |
| Apresentação executiva | Números reconciliados, fonte de cada afirmação decisiva e recomendação consistente | Versão preliminar identificada; não apresentar como resultado final validado |

No fim, releia as pendências e contradições. O trabalho está completo para a solicitação quando todas as perguntas **necessárias à avaliação solicitada** têm resposta verificável ou quando a conclusão foi limitada ao que os dados permitem. Se o usuário encerrar ou limitar o esforço, entregue o estado atual e as lacunas decisivas sem simular certeza.

## Origem do padrão

Adaptação independente do mecanismo de [grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) de Matt Pocock: perguntas ordenadas por dependência, recomendações explícitas, busca de fatos no ambiente e encerramento só após examinar os ramos relevantes. O [grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) acrescenta documentação contínua ao fluxo. A orientação de registrar cada resposta de forma durável também aparece nesta [variante de grill-me](https://github.com/gusinov/grill-me/blob/main/grill-me/SKILL.md). Aqui, esses princípios foram ajustados aos gates de evidência da experimentação; nenhum desses pacotes é requisito de execução.
