# entregaveis_oficiais verification

**Verdict**: PASS
**Mutations**: 3 - C5 e C8; após as correções em `616653b`, três mortas e zero sobreviventes. Os resultados iniciais estão preservados abaixo.
**Proofs**: `proofs.md` no HEAD final; reconferência em `616653b` com 21 provas verdes e três mutações mortas. Suíte completa corrigida: 349 testes e 2.408 subtestes passaram.
**Verifier**: independent sub-agent (author != verifier)

Escopo: diff e53a71c..f2553f5, plano aprovado, checks sem Handoff, provas e árvore real. Fontes visuais são inspiração; nenhuma captura vinculante exige decisão de fidelidade nesta rodada. As alterações preexistentes de `pptx_pdf_visual_parity` não foram lidas nem alteradas.

## Findings

| Finding | Evidence | Fix | Closed |
| --- | --- | --- | --- |
| F1 — C9 aceita esconder uma lacuna com a marca `partial`, sem preservar a receita visível exigida por AC17/33 | `_DESIGN_SYSTEM/tests/test_official_deliverables.py:194` remove o conteúdo da etapa e depois apenas muda o estado para parcial (linha 197). No exemplo próprio A abaixo, apagar título e texto de `e3_outcome` é aceito sem nenhuma indicação visível da lacuna. `render.py:298` pula os validadores semânticos nas parciais; nem a ordem é conservada. | Preservar as seções das etapas aplicadas com indicação explícita de pendência na entrega parcial/inconclusiva. Cobrir o caso em C9 com conteúdo de lacuna visível e com rejeição de receita silenciosamente apagada; não exigir resultado inventado. Manter a validação estrutural aplicável aos oficiais parciais, separando-a da exigência de completude. | `616653b` - C9 e C18 preservam inventário, ordem e pendência explícita nas versões partial/inconclusive; execução sem fonte continua rejeitada. |
| F2 — C5 não isola o significado e o nome do playbook que promete proteger | `test_standard_methods`, linhas 123–129: compara nomes do exemplo, mas o único negativo inverte o inventário sem reordenar os blocos. A receita dinâmica também rejeita isso por ordem; o teste pode passar mesmo sem a proteção dos significados. M2 remove a comparação `actual != expected`, preservando o teste de exclusões. M2 sobreviveu na execução do builder em f2553f5: os seis casos de C5 continuaram verdes. | Acrescentar negativos de nome e significado individualmente alterados em aplicação `standard`, além de inversão coerente de inventário e blocos. Os mesmos casos declarados `adapted`, com motivo, devem continuar válidos. Confirmar M2 morta após ampliar C5 antes de fechar. | `616653b` - C5 altera nome e significado isoladamente e reordena inventário junto dos blocos; variantes adapted seguem aceitas. |
| F3 — C8 não testa o limite de quatro blocos por slide | `test_slide_density`, linhas 172–184, testa títulos e 141 palavras, mas nenhum caso de cinco blocos. M1 amplia exclusivamente o limite de blocos de quatro para cinco. M1 sobreviveu na execução do builder em f2553f5: C8 continuou verde. | Provar quatro blocos aceitos e cinco rejeitados, com texto curto que não ative o limite de palavras, e preservar a aceitação de nova página/slide. Confirmar M1 morta após ampliar C8 antes de fechar. | `616653b` - C8 aceita quatro blocos, rejeita cinco e aceita divisão em novo slide. |
| F4 — Os fechamentos dos seis exemplos usam títulos genéricos onde AC38 exige achados | Todos usam `O desfecho orienta o próximo passo dentro do escopo realizado` e `As dependências precisam de responsáveis antes do próximo avanço`; os três pitches também usam `A decisão solicitada delimita o próximo avanço do projeto`. Esses títulos não informam o desfecho, a dependência ou o pedido concreto. A referência da autora conclui, por exemplo, que as propostas seguem para avaliação de dependências. C14 verifica palavras do guia, tamanho do resumo e citações, não esse aspecto editorial. | Trocar os títulos de fechamento por conclusões específicas do exemplo: 4D pode indicar a visão compartilhada seguindo ao 3E com atualização por esclarecer; 3E, rota e critério ainda abertos; 5C, preferência pela consulta condicionada à atualização. Usar também pedidos concretos nos títulos de decisão e ação. Preservar os rótulos metodológicos de descrição/execução/desfecho do relatório. | `616653b` - gerador e vinte exemplos regenerados usam títulos específicos de achado, dependência, deliberação e ação; C12/C14 preservam conteúdo e tom. |

