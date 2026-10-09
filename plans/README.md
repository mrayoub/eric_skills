# Planos de implementação — skills de inovação

Gerados pela skill `improve` em 2026-09-28, contra o commit `967749d` (tag
`improve-baseline-2026-09-28`). Base: auditoria das 11 skills e revisão crítica de
`MELHORIAS_SKILLS.md`. Execute na ordem abaixo, salvo o que as dependências permitirem
paralelizar. Cada executor: leia o plano inteiro antes de começar, respeite as STOP
conditions e atualize sua linha aqui ao terminar.

Convenções comuns a todos os planos:
- **Fonte x cópia:** para recursos compartilhados, edite só `_DESIGN_SYSTEM/`, `_ERIC_CONTEXT/`, `_SHARED/`; as cópias dentro das skills são geradas por `python3 _TOOLS/sync_shared.py` (plano 001). Scripts e referências específicos podem ser alterados quando listados no escopo do plano; schemas especializados em `references/` não são atualizados pelo sync.
- **Testes de manutenção** ficam fora das skills: `_DESIGN_SYSTEM/tests/` e `_TESTS/`. **Evals** em `_EVALS/`.
- **Nunca** use nada de `_SAMPLE/` (material real, fora do git) em fixtures, testes ou amostras.
- Planos 008, 009 e 010 têm passos que gastam chamadas de modelo (evals): peça autorização ao operador antes.

## Ordem de execução e status

