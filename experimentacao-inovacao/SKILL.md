---
name: experimentacao-inovacao
description: "Conduz a experimentação de inovação com pessoas ou operação em três blocos: aprofundamento e planejamento (fundamentação, escopo, estratégia e cronograma; entregável Hipóteses com Test Cards), execução (modelo de experimentação a executar, construção do MVP e realização dos testes; entregável Modelo de experimentação) e consolidação (resultados, Learning Cards, recomendação e avaliação do MVP; entregável Apresentação da experimentação e direcionamento para a próxima fase da esteira). Escolhe o método pela hipótese (entrevista, think aloud, MVP manual, piloto, comparação A/B e outros) e mantém tudo rastreável. Use quando o usuário falar em testar uma hipótese, piloto, MVP, teste de usabilidade, análise de sessões, resultados de experimento, Test Card ou Learning Card. Não use para testes automatizados de software nem apenas para o E3 de um workshop 3E (use workshop-3e)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.4.7"
---

# Experimentação de inovação

Conduz a fase Experimentar da esteira em três blocos — aprofundamento e planejamento, execução e consolidação —, ligando hipótese master, Test Cards, MVP construído, execução, evidências, Learning Cards, avaliação do MVP e recomendação proporcional ao observado.

## Leia primeiro

- [Base metodológica](references/base-metodologica.md) — pergunta, método e limites.
- [Métodos de execução](references/metodos-de-experimentacao.md) — alternativas conforme risco, evidência, custo, prazo e acesso.
- [Entregáveis](references/entregaveis.md) — os três entregáveis dos blocos e os modelos que os compõem.

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md) antes de sintetizar,
pontuar ou planejar, e reaplique-o a cada arquivo ou resposta novos. Em resumo: resolva
nos arquivos tudo que for pesquisável; pergunte só a fronteira de questões decisivas
cujas dependências já estão resolvidas; registre origem e localizador de cada resposta;
entregue versão parcial quando faltar suporte decisivo. Nunca pergunte a nota, o
resultado ou a conclusão desejada — isso não é dado, e contaminaria a avaliação.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Quando usar

A fase do projeto e o bloco atual são contexto, não pré-requisito. O pedido pode cair em
qualquer bloco: entregue o bloco pedido, uma preparação ou uma versão parcial. Se faltar o
que um bloco anterior deveria ter produzido, registre a lacuna — não invente plano, MVP ou
resultado. Material posterior entra com data; não apresente reconstrução como plano
combinado previamente.

## Antes de cada bloco

Use as decisões vigentes do 3E como referência principal para hipótese, público,
solução, MVP e testes. Briefing e 4D explicam o histórico desse afunilamento: não reabra
questões já resolvidas ou retiradas do escopo no 3E. Confira origem, versão e data;
uma decisão posterior registrada pode atualizar o plano. Questione apenas lacunas
que ainda afetem o teste ou evidências contrárias relevantes. Uma decisão de escopo
não comprova a hipótese nem autoriza mudar critérios após a coleta.

- **Estado:** identifique se a rodada está antes, durante ou depois da execução. Antes, planeje; durante, acompanhe e registre adaptações datadas sem apagar o plano; depois, reconstrua método real, população, unidade, exposição, comparação, janela, medidas/critérios e desvios. Método ambíguo exige descrição verificável, não nome inventado. Sem contrato prévio, preserve a lacuna e planeje nova verificação.
- **Fontes/lacunas:** inventarie roteiro, MVP, gravações, transcrições, feedback, telemetria, saídas, gabaritos e baseline com caminho/ID e estado: examinada, localizada não examinada, indisponível, fora do escopo. Lista inacessível impede alegar inventário completo. Em PDF/imagem sem texto, aplique OCR e confira o original, preservando página e incertezas; transcrição não prova revisão de vídeo. Leia [triagem](references/triagem-de-lacunas.md) nas lacunas; pesquise arquivos antes de perguntar. Pergunte por fatos, restrições e aprovações metodológicas, não pela conclusão desejada.

## Bloco 1 — Aprofundamento e planejamento → entregável **Hipóteses com Test Cards**

