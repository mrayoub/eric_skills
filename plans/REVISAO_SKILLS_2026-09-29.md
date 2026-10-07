# Revisão individual das onze skills — 29/09/2026

Base: commit `32a103a`, branch `advisor/010-skill-md`. Auditoria com a skill `improve`, somente leitura da implementação. As recomendações abaixo ainda não foram implementadas.

Foram examinados os onze SKILL.md, referências específicas, contratos de conteúdo, cálculos próprios, renderizador compartilhado e testes/evals relacionados. Os achados foram confrontados com os arquivos citados. Reproduções locais usam dados fictícios, em memória. A suíte local passou: **59 testes e 28 subtestes**. A sincronização das cópias passou.

Não foram executadas chamadas ao Claude, baterias de acionamento ou avaliações comportamentais com outros modelos. Não foi usado material de `_SAMPLE/`, `_OUTPUTS/` ou históricos privados de `.claude/`. Esta revisão não inclui consulta a bases externas de vulnerabilidades, análise integral de todos os binários originais nem teste de compreensão com usuários. Testes estruturais aprovados não garantem comportamento do modelo.

## Achados priorizados, sem duplicar correções compartilhadas

P1 = corrigir primeiro; P2 = melhoria posterior. Esforço: S = horas, M = cerca de um dia, L = vários dias. Confiança alta significa reprodução ou evidência direta; média indica ambiguidade que depende da interpretação do executor.

| ID | Achado | Prioridade | Esforço | Risco da correção | Confiança |
| --- | --- | --- | --- | --- | --- |
| A01 | Notas arredondadas do potencial divergem do total e da classe | P1 | S | Médio: afeta fronteiras de classificação | Alta |
| A02 | IQB aceita evidência nula como preenchida | P1 | S | Baixo: rejeita entradas inválidas | Alta |
| A03 | Contratos aceitam conteúdo obrigatório em blocos que não o exibem | P1 | M | Médio: JSONs antes aceitos podem passar a ser recusados | Alta |
| A04 | Cards parciais podem perder a estrutura de quatro campos | P1 | S | Médio: manter campos pendentes sem exigir conteúdo inventado | Alta |
| A05 | Markdown/TXT perde a citação ligada a cada card de uma grade | P1 | S | Baixo | Alta |
| A06 | Estado parcial e versão não aparecem automaticamente em todos os formatos | P1 | S | Baixo | Alta |
| A07 | IQB exige pontos fortes e perguntas em quantidade fixa | P2 | S | Baixo | Alta |
| A08 | Schema one-page anuncia retrato, mas a geração exige paisagem | P2 | S | Baixo | Alta |
| A09 | Board 4D associa natureza da mudança a esforço presumido | P2 | S | Baixo | Alta |
| A10 | Board 4D não conserva todas as perguntas da jornada | P2 | S | Baixo | Alta |
| A11 | Experimentação confunde avaliação de critério local com aprovação geral | P2 | S | Baixo | Média |

## 1. briefing-inovacao

**Identificado — A08.** `briefing-inovacao/references/briefing-one-page.schema.json:48` e `_DESIGN_SYSTEM/contracts/briefing-one-page.schema.json:48` aceitam retrato e paisagem; a descrição na linha 53 anuncia retrato como padrão. Entretanto, `briefing-inovacao/SKILL.md:41` determina paisagem, `_DESIGN_SYSTEM/profiles.json` fixa `a4_landscape` e `_DESIGN_SYSTEM/scripts/render.py:101` rejeita orientação contrária ao perfil.

**Impacto:** quem segue o contrato especializado pode montar um JSON válido pelo schema que o gerador rejeita por orientação.

**Recomendação:** manter a decisão vigente de paisagem e alinhar os dois schemas, sua descrição e o perfil. Testar uma one-page completa com o tamanho suportado e a rejeição de orientação não suportada; não resolver a inconsistência apenas marcando a saída como parcial.

**Aplicação de A06:** incluir estado, ID e versão também no briefing editável e na lista de perguntas, para que uma versão preliminar seja reconhecível fora do JSON.

## 2. avaliacao-briefing-iqb

