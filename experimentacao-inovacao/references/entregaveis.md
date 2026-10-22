# Modelos dos entregáveis

Adapte formato e nível de detalhe à organização. Mantenha IDs estáveis para permitir auditoria e atualização sem reescrever toda a análise.

A skill trabalha em três blocos, cada um com um entregável composto pelos modelos abaixo:

| Bloco | Entregável | `deliverable_type` |
|---|---|---|
| Aprofundamento e planejamento | **Hipóteses com Test Cards** | um `test_card` por teste |
| Execução | **Modelo de experimentação** | `experiment_plan` (+ MVP a construir, escopo, cronograma e gate de início) |
| Consolidação | **Apresentação da experimentação e direcionamento** | `executive_presentation` e `evidence_recommendation`; um `learning_card` por card executado |

## Bloco 1: Hipóteses com Test Cards

Reúne suposições priorizadas, hipóteses e um Test Card individual por teste, com o escopo da rodada ([planejamento](planejamento-dos-testes.md)).

### Registro da rodada

- Identificação, pergunta avaliativa neutra, responsável pelo gate posterior, hipótese master e fontes de descoberta.
- Escopo do MVP, versão/configuração, população, amostra prevista, amostra executada e critérios de elegibilidade.
- Test Cards originais e versões/adaptações aprovadas, com datas.
- Fontes disponíveis, fontes ausentes, recorte temporal e protocolo de análise.
- Mapa das suposições críticas: consequência se falsas, evidência atual, lacuna e próximo teste possível.

### Test Card

Entregue um card individual por teste; a linha da tabela do caderno serve só como índice. A [Strategyzer](https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card) define quatro perguntas, que o [modelo](../assets/test-card.md) organiza como:

1. **Hipótese:** uma subhipótese focal e falsificável: quem faz ou percebe o quê, em qual versão.
2. **Teste:** método, público e quantidade, e o que será exposto ou executado.
3. **Medida:** uma medida principal; quantitativa como numerador / denominador, qualitativa como o comportamento observado.
4. **Critério:** um limiar ou condição observável definido antes da coleta, ou `a fechar antes da coleta: [o que falta]`.

Cada campo é uma frase objetiva de até 280 caracteres (o renderizador rejeita textos maiores). Um card testa uma hipótese com uma medida principal; dois resultados independentes viram dois cards. Riscos, guardrails, leituras contrária e inconclusiva, justificativa do limiar, medidas secundárias, janela, fonte e protocolo ficam no plano do experimento ou no caderno, ligados ao ID do card. Metadados fora dos quatro campos: `id`, versão, data, origem, responsável e estado. Um card sem critério decisivo pode ser entregue como rascunho, mas não como teste verificatório pronto. Preserve alterações datadas sem sobrescrever a versão prévia.

## Bloco 2: Modelo de experimentação

O desenho executável da rodada: MVP a construir, protocolo e roteiro de cada teste, público, medidas e registros, guardrails, cronograma e gate de início ([execução e MVP](execucao-e-mvp.md)). Durante a execução, os registros abaixo alimentam a consolidação; não interpretam resultados.

### Registro de execução; sessão quando aplicável

- `execucao_id`, Test Card, data, método, unidade observada, população, versão do MVP/intervenção e fontes com localização.
- Exposição ou procedimento realmente executado, desfecho, desvios, intervenções, guardrails e dados ausentes.
- IDs do livro de evidências que sustentam cada achado; divergências entre registros. Em sessão moderada, inclua tarefa, falas, ajuda e momento, vídeo/transcrição quando houver.

### Matriz de unidades observadas e desfechos

- Relacione cada unidade elegível (participante, caso, obrigação, local ou período) à exposição, ao desfecho, aos desvios e aos códigos relevantes; preserve o vínculo com a evidência primária. Em sessões moderadas, registre também tarefa e ajuda recebida.
- Resuma problemas ou eventos por frequência na amostra, efeito no processo ou resultado, severidade justificada, casos contrários e condição para nova verificação. Use a matriz para priorizar; inferências populacionais ou causais dependem do desenho e da amostragem adequados.

## Bloco 3: Apresentação da experimentação e direcionamento