| Plano | Título | Prioridade | Esforço | Depende de | Status |
|---|---|---|---|---|---|
| 001 | [Sync do design system, limpeza dos pacotes](001-baseline-sync-e-limpeza.md) (git já criado) | P1 | M | — | DONE (sync verificado; 11 skills válidas; 5 testes passaram) |
| 002 | [`table_rows` busca por chave, não rótulo](002-table-rows-chave-rotulo.md) (T03) | P1 | S | 001 | DONE (7 casos novos e suíte com 12 testes passaram; sync verificado) |
| 003 | [Endurecer `score.py` + CLI](003-score-py-endurecer-e-cli.md) (T04) | P1 | S | — | DONE (12 testes passaram; CLI e skill validadas) |
| 004 | [CLI e testes do `iqb.py`](004-iqb-cli.md) | P1 | S | — | DONE (8 testes passaram; CLI e skill validadas; cálculo preservado) |
| 005 | [Validador semântico por tipo: IQB, potencial, citações aninhadas](005-validador-semantico-por-tipo.md) (T02 + parte de T04) | P1 | M | 001, 002, 003, 004 | DONE (51 testes passaram; amostras regeneradas; sync verificado) |
| 006 | [IQB completo nos derivados](006-iqb-completo-nos-derivados.md) (T01) | P1 | M | 001, 002 | DONE (54 testes passaram; PDF sem corte; amostra regenerada; sync verificado) |
| 007 | [PDF sem pango: entregar o resto e avisar](007-fallback-pdf-sem-pango.md) | P2 | S | 001 | DONE (57 testes passaram; sem pango: 33 passaram/4 skips; sync verificado) |
| 008 | [Descriptions + eval de acionamento](008-descriptions-e-eval-de-acionamento.md) | P1 | M | — | TODO (implementação pronta; bateria antes/depois adiada pelo operador; não bloqueia a execução do 009) |
| 009 | [Evals comportamentais (2 por skill)](009-evals-comportamentais.md) | P1 | M | — | DONE (11 conjuntos, 22 casos, 35 fixtures fictícias; integridade e contas verificadas; linha de base não rodada) |
| 010 | [Enxugar os SKILL.md (piloto → rollout)](010-enxugar-skill-md.md) | P2 | L | 001, 003, 004, 007, 008, 009 | DONE (11 skills reestruturadas; grilling unificado; checks locais passaram; evals comportamentais não executados) |
| 011 | [Learning Card ligado ao Test Card](011-learning-card-ligado-ao-test-card.md) | P3 | S | 001, 005 | DONE (vínculo e derivados verificados; 62 testes e 36 subtestes passaram; sync consistente) |
| 012 | [Manifesto de fontes e vigência](012-manifesto-de-fontes.md) | P3 | S | 001 | DONE (27 fontes, 11 páginas; hashes e 5 negativos verificados; 20 testes e 9 subtestes passaram) |
| 013 | [Calcular total e classe com as mesmas notas publicadas](013-potencial-precisao-consistente.md) (A01) | P1 | S | 012; 003 e 005 | DONE (65 testes e 54 subtestes passaram; precisão e exportação consistentes; sync e fontes verificados) |
| 014 | [Rejeitar evidências nulas ou de tipo inadequado no IQB](014-iqb-evidencia-textual.md) (A02) | P1 | S | 012; 004 | DONE (68 testes e 87 subtestes passaram; API e CLI rejeitam evidência inválida; fontes e sync verificados) |
| 015 | [Exigir que seções obrigatórias apareçam nos arquivos entregues](015-secoes-obrigatorias-visiveis.md) (A03) | P1 | M | 012; 001 e 005 | DONE (71 testes e 311 subtestes passaram; 96 casos antes aceitos agora rejeitados; textos preservados em cinco formatos; sync e fontes verificados) |
| 016 | [Manter os quatro campos em cards parciais e inconclusivos](016-cards-parciais-quatro-campos.md) (A04) | P1 | S | 012; 015; 001 e 005 | DONE (73 testes e 385 subtestes passaram; quatro campos obrigatórios preservados nos cards completos, parciais e inconclusivos; sincronização, fontes e diff verificados.) |
| 017 | [Preservar fontes individuais dos cards em Markdown e TXT](017-citacoes-dos-cards-em-md-txt.md) (A05) | P1 | S | 012; 001 e 005 | DONE (74 testes e 387 subtestes passaram; fontes individuais preservadas em MD/TXT, associação HTML/DOCX e referências desconhecidas verificadas; sync, fontes e diff sem divergências.) |
| 018 | [Mostrar estado, ID e versão em todos os formatos de leitura](018-estado-e-versao-nos-editaveis.md) (A06) | P1 | S | 012; 017; 001 e 007 | DONE (78 testes e 425 subtestes passaram; identificação nos formatos e slides, contrato completo para ausência/null, data informada, vínculo TC/LC e card de uma página verificados; sync e fontes consistentes.) |
| 019 | [Permitir até três forças e perguntas sem exigir preenchimento artificial](019-iqb-quantidades-sem-preenchimento-artificial.md) (A07) | P2 | S | 012; 014; 001 e 005 | DONE (81 testes e 437 subtestes passaram; listas de 0–3, rejeição de quatro e de seção ausente, nota de ausência e IQB real com 40 false verificados; schemas iguais, 602 palavras e sync/fontes consistentes.) |
| 020 | [Alinhar o contrato da one-page à orientação paisagem](020-one-page-paisagem-consistente.md) (A08) | P2 | S | 012; 001 | DONE (rejeição de retrato reproduzida e corrigida nos dois schemas; três modos preservados; 79 testes e 442 subtestes passaram, 4 PDF skips por falta de Pango; sync, fontes e diff verificados) |
| 021 | [Separar natureza da mudança e complexidade no mural 4D](021-4d-natureza-separada-do-esforco.md) (A09) | P2 | S | 012; nenhuma | DONE (zonas descrevem natureza; complexidade e justificativa registradas por proposta; checagem estrutural, fontes e diff passaram; avaliação com modelo não rodada) |
| 022 | [Manter quatro perguntas em cada fase da jornada 4D](022-4d-jornada-quatro-perguntas.md) (A10) | P2 | S | 012; 021 (mesmo arquivo; execução sequencial) | DONE (quatro perguntas conferidas nas fases antes, durante e depois; complementos antigos e ajuste do 021 preservados; fontes e diff verificados; avaliação com modelo não rodada) |
| 023 | [Distinguir critério local atingido de aprovação para expansão](023-experimentacao-criterio-local-e-limites.md) (A11) | P2 | S | 012; 009; 016 recomendado antes de exportar os cards | DONE (referências distinguem atingido, não atingido e inconclusivo; quatro casos fictícios adicionais validados estruturalmente; conjunto original preservado; fontes e diff verificados; avaliação com modelo não rodada) |
| 024 | [Confirmar intenção antes de pontuação formal (IQB, potencial, scorecard)](024-confirmar-intencao-antes-de-pontuacao-formal.md) | P3 | S | — | DONE (IQB 631/650 e Scorecard 868/900 palavras, frase adicionada; potencial-inovacao intocado — sem folga de orçamento, decisão correta pelo plano; validador passou; escopo limpo — revisado em worktree isolado, branch `advisor/024-confirmar-intencao-pontuacao`, não mesclado) |
| 025 | [Tratar conteúdo lido como dado, nunca como instrução (grilling)](025-conteudo-lido-como-dado-nao-instrucao.md) | P2 | S | 001 | DONE (cláusula em `_SHARED/grilling-operacional.md`, sincronizada para as 11 cópias com MD5 idêntico; validador passou nas 11; escopo exatamente os 12 arquivos esperados — revisado em worktree isolado, branch `advisor/025-dado-nao-instrucao`, não mesclado) |
| 026 | [Scanner de objetividade (vocabulário absoluto + número sem citação)](026-scanner-de-objetividade.md) | P2 | M | — | DONE (revisão 1/2: `ABSOLUTE_TERMS` corrigido para match com limite de palavra via regex, eliminando os 2 falsos positivos sem perder detecção real; varredura das 18 amostras em `_SAMPLES_ENTREGAVEIS/` sem nenhum erro; 27 testes passaram — revisado em worktree isolado, branch `advisor/026-scanner-objetividade`, 4 commits, não mesclado) |
| 027 | [Contrato estrutural de fonte/cor DOCX/PPTX](027-contrato-estrutural-docx-pptx.md) | P2 | S | — | DONE (render_pptx corrigido para ler tokens.json em vez de literais hardcoded; 2 testes novos + suíte completa de 39 testes/4 skips passaram; `grep` confirma zero literais "Montserrat"/"Roboto" restantes — revisado em worktree isolado, branch `advisor/027-contrato-docx-pptx`, não mesclado) |
| 028 | [Idempotência do PDF (Fase 1) + fidelidade visual (Fase 2, aguarda autorização)](028-idempotencia-e-fidelidade-visual-pdf.md) | P3 | Fase 1: S / Fase 2: L | — | DONE (Fase 1: teste criado, pula corretamente sem `pango` — não pôde validar o caminho de sucesso ponta a ponta nesta máquina, só o de skip; suíte completa 38 testes, 5 skips, sem falhas; escopo limpo, só `tests/test_render.py` — revisado em worktree isolado, branch `advisor/028-idempotencia-pdf-fase1`, não mesclado). Fase 2 não iniciada, aguarda autorização do operador |
| 029 | [`render_pptx` lê posição de `_DESIGN_SYSTEM/layouts/<tipo>.layout.json`](029-render-pptx-le-layout-json.md) | P2 | M | requer `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` commitado | DONE (2 testes novos + suíte completa de 42 testes passaram, 5 skips esperados; `VisualTokenContractTests` do Plano 027 intacto; executor adaptou o teste de posição customizada para usar `unittest.mock.patch.object` em vez de um `deliverable_type` fictício, que falhava em `validate()` por falta de perfil — desvio documentado e aprovado, mesmo padrão já visto no Plano 030 — revisado em worktree isolado, branch `advisor/029-pptx-layout-json`, não mesclado) |
| 030 | [`render_html` (caminho "presentation") posiciona masthead/título/rodapé/conteúdo por `layout.json`](030-render-html-presentation-layout-json.md) | P2 | M | requer `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` commitado (independente do Plano 029, loader próprio) | DONE (2 testes novos + suíte completa de 42 testes passaram, 5 skips esperados sem `pango`; executor corrigiu um bug real no próprio teste do plano — `deliverable_type` fictício colidia com `DELIVERABLE_LABELS` antes de chegar no código novo — via `unittest.mock.patch.object`, desvio documentado e aprovado — revisado em worktree isolado, branch `advisor/030-html-presentation-layout-json`, não mesclado) |
| 032 | [Gerar PDF com ReportLab, sem Pango — prova em `test_card`, `learning_card` e `briefing_one_page`](032-pdf-reportlab-portatil.md) | P1 | M | nenhuma (independente do 031) | DONE (executado pelo Codex em `advisor/032-pdf-reportlab`; revisado em 05/10/2026: 10 testes novos, suíte 101 passou sem Pango e 106 com Pango, sync consistente, código fiel ao plano; mesclado no `main`. Aprovação visual do operador pendente junto com a do 034) |
| 033 | [Reprovar todo PDF com defeito visual (portão de qualidade) e criar a folha de comparação entre motores](033-verificador-de-qualidade-do-pdf.md) | P1 | M | 032 | IN PROGRESS (executado pelo Codex; revisão reprovou: STOP condition ignorada — apresentação executiva reprovada pelo portão e aceita num teste. Correção em [033-correcao-pos-revisao.md](033-correcao-pos-revisao.md)) |
| 034 | [Gerar os 14 relatórios (A4 retrato e paisagem) em PDF com ReportLab, em nível profissional](034-pdf-reportlab-relatorios.md) | P1 | L | 032, 033 + aprovação visual do 032 | IN PROGRESS (executado pelo Codex sem a aprovação visual do 032; revisão achou citações de grades perdidas, legenda órfã, cartões desalinhados e passo 9 não feito. Correção em [034-correcao-pos-revisao.md](034-correcao-pos-revisao.md), depois da do 033) |
| 035 | [Apresentação executiva 16:9 *state of the art*: PDF em ReportLab, regras de conteúdo e tipografia de slide nos tokens](035-apresentacao-executiva-soap.md) | P1 | L | 034 + aprovação visual do 034 | TODO |
| 036 | [Tornar o ReportLab o motor único de PDF e remover WeasyPrint, Pango e `pydyf`](036-reportlab-padrao-remove-weasyprint.md) | P1 | M | 035 + aprovações visuais de 032, 034 e 035 | TODO |
| 037 | [Distribuir as skills por `npx skills`, `.skill` e clone, com versão por skill e aviso de atualização](037-distribuicao-e-versoes.md) | P1 | M | nenhuma (workflow separado do 036) | TODO |
| 038 | [Separar o que é da CCEE do que é de terceiros: tirar os PDFs da Strategyzer, restringir o `LICENSE` e gerar `THIRD_PARTY_NOTICES.md`](038-licenca-e-material-de-terceiros.md) | P1 | M | nenhuma (compatível com o 037 em qualquer ordem) | DONE (executado em 2026-10-07: 3 PDFs da Strategyzer retirados e travados por `RETIRED`; manifesto com titular/licença/distribuição; `THIRD_PARTY_NOTICES.md` gerado e copiado às 12 skills; `LICENSE` restrito à CCEE; DOCX 4D/3E/5C confirmados como CCEE; suíte 110 passou. Guia do Pitch Canvas colocado sob CC BY-SA 4.0 por decisão do operador. Histórico do git reescrito em seguida) |
| 039 | [Organizar a `experimentacao-inovacao` em três blocos: Aprofundamento/Planejamento, Execução e Consolidação](039-experimentacao-em-tres-blocos.md) | P1 | M | nenhuma | TODO |
| 031 | [Corrige offset de `@page margin` no caminho "presentation" e estende `layout.json` para `executive_one_page`/`card_portrait`](031-render-html-offset-fix-e-one-page-card-layout-json.md) | P1 | M | nenhuma (029/030 já mesclados; corrige um defeito no que o 030 entregou) | BLOCKED (executor completou os 6 passos e todos os critérios do próprio plano no ambiente dele — sem Pango, 5 skips esperados; revisor tinha Pango disponível nesta sessão e achou uma regressão real que o executor não podia ver: `RenderTests.test_oversized_card_remains_fatal`, teste pré-existente, passa em `main` e falha depois das mudanças do plano — `position: absolute` com altura fixa remove o título/seções do fluxo normal, então um título gigante não empurra o PDF para 2 páginas; `pypdf` conta 1 página, a checagem de `render.py:946-954` passa, e o conteúdo sai sobreposto/corrompido silenciosamente em vez de travar com erro — confirmado com `pdfplumber`: o texto do título vai de top=6.8mm a top=295.9mm, cobrindo a página inteira por cima de todo o resto do card. Isso invalida a premissa central do plano ("não há risco de corte silencioso"). Branch `advisor/031-html-offset-fix-one-page-card-layout` preservada, não mesclada; plano precisa ser revisado com um mecanismo de detecção de overflow que não dependa só de contagem de páginas antes de reexecutar) |

