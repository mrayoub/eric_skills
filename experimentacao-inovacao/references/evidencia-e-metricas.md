# Contrato de evidência e métricas

## Registro de fontes

Para cada fonte, guarde: `fonte_id`, tipo, caminho ou referência, data/versão, fase (`descoberta`, `plano`, `execução`, `análise`), cobertura, limitações e se foi examinada diretamente. Uma entrevista anterior pode sustentar a origem de uma hipótese; não prova o desempenho do MVP. Um vídeo pode mostrar ações; uma transcrição pode localizar falas; uma base de telemetria pode confirmar eventos persistidos. Registre a fronteira de cada uma.

## Livro de evidências

Cada linha deve ter, no mínimo:

| Campo | Significado |
|---|---|
| `evidencia_id` | Identificador estável e único. |
| `test_card_id` e `execucao_id` | Ligação ao teste e à unidade de execução; use múltiplos IDs se uma observação informar mais de um card. |
| `fonte_id` e `localizacao` | Arquivo e página/linha, intervalo da transcrição, timestamp do vídeo ou chave de evento. |
| `procedimento`, `fase`, `versao_intervencao` | Contexto necessário para interpretar a ocorrência; registre a tarefa e a versão do MVP quando aplicáveis. |
| `observacao` | Ação, fala, evento ou medida registrada, sem explicação causal embutida. |
| `interpretacao` | Leitura analítica separada da observação. |
| `intervencao` | Exposição, ajuda ou alteração ocorrida durante o teste; registre o tipo e se ocorreu antes ou depois do desfecho relevante. Em sessão moderada, classifique lembrete neutro de verbalização, ajuda técnica, orientação e influência de decisão; registre o intervalo afetado e o desfecho que pode ter sido alterado. |
| `qualidade` | Direta, corroborada, indireta, contraditória ou não observável; explique divergências entre fontes. |

Na análise de sessões, acrescente `uso_analitico` (`incluido`, `restrito` ou `excluido_da_inferencia`) e `justificativa` quando houver intervenção relevante. A exclusão é específica da inferência: uma tarefa concluída após orientação pode informar compreensão com ajuda, mas não sucesso autônomo. Não apague o evento nem retire silenciosamente a pessoa do denominador; reporte oportunidades avaliáveis e casos restritos conforme a medida.

Registre exemplos contrários e casos sem evidência, não apenas os que confirmam a hipótese. Evite usar um resumo já produzido como única fonte de uma nova afirmação; quando possível, retorne ao material primário.

## Registro de medidas

Para cada medida ou indicador, registre: `medida_id`, Test Card, pergunta que responde, papel (`critério de decisão`, `medida secundária`, `guardrail` ou `indicador exploratório`), data de definição, unidade, numerador, denominador/elegibilidade, janela, fonte, fórmula, cobertura, linha de base quando relevante, limiar original quando existente, adaptação e resultado. Reserve `KPI` para uma medida de desempenho acompanhada de modo recorrente ou reconhecida como tal pela organização; nem toda contagem de teste de usabilidade é um KPI. Não altere o significado de uma medida mantendo o mesmo nome.

Regras de interpretação:

- Ausência de casos avaliados mede cobertura da avaliação; não equivale a erro ou acerto no resultado.
- Alcançar uma etapa intermediária não equivale a concluir a tarefa, obter aprovação ou produzir o efeito final.
- Ausência de intervenção identificada numa sessão moderada não equivale a autonomia demonstrada em protocolo sem ajuda.
- Fricção observada, discordância verbal, alteração de uma sugestão e erro frente a uma referência independente são medidas distintas.
- Duração da tarefa, duração da sessão e tempo operacional poupado são unidades diferentes.
- Dados históricos de descoberta, sessões oficiais, jornadas do sistema e textos avaliados podem ter denominadores distintos.

Se a medida foi definida depois de observar resultados, rotule como exploratória; ela pode ser útil para síntese e priorização. Se a equipe quiser usá-la como critério verificatório, formule definição e limiar prospectivos para uma próxima rodada. Se o critério original exigia gabarito, baseline, avaliação cega, período ou amostra diferentes, mantenha o status formal inconclusivo até haver evidência adequada ou uma adaptação decidida antes de novo teste.

## Revisão de consistência

Antes de divulgar, confira: mesma amostra oficial em todos os artefatos; critérios originais preservados; casos excluídos nomeados sem duplicar pessoas; percentuais reproduzíveis; fontes localizáveis; versão do MVP identificada ou declarada desconhecida; ajuda do facilitador classificada pelo momento; status do Test Card separado do Learning Card; limites da síntese de evidências e recomendação repetidos na apresentação.