1. **Fundamentação (Test Cards):** formule a pergunta sobre efeito, comportamento ou viabilidade em público/versão delimitados. Priorize suposições por risco e evidência. Siga [planejamento dos testes](references/planejamento-dos-testes.md): um Test Card individual por teste, com quatro campos — hipótese, teste, medida, critério —, cada um em uma frase objetiva (até 280 caracteres); detalhes vão ao plano/caderno. Índice não substitui card. Critério prévio nunca é preenchido depois; card incompleto é rascunho, reconstruído é retrospectivo. Classifique a pergunta como exploratória, formativa, verificatória ou comparativa; escolha o método pela hipótese, não pelo formato do MVP. Leia [análise think aloud](references/analise-think-aloud.md) quando houver essas sessões, desde o planejamento.
2. **Escopo da experimentação:** preserve a hipótese master e o recorte do MVP do 3E; registre versão, público e elegibilidade, objetivos, métricas, denominadores, limiares, amostra, duração e o que fica fora. Efeito do pacote não prova componentes nem causa suposta; contexto de descoberta não é amostra experimental. Adaptações em separado, com data, motivo e responsável.
3. **Estratégia e cronograma:** ordene os testes pela capacidade de reduzir a incerteza com custo e prazo proporcionais; compare evidência, custo, prazo, risco e limites das opções de método. Monte o cronograma com marcos de construção do MVP e de teste, datas, responsáveis e dependências; prepare protocolo, guardrails, interrupções proporcionais e o gate de início.

**Hipóteses com Test Cards** reúne as suposições priorizadas, as hipóteses e um Test Card individual por teste, com o escopo que delimita a rodada. Critérios verificatórios precedem exposição e coleta. Estratégia e cronograma são a base do modelo de experimentação do bloco 2. Quando o pedido for só o bloco 1, as suposições, a hipótese master e o escopo saem num `experiment_plan` parcial (`metadata.completeness: "partial"`, sem perfil) junto dos Test Cards; esse escopo é a fonte da seção `scope` do Modelo de experimentação.

## Bloco 2 — Execução → entregável **Modelo de experimentação**

Abra o bloco com o **Modelo de experimentação**: o desenho que a equipe vai executar, ligado aos Test Cards. Ele traz o MVP a construir (componentes do "precisa ter" do 3E, critério de pronto, versão e responsáveis), o protocolo e o roteiro de cada teste, público e recrutamento, medidas e registros a coletar, guardrails e regra de interrupção, cronograma operacional e o gate de início. Siga [execução e MVP](references/execucao-e-mvp.md). Depois, acompanhe a execução do modelo:

4. **Construção do MVP:** a equipe constrói conforme o modelo; a skill acompanha e registra. Ligue cada componente ao "precisa ter" do 3E, com critério de pronto, responsável e estado; registre versão entregue, trabalho manual por trás do MVP, desvios datados do escopo e a prontidão para testar. MVP que não atende ao protocolo não inicia o teste sem decisão registrada.
5. **Realização dos testes:** execute conforme o protocolo; acompanhe elegibilidade, versão, adesão, qualidade e desvios. Registre cada execução e alimente o livro de evidências com fontes e localizadores. Não interprete resultados neste bloco.

Os registros da construção e da execução — versão, componentes, desvios, execuções por Test Card e dados ausentes — ficam no caderno e alimentam a consolidação. Mudanças no modelo durante a execução entram datadas, sem apagar a versão anterior.

## Bloco 3 — Consolidação → entregável **Apresentação da experimentação e direcionamento**

6. **Resultados, aprendizados e recomendação:** siga [análise da execução](references/analise-da-execucao.md) e [evidência/métricas](references/evidencia-e-metricas.md) antes de interpretar. Reconcilie unidades e fontes, mantenha discrepâncias e gabarito independente; fixe amostra e denominadores, recalcule contagens e preserve contraexemplos. Métrica pós-coleta é exploratória, não sucesso de critério original. Produza um Learning Card individual por Test Card executado, com o [modelo](assets/learning-card.md): hipótese testada, observações, aprendizado e ação, uma frase objetiva por campo, separando observação e inferência com IDs/localizadores. Critério formal: atingido, não atingido, inconclusivo ou fora do escopo; com dados insuficientes, marque inconclusivo sem inventar evidência; sem critério formal, não atribua aprovação retrospectiva. A síntese de evidências e recomendação é entregável próprio, não modelo Strategyzer.
7. **Avaliação do MVP:** siga [avaliação do MVP](references/avaliacao-do-mvp.md), separada da avaliação das hipóteses: aderência ao escopo, funcionamento, experiência de uso observada, viabilidade operacional e técnica, esforço e custo, pendências e prontidão para implantação, cada dimensão com evidência ou `não avaliado`. MVP que funciona não valida hipótese; hipótese não sustentada não torna o MVP ruim.
8. **Fechamento e direcionamento:** confira a cadeia completa e cada card; corrija amostra, versão, números, status e formulações entre documentos. Ligação sem evidência reduz a conclusão ou vira pendência. Direcione para o BP2 com uma saída — avançar, iterar, investigar ou encerrar —, condições verificáveis, responsável e prazo. Piloto como próximo experimento exige perguntas, público, exposição, monitoramento, interrupção e decisor; escala exige evidência dos critérios críticos e decisão responsável; sem isso, recomende a próxima ação verificável com responsável e condição. Separe recomendação da decisão: quem, quando, alternativas, riscos aceitos e gatilho de revisão.

