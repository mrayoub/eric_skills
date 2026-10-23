# Campos da CDT: o que escrever e de onde tirar

A CDT (Cadastro de Demanda Tecnológica) é o ticket que a área abre no Jira para levar uma demanda à Tecnologia. A
qualidade do conteúdo segue a [publicação interna sobre escopo](publicacao-escopo-tecnologia.md): problema antes
da solução, entregas em três grupos e o checklist antes de envolver a Tecnologia. A estrutura dos campos vem de CDTs
reais preenchidas, observadas em outubro de 2026 e descritas aqui sem nomes, siglas de áreas ou números de ticket.

## Sumário

- [Como o Jira organiza a CDT](#como-o-jira-organiza-a-cdt)
- [Princípios](#princípios)
- [Campos que a área preenche](#campos-que-a-área-preenche)
- [Descrição: as seções da publicação](#descrição-as-seções-da-publicação)
- [Campos que a Tecnologia preenche](#campos-que-a-tecnologia-preenche)
- [Iniciativa (ticket pai)](#iniciativa-ticket-pai)
- [Insumos da esteira por seção](#insumos-da-esteira-por-seção)
- [O que os exemplos ensinam](#o-que-os-exemplos-ensinam)
- [Falhas comuns](#falhas-comuns)

## Como o Jira organiza a CDT

A CDT fica no espaço da central de demandas tecnológicas e tem dois níveis:

- **Iniciativa** (ticket pai): agrupa demandas de um tema do roadmap da gerência. Título no padrão
  `SIGLA_NN-AA | Nome da iniciativa` (sigla da gerência, número e ano). Só é criada quando o projeto não cabe em
  uma iniciativa existente.
- **Demanda** (ticket filho): o pedido concreto. Título curto e descritivo, sem o padrão de sigla. Tem sete abas:
  Informações Gerais, Status da Demanda, Solução, Planejamento, Simplificação do Processo, Dados do Solicitante e
  Histórico (Informações Gerais), além de Anexos.

O padrão desta skill é a **Demanda**. Gere também a Iniciativa quando o usuário disser que ela ainda não existe.

## Princípios

- **Problema antes da solução.** A demanda descreve a necessidade e o resultado esperado. A solução testada na
  esteira entra como referência validada (campo Protótipo e seção de evidências), não como especificação fechada:
  a Tecnologia precisa poder avaliar alternativas mais simples ou recursos que já existem.
- **Leitor de fora da inovação.** Quem lê é a Tecnologia. Não use 4D, 3E, BP1, BP2, Test Card ou IQB sem explicar;
  diga o que o método produziu ("o teste com 8 analistas mostrou...") em vez do nome do método.
- **Pronto para colar.** Cada bloco do entregável corresponde a um campo do Jira, com o nome da aba e do campo no
  título. Em campos de lista do Jira, proponha a opção e justifique; a lista válida é a que aparece no Jira.
- **Nada inventado.** Número com unidade, período e fonte. Hipótese marcada como hipótese. Dado ausente vira
  "a confirmar: [o que falta] (responsável)" e entra em Pendências.
- **Decisões vigentes.** Use o recorte mais recente documentado (em geral o 3E, a experimentação e o relatório
  final). Não reabra o que uma decisão posterior encerrou; registre a origem.

## Campos que a área preenche

Uma CDT completa tem todos os campos obrigatórios, cada um com texto visível e fonte. O título de cada bloco no
entregável é `Aba: campo`, para o usuário achar o lugar no Jira.

| `section_key` | Aba: campo no Jira | Obrigatório | O que escrever |
|---|---|---|---|
| `jira_title` | Título da demanda | sim | Nome curto que diga a mudança, sem jargão ("Pedidos de dados com formulário guiado") |
| `objective` a `change_control` | Informações Gerais: Descrição | sim | As seções da publicação, como subtítulos dentro da Descrição (ver abaixo) |
| `theme` | Informações Gerais: Tema(s) | sim | Opção da lista (nos exemplos: "Aprimoramento Tecnológico"), com justificativa |
| `family_service` | Informações Gerais: Família / Serviços | não | Família de serviço da Tecnologia, se a área souber; senão "a definir com a Tecnologia" |
| `product_area` | Informações Gerais: Produto/Área | não | Produto ou área de negócio afetada |
| `operation_date` | Informações Gerais: Data de operação | não | Data em que a solução precisa estar operando e o motivo (prazo regulatório, ciclo do processo) |
| `regulatory` | Informações Gerais: É uma demanda regulatória? e Ato regulatório | sim | Sim ou Não. Se Sim, o ato (norma, número, data) e o link oficial |
| `risk_if_not_done` | Informações Gerais: Há riscos associados à não implementação? e Justificativa | sim | Sim ou Não e o risco concreto, com efeito e alcance |
| `classification` | Informações Gerais: Classificação da Demanda | não | Opção da lista (nos exemplos: "Demandas") |
| `benefits` | Informações Gerais: Benefícios | sim | Benefícios concretos e mensuráveis, ligados aos resultados esperados |
| `prototype` | Solução: Protótipo | não | O protótipo ou MVP usado na experimentação, onde está e o que ele validou; "Não se aplica nesta fase" se não houver |
| `process_simplification` | Simplificação do Processo | sim | Nível de simplificação (opção da lista, nos exemplos "Alta: simplificação total do processo") com justificativa, e "Há processo atual e/ou futuro desenhado?" (Sim ou Não, citando a jornada do 4D quando houver) |
| `requester` | Dados do Solicitante | sim | Diretoria, perfil, gestor, gerência e gerência executiva de quem abre a CDT |
| `personal_data` | Histórico: Faz uso de dados pessoais ou sensíveis (LGPD)? | sim | Sim ou Não e quais dados, de quem e onde aparecem |
| `attachments` | Anexos | não | Entregáveis da esteira a anexar (relatório final, apresentação, jornada, planilhas de linha de base) |

Além dos campos do Jira, o entregável sempre traz cinco seções que não vão ao Jira e garantem a qualidade e a
veracidade do conteúdo: `readiness` (estado), `publication_checklist` (checklist do comunicado), `quality_review`
(pontos fortes e fracos), `data_to_obtain` (dados a obter) e `traceability` (origem e natureza de cada dado). As
regras estão em [Qualidade e veracidade](qualidade-e-veracidade.md).

## Descrição: as seções da publicação

O campo Descrição é o único texto livre longo da Demanda e é onde a Tecnologia entende a necessidade. Ele reúne as
seções abaixo, nesta ordem, cada uma com o subtítulo em negrito, como "**Objetivo da demanda:**" nos exemplos.
No entregável, cada seção é um bloco com o título `Descrição: ...`; o usuário cola todos no mesmo campo.

| `section_key` | Subtítulo na Descrição | Obrigatório | O que precisa responder | Teste de qualidade |
|---|---|---|---|---|
| `objective` | Objetivo da demanda | sim | Que mudança a área quer obter | Uma frase verificável, ligada ao problema |
| `problem` | Problema e contexto | sim | Qual problema existe, onde aparece, frequência e efeito hoje; norma ou fato que motiva | Lido sozinho, não cita ferramenta como se fosse o problema |
| `audience` | Públicos impactados | sim | Quem sofre o problema e quem será afetado (áreas, perfis, agentes de mercado), com volume | Distingue quem usa, quem opera e quem é afetado indiretamente |
| `current_process` | Como funciona hoje | sim | Passos atuais, sistemas e planilhas, onde ocorre a falha | A Tecnologia desenha o fluxo atual só com este texto |
| `expected_results` | Resultados esperados e indicadores | sim | Indicadores com linha de base, meta, fonte e prazo; o que já foi medido | Separa ganho medido de projetado; projeção tem premissa |
| `scope_essential` | Entregas essenciais | sim | O mínimo para atingir o objetivo | Cada item ligado ao objetivo |
| `scope_important` | Entregas importantes, que podem vir depois | sim | O que agrega valor mas pode esperar | Motivo de poder esperar; "nenhuma" é aceito se registrado |
| `scope_out` | Fora do escopo | sim | O que não será contemplado | Lista explícita, inclusive ideias adiadas |
| `priorities` | Prioridades | sim | Ordem das entregas essenciais e a janela que importa | Justificativa por valor, urgência ou risco |
| `constraints` | Regras, restrições e dependências | sim | Regras de negócio, normas, segurança, integrações, legados, prazos externos, outras áreas | Cada restrição com origem; regra escrita como regra verificável |
| `impacted_systems` | Sistemas impactados | não | Sistemas conhecidos que mudam ou são consultados | Só o que as fontes mostram; o levantamento completo é da Tecnologia |
| `responsibles` | Responsáveis | sim | Quem esclarece dúvidas, quem valida entregas, quem decide mudanças de escopo, patrocinador | Papéis com nome quando houver registro; "responsável a definir" se não houver |
| `evidence` | Evidências | não | O que a esteira testou, com quem, resultado e limite | Número com denominador; contraexemplo relevante não some |
| `alternatives` | Alternativas consideradas | não | Opções comparadas, recursos existentes, rota interna, externa ou híbrida | Rota externa ou híbrida muda o pedido: diga o quê |
| `change_control` | Novas solicitações | não | Quem avalia mudanças e por quais critérios (valor, urgência, impacto em prazo, custo e entregas) | Sem combinado registrado, marque como proposta |

## Campos que a Tecnologia preenche

Não gere conteúdo para estes campos; se o usuário perguntar, diga que são preenchidos pela Tecnologia durante a
análise: Status da Demanda (priorização, etapa, evolução, status, squads), Solução (macro requisito, tipo de
solução, solução, "evita SAB?", tamanho, ordem da família, detalhamento da solução), Planejamento (horas, datas,
encerramento, replanejamento), Histórico (ordem de execução, release, GMO), responsável, analista de negócios,
story points e estimativas. A exceção é o Protótipo, na aba Solução, que a área informa quando a esteira produziu
um.

## Iniciativa (ticket pai)

Gere só quando a iniciativa ainda não existir, em um único bloco `initiative`, com as partes em linhas separadas:

- Título no padrão `SIGLA_NN-AA | Nome`.
- **Descrição do objetivo:** o que a iniciativa assegura e o que abrange.
- **Objetivo estratégico:** eixo do planejamento (nos exemplos, "aprimoramento tecnológico").
- **Benefícios esperados:** lista.
- **Indicadores:** lista, com linha de base e meta quando houver.
- **Categorias:** sigla da gerência e roadmap do ano.

## Insumos da esteira por seção

Use primeiro a versão mais recente e decidida. Os nomes abaixo são os entregáveis das outras skills.

| Seção | Fontes principais | Atenção |
|---|---|---|
| `jira_title`, `objective` | Entrevista Inicial (título, HMW, resultados esperados), Relatório 3E (hipótese e valor) | Reescreva o HMW como objetivo afirmativo |
| `problem` | Entrevista Inicial (problema, relevância), Relatório 4D (diagnóstico do D2), parecer do BP1 | Se o 4D corrigiu o problema, use a versão do 4D e cite a mudança |
| `audience` | Entrevista Inicial, jornada do 4D, Relatório 5C, população da experimentação | Agente de mercado é organização, não pessoa |
| `current_process`, `process_simplification` | Jornada do D2 no 4D, Briefing, linha de base da experimentação | Processo desenhado no 4D responde "Sim" e vai como anexo |
| `expected_results`, `benefits` | Entrevista Inicial, Test Cards, Learning Cards, Relatório final, Potencial (impacto) | Resultado de teste com amostra pequena não é ganho em produção |
| `scope_essential`, `scope_important`, `scope_out` | Relatório 3E (E2: precisa ter, pode evoluir, fora do recorte), avaliação do MVP, Learning Cards | Item reprovado no teste não sobe para essencial |
| `priorities`, `operation_date` | Priorização do D4, Potencial (urgência), Relatório final (decisão e prazo) | Prazo regulatório documentado pesa mais que preferência do sponsor |
| `constraints`, `impacted_systems`, `personal_data` | Barco da inovação do D2, dependências do 3E, viabilidade do relatório final | Separe restrição confirmada de risco suposto |
| `regulatory`, `risk_if_not_done` | Entrevista Inicial (relevância), Potencial (urgência), Relatório final (riscos) | "Sim" só com ato ou risco documentado |
| `responsibles`, `requester` | Entrevista Inicial (responsável e sponsor), Relatório 3E, Relatório final (decisor) | Não atribua papel a quem não aparece nas fontes |
| `prototype`, `evidence`, `alternatives` | Modelo de experimentação (MVP), Apresentação da experimentação, D3 e D4, rota do 3E | Diga o que o protótipo validou e o que não validou |

## O que os exemplos ensinam

- **A Descrição boa dá contexto verificável.** Os exemplos abrem com o objetivo, citam a norma que motiva a demanda
  (número e data), explicam o que muda e, em negrito, o que **não** muda, e listam os sistemas impactados.
- **Benefícios fracos são comuns.** Um exemplo respondeu só "Demanda regulatória." em Benefícios. Escreva
  benefícios concretos, ligados aos resultados esperados, mesmo em demanda regulatória.
- **Indicadores sem linha de base.** Os indicadores da iniciativa de exemplo não têm valor atual nem meta. Inclua
  ambos quando a esteira mediu; senão, marque "linha de base a levantar".
- **Ato regulatório com link oficial** e a pergunta de risco com justificativa curta e concreta ("não adesão de
  novos agentes") ajudam a priorização.
- **Anexos carregam o detalhe.** Os exemplos anexam tabelas e relatórios; a Descrição remete a eles.

## Falhas comuns

- Abrir a Descrição pela solução ("criar um sistema que...") sem explicar o problema.
- Copiar o jargão da esteira: "o D4 priorizou a alternativa 2" não diz nada à Tecnologia.
- Pôr tudo como essencial. Se tudo é essencial, a Tecnologia não consegue dimensionar uma primeira entrega.
- Apresentar resultado de teste ou de protótipo como ganho garantido em produção.
- Omitir "fora do escopo", o que abre espaço para pedidos novos sem avaliação.
- Responder "Sim" em demanda regulatória ou em risco sem a norma ou o risco documentado.
- Restrição genérica ("seguir a LGPD") sem dizer quais dados pessoais existem e onde.
- Preencher campos da Tecnologia (tamanho, squad, horas): isso não cabe à área.