Status: TODO | IN PROGRESS | DONE | BLOCKED (motivo em uma linha) | REJECTED (motivo em uma linha)

Retomada do plano 008 (28/09/2026): o operador pediu para deixar o plano como
`TODO` e continuará com Claude quando o limite liberar. Preserve os conjuntos e
as descriptions já implementados. A revisão local em `_EVALS/triggers/resultados.md`
não substitui a medição real. Para medir antes/depois, use as descriptions do commit
`21cef5b` como linha de base e as de `9ac08f3` como versão nova, em checkouts separados,
seguindo `_EVALS/triggers/README.md`. Confirme a autorização antes das chamadas,
conforme o plano. O plano 009 permanece `TODO`; apenas sua branch foi criada,
sem arquivos implementados naquele momento. A implementação posterior do 009
está registrada no status atual acima.

Auditoria da retomada com Claude: sessão `609c5081-03a7-4c59-8e06-7671f031a322`.
Correção adicional do plano 005 preservada em `7344bb7`; suíte revalidada com
58 testes passando e 25 subtestes. A medição do 008 não foi concluída e seus
8/16 são inválidos: erros de limite foram contados como não acionamento.
Diagnóstico e requisitos para uma nova execução em `_EVALS/triggers/resultados.md`
e `_EVALS/triggers/README.md`. Não repetir a bateria original automaticamente.

