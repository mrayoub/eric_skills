# Campos do formulário da CDT no Jira

Levantamento campo a campo do formulário de criação da CDT (Cadastro de Demanda Tecnológica), feito a partir de prints
do Jira em 23/10/2026. Registra rótulo, tipo, opções e a regra de preenchimento de cada campo. As opções das listas
também estão em `assets/design-system/scripts/validators/cdt_options.json`, que o checador usa.

Rótulos e opções estão grafados exatamente como no Jira, inclusive erros ("Tranversal", "Sansões",
"Penalidadades", "encarramento"), acentos ausentes e hífens com espaços. Quem procura a opção na tela precisa achá-la
pelo mesmo texto. Essas grafias são exceção às regras de linguagem dos entregáveis.

## Sumário

- [Regras gerais](#regras-gerais)
- [Padrão de escrita](#padrão-de-escrita)
- [Formato de cada campo no entregável](#formato-de-cada-campo-no-entregável)
- [Descrição](#descrição)
- [Aba Informações Gerais](#aba-informações-gerais)
- [Aba Benefícios da Demanda](#aba-benefícios-da-demanda)
- [Coerência entre campos](#coerência-entre-campos)
- [Lista: Processo e Sub-processo Tranversal](#lista-processo-e-sub-processo-tranversal)
- [Lista: Família / Serviços](#lista-família--serviços)
- [Fora do Jira: checklist do comunicado](#fora-do-jira-checklist-do-comunicado)
- [Insumos da esteira](#insumos-da-esteira)
- [Lições do exemplo real](#lições-do-exemplo-real)

## Regras gerais

- A saída segue as abas do Jira, um bloco por aba, com os campos na ordem da tela.
- Nenhum valor sem base no material. Sem dado, o campo leva "a confirmar: [dado que falta]" e o dado vai para os
  dados a obter. Nada é deduzido pelo assunto.
- Cada coisa é escrita num lugar só: um número ou argumento não se repete entre Descrição, Benefícios e Justificativa.
- Campos de texto curtos: até 3 linhas, no máximo 60 palavras, sem adjetivos vazios ("mais agilidade", "maior
  eficiência") sem número ao lado.
- Campos de Sim ou Não: Sim só com evidência citada; a linha que sustenta o Sim vai no campo de texto que faz par com
  ele.
- **Sem fonte no que vai ao Jira.** O Jira não tem como referenciar fontes: os campos não trazem "Fonte:", códigos de
  citação nem nome de documento como prova. As fontes ficam fora do Jira, na tabela Origem dos dados, campo a campo.
  O checador recusa "Fonte:" nos campos do Jira, e os arquivos gerados não mostram as citações desses campos.
- A skill preenche só os 28 campos das abas Informações Gerais e Benefícios da Demanda listados aqui. Os demais
  campos que aparecem no Jira (Status da Demanda, Planejamento, Simplificação do Processo como aba, Dados do
  Solicitante, Histórico, Responsável, Relator, Analista de Negócios, Story Points, vínculos entre tickets) ficam de
  fora.

## Padrão de escrita

O padrão vem de uma CDT real bem avaliada: texto institucional, curto e direto, que o leitor da Tecnologia entende
sem conhecer a esteira.

- **Descrição em Markdown.** Só a Descrição usa formatação: parágrafos curtos, rótulos em negrito no início da linha
  (`**Objetivo:**`, `**Onde falha:**`), listas com marcador e grupos numerados quando o escopo tem blocos.
- **Demais campos em texto simples.** Sem marcador, negrito, título ou link; um item por linha. O checador recusa
  Markdown fora da Descrição.
- **Justificativa:** um risco por linha, aberto pelo nome do risco e dois-pontos ("Retrabalho contínuo: ...").
- **Frases curtas, sem jargão da esteira** (4D, 3E, BP2, Test Card) e sem narrar o método. Siglas por extenso na
  primeira menção de cada campo, porque cada campo é lido isolado.
- **Natureza do dado no texto, sem rodeio:** "estimativa", "meta proposta", "medido no piloto com 8 analistas",
  "aprovado em 20/10/2026".

## Formato de cada campo no entregável

Cada campo é um bloco com o título `Aba: Rótulo` (a Descrição usa `Descrição: <pergunta>`). Dentro do bloco:

| Tipo de campo | Primeira linha | Linhas seguintes |
|---|---|---|
| Lista de opção única | A opção exata do Jira | `Motivo: ...` em uma linha |
| Lista em dois níveis | `Opção / Segundo nível` ou `Opção / selecionar no Jira` | `Motivo: ...` |
| Tema(s) | Até 2 opções separadas por `; ` | `Motivo: ...` |
| Sim ou Não | `Sim` ou `Não` | A linha que sustenta a resposta, quando houver |
| Texto livre | O texto que vai ao Jira | |
| Campo que a skill não preenche | `Deixar vazio: <motivo>`, `Selecionar no Jira.` ou `Escolher no Jira.` | |
| Dado faltando | `a confirmar: <dado> (<com quem>)` | O dado entra nos dados a obter |

O que vai ao Jira é a primeira linha (nos campos de lista e de Sim ou Não) ou o texto inteiro (nos campos de texto).
A linha `Motivo:` orienta quem preenche e não é colada.

## Descrição

Fica na aba Informações Gerais. Responde às cinco perguntas de "Comece pelo problema" da
[publicação sobre escopo](publicacao-escopo-tecnologia.md), uma seção por pergunta, nesta ordem, e nada além delas:

1. Qual problema queremos resolver?
2. Quem é impactado?
3. Como o processo funciona hoje?
4. Qual resultado esperamos alcançar?
5. O que é prioridade neste momento? Separa as entregas em essencial, importante (pode vir depois) e fora do escopo.

As cinco perguntas são obrigatórias em qualquer versão, inclusive na parcial: com dado faltando, a seção responde o
que o material sustenta e marca "a confirmar:". Cada seção tem até 150 palavras.

O que saiu da Descrição e foi para campos próprios:

| Item | Para onde vai |
|---|---|
| Como vamos medir o resultado | Benefícios mensuráveis e Benefícios |
| Risco de não implementar | Justificativa |
| Riscos da Matriz de Riscos Corporativos | Identificação dos Riscos |
| Incidentes registrados | Identificação de Incidentes de Processo |
| Ato da ANEEL, MME ou CNPE | Ato regulatório e Qual Ato formal |
| Regras, restrições e dependências | Checklist do comunicado, fora do Jira |
| Responsáveis | Checklist do comunicado, fora do Jira |

## Aba Informações Gerais

| # | Rótulo | Tipo | Regra |
|---|---|---|---|
| 1 | Descrição | texto longo | Ver [Descrição](#descrição). |
| 2 | Rótulo Epic | texto livre | É o título do ticket. A skill sugere: o que a demanda é e onde atua, em até 12 palavras (ex.: "Assistente conversacional para consulta de pendências no sistema X"). |
| 3 | Processo e Sub-processo Tranversal | lista em dois níveis, um par | Ver regra abaixo e a [lista](#lista-processo-e-sub-processo-tranversal). |
| 4 | Família / Serviços | lista em dois níveis, um par | Ver regra abaixo e a [lista](#lista-família--serviços). |
| 5 | Produto/Área | lista, opção única | Estratégica; Gestão de Mercado; Inovação e Novos Negócios; Operação de Mercado; Segurança de Mercado; Tecnologia de mercado. Não obrigatório. |
| 6 | Área Responsável pelo Atendimento | lista, opção única | "a definir pela Tecnologia", salvo indicação clara no material. |
| 7 | Release | etiqueta | A skill não sugere: as etiquetas são muitas e mudam. Saída: "selecionar no Jira". |
| 8 | Anexo | arquivos | Ver regra abaixo. |
| 9 | É uma demanda regulatória? | Sim ou Não | Sim só quando a demanda vem da ANEEL, do MME ou do CNPE, com o ato citado. |
| 10 | Data de operação | data ("22 de out. de 2026") | Fica vazio na abertura e é preenchido depois. Saída: "deixar vazio". Um prazo com motivo (vigência de ato, contrato, leilão) vai na Descrição, pergunta 5. |
| 11 | Ato regulatório | texto livre | Só com demanda da ANEEL, MME ou CNPE. Uma linha por ato publicado: `Tipo e número/ano, órgão: o que exige. Vigência: data.` |
| 12 | Tema(s) | lista, várias opções | Ver regra abaixo. |
| 13 | Benefícios mensuráveis | lista, opção única | Ver regra abaixo. |
| 14 | Benefícios | texto livre | Primeira linha quantifica o campo 13: `hoje, meta, unidade e período`, com a natureza do dado (medido, meta proposta) Até dois benefícios secundários. |
| 15 | Simplificação do Processo | lista, opção única | Alta: simplificação Total do processo; Média: simplificação parcial do processo; Baixa: nenhuma simplificação do processo. Justificar contando etapas antes e depois. Baixa não é nota ruim. |
| 16 | Há processo atual e/ou futuro desenhado? | Sim ou Não | Sim só com desenho (fluxograma, BPMN, jornada do D2, blueprint), que entra nos anexos. Texto não conta. |
| 17 | Há riscos associados a não implementação da demanda? | Sim ou Não | Sim só com risco concreto: multa, prazo regulatório, falha com histórico, segurança ou dados, perda de cliente identificado. Ineficiência não é risco. |
| 18 | Justificativa | texto livre | Descreve os riscos de não implementar (campo 17), um por linha, aberto pelo nome do risco, com a consequência. |

No entregável, o Rótulo Epic (título) vem primeiro e a Descrição logo depois, seguidos dos demais campos na ordem da tela.

**Processo e Família.** A skill sugere sempre o primeiro nível, com uma linha de justificativa, e o segundo nível
quando o material permitir; nos outros casos, "selecionar no Jira o subprocesso (ou serviço) de X". O processo e a
família contam a mesma história. Demanda que melhora um serviço prestado ao mercado usa a família desse serviço;
ferramenta interna usa "Não se aplica" com o tipo de sistema. Sem subprocesso exato, a skill escolhe o mais próximo do
resultado da demanda, não da área que a pede, e marca "a confirmar com a Tecnologia". "Desenvolvimento de novas
atribuições" só quando a demanda cria uma atribuição nova para a CCEE.

**Área Responsável pelo Atendimento.** 11 opções ou mais: o aplicativo institucional, uma fábrica de software de
fornecedor externo e as siglas das gerências da Tecnologia. A lista não é transcrita aqui (siglas de áreas e nome de
fornecedor ficam fora do repositório); a pessoa escolhe no Jira.

**Anexo.** O Jira não informa limite. Por concisão, a skill sugere no máximo 5 arquivos, versões finais, de preferência em PDF. Ordem de prioridade: registro
da decisão da gestão; relatório final ou apresentação executiva; relatório da experimentação ou Learning Cards;
Relatório 3E; Relatório 4D; Relatório 5C; Briefing; imagem do protótipo; proposta de fornecedor, quando houver. Nada
com dado pessoal sem tratamento (transcrições, gravações, murais com nomes, planilhas brutas). Uma linha por arquivo, em texto
simples: `Nome do documento: o que ele comprova.`

**Tema(s).** Opções: Abertura de Mercado; Academia CCEE; Aprimoramento Tecnológico; Evolução das Operações de
Mercado; Governança e Gestão; Integração de Sistemas e Inteligência Artificial; Segurança de Mercado. O tema sai do
problema e do resultado, não da tecnologia da solução. "Aprimoramento Tecnológico" só quando nenhum outro descreve o
resultado. No máximo 2 temas, cada um com uma linha de justificativa.

**Benefícios mensuráveis.** Opções: Benefícios direto aos Agentes que podem ser medidos; Contribuição para
atendimento de um indicador estratégico; Elimina risco de penalidade ou multa para a CCEE; Novas receitas para a CCEE;
Reduz custo da CCEE; Reduz horas operacionais internas. Uma opção, a de maior peso comprovado, com número no material.
Indicador estratégico exige nome e meta; receita e custo exigem estimativa em reais e origem.

## Aba Benefícios da Demanda

| # | Rótulo | Tipo | Regra |
|---|---|---|---|
| 1 | Qual a origem da demanda? | lista, opção única | Ver regra abaixo. |
| 2 | Qual Ato formal publicado ou não por órgão do setor (ANEEL/MME/CNPE)? | texto livre | Só com demanda da ANEEL, MME ou CNPE. Repete os atos publicados do campo Ato regulatório e acrescenta os não publicados (ofício, despacho, consulta pública), com a situação no início da linha. |
| 3 | Há benefícios para os Agentes? | Sim ou Não | Sim só com ganho direto e observável, nomeando o agente; a linha do ganho vai abaixo do Sim. Ganho indireto leva a Não. |
| 4 | Grau de impacto no mercado | lista, opção única | 1 Classe de Agente; 2 Classes de Agente; 3 Classes de Agente; 4 Classes de Agente. Nomear as classes ao lado. Demanda interna: vazio. |
| 5 | Frequência de utilização | lista, opção única | Anual; Menor que mensal; Mensal; Sob demanda; Não sei opinar. Sai da frequência do processo atual, com o número real ao lado. "Não sei opinar" é último recurso. |
| 6 | Reduz custo de transação do agente? | Sim ou Não | Sim só quando o agente gasta menos para cumprir o que faz com a CCEE. Informação nova não é custo de transação. |
| 7 | Reduz risco identificado na Matriz de Riscos Corporativos? | Sim ou Não | Sim só com risco da Matriz citado no material ou confirmado pela área de riscos. Risco do projeto não basta. A skill não guarda a Matriz. |
| 8 | Identificação dos Riscos | texto livre | Só riscos da Matriz, até 3: `[código ou nome]: como a demanda reduz o risco.` Vazio se o campo 7 for Não. |
| 9 | Resolve Incidentes de Processo Registrados no Processo Transversal? | Sim ou Não | Sim só com incidentes registrados formalmente no processo do campo 3 de Informações Gerais. Relato em entrevista não conta. |
| 10 | Identificação de Incidentes de Processo | texto livre | `[quantidade] incidentes em [período], no processo [X]: [tipo de falha].` Até 5 códigos. Sem nomes de pessoas. |
| 11 | Frequência de utilização (escala de 1 a 10) | lista, 1 a 10 | Sempre vazio na saída, com o aviso "escolher no Jira". |

**Qual a origem da demanda?** Opções: Backlog de Projeto; Proposta interna da CCEE; Regulatório; Solicitações de
órgãos externos (ANEEL/ONS/ MME/ EPE); Solicitações dos Clientes. Projetos da esteira ERIC costumam ser "Proposta
interna da CCEE". "Solicitações dos Clientes" só com pedido registrado de agentes. "Regulatório" com norma publicada;
"Solicitações de órgãos externos" com pedido formal sem norma. Pedido do ONS ou da EPE entra aqui, mas os campos de
ato ficam vazios. "Backlog de Projeto" exige nome ou chave do projeto.

**"Menor que mensal"** quer dizer intervalo menor que um mês: uso diário ou semanal. Uso trimestral ou semestral não
tem opção própria: a skill marca "Anual" e escreve a frequência real ao lado, por exemplo "Anual (uso trimestral)".

## Coerência entre campos

A skill aponta na avaliação qualquer combinação incoerente:

- Regulatória Sim exige ato nos dois campos de ato.
- "Elimina risco de penalidade ou multa" exige Sim em riscos de não implementar.
- "Benefícios direto aos Agentes" exige Sim em Há benefícios para os Agentes.
- Reduz custo de transação Sim exige Sim em Há benefícios para os Agentes e ao menos uma classe de agente.
- "Reduz horas operacionais internas" dificilmente combina com Simplificação Baixa.
- Origem "Solicitações dos Clientes" quase sempre leva a Sim em Há benefícios para os Agentes.
- Incidentes precisam ser do processo marcado em Processo e Sub-processo Tranversal.
- Ganho em horas por mês precisa de frequência compatível.

## Lista: Processo e Sub-processo Tranversal

| Processo | Subprocessos |
|---|---|
| Atender Mercado | Emitir certidão de adimplemento; Gerir Chamados Ativos; Gerir Chamados Receptivos |
| Capacitar Mercado | Realizar capacitação |
| Contabilizar e Liquidar MCP | Apurar desconto; Gerir equacionamento dos débitos; Processar e liquidar MCP |
| Contabilizar e Liquidar Mercado Regulado | Constrained-Off Eólicas - ACR; Constrained-Off Solar - ACR; Gerir Angra I e II; Gerir Cotas de garantia física; Gerir Energia de Reserva; Gerir MCSD (mensal, trocas livres e 4%); Gerir MCSD de Energia Nova; Gerir MCSD escalonado; Gerir Mecanismo de Venda de Excedentes (MVE); Gerir MVE; Gerir RRV |
| Gerir Contas Setoriais | Conta ACR; Conta CCC; Conta CDE; Conta RGR; Gerir conta centralizadora das Bandeiras (Conta Bandeiras); Gerir processos de operacionalização comuns às contas CCC, CDE e RGR; Gerir processos de operacionalização comuns às contas CCC, CDE, RGR |
| Gerir contratos provenientes dos leilões | Gerir termos de cessão; Realizar confecção de contratos de garantia para regimes de cotas; Realizar Manutenção de Contratos ACR; Realizar manutenção de dados bancário e/ou anuência de direitos creditórios CER; Registrar Contratos ACR |
| Gerir Habilitação Técnica e Comercial | Gerir encarramento de representado; Gerir encerramento do representado; Habilitar representado do varejista; Habilitar varejista; Realizar Desativação comercial e técnica; Realizar habilitação comercial; Realizar habilitação técnica; Realizar manutenção comercial e técnica; Realizar portabilidade |
| Gerir Leilões | Realizar leilão; Gerir garantias de leilão |
| Gerir Recontabilizações | Gerir recontabilizações |
| Gerir Regras e Procedimentos de comercialização | Gerir Procedimentos de Comercialização; Gerir Regras de Comercialização |
| Monitorar e aplicar sanções de Mercado | Desligar comercializador varejista; Gerir Desligamento; Monitorar Mercado; Processar, Administrar e Liquidar Penalidadades |
| Processos de apoio | Apoio ao CAD; Compras e Contratações; Contabilidade; Desenvolvimento de Pessoas; Finanças; Infraestrutura; Jurídico; Relações Institucionais |
| Processos de gestão | Desenvolvimento de novas atribuições; Gestão da Qualidade; Gestão de conformidade e riscos; Planejamento Estratégico |
| Prover Informações ao Mercado | Calcular Preço e CVU; Disponibilizar informações ao Mercado; Gerir DRI |
| Viabilizar Dados para o MCP e Mercado Regulado | Administrar Cotas do Proinfa; Cadastrar Demais Dados e Parametros; Calcular fatores anuais de performance do ativo; Coletar Dados de Energia; Gerir Exportação; Gerir liminares; Importar Encargos e demais parametros do ONS; Incluir participante no programa de resposta à demanda; Inserir alivio de exposição; Manutenção de contratos CBR; Processar MCSD Ex Post; Realizar alocação de geração própria; Realizar contratação ACR; Realizar contratação bilateral (ACL e CBR); Realizar manutenção dos participantes do programa de resposta à demanda; Sazonalizar Garantia Fisica |

Opções duplicadas: a skill usa a versão por extenso e sem erro ("Gerir Mecanismo de Venda de Excedentes (MVE)",
"... CCC, CDE e RGR", "Gerir encerramento do representado") e não usa a outra.

## Lista: Família / Serviços

| Família | Serviços |
|---|---|
| Adesão | Adesão à CCEE |
| Certificação de Energia | Certificação de Energia Renovável |
| Desligamento | Desligamento Compulsório; Desligamento por Descumprimento; Desligamento Voluntário; Penalidades |
| Gestão de Pagamentos | Certidão de Adimplemento; Contribuição Associativa; Débitos em Aberto |
| Gestão Pré Operações | Alteração de Propriedade; Gestão dos Dados de Medição do SIN; Gestão Varejista; Inclusão de Usinas e Cargas do Portfolio; Manutenção Cadastral; Manutenção de Ativos; Manutenção do Comercializador; Manutenção dos Contratos CCEAR; Registro e Ajustes de Contrato; Retirada de Usinas e Cargas do Portfolio; Sazonalização da Garantia Física |
| Informações aos Clientes | Disponibilizar dados históricos sob demanda; Info CCEE |
| Leilões | Leilões; Gestão de Garantias dos Leilões |
| Monitoramento e Segurança | Monitoramento Aleatório; Monitoramento Prudencial; Sansões |
| Não se aplica | Aplicativo; Corporativo; Estratégico; Plataforma de integração; Tecnologia de mercado; Não se aplica |
| Operações de Comercialização MCP | Alocação de Geração Própria; Apuração de multa por falta de combustível; Apuração do Desconto na TUSD/TUST; Exportação; Importação; Lastro de Energia; Mercado de Curto Prazo; Recontabilização; Resposta de Demanda |
| Operações de Comercialização Mercado Regulado | Cotas Angra; Cotas de Garantia Física; Energia de Reserva; MCSD Energia Existente; MCSD Energia Nova; Mecanismo de Venda de Excedentes; Proinfa; Receita de Venda de CCEAR; Reserva de Capacidade |
| Operações de Contas Setoriais | Bandeiras Tarifárias; Conta de Consumo de Combustíveis; Conta de Desenvolvimento Energético - Pagamentos; Conta de Desenvolvimento Energético - Recebimentos; Gestão da Conta Escassez Hídrica; Prêmio de Risco; Reserva Global de Reversão |
| PLD - Preço de Liquidação das Diferenças | Boletins (InfoPLD e InfoBandeiraTarifária); CT PMO/PLD (Comitê Técnico do PMO/PLD); Cálculo e Publicação do PLD; Encontro do PLD; Projeção do PLD, GSF, encargos e cenários energéticos; Reajuste do CVU |
| Relacionamento | Atendimento Especial; Atendimento Personalizado; Ouvidoria |
| Serviços Internos | Preparação para Reuniões dos Colegiados |
| Treinamento e Capacitação | Certificado Operador de Mercado de Energia Elétrica; Treinamento In Company; Treinamento Online |

## Fora do Jira: checklist do comunicado

O entregável tem duas partes: o conteúdo para colar no Jira, campo a campo, e uma parte fora do Jira. Na parte fora do
Jira, a skill responde ao "Checklist antes de envolver a Tecnologia" da
[publicação sobre escopo](publicacao-escopo-tecnologia.md), um item por linha, com a resposta curta:

| Item do checklist | Onde a resposta aparece |
|---|---|
| O problema e o objetivo do projeto | Descrição, perguntas 1 e 4 (remeter) |
| Os públicos impactados | Descrição, pergunta 2 (remeter) |
| As entregas essenciais | Descrição, pergunta 5 (remeter) |
| As prioridades e os resultados esperados | Descrição, perguntas 4 e 5 (remeter) |
| As regras, restrições e dependências | Só aqui: as regras, restrições e dependências, separadas por ponto e vírgula |
| Os responsáveis por esclarecer dúvidas e validar decisões | Só aqui: papel e área de cada responsável |

Os itens já respondidos na Descrição só remetem a ela, sem repetir o texto. Item sem resposta no material fica "a
obter" e entra nos dados a obter. Nada desta parte é colado no Jira.

## Insumos da esteira

Use a decisão mais recente documentada; não reabra o que ela encerrou.

| Campo | Fontes principais |
|---|---|
| Problema, resultado esperado | Entrevista Inicial, Briefing, Relatório 4D (diagnóstico), Relatório final, decisão de gestão |
| Quem é impactado, processo atual | Entrevista Inicial, jornada do 4D, Relatório 5C, população da experimentação |
| Prioridade | Relatório 3E (precisa ter, pode evoluir, fora do recorte), Learning Cards, avaliação do MVP |
| Benefícios, frequência | Test Cards (medida e critério), Learning Cards, Relatório final |
| Riscos, regras, dependências | Barco da inovação do 4D, dependências do 3E, viabilidade do Relatório final |
| Responsáveis | Entrevista Inicial (responsável e sponsor), Relatório final (decisor), resposta do usuário |

Item reprovado ou não testado não sobe para essencial. Resultado de teste com protótipo não é ganho em produção.

## Lições do exemplo real

Uma CDT real de demanda vinda da esteira (assistente conversacional para consulta e orientação num sistema da CCEE)
foi analisada; nomes, fornecedor e números foram retirados. O que copiar: título que diz o que a demanda é e onde
atua; problema contado pelo usuário; escopo agrupado em blocos; experimentação citada e anexada. O que evitar: campo
Benefícios sem nenhum número apesar de "que podem ser medidos"; o mesmo parágrafo repetido na Descrição, na
Justificativa e em Benefícios; Descrição sem o processo atual, sem quem é impactado com precisão e sem o que está fora
do escopo.
