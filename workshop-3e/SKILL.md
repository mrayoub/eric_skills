---
name: workshop-3e
description: "Prepara, conduz ou registra o workshop 3E de estruturação da solução: E1 esclarecer hipótese e escopo, E2 estruturar componentes (precisa ter, pode evoluir, fora do recorte) e E3 planejar experimentos com Test Cards individuais da Strategyzer. Use para montar pauta, perguntas, board ou registrar as decisões do grupo sobre a solução candidata. Não use para compilar o relatório 3E (use relatorio-3e) nem para planejar em detalhe ou analisar uma rodada de experimentação (use experimentacao-inovacao)."
---

# Facilitar o 3E

Prepara, conduz ou registra a solução candidata em E1–E3; preserva decisões, propostas e cronologia.

## Leia primeiro

- [Playbook 3E](references/3e-solution-structuring-playbook.md) — dinâmicas e tempos.
- [Test Card](assets/test-card.md) — quatro campos individuais.
Para conferir a fonte: [transcrição](<assets/Modelo 3E Estruturação da Solução.transcricao.md>), [DOCX](<assets/Modelo 3E Estruturação da Solução.docx>), [divergências](references/fonte-3e-e-divergencias.md), [original RC6](assets/3e-solution-structuring-playbook-original-rc6.md). Preserve originais e registre diferenças/data.
[Blueprint Mural](references/mural-board-3e-template.md) opcional: ferramenta autorizada ou registro manual.

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md) antes de sintetizar,
pontuar ou planejar, e reaplique-o a cada arquivo ou resposta novos. Em resumo: resolva
nos arquivos tudo que for pesquisável; pergunte só a fronteira de questões decisivas
cujas dependências já estão resolvidas; registre origem e localizador de cada resposta;
entregue versão parcial quando faltar suporte decisivo. Nunca pergunte a nota, o
resultado ou a conclusão desejada — isso não é dado, e contaminaria a avaliação.

## Quando usar

A fase do projeto é contexto, não pré-requisito. Se o pedido vier antes do momento
usual, entregue preparação ou versão parcial; se vier depois, use o material posterior
com data e não apresente reconstrução como plano combinado previamente.

## Passos

Prepare hipótese, problema, 4D, BP1, resultados e restrições existentes; não exija fase específica. Pergunte só por solução, papéis, dados e prazos não documentados; formule decisão neutra.

1. **E1 — Esclarecer:** explicite hipótese de origem, dor, público, o que a solução é/não é/não resolve agora. Resultados esperados são hipóteses; critérios apontam medidas verificáveis ou lacunas.
2. **E2 — Estruturar:** classifique `precisa ter`, `pode evoluir`, `fora deste recorte`. Separe existente de construção/contratação; registre ação, responsável, apoio, dependência e prazo sem inventá-los.
3. **E3 — Experimentar:** priorize suposições pelo risco; escolha método apropriado, não automaticamente think aloud. Produza Test Card individual por teste: hipótese, teste, medida, critério, uma frase objetiva por campo (até 280 caracteres); detalhes ficam no plano. Feche medidas/critérios verificatórios antes da execução; ausência de baseline/limiar mantém rascunho. Planeje evidências para Learning Cards; somente após execução registre achados. Distinga cards originalmente pactuados de reconstruções retrospectivas.

Registre quem assumiu dependências e quando, separando decisão de sugestão. Tempos são sugestões, não prova de conclusão; etapa ausente mantém registro parcial e impacto da lacuna. `relatorio-3e` compila; `experimentacao-inovacao` pode detalhar/analisar testes, sem ser dependência obrigatória.

## Exemplo

Entrada: “Prepare o 3E do Portal de Solicitações de Dados.”
Saída (trecho):
> E3: testar checklist contra gabarito independente.
> Test Card: critério pendente de baseline; rascunho.
> Sem coleta, nenhum Learning Card preenchido.

## Checagem final

- [ ] E1–E3 e escopo registrados sem etapas inventadas
- [ ] Ações, papéis, prazos e decisões rastreáveis
- [ ] Um Test Card completo ou rascunho explícito por teste
- [ ] Método pelo risco; critérios prévios preservados
- [ ] Learning Cards somente após execução

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `three_e_workshop_record` e `test_card` por teste: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** reescrita de fonte metodológica RC6 (`facilitate-3e-workshop/`). A ordem interna E1–E3 e a separação entre plano e evidência foram preservadas sem restringir a fase de uso.
