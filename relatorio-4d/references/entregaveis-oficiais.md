# Entregáveis oficiais 4D

Esta receita orienta Relatório oficial 4D e Apresentação oficial 4D, padrão da skill. Leia também
[o tom comum](tom-oficial.md), derivado da apresentação 5C da autora do playbook. As estruturas antigas continuam
acessíveis como depreciadas; não aplique seus limites de slides ou listas fixas de seções aos oficiais.

## Playbook como referência, aplicação como registro

Padrão do 4D: D1 Descongelar; D2 Diagnosticar; D3 Desenhar; D4 Decidir.
Use os significados de `assets/design-system/official-methods.json` no inventário de uma aplicação padrão.
Não copie participantes, horários, votos ou resultados do playbook como se fossem de uma execução real.

As três skills de relatório admitem adaptações de nome, significado, ordem, dinâmica, duração e quantidade de fases,
além de versões pocket. Registre cada sessão separadamente, seu objetivo, formato, profundidade e cobertura.
Explique padrão do playbook, aplicação efetiva, motivo e fontes. Não interprete o significado só pela letra.
Uma etapa pode corresponder a várias oficiais, ou não ter correspondência; explique esses casos na estruturação.

**Fora do escopo por desenho:** não ocorreu porque a sessão não a previa. **Lacuna de registro:** era prevista, mas
não há registro suficiente. **Omitida na apresentação:** conteúdo existente não exibido por uma decisão editorial;
isso não altera o que foi executado. Nos oficiais, as sínteses das etapas aplicadas e o fechamento são obrigatórios.
Não transfira uma lacuna para fora do escopo só para obter uma versão completa.

Uma pocket pode estar completa no seu escopo: 5C remoto com C1 a C3 e confirmação curta, sem C4 e C5; 4D com D1 e D2;
ou 3E com E1 e E2, se esse recorte estiver documentado. Esses exemplos não impõem que toda pocket tenha o mesmo corte.
Se houver sessão curta e sessão integral, preserve a contribuição e os limites de cada uma, sem atribuir votação,
cocriação ou decisão a quem não participou dessas etapas. A conexão com a esteira é contexto, não bloqueio de uso.

## Relatório oficial

Use `four_d_official_report`. A ordem é:

1. **Título e legenda:** assunto no `title`; finalidade em `purpose`, explicando para que serve e quem usará.
2. **Introdução (`introduction`):** origem do desafio, briefing disponível, preparação, execução e direcionamento.
   Antecedente inexistente deve ser explicitado, sem criar uma fonte fictícia.
3. **Estruturação (`structuring`):** por que o método foi usado, escolha do formato, empresas ou perfis participantes,
   etapas, ferramentas e modelo; justificativas registradas, adaptações e exclusões. Na falta do motivo, investigue;
   se não houver resposta, registre motivo não registrado e o limite que isso cria.
4. **Cada etapa aplicada, em ordem:** descrição da etapa e de seu significado (`<id>_description`), execução realizada
   (`<id>_execution`) e desfecho (`<id>_outcome`). Três textos distintos, com fontes. Títulos e tabelas não os substituem.
5. **Conclusão (`conclusion`):** sintetize análise e resultados do trabalho realizado, alcance e questões abertas.
6. **Recomendações e próximos passos (`recommendations`):** direcione ações, decisões e aprovações necessárias,
   com responsáveis e prazos registrados ou a definir. Separe recomendação de decisão efetiva.

Preserve a profundidade analítica própria do método: padrões e hipótese sustentada no 4D; relação com as dores,
escopo, construção, rota e Test Cards prospectivos no 3E; escuta, critérios, propostas, prioridades e divergências no
5C, conforme as etapas cobertas. Esses conteúdos entram nos desfechos, conclusão e recomendações, sem substituir
outra receita. E3 planeja experimentos; não declare aprendizado empírico antes da execução dos testes.

## Apresentação oficial

Use `four_d_official_presentation`, na mesma base de fontes e conclusões do relatório:

1. **Contextualização (`challenge_context`):** trajetória do desafio, o que já foi feito e pergunta desta aplicação.
2. **Estruturação (`structuring`):** o que é o método, por que foi aplicado e como foi adaptado, se for o caso.
3. **Execução (`execution_<id>` por etapa aplicada):** síntese dos achados, com evidências e linha de leitura.
4. **Conclusão (`conclusion`):** desfecho da aplicação, proporcional ao escopo e às evidências.
5. **Recomendações (`recommendations`):** próximos passos e dependências.
6. **Decisão (`decision`):** quando necessário, pedido de deliberação, alternativas relevantes, quem decide e limites.
7. **Call to action (`call_to_action`):** ação solicitada ao público, destinatário e prazo registrado ou a definir.

Declare `metadata.decision_required` como booleano. `true` exige o slide de decisão; `false` permite omiti-lo.
Se a necessidade é desconhecida, registre a pendência em versão parcial, sem assumir `false` para declarar completa.
Os títulos dos slides comunicam uma conclusão em 4 a 14 palavras; cada slide tem até 4 blocos e 140 palavras, com
mensagem da capa em até 35 palavras. Divida conteúdos extensos em slides; não há limite legado de seis slides.

## JSON e validação

Use o envelope comum e `metadata.method_application.sessions`, uma lista ordenada. Cada sessão tem:

- `id`: identificador estável; `variant`: `standard`, `adapted` ou `pocket`;
- `stages`: etapas na ordem aplicada, cada uma com `id`, `label`, `meaning` e `official_stage_ids`;
- `out_of_scope_stages`: lista de `official_stage_id` e `reason` para exclusões por desenho;
- `adaptation_reason`: motivo, obrigatório nas variantes adaptadas e pocket.

IDs de etapas são únicos em todo o documento. Para sessões combinadas, use prefixos como `remoto_c1` e
`presencial_c1`. A lista `official_stage_ids` pode ser múltipla ou vazia; uma relação inexistente exige explicação
visível em `structuring`. Em cada sessão, toda etapa do playbook tem correspondência ou exclusão explícita.
Metadados não substituem o texto: a estruturação e as etapas explicam escopo, significado e desfecho ao leitor.

No relatório, use `<id>_description`, `<id>_execution` e `<id>_outcome`; no pitch, `execution_<id>`.
Nos blocos obrigatórios, use `paragraph`, `callout` ou `metric` com `data.text` não vazio e `citation_ids` com
localizadores existentes. Use `heading` da mesma seção para os títulos; resumo, título ou tabela isolados não bastam.
Mantenha a ordem da receita nos blocos e o inventário coerente nos dois oficiais. Sem registro de etapa prevista,
entregue parcial ou inconclusivo com a pendência, preservando os campos e sem antecipar resultados.

O renderer valida o schema e o significado estrutural do inventário antes de gerar derivados. Relatórios são A4
paisagem; apresentações, 16:9. Os layouts reaproveitam a identidade visual existente. Gere JSON, PDF, HTML e DOCX
ou PPTX pelo script incluído, entregando o JSON e manifesto com os arquivos de leitura.
