# Revisão e validação das skills — 28 set 2026

## Resultado

As **11 skills** passam na validação estrutural do skill-creator. Os links locais dos SKILL.md e das referências metodológicas resolvem. Os **19 schemas compartilhados** têm sintaxe válida, e os **18 inputs de amostra** passam na validação dos respectivos contratos. As 11 cópias do design system correspondem à fonte de manutenção. Os cinco testes existentes do renderizador passaram.

Esses resultados comprovam estrutura e o comportamento coberto pelos testes; não certificam aprovação institucional das fontes nem todas as propriedades semânticas dos entregáveis. A auditoria identificou quatro falhas executáveis descritas abaixo, que permanecem pendentes.

## Cobertura por skill e fonte disponível

| Skill | Validação estrutural | Fonte metodológica disponível | Situação da origem |
| --- | --- | --- | --- |
| briefing-inovacao | Passou | Modelo Markdown de sete campos extraído do RC6; DOCX histórico localizado em ERIC_v4 | Confirmar se o modelo histórico continua vigente e se há roteiro oficial adicional. |
| avaliacao-briefing-iqb | Passou | Rubrica Markdown de 40 itens e calculador local | Fonte RC6 disponível; falta confirmar norma institucional aprovada e vigência. |
| potencial-inovacao | Passou | Rubrica Markdown de cinco critérios, pesos e faixas; calculador local | Fonte RC6 disponível; falta confirmar norma institucional e calibração das notas. |
| workshop-4d | Passou | DOCX fornecido, transcrição integral, playbook adaptado e original histórico RC6 | Fonte primária importada nesta revisão; versão textual “3h”, sem autor/data de aprovação no documento. |
| relatorio-4d | Passou | Mesmas fontes 4D, referência visual e guia de cards | Fonte primária importada; conteúdo de relatório depende dos registros do encontro. |
| workshop-3e | Passou | DOCX fornecido, transcrição integral, playbook adaptado e original histórico RC6 | Fonte primária importada; adaptação dos cards Strategyzer explicitada. |
| relatorio-3e | Passou | Mesmas fontes 3E e template local de Test Card | Fonte primária importada; original não constitui evidência de execução. |
| workshop-5c | Passou | DOCX original e transcrição integral, método adaptado | Fonte é um encontro de Centralidade no Cliente; participantes e serviço não são requisitos universais. |
| relatorio-5c | Passou | Mesmas fontes 5C | Mesma delimitação; relatório precisa dos registros de uma execução. |
| experimentacao-inovacao | Passou | PDFs oficiais Test/Learning Card, referências primárias de métodos, protocolo think aloud | Fontes rastreadas localmente; método selecionado pela hipótese, sem restringir à interface. |
| scorecard-inovacao | Passou | PDF oficial Strategyzer, estrutura/adaptação e extração documental | Instrumento oficial preservado; adaptação institucional identificada como própria. |

O contexto ERIC incluído nas 11 skills é idêntico e descreve a Esteira Robusta de Inovação Colaborativa. Seu texto registra que parte das especificações RC6 está em draft: confirmar documentação institucional vigente continua relevante.

## Originais e transcrições

Os DOCX 4D e 3E foram importados para suas duas skills, preservando os arquivos byte a byte. As cópias históricas RC6 permanecem separadas. As transcrições mantêm o texto e a ordem dos parágrafos e tabelas; marcadores automáticos de listas são representados em Markdown, e o DOCX preserva a aparência original.

| Fonte | Conteúdo textual conferido | Tabelas | SHA-256 do DOCX |
| --- | --- | --- | --- |
| Modelo 4D de Aprofundamento.docx | 137 parágrafos não vazios, incluindo células | 1 | `d5071f2ab0d62e153b8f0bb7e89108a10bca6980d807dbd43c90bbd80fd115e3` |
| Modelo 3E Estruturação da Solução.docx | 111 parágrafos não vazios, incluindo células | 1 | `530cc4691c6cf5b5f093ba972b05d08649b4000a1fd077ee6020c94b00637e34` |
| Playbook_Modelo_5C_Centralidade_Cliente.docx | 171 parágrafos não vazios, incluindo células | 3 | `3b793187dccd6691e124e61b9a407e6f383513d55de255c1049deae31df4e3c7` |

A transcrição integral do 5C já existia em ambas as skills. Nesta revisão, seu conteúdo foi confrontado integralmente com o DOCX e recebeu o hash da fonte e o registro da conferência.

### Divergências resolvidas ou explicitadas

- **4D:** o DOCX confirma 10 créditos por participante, distribuição livre e Ventos / Âncoras / Icebergs / Porto. O blueprint Mural usava três notas de R$100 e outros rótulos; foi alinhado à fonte para novas execuções. As regras realmente executadas em encontros passados devem continuar registradas como ocorreram.
- **3E:** o DOCX contém um Test Card simplificado (“Acreditamos que / Vamos testar com / Durante / Teremos sucesso se”). As skills adotam, por orientação do usuário, hipótese / teste / medida / critério da Strategyzer. O documento de comparação explicita essa adaptação. Planejar Learning Cards não autoriza preenchê-los com resultados futuros.
- **Agendas:** os originais têm intervalos e campos não fechados. O 3E contém “x min”; o 5C tem duração declarada que não coincide com todos os intervalos. As transcrições preservam essas lacunas.