## Exemplos próprios executados

Executados em f2553f5 pelo Python de `/private/tmp/eric-pptx-validation-venv`, importando o renderer real e chamando `validate` com `_DESIGN_SYSTEM/profiles.json`; não geraram arquivos nem alteraram implementação.

**A — Pocket 3E dedicada somente ao E3.** Diferente do exemplo E1/E2 do plano: parti do relatório 3E, mantive apenas E3 no inventário e nos blocos, excluí E1/E2 por desenho com motivo explícito, e expliquei o recorte em `structuring`. Resultado: aceito como `complete`, conforme AC32. Em seguida, removi título e texto de `e3_outcome` e marquei `partial`: aceito sem lacuna visível. Inverter todos os blocos dessa versão parcial também foi aceito. Esse segundo resultado fundamenta F1; a redução de escopo legítima permaneceu válida.

**B — Adaptação 5C sem correspondência com qualquer C.** Substituí as cinco etapas por `retrospectiva`, com rótulo e significado próprios, `official_stage_ids: []`, cinco exclusões justificadas e explicação visível em `structuring`. Acrescentei os três conteúdos `retrospectiva_description`, `retrospectiva_execution` e `retrospectiva_outcome`, com fontes e na ordem. Resultado: aceito completo, conforme door 4 e AC35. A adaptação é aceita pela documentação da aplicação, sem presumir equivalência pela letra.

## Tom dos seis oficiais

Comparação independente com `relatorio-5c/references/exemplos/5c-oficial-sessao-coletiva-apresentacao.md`. A referência distingue relato, consequência a examinar, contagem, preferência, hipótese e decisão; usa achados nos títulos e ressalvas próximas à afirmação. A orientação comum está distribuída igualmente nas três skills. Os trechos abaixo foram lidos nos seis `input.json` atuais; não se tomou o checklist de C14 como prova de tom.

| Oficial | Trecho e julgamento |
| --- | --- |
| Relatório 4D | `O registro disperso apareceu nas duas dinâmicas. A leitura sugere examinar a passagem entre áreas [...] não houve medição de retrabalho.` Relaciona evidência e leitura, com limite junto à inferência. A preferência segue separada da aprovação. Desvio de títulos de fechamento em F4. |
| Apresentação 4D | `Cada participante recebeu três créditos [...] oito dos doze créditos [...] a ata conservou a objeção sobre atualização dos dados.` A estruturação informa quatro presentes; a regra e o total reconciliam, e a objeção é preservada. `Não houve aprovação de construção` calibra o desfecho. Desvio de títulos de fechamento em F4. |
| Relatório 3E | `A construção está planejada, não concluída. A rota permanece indefinida até a avaliação técnica; a dependência central é manter o registro atualizado sem duplicar trabalho.` Concreto e analítico, separa plano e execução. O E3 descreve Test Card prospectivo, sem inventar eficácia. Desvio de títulos de fechamento em F4. |
| Apresentação 3E | `O Test Card é prospectivo e ainda precisa do critério aprovado antes da coleta. Não há resultado de uso ou eficácia.` A ressalva acompanha o teste; o texto explica o que observar e o que permanece aberto. Desvio de títulos de fechamento em F4. |
| Relatório 5C | `Quatro dos seis presentes relataram procurar atendimento quando não viam uma previsão [...] Dois participantes também citaram utilidade no protocolo de abertura.` Denominador explícito e experiência positiva preservada; o desfecho distingue menções de prevalência e votos. Desvio de títulos de fechamento em F4. |
| Apresentação 5C | `Menos contatos de acompanhamento é benefício esperado, ainda sem medição; atualização dos dados e acesso às informações são dependências a avaliar.` O benefício permanece hipótese, com ressalva local e dependências concretas. A contagem do C5 reconcilia seis presentes, dez créditos cada, quarenta e vinte. Desvio de títulos de fechamento em F4. |

