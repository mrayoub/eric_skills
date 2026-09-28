# Comparação local das descriptions — plano 008

## Método e limites

Em 28/09/2026, o operador pediu as duas avaliações nesta sessão em vez de chamadas ao Claude Opus. A linha de base foi revisada antes de editar as descriptions. O avaliador é o próprio Codex nesta sessão, com acesso prévio ao plano e aos rótulos esperados: avaliação **não cega**, sujeita a influência do contexto. Não houve execução do `run_eval`, invocação real das skills ou três tentativas independentes por consulta. Portanto, os números abaixo são concordâncias de uma revisão de seleção, não taxas empíricas de acionamento.

Para cada consulta, foi escolhida uma skill primária entre as onze irmãs, ou `nenhuma` quando o pedido não justificava carregar uma dessas skills. A comparação usa `(selecionada == skill do conjunto) == should_trigger`. Uma negativa pode acertar mesmo que a escolha de outra skill seja discutível. Não foram usados dados de `_SAMPLE/`.

Na consulta 11 de briefing-inovacao, escrever apenas um e-mail de convite foi considerado tarefa simples (`nenhuma`); preparar convite e regras/dinâmicas do encontro, nas consultas de workshop-5c, justifica a skill.

## Antes e depois

Catálogo antes: descriptions do commit `ae5e211`. A linha de base foi registrada no commit `c83d4de`. Catálogo depois: os onze textos exatos do Step 3 do plano 008, sem ajustes adicionais. As mesmas 176 consultas foram revistas com o novo catálogo; as escolhas primárias permaneceram iguais. Os registros individuais estão abaixo.

| Skill | True antes | False antes | True depois | False depois | Consultas erradas |
|---|---:|---:|---:|---:|---|
| avaliacao-briefing-iqb | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| briefing-inovacao | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| experimentacao-inovacao | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| potencial-inovacao | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| relatorio-3e | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| relatorio-4d | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| relatorio-5c | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| scorecard-inovacao | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| workshop-3e | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| workshop-4d | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |
| workshop-5c | 8/8 | 8/8 | 8/8 | 8/8 | Nenhuma |

Total da revisão: **176/176 antes e 176/176 depois**, uma escolha por consulta em cada etapa. A meta de 7/8 por lado é atendida nesta revisão; a meta empírica do `run_eval` não foi medida. **Não foi observado ganho de acerto** e não é possível inferir desempenho perfeito em uso real.

## Interpretação

As novas descriptions explicitam vocabulário e fronteiras que antes precisavam ser inferidos. Exemplos revisados: notas do briefing → IQB; criação/one-page → briefing; decisão de prioridade → potencial; evidência para gate → scorecard; facilitação E3 → workshop-3e; protocolo detalhado e Learning Cards → experimentação. Nos pares workshop/relatório, o produto pedido (conduzir encontro ou consolidar entrega) continuou determinando a seleção.

Pedidos de relatório 3E com Test Cards foram mantidos em relatorio-3e: a nova experimentacao-inovacao também cita Test Card, mas o pedido explícito de consolidar registros E1–E3 é mais específico. Não foi necessário alterar os textos definidos pelo plano.

A comparação serve como revisão de coerência das fronteiras. Para avaliar acionamento efetivo, subacionamento, variação entre tentativas ou o efeito em outro ambiente/modelo, ainda é necessário executar o procedimento independente do README. O mesmo avaliador conhecia os resultados da primeira etapa e os rótulos; o segundo resultado não é uma replicação independente.

## Registro por consulta

O número corresponde à posição (1–16) no JSON da skill, contando a partir de 1. A consulta aparece integralmente para permitir revisão.