O operador autorizou adiar a bateria de acionamento do plano 008 e continuar os
planos em sequência. A medição permanece pendente para execução posterior com
runner corrigido e nova autorização de custo; nenhuma nova chamada de diagnóstico
ou bateria será disparada nesta retomada. O plano 009 pode prosseguir, pois não
depende do 008. A criação e validação estrutural de seus casos não exige chamadas
de modelo; sua linha de base opcional ficará registrada como não rodada.

Piloto do plano 010: o operador autorizou seu início. Apenas o corpo de
`potencial-inovacao/SKILL.md` foi reestruturado; frontmatter, cálculo, referências
e design system preservados. O arquivo passou de 839 para 650 palavras
(corpo: 740 para 551). O texto prescrito no Step 3, expandido com os blocos
obrigatórios e o contrato `scores`, somava 723 palavras com frontmatter; os
passos específicos foram condensados para cumprir também o `wc -w` ≤650,
mantendo os quatro blocos padrão exatos e as regras do método. A instrução
adicional do plano 005 registrada em `7344bb7` foi mantida no contrato `scores`.
Validador da skill, links locais, frontmatter, orçamento e blocos padrão
verificados; 12 testes de potencial e 7 subtestes passaram; sync verificado.
Nenhuma chamada de modelo foi feita nessa etapa; o rollout aguardou a revisão
do operador, conforme o Step 3.