Consolida resultados, Learning Cards, avaliação do MVP e a recomendação que serve à próxima fase da esteira (BP2). A apresentação mostra, em seções próprias, o status dos cards e a [avaliação do MVP](avaliacao-do-mvp.md), e termina no direcionamento: avançar, iterar, investigar ou encerrar, com condições, responsável e prazo.

### Learning Card, um por Test Card

Entregue um card individual para cada Test Card executado. A [Strategyzer](https://www.strategyzer.com/library/capture-customer-insights-and-actions-with-the-learning-card) define quatro etapas, que o [modelo](../assets/learning-card.md) organiza como:

1. **Hipótese testada:** a hipótese e o critério do TC, sem reescrever a previsão.
2. **Observações:** o resultado medido com número e denominador e o principal contraexemplo, citando `evidencia_id`. Ausência de dados também é explícita.
3. **Aprendizado:** status do critério (atingido, não atingido, inconclusivo ou fora do escopo) e o principal aprendizado, sem repetir os números.
4. **Ação:** uma decisão ou próximo teste, com responsável e prazo ou condição, proporcional à força da evidência.

Cada campo é uma frase objetiva de até 280 caracteres. Adaptações datadas, cobertura completa, demais contraexemplos, explicações alternativas e incerteza detalhada ficam no relatório ou no caderno, ligados ao ID do card. Metadados fora dos quatro campos: `id`, vínculo com TC, versão, data e estado. Um card pode produzir aprendizado útil e continuar formalmente inconclusivo. Não produza Learning Card como resultado de teste ainda não executado.

### Síntese de evidências e recomendação

Este é um entregável próprio da skill para consolidar a decisão da rodada; não é um card oficial da Strategyzer.

- Pergunta avaliada e recomendação derivada das evidências: avançar, iterar, investigar ou encerrar.
- Evidências favoráveis e contrárias com IDs; status dos Test Cards; riscos e limitações.
- O que a rodada autoriza agora e o que permanece sem medição.
- Condições verificáveis para o próximo gate, responsáveis e fonte de comprovação.
- Alternativas consideradas e motivo para preferir a ação proposta, com incerteza residual explícita.
- Se a ação recomendada for um piloto, descreva-o como teste: perguntas, população e duração, limites de exposição, medidas e guardrails, monitoramento, interrupção e decisão ao final. Não trate o piloto como autorização implícita para escala.

### Gate de decisão

- Registre a decisão tomada, quem a tomou e quando. Saídas possíveis: `avançar`, `iterar`, `investigar` ou `encerrar`; ajuste a nomenclatura à esteira da organização.
- Associe a saída aos critérios críticos e às evidências suficientes ou faltantes. Para `iterar` ou `investigar`, indique a incerteza, o ajuste ou teste seguinte e o critério de avanço. Separe a recomendação analítica da decisão efetivamente aprovada; registre alternativas rejeitadas, motivo e condição para reabrir a decisão.

### Relatório e apresentação

Estruture a narrativa como `problema e hipótese → pergunta → método e amostra → MVP construído → evidências e problemas prioritários → status dos cards → avaliação do MVP → recomendação → próximo gate`. Uma apresentação executiva pode mostrar um scorecard descritivo, 3 a 5 achados principais, exemplos verificáveis e as condições para a próxima rodada; adapte o número de slides ao público. Use números somente com unidade, denominador, cobertura e nome correto. Nas notas ou apêndice, inclua um índice que permita voltar de cada afirmação relevante ao livro de evidências. Compare a versão final com os registros antes de apresentar; relatório, cards e slides devem expressar a mesma decisão e o mesmo recorte.

Na apresentação, escreva na capa a mensagem principal em até 35 palavras. Cada slide deve ter um título-mensagem de 4 a 12 palavras que diga sua conclusão e desenvolver uma ideia em até 4 blocos e 60 palavras. Destaque números-chave em blocos `metric`; deixe detalhes e evidências completas no relatório ou apêndice. O renderizador recusa versões completas que ultrapassem esses limites.

### Passagem para a próxima fase

Entregue um resumo de uma página ou seção equivalente com decisão efetiva, hipóteses sustentadas e ainda abertas, riscos aceitos, ações e donos, critérios de avanço, evidências que precisarão ser coletadas e localização dos registros originais. Identifique a versão do MVP a que a decisão se refere para que a próxima rodada não herde uma conclusão de versão anterior sem revisão.
