# Rubrica IQB — adaptação portátil 1.1.0

Preserva os 40 critérios, vetos e faixas do ERIC_RC6 1.0.0. O cálculo portátil exige todos os itens com resposta e justificativa explícitas; a auditoria de agrupamento é tarefa do avaliador, não algo que o script pode declarar como concluído sozinho.

## Sumario

1. Principios
2. Escala e calculo
3. Clareza do problema
4. Forca das evidencias
5. Definicao dos resultados
6. Acionabilidade
7. Vetos
8. Auditoria de agrupamento
9. Casos especiais
10. Contrato de avaliacao

## 1. Principios

- Avaliar somente o que esta sustentado pelas fontes da execucao.
- Responder todos os criterios com `yes` ou `no`.
- Tratar evidencia ausente, vaga ou ambigua como `no`.
- Nao escolher a nota diretamente; deriva-la das respostas.
- Nao exigir cargo de responsavel ou sponsor. O nome identifica a pessoa; cargo e metadado opcional de governanca.
- Nao recompensar extensao textual por si so. Avaliar substancia, contexto e rastreabilidade.
- Nao exigir varios resultados quando existe um outcome principal mensuravel e suficiente.

## 2. Escala e calculo

Cada dimensao possui nove criterios pontuaveis e um veto. O veto nao entra em `yes_count`.

| `yes_count` | `raw_score` | Label |
|---:|---:|---|
| 8-9 | 5 | Excelente |
| 6-7 | 4 | Saudavel |
| 4-5 | 3 | Adequado |
| 2-3 | 2 | Fragil |
| 0-1 | 1 | Insuficiente |

Aplicar o teto do veto para obter `final_score`. Calcular:

```text
IQB = round((clarity + evidence + outcomes + actionability) / 4, 1)
```

| IQB | Classificacao | Orientacao |
|---|---|---|
| 4.5-5.0 | Excelente | Pronto para execucao |
| 3.5-4.4 | Saudavel | Ajustes rapidos antes do kick-off |
| 2.5-3.4 | Adequado | Revisao estruturada necessaria |
| 1.5-2.4 | Fragil | Retornar ao sponsor |
| 1.0-1.4 | Insuficiente | Reiniciar o enquadramento |

## 3. Clareza do problema

| ID | Criterio |
|---|---|
| `CLA-01` | Identifica pessoas especificas afetadas, nao apenas "a empresa" ou "o mercado". |
| `CLA-02` | Delimita um problema coerente, sem misturar problemas independentes. |
| `CLA-03` | Diferencia sintomas de causas ou reconhece explicitamente que as causas ainda precisam ser investigadas. |
| `CLA-04` | Descreve o contexto em que o problema ocorre: processo, momento ou situacao. |
| `CLA-05` | Permite que uma pessoa externa compreenda a situacao sem depender de conhecimento tacito. |
| `CLA-06` | Centra o problema em necessidades e impactos, nao na falta de uma ferramenta especifica. |
| `CLA-07` | Dimensiona quem e afetado, frequencia, volume ou abrangencia quando as fontes permitem. |
| `CLA-08` | Registra o que ja foi tentado ou informa explicitamente que nenhuma tentativa foi realizada. |
| `CLA-09` | A descricao apresenta contexto, impacto e informacao suficiente para investigar, independentemente da quantidade de frases. |
| `CLA-10` | **VETO:** apresenta um problema real e compreensivel, nao apenas uma solucao disfarçada. |

## 4. Forca das evidencias

| ID | Criterio |
|---|---|
| `EVI-01` | Contem ao menos um dado quantitativo concreto: valor, percentual, volume, tempo ou quantidade. |
| `EVI-02` | Identifica a fonte do dado quantitativo. |
| `EVI-03` | Contem ao menos uma evidencia qualitativa: relato, depoimento ou observacao. |
| `EVI-04` | As evidencias sao especificas ao problema descrito. |
| `EVI-05` | Ha evidencia de urgencia, prioridade, perda ou risco. |
| `EVI-06` | **VETO:** existe evidencia de que o problema realmente ocorre, alem de uma suposicao do autor. |
| `EVI-07` | As evidencias combinam mais de uma fonte ou perspectiva. |
| `EVI-08` | Os dados possuem periodo ou contexto temporal. |
| `EVI-09` | Existe impacto financeiro ou operacional mensuravel. |
| `EVI-10` | As evidencias permitem justificar a prioridade deste problema no contexto declarado. |