**Identificado — A02.** `avaliacao-briefing-iqb/scripts/iqb.py:215` faz `str(evidence)` antes de conferir se há texto. `null` vira `None` como texto e passa. Reproduzi a aceitação das quarenta respostas com evidência nula; isso contraria a exigência de evidência ou descrição objetiva de ausência da rubrica.

**Impacto:** a checagem de entrada aceita respostas sem registro de suporte. Não se trata de julgar automaticamente se uma evidência é boa: primeiro é preciso exigir que ela seja realmente uma string preenchida.

**Recomendação:** exigir string não vazia, sem converter números, listas, objetos ou nulos em evidência. Cobrir esses tipos nos testes, preservando descrições explícitas de ausência e o cálculo dos vetos.

**Identificado — A07.** `_DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json:623` exige pelo menos dois itens no bloco de pontos fortes; `:737` exige exatamente três provocações. A skill pede até três perguntas (`avaliacao-briefing-iqb/SKILL.md:36`). A rubrica também permite avaliar um briefing vazio, que pode não ter forças demonstráveis.

**Impacto:** uma avaliação concluída pode falhar na exportação por ter somente uma pergunta relevante ou nenhum ponto forte, incentivando preenchimento artificial.

**Recomendação:** permitir de zero a três forças/perguntas, com declaração de ausência quando cabível. Alinhar a fonte compartilhada e a referência específica da skill. Testar briefing vazio e diagnóstico com uma pergunta.

## 3. potencial-inovacao

**Identificado — A01.** `potencial-inovacao/scripts/score.py:69` publica notas com uma casa decimal, mas `:76` usa as notas originais no total. `_DESIGN_SYSTEM/scripts/validators/innovation_potential_assessment.py:45` recalcula com as notas publicadas.

**Reprodução:** entradas `69.91, 69.91, 69.95, 70.04, 70.04` retornam notas `69.9, 69.9, 70.0, 70.0, 70.0`, total `70.0`, classe `priorizar`. O relatório com essas notas é recalculado como `69.9`, classe `monitorar`, e rejeitado pelo validador.

**Impacto:** o próprio resultado do script pode não ser exportável e sua classificação não corresponde às notas visíveis.

**Recomendação:** escolher uma única política de precisão e aplicá-la às notas, contribuições e total. Testar o caminho completo da saída real do script até o relatório, com duas/três casas e limites 40/70. Os testes atuais passam, mas não cobrem essa combinação de precisão e transformação da saída.

## 4. workshop-4d

**Identificado — A09.** `workshop-4d/references/mural-board-4d-template.md:120` associa incremental/estrutural/radical a baixo/médio/alto esforço. O playbook pede complexidade separada por proposta (`references/4d-workshop-playbook.md:161`).

**Impacto:** o board pode induzir uma estimativa de esforço antes de avaliar a proposta concreta.

**Recomendação:** separar natureza da mudança e esforço. Uma mudança radical pode ser simples; uma incremental pode ser difícil. Registrar a complexidade como campo próprio e preservar registros históricos já produzidos.

**Identificado — A10.** O board usa perguntas distintas nas três colunas da jornada (`mural-board-4d-template.md:81`), enquanto o playbook pede acontecimento, dor, valor e retrabalho em cada fase (`4d-workshop-playbook.md:73`).

**Impacto:** o diagnóstico pode omitir valor e retrabalho em partes da jornada.

**Recomendação:** incluir as quatro perguntas em antes/durante/depois, permitindo perguntas adicionais como complemento.

**Aplicação de A03:** o contrato `four-d-workshop-record.schema.json:22` aceita D1–D4 dentro de blocos que não exibem o texto. Corrigir a validação comum antes de considerar presença das seções como prova de entrega completa.

## 5. relatorio-4d

**Identificado — A05.** O layout exige fonte ligada a cada card (`relatorio-4d/references/relatorio-4d-layout.md:16`). Na grade Markdown, `_DESIGN_SYSTEM/scripts/render.py:554` escreve o conteúdo, mas omite `card.citation_ids`. HTML e DOCX mantêm esse vínculo.

**Impacto:** a bibliografia continua no fim, mas o leitor do MD/TXT não consegue ligar cada achado à respectiva fonte, sobretudo em cards contraditórios.