## Grilling incorporado às 11 skills

Cada SKILL.md passa a exigir `references/grilling-operacional.md`, incorporado localmente. O protocolo une questionamento crítico dos arquivos e entrevista por fronteiras. Mantém origem/localizador, dependências, estados, respostas e efeitos na entrega. Distingue fatos pesquisáveis de decisões humanas; não pergunta pela nota ou conclusão desejada. Fontes novas e respostas reabrem ramos contraditórios. Pergunta enviada, opção preselecionada e silêncio não contam como resposta.

A base é a árvore/fronteira de grilling de Matt Pocock e a documentação de termos/decisões de grill-with-docs e domain-modeling. A extração e avaliação de evidência são adaptações explícitas para estas skills. O uso não exige outras skills ou uma ferramenta de perguntas específica.

### Ensaios comportamentais independentes

Foram usados dois casos fictícios, com arquivos fornecidos diretamente ao agente avaliador e sem fornecer a resposta esperada:

1. **Briefing com lacunas:** o agente leu os três arquivos, calculou 24/120 = 20%, manteve a sugestão de 30% como não aprovada e perguntou pelo sponsor ausente. Após a resposta, registrou a origem humana e abriu a pergunta dependente sobre acompanhamento. Ao receber a instrução de concluir parcialmente com o prazo indefinido, preservou a pendência e encerrou a rodada. A primeira pergunta também pediu cargo, embora opcional; o protocolo foi reforçado para evitar converter metadados opcionais em bloqueios.
2. **Experimentação com resumo conflitante:** o agente examinou plano, planilha e notas. Reconheceu três conclusões sem orientação em cinco participantes, em vez de cinco; preservou as duas conclusões assistidas no denominador; marcou o critério original 4/5 como não atingido; rejeitou economia de tempo não medida e produziu os quatro campos do Learning Card. Não pediu perguntas humanas artificiais, pois o material bastava para a finalidade solicitada. Não declarou vídeos examinados nem tratou a citação de um resumo como leitura do original.

Os ensaios verificam leitura e interação em cenários concretos. Não equivalem a teste em todas as LLMs, a uma pesquisa com participantes reais ou a garantia absoluta de execução futura.

## Falhas técnicas encontradas — pendentes

| ID | Evidência | Consequência | Esforço / risco / confiança |
| --- | --- | --- | --- |
| T01 | `_DESIGN_SYSTEM/scripts/render.py`, função `table_rows`, linhas 128–135 | Nos derivados do IQB, a conversão das dimensões conserva as 40 respostas, mas omite contagens, notas brutas/finais, detalhes de veto, auditoria de agrupamento e citações por critério presentes naquele bloco JSON. A equivalência semântica fica incompleta. | M / baixo / alta |
| T02 | `_DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json` e `scripts/render.py`, validação | O schema aceita nota, classe e itens matematicamente incoerentes: por exemplo, IQB 1 com classe Excelente; critérios repetidos; notas incompatíveis com veto; referência interna inexistente. O calculador IQB é mais rigoroso, mas o renderizador não reconcilia sua saída. | M / médio / alta |
| T03 | `_DESIGN_SYSTEM/scripts/render.py`, linhas 136–146 | Ao usar colunas como `{key, label}` e linhas como objetos, o rótulo é usado para buscar a chave. Valores válidos podem virar células vazias. | S / baixo / alta |
| T04 | `potencial-inovacao/scripts/score.py`, linhas 55–64 e 89–93; schema de potencial | O calculador aceita booleanos como notas e declara avaliação completa sem justificativa. O schema também permite uma avaliação completa sem as cinco notas, pesos, total e classe estruturados. | M / médio / alta |

O núcleo aritmético do IQB e os pesos/faixas do potencial correspondem às rubricas locais. Os problemas acima são de enforcement e preservação dos dados; não autorizam concluir que as normas institucionais estão erradas. A origem institucional e a vigência ainda dependem dos materiais solicitados.

## Insumos ainda solicitados ao usuário

1. Confirmar se o DOCX histórico `ERIC_v4/static/doc/briefing_template.docx` continua sendo o modelo oficial das sete perguntas. Se existir roteiro oficial adicional ou versão mais recente, informar caminho/anexo.
2. Fornecer, quando disponíveis, as normas aprovadas do IQB, potencial de inovação e esteira ERIC, com versão/data ou responsável institucional.
3. Para os DOCX 4D/3E recém-fornecidos, informar apenas se houver metadados de aprovação, revisão ou autoria fora do documento. A ausência deles não impede preservar e usar a fonte fornecida, mas impede afirmar sua aprovação institucional.

Os originais DOCX 4D e 3E já foram fornecidos e não precisam ser solicitados novamente. O DOCX 5C também está disponível e integralmente transcrito.

## Escopo e limites da revisão

Foram examinados os 11 SKILL.md, referências metodológicas e suas fontes locais, links, bundles, schemas e amostras, os cálculos principais e as falhas executáveis acima. Não foi feito teste de todos os formatos em todas as aplicações Office ou de execução comportamental de cada skill em cada provedor de LLM. A inspeção dos projetos RC5/RC6 foi dirigida à proveniência documental; não foi auditoria de seus aplicativos. Nenhuma dependência de execução em `/private/tmp` foi adicionada às skills; a pasta foi usada somente como área de trabalho da revisão.