## 5. Definicao dos resultados

| ID | Criterio |
|---|---|
| `OUT-01` | Descreve valor ou mudanca gerada (`outcome`), nao apenas uma entrega (`output`). |
| `OUT-02` | Contem ao menos uma meta quantificada. |
| `OUT-03` | Define prazo ou horizonte de verificacao. |
| `OUT-04` | Permite verificar objetivamente se o resultado foi alcancado. |
| `OUT-05` | Relaciona o resultado a uma prioridade ou estrategia declarada nas fontes. |
| `OUT-06` | Explica como a situacao sera diferente apos a resolucao. |
| `OUT-07` | Diferencia resultado, requisito e funcionalidade. |
| `OUT-08` | Explicita premissas ou restricoes suficientes para avaliar viabilidade, sem exigir conhecimento externo. |
| `OUT-09` | Identifica baseline, indicador ou metodo de verificacao para o outcome principal. Um unico outcome pode ser suficiente. |
| `OUT-10` | **VETO:** existe ao menos um resultado definido e ele nao e apenas uma lista de funcionalidades. |

## 6. Acionabilidade

| ID | Criterio |
|---|---|
| `ACT-01` | Uma equipe externa consegue entender o briefing sem reuniao inicial apenas para decodifica-lo. |
| `ACT-02` | A pessoa responsavel esta identificada pelo nome. Cargo e opcional e nao afeta a resposta. |
| `ACT-03` | O sponsor esta identificado pelo nome. Cargo e opcional e nao afeta a resposta. |
| `ACT-04` | Registra restricoes conhecidas de prazo, orcamento, tecnologia ou regulacao, ou declara que ainda nao foram definidas. |
| `ACT-05` | Delimita o que esta dentro e fora do escopo. |
| `ACT-06` | Registra recursos disponiveis ou a necessidade de defini-los. |
| `ACT-07` | Identifica dependencias ou condicoes para comecar. |
| `ACT-08` | Define ou reconhece como pendente o nivel de autonomia da equipe. |
| `ACT-09` | As sete secoes obrigatorias estao preenchidas ao menos com uma lacuna explicita. |
| `ACT-10` | **VETO:** ha informacao minima para iniciar a descoberta: problema e pessoa afetada. |

## 7. Vetos

| Dimensao | Item | Teto quando `no` |
|---|---|---:|
| Clareza | `CLA-10` | 2 |
| Evidencias | `EVI-06` | 1 |
| Resultados | `OUT-10` | 2 |
| Acionabilidade | `ACT-10` | 2 |

Registrar sempre `veto_triggered`, `veto_detail`, `raw_score` e `final_score`.

## 8. Auditoria de agrupamento

Calcular `span = max(final_scores) - min(final_scores)`. Quando `span <= 1`:

1. marcar `triggered=true`;
2. preservar as notas originais em `original_scores`;
3. reexaminar cada `yes` contra sua evidencia;
4. registrar a conclusao em `re_evaluation_notes`;
5. alterar uma resposta somente quando a evidencia nao sustenta o resultado original.

Notas iguais continuam validas. A auditoria nao pode fabricar diferencas entre dimensoes.

## 9. Casos especiais

- **Briefing vazio ou ilegivel:** todos os criterios `no`, notas 1 e gap de conteudo minimo.
- **Transcricao:** marcar evidencia como `transcription` e registrar a necessidade de formalizacao sem invalidar fatos explicitamente ditos.
- **Modelo fornecido:** usar o modelo como referencia estrutural e registrar discrepancias em Acionabilidade.
- **Secao vazia:** marcar criterios dependentes como `no` e identificar a secao ausente.
- **Multiplos briefings:** avaliar cada briefing e cada versao de forma independente.

## 10. Contrato de avaliacao

Cada item deve conter:

```json
{
  "criterion_id": "CLA-01",
  "answer": true,
  "evidence": "Trecho ou descricao objetiva do que esta ausente",
  "evidence_source": "briefing",
  "citation_id": "citation-optional"
}
```

Valores de `evidence_source`: `briefing`, `transcription`, `briefing_model` ou `absent`.

Cada dimensao deve conter `items`, `veto_item_id`, `veto_max_score`, `veto_triggered`, `veto_detail`, `yes_count`, `raw_score`, `final_score`, `label` e `justification`.