**Recomendação:** exibir os IDs de fonte no conteúdo de cada card também em MD/TXT. Verificar uma grade com duas fontes distintas e um card sem citação. Confirmar equivalência da ligação entre fonte e achado, não igualdade binária dos arquivos.

**Aplicação de A06:** mostrar estado parcial e versão no relatório editável, especialmente quando só D1/D2 existirem.

## 6. workshop-3e

**Identificado — A03.** `_DESIGN_SYSTEM/contracts/three-e-workshop-record.schema.json:22` verifica `section_key/text`, mas não que o tipo do bloco mostre esse texto. Reproduzi um registro completo com E1–E3 em `page_break`, aceito e sem essas sínteses no Markdown.

**Recomendação:** exigir blocos que realmente exibam o conteúdo usado para cumprir E1–E3. Quebras de página podem continuar existindo, mas não podem substituir sínteses de etapas.

**Identificado — A04/A06.** A skill exige quatro campos por card, inclusive rascunhos (`workshop-3e/SKILL.md:38`). O gerador troca para o envelope genérico quando a saída é parcial (`render.py:108`), permitindo um card de um único campo. MD/TXT/DOCX tampouco exibem automaticamente o estado e a versão.

**Recomendação:** conservar os quatro campos com pendências explícitas e apresentar estado/versão em todos os formatos, sem inventar critérios para passar a validação.

## 7. relatorio-3e

**Identificado — A03.** O contrato `three-e-report.schema.json:22` permite a mesma perda de E1–E3 e rota em blocos descartados pelo renderizador. A reprodução local validou o documento completo, mas suas sínteses não apareceram no Markdown.

**Recomendação:** testar presença real das seções nos derivados, incluindo rota, e rejeitar quebras de página usadas como conteúdo obrigatório.

**Aplicação de A04/A06:** `relatorio-3e/SKILL.md:36` exige cards individuais, quatro campos e distinção entre plano anterior e reconstrução posterior. Conservar essa forma nos cards parciais e mostrar seu estado/versão nos editáveis. Não alterar o compromisso já registrado com o critério original.

## 8. workshop-5c

**Identificado — A03.** `_DESIGN_SYSTEM/contracts/five-c-workshop-record.schema.json:21` aceita C1–C5 dentro de `page_break` com texto e citação. A validação aceita a entrega completa, enquanto o Markdown descarta as cinco sínteses. Reproduzido localmente.

**Recomendação:** impedir que blocos invisíveis cumpram o conteúdo obrigatório e acrescentar um teste com as cinco etapas presentes em tipos inadequados.

**Aplicação de A06:** quando falta presença, regra de voto ou uma etapa, o documento editável precisa mostrar claramente que o registro é parcial, mesmo se o agente não repetir esse aviso no resumo.

Não identifiquei uma nova contradição forte nas instruções de créditos, elegibilidade e distinção entre preferência e validação. Não recomendo reescrever essas regras sem motivo.

## 9. relatorio-5c

**Identificado — A03.** `five-c-report.schema.json:21` aceita o mesmo caso de C1–C5 em blocos descartados. O relatório pode ser aprovado estruturalmente sem entregar as sínteses dessas etapas.

**Recomendação:** corrigir o contrato na fonte compartilhada e testar que as cinco sínteses e suas citações aparecem no arquivo, não apenas no JSON.

**Aplicação de A06:** apresentar a incompletude e a versão em MD/TXT/DOCX. Preservar o tratamento atual de divergências entre ata, votos e decisão formal; a correção não deve fabricar ranking nem resolver conflitos por conveniência.

## 10. experimentacao-inovacao

**Identificado — A11.** `experimentacao-inovacao/references/analise-da-execucao.md:7` proíbe genericamente aprovação formal de um Test Card em estudo qualitativo curto. Entretanto, `references/base-metodologica.md:9` permite avaliar o critério original quando a evidência exigida foi produzida. O exemplo da skill e o eval com três acertos em cinco sessões também exigem dizer se o critério foi atingido.

**Impacto:** o executor pode deixar inconclusivo um critério local previamente definido e efetivamente medido, confundindo sua avaliação com uma conclusão válida para toda a população.

