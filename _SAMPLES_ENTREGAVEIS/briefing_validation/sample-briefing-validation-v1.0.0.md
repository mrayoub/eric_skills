# EXEMPLO FICTÍCIO — Validacao do briefing: solicitacoes internas

Amostra fictícia do formato original RC6. Não descreve um projeto real. Exemplo neutro da validacao IQB auditavel consolidada a partir dos ERIC RC1 e RC5.

| Campo | Valor |
| --- | --- |
| Title | Melhorar a experiencia de solicitacoes internas |
| Sponsor | {'name': 'Nao informado'} |
| Owner | {'name': 'Nao informado'} |

Fontes: FIC-01

Status: attention
Original: Como podemos reduzir o esforco de quem solicita e de quem atende?
Analysis: A formulacao identifica as pessoas e o efeito desejado, mas ainda nao explicita o contexto em que o problema ocorre.
Suggestion: Como podemos reduzir o esforco de quem solicita e de quem atende para que as demandas sejam resolvidas com clareza de modo que o processo seja previsivel?

Fontes: FIC-01

| Dimensão | Critério | Resposta | Evidência | Fonte |
| --- | --- | --- | --- | --- |
| clarity | CLA-01 | True | O briefing identifica quem solicita e as equipes que atendem. | briefing |
| clarity | CLA-02 | True | O texto delimita o problema de solicitacoes incompletas e pouco rastreaveis. | briefing |
| clarity | CLA-03 | False | As causas ainda nao foram diferenciadas dos sintomas. | absent |
| clarity | CLA-04 | True | O problema ocorre na entrada e no acompanhamento das solicitacoes internas. | briefing |
| clarity | CLA-05 | True | O fluxo e os atores podem ser compreendidos sem contexto organizacional adicional. | briefing |
| clarity | CLA-06 | True | O briefing descreve esforco, retrabalho e previsibilidade, sem prescrever tecnologia. | briefing |
| clarity | CLA-07 | False | Nao ha volume, frequencia ou abrangencia quantificada. | absent |
| clarity | CLA-08 | False | O briefing nao registra tentativas anteriores nem declara que nada foi tentado. | absent |
| clarity | CLA-09 | True | A descricao apresenta contexto, atores e impacto operacional suficientes para iniciar a investigacao. | briefing |
| clarity | CLA-10 | True | Existe um problema real de retrabalho e falta de visibilidade, sem solucao predefinida. | briefing |
| evidence | EVI-01 | False | Nao ha dado quantitativo no briefing. | absent |
| evidence | EVI-02 | False | Nao existe fonte de dado quantitativo identificada. | absent |
| evidence | EVI-03 | True | As fontes relatam devolucoes e repeticao de triagens. | briefing |
| evidence | EVI-04 | True | Os relatos tratam especificamente das solicitacoes internas descritas. | briefing |
| evidence | EVI-05 | False | Nao ha prazo, perda ou risco que demonstre urgencia. | absent |
| evidence | EVI-06 | True | Os relatos de devolucoes e triagens repetidas demonstram que o problema ocorre. | briefing |
| evidence | EVI-07 | False | As fontes ou perspectivas dos relatos nao estao identificadas individualmente. | absent |
| evidence | EVI-08 | False | Os relatos nao possuem periodo de referencia. | absent |
| evidence | EVI-09 | False | O impacto operacional nao foi medido. | absent |
| evidence | EVI-10 | False | As evidencias nao permitem comparar a prioridade com outros problemas. | absent |
| outcomes | OUT-01 | True | Reduzir retrabalho e tornar o processo previsivel descrevem mudancas de resultado. | briefing |
| outcomes | OUT-02 | False | Nao existe meta quantificada. | absent |
| outcomes | OUT-03 | False | Nao existe prazo ou horizonte de verificacao. | absent |
| outcomes | OUT-04 | True | Devolucoes e visibilidade de status podem ser verificadas objetivamente. | briefing |
| outcomes | OUT-05 | False | A conexao com uma prioridade estrategica nao foi declarada. | absent |
| outcomes | OUT-06 | True | O estado futuro inclui solicitacoes completas, rastreaveis e previsiveis. | briefing |
| outcomes | OUT-07 | True | Os resultados nao prescrevem uma funcionalidade ou ferramenta especifica. | briefing |
| outcomes | OUT-08 | False | Premissas e restricoes de viabilidade nao foram registradas. | absent |
| outcomes | OUT-09 | False | Nao ha baseline nem metodo de verificacao formalizado. | absent |
| outcomes | OUT-10 | True | Existe pelo menos um outcome definido alem de funcionalidades. | briefing |
| actionability | ACT-01 | True | Uma equipe externa consegue compreender o problema e os atores principais. | briefing |
| actionability | ACT-02 | False | A pessoa responsavel nao foi identificada; a ausencia de cargo nao seria penalizada. | absent |
| actionability | ACT-03 | False | O sponsor nao foi identificado; a ausencia de cargo nao seria penalizada. | absent |
| actionability | ACT-04 | False | Restricoes conhecidas ou pendentes nao foram registradas. | absent |
| actionability | ACT-05 | False | O que esta fora do escopo nao foi definido. | absent |
| actionability | ACT-06 | False | Recursos disponiveis ou pendentes nao foram registrados. | absent |
| actionability | ACT-07 | False | Dependencias para iniciar nao foram identificadas. | absent |
| actionability | ACT-08 | False | O nivel de autonomia da equipe nao foi definido nem marcado como pendente. | absent |
| actionability | ACT-09 | True | As sete secoes existem e as pessoas ausentes foram marcadas como nao informadas. | briefing |
| actionability | ACT-10 | True | Ha problema e pessoas afetadas suficientes para iniciar a descoberta. | briefing |

Fontes: FIC-01

Score: 2.8
Classification: Adequado
Diagnosis: O briefing permite iniciar a descoberta, mas ainda depende de evidencias mensuraveis e definicoes de governanca e escopo. A clareza e o principal ponto forte. Evidencias e acionabilidade concentram as lacunas prioritarias.

Fontes: FIC-01

- O problema diferencia solicitantes e equipes de atendimento.
- O estado futuro desejado de clareza e previsibilidade esta explicito.

Fontes: FIC-01

| priority | title | problem | impact | action | tag |
| --- | --- | --- | --- | --- | --- |
| 1 | Evidencias sem linha de base | Nao ha volume, tempo, periodo ou fonte consolidada para os relatos de retrabalho. | Sem linha de base, o resultado posterior nao podera ser comparado de forma confiavel. | Consolidar os dados existentes e registrar fonte, periodo e unidade de cada medida. | critical |
| 2 | Governanca e escopo pendentes | Responsavel, sponsor, limites do escopo e dependencias nao foram identificados. | A descoberta pode comecar, mas decisoes e encaminhamentos ficarao sem donos claros. | Identificar responsavel e sponsor pelo nome e registrar escopo, restricoes e dependencias conhecidas. | critical |
| 3 | Resultados sem meta e prazo | Os outcomes sao compreensiveis, mas nao possuem meta, baseline ou horizonte de verificacao. | Nao sera possivel determinar objetivamente quando o resultado foi alcancado. | Definir uma metrica principal, sua linha de base, meta e prazo de verificacao. | warning |

Fontes: FIC-01

- Qual numero precisa mudar para demonstrar que o problema foi resolvido?
- Quais canais e tipos de solicitacao estao dentro e fora do escopo?
- Quem possui autoridade para priorizar mudancas no processo e remover dependencias?

Fontes: FIC-01

## Fontes

- FIC-01: ata-simulada-5c exemplo fictício, sem coleta real
