# Base metodológica e escolha do método

Escolha o desenho da rodada pela decisão necessária e pela força de evidência exigida. A distinção abaixo é uma síntese operacional das fontes, não uma taxonomia universal.

| Finalidade | Planeje antes da coleta | Pode surgir na análise | Conclusão permitida |
|---|---|---|---|
| Explorar problema ou comportamento | Perguntas, público, roteiro e forma de registrar evidências | Temas, hipóteses, códigos e indicadores descritivos | Aprendizados e perguntas para novos testes |
| Avaliar formativamente um MVP | Tarefas, público, desfechos observáveis, intervenções e critérios práticos de priorização | Fricções inesperadas e sua frequência na amostra | O que melhorar e reavaliar; observações não estimam prevalência populacional |
| Verificar um Test Card com critério de sucesso | Hipótese, medida, coleta, elegibilidade, fonte independente e limiar aplicável | Explicações, anomalias e hipóteses secundárias | Status do critério original, se o teste efetivamente produziu a evidência exigida |
| Comparar alternativas quantitativamente ou medir efeito | Métrica primária, secundárias e guardrails, desenho de comparação, amostra, duração e regra de decisão | Análises adicionais rotuladas como exploratórias | Inferência compatível com desenho e tamanho da amostra; causalidade só quando o desenho permitir |

Uma rodada pode combinar finalidades, mas cada afirmação precisa carregar o método que a sustenta. Não chame automaticamente de KPI toda medida de tarefa. Em pesquisa qualitativa pequena, uma contagem como `4 de 10 participantes` descreve os casos observados; não é estimativa confiável de prevalência nem comprova que o MVP atingiu um limiar populacional.

Quando a rodada já terminou, recupere a versão original do plano. Se ela não trouxe medida ou limiar, faça análise exploratória honesta e proponha o contrato de medição da próxima rodada. Não atribua ao Test Card um critério que foi inventado após conhecer os resultados. Quando o objetivo original era apenas explorar, a ausência de um KPI formal não é, por si só, falha metodológica.

## Da suposição ao desenho do teste

Antes de escolher uma técnica, mapeie cada suposição crítica da hipótese master: o que deixa de funcionar se ela estiver errada, qual evidência já existe, qual evidência falta e que teste viável poderia reduzi-la. Comece pelas suposições de maior consequência e menor evidência. Quando uma hipótese exigir mais de um teste, use os resultados de métodos leves para especificar uma verificação mais forte; não some sinais de naturezas diferentes em um único percentual.

Escolha o método pela pergunta, usando o [catálogo de métodos de execução](metodos-de-experimentacao.md): observação e entrevistas para contexto; conceitos, simulações ou MVP manual para testar a solução; casos com gabarito para regras; piloto para viabilidade; comparação controlada para atribuir efeito. Defina guardrails, interrupção e dono da decisão de acordo com os riscos reais. Poder estatístico, tamanho de amostra e significância só entram quando o desenho pretende sustentar inferência quantitativa; não os transplante para sessões qualitativas.

Em pilotos de processo, explicite a unidade de elegibilidade e atribuição (pessoa, agente, obrigação ou período), a condição de comparação, o risco de contaminação, a fonte de cada desfecho e o tempo necessário para observá-lo. Um histórico recente ajuda a dimensionar e contextualizar, mas comparar uma amostra selecionada por inadimplência passada com todos os agentes futuros pode confundir regressão à média, sazonalidade e efeito da intervenção. Se um grupo contemporâneo for inviável, proponha um desenho escalonado ou histórico com limites explícitos de atribuição. Para um pacote de ações, não infira qual componente causou o resultado sem um desenho capaz de isolá-lo.

Quando um perfil histórico como reincidência orientar o recrutamento, defina-o com janela e regra anteriores à atribuição. Inclua grupos de intervenção e comparação dentro de cada perfil quando o objetivo for comparar o efeito entre perfis; relate os resultados por perfil se a amostra alterar sua proporção na população. A reincidência futura é um desfecho diferente do rótulo histórico e precisa de pelo menos oportunidades de ocorrência e seguimento suficientes. Não prometa sua redução com uma janela que só permite observar um ciclo.

## Fontes para consultar quando a decisão metodológica for controversa

- [Strategyzer, Test Card](https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card): hipótese, teste, medida e aparência do sucesso explicitados no planejamento de uma validação.
- [Strategyzer, desenho de experimentos](https://www.strategyzer.com/programs/design-experiments-prepare-to-test-your-business-idea-part-2): escolha de método e força de evidência conforme risco da hipótese.
- [Nielsen Norman Group, thinking aloud](https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/): referência incorporada ao [protocolo de sessões](analise-think-aloud.md); consulte-o antes da condução e na análise.
- [Nielsen Norman Group, pesquisa qualitativa e quantitativa](https://www.nngroup.com/articles/quant-vs-qual/): perguntas e resultados distintos para observação qualitativa e medição quantitativa.
- [Nielsen Norman Group, métricas em estudos qualitativos](https://www.nngroup.com/articles/metrics-qualitative/): contagens podem apoiar relatos, com limites explícitos de generalização.
- [GOV.UK, planejamento de pesquisa](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service): objetivos e perguntas de pesquisa evoluem com a fase do produto.
- [GOV.UK, análise de sessões](https://www.gov.uk/service-manual/user-research/analyse-a-research-session): separe observações de interpretação e use achados para decidir mudanças ou nova pesquisa.
- [PM Skills, desenho de experimentos](https://github.com/product-on-purpose/pm-skills/blob/main/skills/measure-experiment-design/SKILL.md): definição prévia de métricas e sucesso para A/B ou experimento controlado.
- [PM Skills, resultados](https://github.com/product-on-purpose/pm-skills/blob/main/skills/measure-experiment-results/SKILL.md): leitura de resultados e limites, voltada a experimento quantitativo.
- [Product Experimentation](https://github.com/magnus919/agent-skills/blob/main/product-experimentation/SKILL.md): seleção entre métodos qualitativos, protótipos e testes quantitativos conforme pergunta.
- [Testing Business Ideas skill](https://github.com/nimitbhargava/testing-business-ideas-skill/blob/main/skills/testing-business-ideas/SKILL.md): Test Card com medida e critério antes do teste; Learning Card depois. Use como referência de fluxo, não como protocolo estatístico.
- [Anthropic, síntese de pesquisa](https://github.com/anthropics/knowledge-work-plugins/blob/main/product-management/skills/synthesize-research/SKILL.md): codificação temática, contradições, impacto e perguntas abertas; adapte contagens pequenas como frequência observada, não prevalência.

## Padrões incorporados das skills

- **Strategyzer e Testing Business Ideas:** suposição → hipótese focal → Test Card → evidência → Learning Card. Adaptação: o critério numérico é exigido para verificação, não para toda exploração qualitativa.
- **Product Experimentation:** priorização de suposições por risco e evidência, escolha do método, guardrails proporcionais, dono da decisão e registro do resultado. Adaptação: nenhuma dependência de skills vizinhas ou ferramentas específicas.
- **PM Skills:** contratos separados de desenho, resultado e decisão, com métricas e critérios prospectivos quando o teste for quantitativo. Adaptação: sem exigir A/B, significância ou tamanho de amostra quantitativo em think aloud.
- **Anthropic Research Synthesis:** codificação, temas, exceções e consequências para o produto. Adaptação: cada achado exige vínculo com evidência primária e explicita contraexemplos e limites.

Os padrões foram reescritos para este fluxo; os textos e templates originais das skills não foram copiados.