**Apresentação da experimentação e direcionamento** traz resultados, aprendizados, avaliação do MVP e a recomendação que serve à próxima fase da esteira (BP2), a partir do mesmo registro do relatório; números e afirmações apontam definições, denominadores e evidências.

Produza somente os documentos solicitados, preservando fontes e status para regeneração. O [caderno](assets/caderno-da-rodada.md) editável é opcional; preserve IDs. Não declare bloco, card ou recomendação prontos com lacuna decisiva: entregue pronto para decisão proposta, parcial ou inconclusivo, nomeando só as pendências relevantes. Respeite escopo parcial ou encerramento do usuário. Material bruto permanece no projeto, fora da skill; anonimização e trechos mínimos sustentam a análise.

## Exemplo

Entrada: “Analise o Portal de Solicitações de Dados: três sucessos em cinco sessões.”
Saída (trecho):
> Bloco 3. TC-01: critério prévio quatro de cinco; não atingido.
> LC-01: hipótese, observações, aprendizado e próximo teste citados.
> Avaliação do MVP: dimensões sem evidência marcadas como `não avaliado`; economia de tempo não medida.
> Direcionamento: iterar a orientação do campo de classificação e repetir o teste.

## Checagem final

- [ ] Bloco e entregável identificados; lacunas de blocos anteriores registradas
- [ ] Hipótese master, escopo e recorte do MVP preservados
- [ ] Cards individuais, completos ou pendências explícitas
- [ ] Modelo de experimentação executável: MVP, protocolo, registros, cronograma e responsáveis
- [ ] MVP construído registrado contra o modelo, com versão e desvios
- [ ] Cronologia, critérios prévios e adaptações registrados
- [ ] Amostra/denominadores conferidos; achados rastreáveis
- [ ] Avaliação do MVP separada da avaliação das hipóteses
- [ ] Observação, inferência, recomendação e decisão separadas; contraevidência preservada
- [ ] Mesma cadeia e conteúdo entre entregáveis

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Os três blocos organizam o trabalho desta skill dentro da etapa
Experimentar; não são etapas da esteira. Consulte [a esteira](references/eric-esteira.md)
quando precisar interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações
entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md):

| Entregável | `deliverable_type` |
|---|---|
| Hipóteses com Test Cards | um `test_card` por teste |
| Modelo de experimentação | `experiment_plan` com `metadata.content_profile: "experimentation_model"` e as seções `mvp_build`, `scope`, `schedule` e `start_gate` |
| Apresentação da experimentação e direcionamento | `executive_presentation` com `metadata.content_profile: "experimentation_presentation"`, as seções do schema `context`, `method`, `findings`, `recommendation` e `next_steps`, e as seções do perfil `mvp_evaluation` e `direction`; `direction` vem depois de `recommendation` e `next_steps`, sem substituí-las. Use títulos-mensagem de 4 a 12 palavras por slide (ex.: "O MVP funcionou, mas a economia de tempo não foi medida") e coloque a `section_key` no bloco de conteúdo. Entregue também `evidence_recommendation`, um `learning_card` por card executado e `experiment_report` quando um relatório detalhado for pedido |

Monte o JSON canônico, rode `python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** skill própria desta pasta; cards seguem os modelos Test Card e Learning Card da Strategyzer AG (links em `references/fontes.md`); os modelos em `assets/` são adaptações locais.