Fechamento do plano 010: o operador aprovou o piloto e autorizou o rollout.
As outras dez skills foram reestruturadas, com um commit por skill, preservando
frontmatter e regras específicas nos textos principais ou referências linkadas.
Planejamento e análise da experimentação foram movidos integralmente para duas
referências locais, com ajuste apenas dos caminhos relativos dos links.
O levantamento documental foi incorporado ao grilling comum e suas nove cópias
aposentadas foram removidas pela sincronização.

As 11 skills passaram no validador, na checagem de links, na estrutura de seções
e no orçamento: até 650 palavras nas skills comuns, 900 no scorecard e 1.400 na
experimentação. Os quatro blocos padrão foram conferidos; frontmatter, scripts,
assets, design system e contexto ERIC foram preservados. A suíte local passou
com 58 testes e 25 subtestes; `sync_shared.py --check` e `git diff --check` passaram.
As evals comportamentais do plano 009 contra a linha de base não foram executadas:
as chamadas de modelo seguem adiadas, sem autorização específica de custo nesta
etapa. Os checks locais não comprovam ausência de regressão comportamental.
O plano permite o fechamento com esse registro; a comparação permanece pendente.

Ajuste posterior solicitado pelo operador: linguagem simples e direta nas onze
skills, tanto no chat quanto nos entregáveis. A orientação comum está em
`_SHARED/linguagem-dos-entregaveis.md`, distribuída por sync e linkada em cada
SKILL.md. Ela atualiza o bloco padrão de entrega do plano 010 para exigir clareza
ao leitor, preservando os métodos. Cabeçalhos e estados visíveis do renderizador
foram traduzidos para português; os campos canônicos continuam preservados.
Validação local: onze skills válidas, links e orçamentos conferidos, sync consistente;
59 testes e 28 subtestes passaram. Nenhuma avaliação com modelo foi disparada.

Em 29 set 2026, o operador pediu explicitar o afunilamento briefing → 4D → 3E.
A skill de experimentação e sua triagem agora usam as decisões vigentes do 3E
como referência principal, sem reabrir dúvidas resolvidas ou retiradas do escopo.
Contexto ERIC e grilling comum foram alinhados e sincronizados. Lacunas relevantes,
evidências contrárias e critérios anteriores à coleta continuam preservados.
Onze skills passaram no validador, com links e orçamentos conferidos; sync consistente.
A verificação foi documental e estrutural, sem nova avaliação comportamental de modelo.

## Notas de dependência

- **001 antes de tudo que toca o design system** (002, 005, 006, 007, 011): sem o script de sync, cada correção teria de ser copiada à mão para 11 pastas.
- **002 antes de 005 e 006**: 005 usa tabela `columns`/`rows` com `{key,label}` no bloco de notas do potencial; 006 reescreve a mesma função `table_rows`.
- **003 e 004 antes de 005**: o validador copia as regras dos scripts e tem teste de paridade contra eles.
- **009 antes de 010**: as evals são a rede de segurança da reescrita dos SKILL.md. 010 também usa o frontmatter do 008 e as frases de CLI de 003/004, e remete ao fallback de PDF do 007 no README do design system.
- Paralelizáveis desde já: 003, 004, 008, 009 (e 001).

## Relação com `MELHORIAS_SKILLS.md`

| Item de MELHORIAS | Plano |
|---|---|
| 4.1 IQB nos derivados | 006 |
| 4.2 Consistência matemática do IQB | 005 |
| 4.3 Chave × rótulo | 002 |
| 4.4 Potencial sustentado | 003 (script) + 005 (contrato/validador) |
| 5 Rastreabilidade verificável | reduzido: citações aninhadas (005) + Learning↔Test Card (011) |
| 6 Testes comportamentais | 009 (+ acionamento em 008) |
| 7 Proveniência | 012 (manifesto único, não 11 registros) |
| 8 Equivalência entre formatos | 006 para o IQB; demais tipos adiados (ver abaixo) |
| 9 Organização da implementação | 001 (sync + git) |
| 10 Comandos de verificação | corrigidos nos planos: validador do skill-creator da Anthropic (não o do Codex); testes pulam sem pango (007) |

Achados novos, fora de MELHORIAS: scripts sem CLI (003, 004), descriptions/acionamento (008), SKILL.md prolixos e repetidos (010), `levantamento-documental` sobreposto ao grilling (010), lixo nos pacotes e `tests/` distribuído (001), PDF quebrando todos os formatos sem pango (007), chaves do `score.py` diferentes das `section_key` do schema do potencial (tratado em 005), "nove skills" no contexto ERIC (001).

## Achados da revisão externa de 02/10/2026 (comparação com 7 repositórios de skills)