**Recomendação:** esclarecer que se pode declarar atingido/não atingido um critério local sustentado pelo protocolo; isso não aprova escala nem autoriza generalização ou causalidade. Acrescentar um caso fictício em que o critério local foi atingido, mas a expansão ainda não tem suporte. A evidência de ambiguidade é direta; seu efeito em uma execução de modelo não foi medido nesta revisão.

**Identificado — A04.** Reproduzi `test_card` parcial com uma única hipótese aceito por `render.validate`. A skill exige quatro campos também quando os dados são insuficientes. O mesmo caminho de validação genérica alcança Learning Cards parciais.

**Recomendação:** manter os quatro campos e indicar o que falta dentro de cada campo. Isso é diferente do vínculo LC/TC já planejado no 011.

**Aplicação de A06:** estado, ID e versão precisam acompanhar planos/cards em todos os formatos. A regra recente de usar decisões vigentes do 3E está explícita; não a listei novamente como correção pendente.

## 11. scorecard-inovacao

**Identificado — A03.** `_DESIGN_SYSTEM/contracts/innovation-scorecard.schema.json:22` aceita as três seções obrigatórias em `page_break`. Reproduzi validação completa sem texto dessas seções no Markdown.

**Recomendação:** exigir sínteses exibidas e testar que alinhamento/oportunidade, redução de riscos e próximo passo aparecem na entrega. A correção deve preservar a ausência de média geral e de aprovação automática.

**Aplicação de A06:** mostrar data/versão e estado parcial também nos formatos editáveis para que o leitor identifique o retrato recebido.

Não identifiquei nova contradição metodológica forte independente: a adaptação institucional, os estados distintos de evidência e a separação entre opinião, observação e decisão estão coerentes nas referências examinadas. Não há motivo demonstrado para mudar a rubrica nessa revisão.

## Por que os testes atuais não barraram esses casos

`_DESIGN_SYSTEM/tests/test_render.py:342` verifica as seções completas usando apenas `paragraph`; remover uma seção é testado, mas trocar seu tipo por um bloco que descarta texto não é. O teste de paridade do potencial usa inteiros/uma casa e não verifica a transformação das notas retornadas do script. Os testes de IQB não cobrem a evidência nula aceita pela coerção.

As novas regressões devem usar somente fixtures fictícias e ficar fora dos pacotes distribuídos. A leitura semântica pelo modelo continua sendo uma verificação distinta, com custo e autorização próprios.

## Correções compartilhadas e ordem sugerida

1. A01 e A02: corrigir primeiro cálculos/entradas que podem aceitar ou classificar informação de forma errada.
2. A03 e A04: garantir conteúdo exibido e forma mínima dos cards, com cuidado de compatibilidade.
3. A05 e A06: preservar fontes e estado nos formatos que o usuário recebe.
4. A07 e A08: alinhar contratos à quantidade real de achados e ao formato suportado.
5. A09, A10 e A11: alinhar instrumentos de facilitação e esclarecer o alcance das conclusões.

A03, A05 e A06 são alterações na fonte `_DESIGN_SYSTEM/`, seguidas de sync, não onze correções manuais. A04 deve distinguir estrutura mínima de informação ausente: não transformar pendência em conteúdo inventado. As mudanças metodológicas não devem reescrever registros históricos já produzidos.

## Itens já previstos ou rejeitados nesta rodada

- Plano 008: medição de acionamento continua pendente. Não criar outro plano igual nem executar a bateria automaticamente.
- Plano 011: vínculo entre Learning Card e Test Card continua previsto; não duplicado.
- Plano 012: manifesto de fontes e vigência continua previsto; não duplicado.
- Linguagem simples e prioridade das decisões vigentes do 3E: já implementadas; manter e medir comportamento depois, sem propor a mesma alteração novamente.
- Remover cópias para centralizar as skills: rejeitado, pois os pacotes independentes são uma decisão do projeto.
- “Tudo passou nos testes, logo não há falha”: rejeitado; as reproduções locais mostram caminhos não cobertos.
- Reescrever a metodologia do scorecard ou do 5C sem problema comprovado: rejeitado.

Este arquivo é o relatório da auditoria. Após a seleção de todos os achados pelo operador, foram criados os planos 013–023, todos em TODO; consulte o [índice dos planos](README.md) para execução, dependências e cobertura por skill. Nenhuma correção foi implementada nesta etapa.