A densidade maior dos relatórios vem da descrição, execução e desfecho separados; os pitches sintetizam a mesma análise. Os exemplos 4D/3E tratam pedidos internos e não transportam achados, números ou contexto varejista do exemplo da autora. Não encontrei promessa de eficácia ou resultado experimental inventado nesses seis modelos.

## Observações de orientação

A frase `somente D1/D2 exige parcial`, em `relatorio-4d/SKILL.md:56`, merece explicitar `quando D3/D4 estavam previstas`: isolada, pode sugerir conflito com a pocket completa. Contudo está sob `Passos de análise: aplicação integral de referência`, e a checagem final subordina os itens ao escopo. Essa limitação permite a leitura correta; não a conto como rejeição comprovada da pocket. Não encontrei contradição equivalente nos SKILL.md de 3E e 5C.

## Mutações executadas

| Mutação | Regra | Prova estreita | Estado |
| --- | --- | --- | --- |
| M1: limite de blocos 4 → 5 | AC27 / C8 | `test_slide_density` | Sobreviveu (`not`); confirma F3 |
| M2: remover comparação de nome e significado standard | AC10–12 / C5 | `test_standard_methods` | Sobreviveu (`not`); confirma F2 |
| M3: limite de palavras 140 → 141 | AC27 / C8 | `test_slide_density` | Morta (`killed`); limite de palavras protegido |

O arquivo `mutations.json` contém os snippets únicos confirmados na árvore. O builder executou as mutações em f2553f5 e informou 20 provas verdes, M1 e M2 sobreviventes e M3 morta. A execução autorizada pelo fluxo é `PATH=/private/tmp/eric-pptx-validation-venv/bin:$PATH python3 /Users/mayoub/.agents/skills/tlc-spec-lean/scripts/check_proofs.py entregaveis_oficiais --mutations .specs/features/entregaveis_oficiais/mutations.json`, fora do sandbox para o journal de restauração em `.git` e o Chrome. Os resultados confirmam as lacunas F2 e F3. O estado FAIL permanece até corrigir e fechar os quatro achados, com nova execução das provas e das mutações pelo builder.

## Correções do builder

Os quatro achados foram corrigidos no commit `616653b`, preservando os relatos e os resultados da revisão inicial. C18 foi acrescentado para tornar explícita a obrigação de receita visível nas parciais e inconclusivas. A regra D1/D2 da skill 4D também foi esclarecida: parcial quando faltam etapas previstas; pocket completa quando o recorte foi documentado. Provas e mutações serão reconferidas no commit corrigido.

## Reconferência final

O verdict inicial da revisão independente foi FAIL. Os achados permanecem acima com suas evidências originais e com o commit que os corrigiu. O builder executou `check_proofs.py entregaveis_oficiais --mutations mutations.json` em `616653b`: 21 provas passaram; M1, M2 e M3 foram mortas; zero falhas e árvore de produção limpa. O passeio real pelo Studio e pela galeria também passou. A suíte completa corrigida terminou com 349 testes e 2.408 subtestes verdes.

Os fechamentos foram conferidos nos seis JSONs regenerados: 4D liga a visão compartilhada ao 3E e à responsabilidade pela atualização; 3E explicita rota e critério antes da construção; 5C condiciona a preferência pela consulta à atualização e ao acesso. As variantes pocket e adaptadas têm conclusões próprias. Não foi necessária nova rodada de avaliação visual vinculante: os modelos visuais são inspiração.