Auditoria feita fora deste fluxo, comparando as 11 skills com padrões extraídos de
`anthropics/skills`, `obra/superpowers`, `mattpocock/skills`, `vercel-labs/agent-skills`,
`andrej-karpathy-skills`, `coreyhaines31/marketingskills` e 3 skills locais do operador
(relatório completo fora deste repositório, em `~/skills-research/relatorio/`). A maioria
dos achados dessa comparação já estava coberta pelo que este backlog tinha implementado
(sync de fonte única via `001`, evals via `008`/`009`, manifesto de proveniência via `012`)
— **a independente nunca viu `plans/` nem `_SHARED/`/`_TOOLS/` antes de comparar**, então
o achado inicial de "duplicação sem fonte única" estava incorreto para este repositório e
foi descartado após a leitura de `_TOOLS/README.md` e `plans/README.md`. Dos 6 achados
originais, só 2 eram genuinamente novos; viraram os planos 024 e 025 acima, com escopo
corrigido para caber no schema real validado por `quick_validate.py` (`disable-model-invocation`
não existe em `ALLOWED_PROPERTIES` — por isso o 024 vira confirmação em prosa, não campo
de frontmatter).

## Achados da análise de fidelidade visual + objetividade de 02/10/2026

Documento completo em `~/skills-research/relatorio/analise-fidelidade-visual-objetividade.md`
(fora deste repositório). Investigou `_DESIGN_SYSTEM/` a fundo e gerou os planos 026-028:

- **026** (scanner de objetividade): achado de design corrigido durante a escrita do plano —
  `scripts/validators/__init__.py:run()` despacha **um único** arquivo por `deliverable_type`,
  não uma lista de validators; um scanner cross-cutting exige alterar o dispatcher para sempre
  chamar um módulo comum (`_common.py`) além do validator específico, não só "adicionar um 4º
  arquivo" como a análise original sugeriu.
- **027** (contrato estrutural DOCX/PPTX): achou um bug real e verificado por render direto —
  `render_pptx`/`slide()` usa `"Montserrat"`/`"Roboto"` como literais hardcoded em vez de ler
  `tokens["typography"]["font_brand"/"font_body"]` (só o rodapé lê o token corretamente). Hoje
  os valores coincidem por acaso; sem teste, uma mudança futura de marca quebraria silenciosamente
  só no PPTX, não no DOCX.
- **028** (idempotência/fidelidade visual de PDF): dividido em Fase 1 (teste de idempotência por
  texto extraído via `pypdf`, já é dependência, autônomo) e Fase 2 (comparação visual com limiar
  contra golden image, explicitamente **não autorizada** — exige dependência nova e aprovação
  humana da primeira imagem por orientação). Verificado nesta máquina que `pango`/WeasyPrint não
  está disponível no ambiente de autoria, então a Fase 1 foi especificada mas não pôde ser
  executada ponta a ponta — o executor deve confirmar o ambiente antes de rodar.
- O manifesto de hash que `render.py` já grava (`content_sha256`/`profile_sha256`/`tokens_sha256`/
  hash por arquivo) foi avaliado e descartado como base para idempotência: o próprio README já
  avisa que bytes de PDF/DOCX/PPTX variam por metadado interno das bibliotecas.

## Planos 029-030 — origem

Gerados a partir de uma ferramenta nova de autoria visual (`_LAYOUT_STUDIO/`, fora do git
de skills) que define, por `deliverable_type`, a posição/tamanho de cada "slot" de um
entregável — exportando `_DESIGN_SYSTEM/layouts/<tipo>.layout.json`. Hoje `render.py` não
lê esses arquivos; os Planos 029/030 são os primeiros passos de integração, escolhendo
`executive_presentation` como piloto (PPTX no 029, PDF/HTML no 030) porque é o único tipo
com posição absoluta no código atual (tanto em `render_pptx` quanto no sub-caminho
`"presentation"` de `render_html`) — os outros 17 tipos são renderizados em fluxo e
exigiriam uma abordagem diferente (aproximação por caixa de margem CSS, não posição
livre), avaliada só depois que este piloto for validado em dois formatos. Os dois planos
têm loaders independentes (029 converte mm→polegadas para `python-pptx`; 030 usa mm direto,
já que CSS aceita a unidade nativamente) — decisão deliberada para não acoplar os dois
planos um ao outro. Os outros 17 `*.layout.json` existem (rascunho, com `_draft_note`) mas
não têm efeito em nada ainda, em nenhum dos dois planos.

Regra decidida para quando (e se) os 14 tipos genuinamente multi-página forem endereçados
no futuro: posição fixa só vale para slots **estruturais** (`logo`, `titulo_documento`,
`identificacao_versao`/`rodape`) — nunca para slots cujo `section_key` é uma seção de
conteúdo real do schema. Seções de conteúdo continuam em fluxo, sem risco de corte. Essa
regra ainda não tem plano escrito; fica registrada aqui para a próxima vez que o assunto
for retomado.

## Plano 031 — origem e correção de bug encontrado no 030