| Conjunto | Nº | Esperado | Escolha antes | Escolha depois | Consulta |
|---|---:|---|---|---|---|
| avaliacao-briefing-iqb | 1 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Esse briefing está bom o suficiente pra seguir pro aprofundamento? Avalia pela rubrica |
| avaliacao-briefing-iqb | 2 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Compara a versão 1 e a 2 do briefing e diz se a qualidade melhorou |
| avaliacao-briefing-iqb | 3 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Roda o checklist dos 40 critérios nesse briefing |
| avaliacao-briefing-iqb | 4 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Dê a nota IQB do briefing de Atendimento, justificando cada resposta e mostrando os vetos aplicados. |
| avaliacao-briefing-iqb | 5 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Audite a qualidade deste enquadramento pela rubrica interna, com clareza, evidências, resultados e acionabilidade. |
| avaliacao-briefing-iqb | 6 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Verifique se briefing-v4.md permite iniciar a descoberta; preciso da matriz completa de critérios e da classificação calculada. |
| avaliacao-briefing-iqb | 7 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | A diretoria quer saber se a qualidade do briefing melhorou depois da revisão de 15 de setembro: compare as duas versões pelo IQB. |
| avaliacao-briefing-iqb | 8 | true | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Valide este briefing preenchido e explique quais critérios impedem uma nota maior, preservando a evidência usada em cada resposta. |
| avaliacao-briefing-iqb | 9 | false | briefing-inovacao | briefing-inovacao | Melhora a redação do HMW desse briefing |
| avaliacao-briefing-iqb | 10 | false | scorecard-inovacao | scorecard-inovacao | Quão validado está o projeto de adimplemento hoje? |
| avaliacao-briefing-iqb | 11 | false | potencial-inovacao | potencial-inovacao | Pontua essa oportunidade em impacto, viabilidade e urgência |
| avaliacao-briefing-iqb | 12 | false | briefing-inovacao | briefing-inovacao | Transforme a transcrição da conversa com o sponsor em um briefing de sete campos com lacunas explícitas. |
| avaliacao-briefing-iqb | 13 | false | briefing-inovacao | briefing-inovacao | Monte a one-page do desafio de cadastro para a reunião do comitê, usando o briefing v2 como fonte. |
| avaliacao-briefing-iqb | 14 | false | potencial-inovacao | potencial-inovacao | Ranqueie as quatro oportunidades do garimpo e justifique qual merece investimento primeiro. |
| avaliacao-briefing-iqb | 15 | false | relatorio-4d | relatorio-4d | Compila o relatório 4D a partir do mural, dos dissensos e da planilha de votos anexada. |
| avaliacao-briefing-iqb | 16 | false | experimentacao-inovacao | experimentacao-inovacao | Planeje um teste de usabilidade do formulário com hipóteses, métricas, Test Cards e protocolo de coleta. |
| briefing-inovacao | 1 | true | briefing-inovacao | briefing-inovacao | Transforma essa transcrição da conversa com a área de adimplemento num briefing do desafio |
| briefing-inovacao | 2 | true | briefing-inovacao | briefing-inovacao | Preciso de uma one-page do briefing v2 pra levar pro comitê amanhã |
| briefing-inovacao | 3 | true | briefing-inovacao | briefing-inovacao | Quais perguntas eu deveria mandar pro sponsor pra fechar as lacunas desse briefing? |
| briefing-inovacao | 4 | true | briefing-inovacao | briefing-inovacao | A entrevista de 12 de setembro com Operações está em entrevista.md; reconstrua o desafio nos sete campos e destaque o que ainda falta confirmar. |
| briefing-inovacao | 5 | true | briefing-inovacao | briefing-inovacao | A área de Atendimento trouxe um problema de devolução de solicitações; escreva o enquadramento com pessoas afetadas, relevância e resultados esperados. |
| briefing-inovacao | 6 | true | briefing-inovacao | briefing-inovacao | Revise nosso briefing v3 com base na nova conversa com a responsável e registre as mudanças em relação à versão anterior. |
| briefing-inovacao | 7 | true | briefing-inovacao | briefing-inovacao | Ajude a formular o how might we dessa dor de cadastro e complete a proposta de briefing sem antecipar a solução. |
| briefing-inovacao | 8 | true | briefing-inovacao | briefing-inovacao | Monte um resumo executivo de uma página e perguntas para o sponsor a partir deste briefing com escopo e resultados ainda incompletos. |
| briefing-inovacao | 9 | false | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Dá uma nota IQB pra esse briefing |
| briefing-inovacao | 10 | false | potencial-inovacao | potencial-inovacao | Entre essas três dores, qual devemos priorizar? |
| briefing-inovacao | 11 | false | nenhuma | nenhuma | Escreve um e-mail convidando os clientes pro workshop 5C |
| briefing-inovacao | 12 | false | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Compare a qualidade dos briefings v1 e v2 pelos 40 critérios, aplicando vetos e mostrando as notas por dimensão. |
| briefing-inovacao | 13 | false | scorecard-inovacao | scorecard-inovacao | Avalie a maturidade das evidências do projeto de adimplemento e identifique o que falta para o gate de piloto. |
| briefing-inovacao | 14 | false | relatorio-4d | relatorio-4d | Temos notas e votos de D1 a D4; compile o relatório do aprofundamento e a síntese para o BP1. |
| briefing-inovacao | 15 | false | workshop-3e | workshop-3e | Prepare a pauta E1-E3 para o grupo estruturar a solução de cadastro e discutir seus componentes. |
| briefing-inovacao | 16 | false | experimentacao-inovacao | experimentacao-inovacao | O piloto terminou em setembro; analise as observações e monte Learning Cards com recomendações para a próxima rodada. |
| experimentacao-inovacao | 1 | true | experimentacao-inovacao | experimentacao-inovacao | Quero testar se o formulário guiado reduz devoluções; qual método e quais Test Cards? |
| experimentacao-inovacao | 2 | true | experimentacao-inovacao | experimentacao-inovacao | Rodamos 5 sessões de think aloud, analisa e gera os Learning Cards |
| experimentacao-inovacao | 3 | true | experimentacao-inovacao | experimentacao-inovacao | O piloto terminou, faz a síntese de evidências e a recomendação |
| experimentacao-inovacao | 4 | true | experimentacao-inovacao | experimentacao-inovacao | Planeje uma rodada de teste de usabilidade para validar a hipótese de que os agentes entendem o status das solicitações. |
| experimentacao-inovacao | 5 | true | experimentacao-inovacao | experimentacao-inovacao | Prepare Test Cards individuais, amostragem e protocolo para comparar dois fluxos de atendimento em setembro. |
| experimentacao-inovacao | 6 | true | experimentacao-inovacao | experimentacao-inovacao | Temos observações do MVP manual e entrevistas; analise o que foi aprendido e proponha os próximos testes. |
| experimentacao-inovacao | 7 | true | experimentacao-inovacao | experimentacao-inovacao | Escreva o plano de experimentação e a apresentação dos resultados, distinguindo hipóteses prévias de evidência coletada. |
| experimentacao-inovacao | 8 | true | experimentacao-inovacao | experimentacao-inovacao | Ajude a escolher entre entrevista, teste think aloud e piloto operacional para investigar esta hipótese; registre critérios e riscos de cada método. |
| experimentacao-inovacao | 9 | false | nenhuma | nenhuma | Escreve testes unitários pro módulo de cobrança |
| experimentacao-inovacao | 10 | false | relatorio-3e | relatorio-3e | Compila o relatório 3E |
| experimentacao-inovacao | 11 | false | scorecard-inovacao | scorecard-inovacao | Quão maduro está o projeto no scorecard? |
| experimentacao-inovacao | 12 | false | workshop-3e | workshop-3e | Prepare apenas a pauta e o board do E3 do workshop 3E, para o grupo planejar seus Test Cards iniciais. |
| experimentacao-inovacao | 13 | false | relatorio-3e | relatorio-3e | Consolide os cards prospectivos já definidos em E1-E3 no relatório de solução e decisão de rota. |
| experimentacao-inovacao | 14 | false | potencial-inovacao | potencial-inovacao | Compare oportunidades de triagem e cadastro pela rubrica de potencial e recomende uma priorização calculada. |
| experimentacao-inovacao | 15 | false | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Avalie o briefing pelo IQB e aplique os 40 critérios com vetos e nota por dimensão. |
| experimentacao-inovacao | 16 | false | relatorio-5c | relatorio-5c | Compile os registros C1-C5 do encontro com clientes em relatório, incluindo falas, votação e dissensos. |
| potencial-inovacao | 1 | true | potencial-inovacao | potencial-inovacao | Temos 5 dores levantadas no garimpo, me ajuda a ranquear qual atacar primeiro |
| potencial-inovacao | 2 | true | potencial-inovacao | potencial-inovacao | Vale a pena investir nessa ideia de triagem automática? Classifica o potencial |
| potencial-inovacao | 3 | true | potencial-inovacao | potencial-inovacao | Revisa a priorização que fizemos mês passado com os dados novos |
| potencial-inovacao | 4 | true | potencial-inovacao | potencial-inovacao | Compare as oportunidades de cadastro e atendimento pela rubrica de impacto, viabilidade, alinhamento, urgência e novidade. |
| potencial-inovacao | 5 | true | potencial-inovacao | potencial-inovacao | Preciso triar as sugestões da área de Operações em priorizar, monitorar ou arquivar; registre notas justificadas e fontes. |
| potencial-inovacao | 6 | true | potencial-inovacao | potencial-inovacao | Avalie o potencial dessa proposta de conciliação e calcule a recomendação com os pesos da rubrica interna. |
| potencial-inovacao | 7 | true | potencial-inovacao | potencial-inovacao | As restrições de orçamento mudaram em setembro; reavalie nossa decisão de priorização das três dores registradas. |
| potencial-inovacao | 8 | true | potencial-inovacao | potencial-inovacao | Qual destas ideias merece atenção primeiro? Use as evidências disponíveis para pontuar cada critério e mostre as lacunas que impedem a comparação. |
| potencial-inovacao | 9 | false | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Qual é o IQB desse briefing? |
| potencial-inovacao | 10 | false | scorecard-inovacao | scorecard-inovacao | O projeto tem evidência pra passar no gate de piloto? |
| potencial-inovacao | 11 | false | experimentacao-inovacao | experimentacao-inovacao | Monta os Test Cards para essa hipótese |
| potencial-inovacao | 12 | false | briefing-inovacao | briefing-inovacao | Reescreva o briefing de adimplemento a partir da entrevista, preenchendo seus sete campos. |
| potencial-inovacao | 13 | false | scorecard-inovacao | scorecard-inovacao | Compare os retratos de maturidade de junho e setembro pelo Innovation Project Scorecard da Strategyzer. |
| potencial-inovacao | 14 | false | workshop-4d | workshop-4d | Organize o roteiro do workshop 4D com barco da inovação e votação para sexta-feira. |
| potencial-inovacao | 15 | false | relatorio-5c | relatorio-5c | Consolide o relatório 5C do encontro com clientes, incluindo os votos e os dissensos de C1 a C5. |
| potencial-inovacao | 16 | false | experimentacao-inovacao | experimentacao-inovacao | Analise as sessões de think aloud já realizadas e produza Learning Cards e recomendação para a próxima rodada. |
| relatorio-3e | 1 | true | relatorio-3e | relatorio-3e | Com as notas do E1-E3, monta o relatório 3E e a decisão de rota |
| relatorio-3e | 2 | true | relatorio-3e | relatorio-3e | Revisa o relatório 3E e confere se cada Test Card tem os quatro campos |
| relatorio-3e | 3 | true | relatorio-3e | relatorio-3e | A rota ficou híbrida; compila o relatório com o plano de construção |
| relatorio-3e | 4 | true | relatorio-3e | relatorio-3e | Consolide as decisões do workshop de estruturação em solução, recorte, componentes, responsáveis e prazos. |
| relatorio-3e | 5 | true | relatorio-3e | relatorio-3e | Temos o board do E1, a lista do E2 e os cards do E3; produza o documento final da estruturação. |
| relatorio-3e | 6 | true | relatorio-3e | relatorio-3e | Atualize o Relatório 3E com a decisão de construção interna e preserve os Test Cards ainda prospectivos. |
| relatorio-3e | 7 | true | relatorio-3e | relatorio-3e | Revise o relatório da solução de cadastro e identifique lacunas do plano de construção sem inventar evidência observada. |
| relatorio-3e | 8 | true | relatorio-3e | relatorio-3e | Prepare a consolidação dos Test Cards e da decisão de rota a partir da ata de E1-E3 de 18 de setembro. |
| relatorio-3e | 9 | false | workshop-3e | workshop-3e | Facilita o E1 comigo agora |
| relatorio-3e | 10 | false | experimentacao-inovacao | experimentacao-inovacao | Gera os Learning Cards dos testes que rodamos |
| relatorio-3e | 11 | false | relatorio-4d | relatorio-4d | Escreve o relatório 4D |
| relatorio-3e | 12 | false | workshop-3e | workshop-3e | Monte a pauta e o board do workshop de estruturação da solução para a próxima semana. |
| relatorio-3e | 13 | false | workshop-3e | workshop-3e | Organize a dinâmica precisa ter, pode evoluir e fora do recorte para o grupo decidir os componentes no E2. |
| relatorio-3e | 14 | false | experimentacao-inovacao | experimentacao-inovacao | Analise o resultado das sessões de usabilidade e recomende como testar a hipótese na próxima rodada. |
| relatorio-3e | 15 | false | relatorio-5c | relatorio-5c | Compile a devolutiva do encontro de cocriação com clientes, ligando C1-C5 às falas e votos registrados. |
| relatorio-3e | 16 | false | potencial-inovacao | potencial-inovacao | Avalie o potencial das oportunidades do garimpo e classifique cada uma em priorizar, monitorar ou arquivar. |
| relatorio-4d | 1 | true | relatorio-4d | relatorio-4d | Tenho o mural, a transcrição e os votos do D4, compila o relatório |
| relatorio-4d | 2 | true | relatorio-4d | relatorio-4d | Revisa esse relatório 4D antes de ir pro BP1 |
| relatorio-4d | 3 | true | relatorio-4d | relatorio-4d | Só fizemos D1 e D2, consegue consolidar o que temos? |
| relatorio-4d | 4 | true | relatorio-4d | relatorio-4d | Produza o Relatório 4D do aprofundamento de Cadastro usando notas, snapshot da jornada e a planilha de créditos. |
| relatorio-4d | 5 | true | relatorio-4d | relatorio-4d | Consolide as evidências de D1-D4 em uma síntese para o BP1, incluindo diagnóstico, alternativas e dissensos. |
| relatorio-4d | 6 | true | relatorio-4d | relatorio-4d | Revise a versão 2 do relatório de aprofundamento e confira denominadores dos votos e rastreabilidade das conclusões. |
| relatorio-4d | 7 | true | relatorio-4d | relatorio-4d | O encontro não teve gravação, mas temos registros completos dos quatro Ds; monte o relatório e marque os limites das fontes. |
| relatorio-4d | 8 | true | relatorio-4d | relatorio-4d | Atualize o Relatório 4D com a ata da votação de setembro, preservando os registros anteriores e as lacunas do diagnóstico. |
| relatorio-4d | 9 | false | workshop-4d | workshop-4d | Quais perguntas uso para abrir o D1 amanhã? |
| relatorio-4d | 10 | false | relatorio-5c | relatorio-5c | Escreve o relatório do encontro com clientes de ontem (5C) |
| relatorio-4d | 11 | false | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Avalia o briefing pelo IQB |
| relatorio-4d | 12 | false | workshop-4d | workshop-4d | Organize o board e o roteiro do barco da inovação para uma sessão remota com 12 participantes. |
| relatorio-4d | 13 | false | workshop-4d | workshop-4d | Prepare um 4D assíncrono para aprofundar o desafio de atendimento, com instruções e regras de decisão. |
| relatorio-4d | 14 | false | relatorio-3e | relatorio-3e | Compile as decisões de E1-E3 em relatório de solução com plano de construção e Test Cards individuais. |
| relatorio-4d | 15 | false | experimentacao-inovacao | experimentacao-inovacao | Monte os Learning Cards a partir dos resultados do piloto operacional e sintetize a recomendação. |
| relatorio-4d | 16 | false | scorecard-inovacao | scorecard-inovacao | Compare a maturidade do projeto nos retratos de junho e setembro usando o scorecard da Strategyzer. |
| relatorio-5c | 1 | true | relatorio-5c | relatorio-5c | Aqui está a gravação e a ata do encontro 5C, faz o relatório |
| relatorio-5c | 2 | true | relatorio-5c | relatorio-5c | Consolida os votos do C2 e do C5 e escreve a devolutiva aos clientes |
| relatorio-5c | 3 | true | relatorio-5c | relatorio-5c | Revisa esse relatório 5C: os totais batem? |
| relatorio-5c | 4 | true | relatorio-5c | relatorio-5c | Monte o Relatório 5C a partir do mural e das falas de oito agentes de mercado, registrando propostas e dissensos. |
| relatorio-5c | 5 | true | relatorio-5c | relatorio-5c | Precisamos da síntese do encontro de cocriação de 22 de setembro para enviar aos participantes, com fontes e próximos passos. |
| relatorio-5c | 6 | true | relatorio-5c | relatorio-5c | Atualize o relatório do workshop com clientes usando a planilha de créditos e explicite os denominadores dos votos. |
| relatorio-5c | 7 | true | relatorio-5c | relatorio-5c | Só temos notas de C1-C3; consolide uma versão parcial do relatório com limites e lacunas das etapas restantes. |
| relatorio-5c | 8 | true | relatorio-5c | relatorio-5c | Revise a rastreabilidade entre experiência atual, experiência desejada e propostas cocriadas neste relatório de C1 a C5. |
| relatorio-5c | 9 | false | workshop-5c | workshop-5c | Monta o roteiro do encontro 5C da semana que vem |
| relatorio-5c | 10 | false | relatorio-4d | relatorio-4d | Compila o relatório 4D |
| relatorio-5c | 11 | false | experimentacao-inovacao | experimentacao-inovacao | Analisa as sessões de think aloud |
| relatorio-5c | 12 | false | workshop-5c | workshop-5c | Prepare o convite e as dinâmicas do workshop 5C para cocriação com clientes de Atendimento. |
| relatorio-5c | 13 | false | workshop-5c | workshop-5c | Como devemos facilitar os pitches e créditos de votação no C5? Organize instruções para os participantes. |
| relatorio-5c | 14 | false | relatorio-3e | relatorio-3e | Consolide os registros E1-E3 no relatório da solução com decisão de rota e plano de construção. |
| relatorio-5c | 15 | false | scorecard-inovacao | scorecard-inovacao | Compare os retratos de maturidade de junho e setembro e indique as lacunas de evidência do projeto. |
| relatorio-5c | 16 | false | briefing-inovacao | briefing-inovacao | Transforme a transcrição da entrevista com o sponsor em briefing de sete campos e perguntas de esclarecimento. |
| scorecard-inovacao | 1 | true | scorecard-inovacao | scorecard-inovacao | Quão validado está o projeto de adimplemento? Usa o scorecard da Strategyzer |
| scorecard-inovacao | 2 | true | scorecard-inovacao | scorecard-inovacao | Temos evidência suficiente pra passar pro piloto? |
| scorecard-inovacao | 3 | true | scorecard-inovacao | scorecard-inovacao | Compara o retrato de maturidade de junho com o de hoje |
| scorecard-inovacao | 4 | true | scorecard-inovacao | scorecard-inovacao | Avalie a força das evidências do projeto de cadastro com o Innovation Project Scorecard e identifique lacunas decisivas. |
| scorecard-inovacao | 5 | true | scorecard-inovacao | scorecard-inovacao | Prepare um retrato datado da maturidade deste projeto, sem média geral, separando o que foi demonstrado do que ainda é hipótese. |
| scorecard-inovacao | 6 | true | scorecard-inovacao | scorecard-inovacao | O comitê pediu uma análise de evidências para o gate de setembro; use o scorecard e recomende os próximos testes. |
| scorecard-inovacao | 7 | true | scorecard-inovacao | scorecard-inovacao | Revise a avaliação institucional de maturidade e declare o que foi adaptado do instrumento oficial da Strategyzer. |
| scorecard-inovacao | 8 | true | scorecard-inovacao | scorecard-inovacao | Compare o projeto antes e depois do piloto quanto à maturidade das evidências, preservando as fontes e limites de cada retrato. |
| scorecard-inovacao | 9 | false | potencial-inovacao | potencial-inovacao | Pontua o potencial dessa oportunidade |
| scorecard-inovacao | 10 | false | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Dá nota IQB no briefing |
| scorecard-inovacao | 11 | false | experimentacao-inovacao | experimentacao-inovacao | Gera Learning Cards dos testes |
| scorecard-inovacao | 12 | false | potencial-inovacao | potencial-inovacao | Priorize as cinco dores do garimpo usando impacto, viabilidade, alinhamento, urgência e novidade. |
| scorecard-inovacao | 13 | false | avaliacao-briefing-iqb | avaliacao-briefing-iqb | Rode o checklist dos 40 critérios no briefing de Atendimento e calcule a classificação por dimensão. |
| scorecard-inovacao | 14 | false | experimentacao-inovacao | experimentacao-inovacao | Planeje um piloto operacional detalhado, com Test Cards, método de coleta e protocolo de análise. |
| scorecard-inovacao | 15 | false | experimentacao-inovacao | experimentacao-inovacao | Analise os dados do experimento e escreva a síntese de aprendizados e a recomendação final. |
| scorecard-inovacao | 16 | false | relatorio-3e | relatorio-3e | Com base na ata de E1-E3, compile o relatório da solução com recorte, plano de construção e decisão de rota. |
| workshop-3e | 1 | true | workshop-3e | workshop-3e | Prepara a pauta do workshop de estruturação da solução E1 a E3 |
| workshop-3e | 2 | true | workshop-3e | workshop-3e | Como conduzo a classificação precisa ter / pode evoluir / fora do recorte? |
| workshop-3e | 3 | true | workshop-3e | workshop-3e | Registra o que o grupo decidiu no E2 hoje |
| workshop-3e | 4 | true | workshop-3e | workshop-3e | Monte um board para esclarecer a hipótese, delimitar o escopo e estruturar os componentes da solução candidata. |
| workshop-3e | 5 | true | workshop-3e | workshop-3e | Vamos fazer a estruturação com a área de Operações na quinta: organize roteiro, perguntas e os Test Cards do E3. |
| workshop-3e | 6 | true | workshop-3e | workshop-3e | Ajude a facilitar o E1 ao vivo e registrar o que o grupo concordou sobre hipótese e escopo. |
| workshop-3e | 7 | true | workshop-3e | workshop-3e | Organize um workshop 3E assíncrono, com tarefas de esclarecimento, estruturação e planejamento inicial de testes. |
| workshop-3e | 8 | true | workshop-3e | workshop-3e | Prepare a dinâmica do E2 para separar o mínimo necessário das evoluções futuras e dos itens fora do recorte. |
| workshop-3e | 9 | false | relatorio-3e | relatorio-3e | Compila o relatório 3E com os Test Cards |
| workshop-3e | 10 | false | experimentacao-inovacao | experimentacao-inovacao | Analisa os resultados do piloto que rodou em agosto |
| workshop-3e | 11 | false | workshop-4d | workshop-4d | Roteiro do workshop 4D |
| workshop-3e | 12 | false | relatorio-3e | relatorio-3e | Consolide as notas de E1-E3 em relatório de solução, responsáveis, prazos e decisão de rota híbrida. |
| workshop-3e | 13 | false | relatorio-3e | relatorio-3e | Revise o relatório 3E existente e confira se os cards prospectivos mantêm os quatro campos da Strategyzer. |
| workshop-3e | 14 | false | experimentacao-inovacao | experimentacao-inovacao | Defina um protocolo detalhado para cinco sessões de think aloud e as regras de análise dos resultados. |
| workshop-3e | 15 | false | experimentacao-inovacao | experimentacao-inovacao | Escreva os Learning Cards dos experimentos concluídos em setembro, ligando observações e próximos passos. |
| workshop-3e | 16 | false | workshop-5c | workshop-5c | Prepare um encontro 5C com clientes para compreender experiência atual, cocriar propostas e votar os pitches. |
| workshop-4d | 1 | true | workshop-4d | workshop-4d | Monta o roteiro do aprofundamento 4D de sexta com as perguntas de cada D |
| workshop-4d | 2 | true | workshop-4d | workshop-4d | Como facilito o barco da inovação no D2 com 12 pessoas remotas? |
| workshop-4d | 3 | true | workshop-4d | workshop-4d | Vamos fazer o 4D de forma assíncrona, organiza as etapas |
| workshop-4d | 4 | true | workshop-4d | workshop-4d | Prepare a pauta D1-D4 para aprofundar a dor de solicitações internas, com tempos, perguntas e regras de votação. |
| workshop-4d | 5 | true | workshop-4d | workshop-4d | Crie um board colaborativo para descongelar percepções, mapear jornada, desenhar alternativas e decidir com créditos. |
| workshop-4d | 6 | true | workshop-4d | workshop-4d | Estamos ao vivo no D3; organize as alternativas que o grupo propôs e as perguntas para seguir ao D4. |
| workshop-4d | 7 | true | workshop-4d | workshop-4d | Registre o que aconteceu em cada D na sessão de hoje, incluindo divergências e decisões, sem montar o relatório final. |
| workshop-4d | 8 | true | workshop-4d | workshop-4d | A equipe de Cadastro quer explorar ventos, âncoras, icebergs e porto; monte a dinâmica e a orientação para a facilitação. |
| workshop-4d | 9 | false | relatorio-4d | relatorio-4d | Com essas fotos do mural e a planilha de votos, escreve o relatório 4D |
| workshop-4d | 10 | false | workshop-5c | workshop-5c | Prepara o workshop 5C com os clientes |
| workshop-4d | 11 | false | workshop-3e | workshop-3e | Planeja o E3 do workshop de estruturação |
| workshop-4d | 12 | false | relatorio-4d | relatorio-4d | Revise o relatório do aprofundamento antes do BP1 e confira se as conclusões estão ligadas aos registros D1-D4. |
| workshop-4d | 13 | false | relatorio-4d | relatorio-4d | Compile os registros de D1 e D2 em uma versão parcial do Relatório 4D, mostrando o que falta. |
| workshop-4d | 14 | false | workshop-5c | workshop-5c | Monte o roteiro de cocriação com oito agentes de mercado, da experiência atual aos pitches e votos em C5. |
| workshop-4d | 15 | false | relatorio-3e | relatorio-3e | A partir das notas E1-E3, produza o relatório de solução, o plano de construção e a decisão de rota. |
| workshop-4d | 16 | false | experimentacao-inovacao | experimentacao-inovacao | Planeje um piloto operacional para testar a hipótese de redução de devoluções, com Test Cards, métricas e protocolo. |
| workshop-5c | 1 | true | workshop-5c | workshop-5c | Vamos receber 8 agentes de mercado para cocriar, monta o roteiro 5C |
| workshop-5c | 2 | true | workshop-5c | workshop-5c | Como faço a votação de créditos no C5? |
| workshop-5c | 3 | true | workshop-5c | workshop-5c | Prepara as perguntas do C2 sobre a experiência atual |
| workshop-5c | 4 | true | workshop-5c | workshop-5c | Monte a pauta do encontro com clientes para contextualizar, compreender a jornada, confirmar expectativas e cocriar propostas. |
| workshop-5c | 5 | true | workshop-5c | workshop-5c | Prepare o convite e as regras de participação do workshop 5C de Atendimento em 22 de setembro. |
| workshop-5c | 6 | true | workshop-5c | workshop-5c | Ajude a facilitar o C3 ao vivo e registrar os critérios da experiência desejada que os agentes estão discutindo. |
| workshop-5c | 7 | true | workshop-5c | workshop-5c | Organize pitches e créditos de votação para o C5, incluindo como registrar totais e dissensos do grupo. |
| workshop-5c | 8 | true | workshop-5c | workshop-5c | Reconstrua o registro do encontro de cocriação por etapa C1-C5 usando estas notas, sem elaborar ainda o relatório consolidado. |
| workshop-5c | 9 | false | relatorio-5c | relatorio-5c | Escreve o relatório do 5C de ontem com base nas notas |
| workshop-5c | 10 | false | workshop-4d | workshop-4d | Planeja o workshop 4D |
| workshop-5c | 11 | false | workshop-3e | workshop-3e | Monta a pauta do E1-E3 |
| workshop-5c | 12 | false | relatorio-5c | relatorio-5c | Consolide a gravação, a ata e os votos do encontro com clientes em um Relatório 5C com próximos passos. |
| workshop-5c | 13 | false | relatorio-5c | relatorio-5c | Revise o Relatório 5C antes da devolutiva aos participantes e confira os denominadores da votação. |
| workshop-5c | 14 | false | workshop-4d | workshop-4d | Prepare perguntas, jornada e barco da inovação para aprofundar o desafio interno no D2. |
| workshop-5c | 15 | false | experimentacao-inovacao | experimentacao-inovacao | Planeje entrevistas de teste e sessões de think aloud para verificar a hipótese do formulário guiado. |
| workshop-5c | 16 | false | briefing-inovacao | briefing-inovacao | Produza uma one-page do briefing para o sponsor com resultados esperados e lacunas decisivas. |
