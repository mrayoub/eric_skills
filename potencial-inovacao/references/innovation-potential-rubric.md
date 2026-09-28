# Rubrica de Potencial de Inovação — adaptação portátil 1.1.0

Preserva critérios, pesos e faixas do ERIC_RC6 1.0.0. A regra de ausência foi corrigida: nota faltante ou inválida não é zero; sem os cinco critérios sustentados o resultado permanece incompleto e sem classificação. Zero continua possível quando há avaliação explícita e justificada.

Cada critério recebe nota de 0 a 100, sustentada por justificativa e pelas
evidências disponíveis.

| Critério | Peso | Pergunta de avaliação |
|---|---:|---|
| Impacto | 30% | Qual é a magnitude verificável do benefício ou da dor evitada? |
| Viabilidade | 25% | Há capacidade, tecnologia, prazo e recursos plausíveis? |
| Alinhamento estratégico | 20% | A oportunidade contribui para objetivos explícitos da CCEE? |
| Urgência | 15% | Existe janela, risco ou custo de adiamento demonstrável? |
| Inovação | 10% | Há novidade ou diferenciação relevante para o contexto? |

O total é a soma ponderada, arredondada para uma casa decimal:

- `>= 70`: `priorizar`
- `>= 40` e `< 70`: `monitorar`
- `< 40`: `arquivar`

Notas ausentes impedem o total e a classificação; notas inválidas ou fora de
0 a 100 geram erro para correção. O cálculo e a classificação nunca são
ajustados por julgamento editorial do modelo.