Ao gerar amostras de antes/depois do `executive_presentation` para o operador conferir,
descobrimos empiricamente (teste controlado com WeasyPrint, não suposição) que o `@page
{ margin: 0.4in }` definido em `css()` para `presentation_16_9` desloca todo elemento
`position: absolute` do sub-caminho `"presentation"` (Plano 030) em ~10,16mm da posição
real do canvas — porque CSS mede `position: absolute` a partir da área de conteúdo da
página, já descontada a margem do `@page`, enquanto o `layout.json`/PPTX usa coordenadas
relativas à página inteira. Ou seja: o PDF e o PPTX de `executive_presentation` **não
batem pixel a pixel** hoje, apesar de lerem o mesmo arquivo — o objetivo declarado do
Plano 030 ("fechar os dois formatos na mesma fonte de verdade") não foi atingido na
prática. O Plano 031 corrige isso (regra `@page { margin: 0; }` adicional, só quando
`layout_slots` existe) como primeiro passo, antes de estender a mesma técnica para
`briefing_one_page` (perfil `executive_one_page`) e `test_card`/`learning_card` (perfil
`card_portrait`).

Esses 3 tipos ficaram de fora da regra "só slots estruturais" registrada acima — e isso é
deliberado, não uma inconsistência: diferente dos 14 tipos genuinamente multi-página,
`render.py:946-954` já rejeita com `ValueError` qualquer PDF desses 3 tipos (mais
`executive_presentation`, que também está nessa lista) que saia de uma página, contando
páginas de verdade via `pypdf` depois de gerar o PDF. Não há risco de corte silencioso de
conteúdo — por isso o Plano 031 posiciona cada seção de conteúdo individualmente (não só
os slots estruturais), usando os rascunhos de `layout.json` que já existem para os 3 tipos
desde a extração feita em sessão anterior (corrigidos nesta sessão: `test_card.layout.json`
e `learning_card.layout.json` tinham canvas 148×210mm, tamanho A5, incompatível com o
perfil real `a4_portrait` — 210×297mm — usado por `render.py`; `briefing_one_page.layout.json`
já estava correto, 297×210mm batendo com `a4_landscape`).

## Plano 032 — origem e reescrita (ReportLab)

A primeira versão do Plano 032 propunha o Chromium (Playwright) como motor de PDF de
reserva. O operador a rejeitou: o PDF do Chromium saía com a camada de texto corrompida
(cada caractere repetido ~7 vezes na extração), o que não resolve o uso real. Contexto
completo em [PROBLEMA_MOTOR_PDF_CROSS_PLATFORM.md](PROBLEMA_MOTOR_PDF_CROSS_PLATFORM.md).

Em 05/10/2026 o plano foi reescrito com foco no **ReportLab**: Python puro, instalado só
com `pip`, sem Pango/Cairo. Antes de escrever, uma prova fora do repositório confirmou:
fontes estáticas geradas das variáveis do projeto com nomes internos corretos; Test Card
em uma página A4 com acentos extraídos corretamente; bytes idênticos entre execuções;
transbordo detectado como erro (sem a sobreposição silenciosa que bloqueou o 031);
one-page em duas colunas com logo em uma página A4 paisagem. O plano entrega o motor
atrás de `--pdf-engine reportlab`, sem mudar o padrão, para 3 tipos; a migração dos
demais e a troca do padrão dependem da revisão visual do operador (Passo 8).

## Planos 033–036 — caminho até remover o WeasyPrint, com qualidade *state of the art*

Em 05/10/2026 o operador aprovou o caminho: provar o ReportLab (032), estender aos
relatórios e à apresentação e, por fim, remover o WeasyPrint. No meio do planejamento,
definiu o nível de qualidade: entregáveis *state of the art*. Por isso foi acrescentado
um plano antes dos relatórios:

- **033 — portão de qualidade**: todo PDF, de qualquer motor, é reprovado se tiver texto
  fora da página, fonte abaixo de 7,5 pt ou caracteres sobrepostos (regras que já estavam
  em `tokens.json` → `density`, mas não eram verificadas). Validado nas 18 amostras:
  nenhum falso positivo e um defeito real (citações de 7,2 pt no resumo do briefing).
  Inclui a ferramenta de comparação visual lado a lado usada nas aprovações do operador.
- **034 — relatórios**: os 14 tipos, com acabamento além do HTML atual (página X de Y,
  marcadores de navegação, faixa de seção nunca órfã, cabeçalho de tabela repetido).
- **035 — apresentação**: títulos-mensagem, uma ideia por slide e limites de texto
  verificados pelo validador; tipografia de slide nos tokens, compartilhada por PDF e PPTX;
  slide que não cabe vira erro, nunca sobreposição.
- **036 — troca**: ReportLab como motor único, remoção de WeasyPrint/Pango/`pydyf`,
  testes de PDF sem pular, amostras regeneradas e CI em Windows, macOS e Linux.

