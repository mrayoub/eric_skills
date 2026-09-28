# Modelos dos entregáveis

Adapte formato e nível de detalhe à organização. Mantenha IDs estáveis para permitir auditoria e atualização sem reescrever toda a análise.

## Registro da rodada

- Identificação, pergunta avaliativa neutra, responsável pelo gate posterior, hipótese master e fontes de descoberta.
- Escopo do MVP, versão/configuração, população, amostra prevista, amostra executada e critérios de elegibilidade.
- Test Cards originais e versões/adaptações aprovadas, com datas.
- Fontes disponíveis, fontes ausentes, recorte temporal e protocolo de análise.
- Mapa das suposições críticas: consequência se falsas, evidência atual, lacuna e próximo teste possível.

## Test Card

Entregue um card individual por teste; a linha da tabela do caderno serve só como índice. A [Strategyzer](https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card) define quatro perguntas, que o [modelo](../assets/test-card.md) organiza como:

1. **Hipótese:** o que precisa ser verdade, com subhipótese focal, vínculo com a master e resultado que a colocaria em dúvida.
2. **Teste:** como verificar, com método, tarefa/cenário, elegibilidade, versão do MVP, fonte independente quando necessária e riscos.
3. **Medida:** o que observar/medir; em teste quantitativo, unidade, numerador, denominador, janela e fonte; em teste qualitativo, tarefa, observações previstas, forma de registro e limites.
4. **Critério:** como reconhecer o sucesso antes da coleta; limiar justificado ou condição prática de decisão, leituras contrária e inconclusiva, e guardrails.

Metadados fora dos quatro campos: `id`, versão, data, origem, responsável e estado. Um card sem critério decisivo pode ser entregue como rascunho, mas não como teste verificatório pronto. Preserve alterações datadas sem sobrescrever a versão prévia.

## Registro de execução; sessão quando aplicável

- `execucao_id`, Test Card, data, método, unidade observada, população, versão do MVP/intervenção e fontes com localização.
- Exposição ou procedimento realmente executado, desfecho, desvios, intervenções, guardrails e dados ausentes.
- IDs do livro de evidências que sustentam cada achado; divergências entre registros. Em sessão moderada, inclua tarefa, falas, ajuda e momento, vídeo/transcrição quando houver.

## Matriz de unidades observadas e desfechos

- Relacione cada unidade elegível (participante, caso, obrigação, local ou período) à exposição, ao desfecho, aos desvios e aos códigos relevantes; preserve o vínculo com a evidência primária. Em sessões moderadas, registre também tarefa e ajuda recebida.
- Resuma problemas ou eventos por frequência na amostra, efeito no processo ou resultado, severidade justificada, casos contrários e condição para nova verificação. Use a matriz para priorizar; inferências populacionais ou causais dependem do desenho e da amostragem adequados.

## Learning Card, um por Test Card

Entregue um card individual para cada Test Card executado. A [Strategyzer](https://www.strategyzer.com/library/capture-customer-insights-and-actions-with-the-learning-card) define quatro etapas, que o [modelo](../assets/learning-card.md) organiza como:

1. **Hipótese testada:** retome o TC e seu critério original; identifique adaptações sem reescrever a previsão.
2. **Observações:** descreva dados e comportamentos de campo, com `evidencia_id`, localização, medida/denominador, cobertura e contraexemplos. Ausência de dados também deve ser explícita.
3. **Aprendizado:** diga o que se pode deduzir dessas observações, se o critério foi atingido, não atingido, é inconclusivo ou ficou fora do escopo, e qual incerteza permanece. Separe inferência de observação.
4. **Ação:** indique ajuste, decisão ou próximo teste, responsável e condição de avanço, proporcional à força da evidência.

Metadados fora dos quatro campos: `id`, vínculo com TC, versão, data e estado. Um card pode produzir aprendizado útil e continuar formalmente inconclusivo. Não produza Learning Card como resultado de teste ainda não executado.

## Síntese de evidências e recomendação

Este é um entregável próprio da skill para consolidar a decisão da rodada; não é um card oficial da Strategyzer.

- Pergunta avaliada e recomendação derivada das evidências: avançar, iterar, investigar ou encerrar.
- Evidências favoráveis e contrárias com IDs; status dos Test Cards; riscos e limitações.
- O que a rodada autoriza agora e o que permanece sem medição.
- Condições verificáveis para o próximo gate, responsáveis e fonte de comprovação.
- Alternativas consideradas e motivo para preferir a ação proposta, com incerteza residual explícita.
- Se a ação recomendada for um piloto, descreva-o como teste: perguntas, população e duração, limites de exposição, medidas e guardrails, monitoramento, interrupção e decisão ao final. Não trate o piloto como autorização implícita para escala.

## Gate de decisão

- Registre a decisão tomada, quem a tomou e quando. Saídas possíveis: `avançar`, `iterar`, `investigar` ou `encerrar`; ajuste a nomenclatura à esteira da organização.
- Associe a saída aos critérios críticos e às evidências suficientes ou faltantes. Para `iterar` ou `investigar`, indique a incerteza, o ajuste ou teste seguinte e o critério de avanço. Separe a recomendação analítica da decisão efetivamente aprovada; registre alternativas rejeitadas, motivo e condição para reabrir a decisão.

## Relatório e apresentação

Estruture a narrativa como `problema e hipótese → pergunta → método e amostra → evidências e problemas prioritários → status dos cards → recomendação → próximo gate`. Uma apresentação executiva pode mostrar um scorecard descritivo, 3 a 5 achados principais, exemplos verificáveis e as condições para a próxima rodada; adapte o número de slides ao público. Use números somente com unidade, denominador, cobertura e nome correto. Nas notas ou apêndice, inclua um índice que permita voltar de cada afirmação relevante ao livro de evidências. Compare a versão final com os registros antes de apresentar; relatório, cards e slides devem expressar a mesma decisão e o mesmo recorte.

## Passagem para a próxima fase

Entregue um resumo de uma página ou seção equivalente com decisão efetiva, hipóteses sustentadas e ainda abertas, riscos aceitos, ações e donos, critérios de avanço, evidências que precisarão ser coletadas e localização dos registros originais. Identifique a versão do MVP a que a decisão se refere para que a próxima rodada não herde uma conclusão de versão anterior sem revisão.