Cada plano de 032 a 035 termina numa aprovação visual do operador; o seguinte não começa
sem ela. Com o 036, o Plano 031 (BLOCKED) perde o motivo original (PDF gerado do HTML) e
deve ser reavaliado só para o formato HTML.

## Achados considerados e rejeitados

- **Rastreabilidade executável completa** (afirmação → fonte → evidência → teste → aprendizado → recomendação, para os 18 tipos; MELHORIAS §5): custo alto e sobreposição com julgamento que só o modelo faz ("a evidência sustenta a conclusão?"). Automatizamos só o que é estrutural e inequívoco (005, 011).
- **Registro de proveniência copiado em cada skill** (MELHORIAS §7.1): 11 cópias para manter; substituído por manifesto único + página gerada (012).
- **Comparar hash binário de PDF/DOCX/PPTX entre renderizações**: bibliotecas gravam metadados variáveis; o próprio README do design system já descarta isso. A equivalência é checada por conteúdo (006).
- **Teste de equivalência de conteúdo para os 18 tipos agora** (MELHORIAS §8): só o IQB tinha perda de dados comprovada. Reavaliar depois de 006, se aparecer outro tipo com estrutura composta em `data`.
- **Tirar o design system de dentro das skills para evitar 11 cópias**: rejeitado — a independência de cada skill é requisito explícito do mantenedor. O custo das cópias é resolvido pelo sync (001).
- **Traduzir SKILL.md para inglês**: os usuários e as fontes são em português; as descriptions em português acionam melhor para pedidos em português.

## Revisão individual de 29/09/2026

Auditoria contra `32a103a`, com as onze skills revisadas separadamente:
[achados, evidências e recomendações](REVISAO_SKILLS_2026-09-29.md).
Foram encontrados onze grupos de correções, incluindo problemas compartilhados
que não devem virar onze implementações repetidas. A suíte existente passou com
59 testes e 28 subtestes; reproduções locais revelaram caminhos não cobertos.
A implementação foi preservada. Nenhuma bateria de modelos foi executada.
O operador selecionou todos os achados para planejamento. Os novos planos
013–023 estão em TODO; os TODOs 008, 011 e 012 permanecem preservados.
Nenhuma correção foi implementada nesta etapa.

## Execução dos planos da revisão de 29/09/2026

Onze novos planos cobrem A01–A11, um por grupo de correção. Os problemas comuns
são corrigidos na fonte e distribuídos por sync, sem onze implementações manuais.
Todos foram escritos contra `32a103a`; conferir deriva antes de executar.

Ordem recomendada: **013 → 014 → 015 → 016 → 017 → 018 → 019 → 020 → 021 → 022 → 023**.
A ordem evita conflitos em contratos, renderizador e testes compartilhados.
Os planos não dependem da bateria adiada do 008. Não executar chamadas de modelo
para concluir as verificações locais. O 023 prepara casos adicionais, mas deixa
sua execução comportamental para uma etapa posterior com autorização de custo.

Dependências novas:

- 016 vem após 015 para manter a mesma distinção entre síntese textual e bloco visual.
- 018 vem após 017 para preservar o vínculo das fontes durante a mudança dos editáveis.
- 019 vem após 014: avaliação sem forças comprovadas continua exigindo texto de evidência ou ausência em cada critério.
- 022 vem após 021 porque ambos alteram subseções do mesmo mural; preservar a mudança anterior.
- 023 não depende da execução de 016 para corrigir o texto/criar casos; 016 é recomendado antes de exportar cards desses casos.
- 011 continua sendo vínculo Learning↔Test Card; 016 é estrutura de quatro campos, e 018 é identificação visível. Não duplicar ou fundir esses escopos.
- 012 continua sendo manifesto de fontes/vigência; 018 não substitui esse manifesto.

### Cobertura por skill

| Skill | Planos novos que cobrem os achados |
| --- | --- |
| briefing-inovacao | 018, 020 |
| avaliacao-briefing-iqb | 014, 018, 019 |
| potencial-inovacao | 013, 018 |
| workshop-4d | 015, 018, 021, 022 |
| relatorio-4d | 017, 018 |
| workshop-3e | 015, 016, 018 |
| relatorio-3e | 015, 016, 018 |
| workshop-5c | 015, 018 |
| relatorio-5c | 015, 018 |
| experimentacao-inovacao | 016, 018, 023 |
| scorecard-inovacao | 015, 018 |

A antiga decisão de adiar equivalência de formatos permanece para uma cobertura
indiscriminada de todos os tipos. As perdas agora comprovadas são tratadas de forma
restrita em 015 e 017; identificação em 018. Não ampliar para igualdade binária.

Manutenção após 012: planos 013–023 também conferem `build_sources.py --check`.
Quando modificarem fonte registrada no manifesto, regeneram somente as páginas
`references/fontes.md` afetadas e as incluem no commit daquela correção.
