---
name: relatorio-3e
description: "Compila ou revisa o Relatório 3E: solução e escopo, plano de construção com responsáveis e prazos, Test Cards individuais prospectivos e decisão de rota (interna, externa, híbrida ou indefinida), separando plano de evidência observada. Use quando houver registros de E1 a E3 ou material equivalente e o usuário quiser o relatório ou os Test Cards consolidados. Não use para facilitar o workshop (use workshop-3e) nem para analisar resultados de testes já executados (use experimentacao-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.1"
---

# Compilar o Relatório 3E

Consolida solução, construção, experimentos e rota; separa plano, execução e reconstrução posterior.

## Leia primeiro

- [Playbook 3E](references/3e-solution-structuring-playbook.md) — estrutura do relatório.
- [Test Card](assets/test-card.md) — quatro campos por teste.
Para conferir a fonte: [transcrição](<assets/Modelo 3E Estruturacao da Solucao.transcricao.md>), [DOCX](<assets/Modelo 3E Estruturacao da Solucao.docx>), [divergências](references/fonte-3e-e-divergencias.md), [original RC6](assets/3e-solution-structuring-playbook-original-rc6.md). Preserve originais; registre diferença e data.

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

A fase do projeto é contexto, não pré-requisito. Se o pedido vier antes do momento
usual, entregue preparação ou versão parcial; se vier depois, use o material posterior
com data e não apresente reconstrução como plano combinado previamente.

## Passos

1. **Entrada:** identifique fontes, versões, participantes e decisões de hipótese, problema, 4D, BP1, E1–E3 e experimentação que existirem. Não exija documentos alheios ao projeto. Em modo assíncrono, indique registros substitutos e deliberações ausentes; etapas incompletas exigem parcial. Não atribua aprovação a ausentes nem reescreva decisões anteriores.
2. **Solução/valor:** problema focal, população, hipótese master, escopo, componentes `agora/futuro/fora`, riscos e limites. Expectativa não é resultado observado.
3. **Construção:** recursos, itens a desenvolver, dependências, responsável, apoio e prazo por ação; exponha lacunas antes de declarar MVP pronto.
4. **Experimento:** suposições prioritárias, público elegível, método, intervenção, medida, fonte e critério. Entregue Test Card individual por teste com hipótese, teste, medida e critério, uma frase objetiva por campo (até 280 caracteres); tabela é só índice. Critérios/limiares sem baseline ficam `a fechar antes da coleta`. Preserve originais; cards reconstruídos são retrospectivos. Resultados existentes precisam de fontes/data; Learning Cards somente após execução, nunca achados antes do teste.
5. **Rota:** registre `internal`, `external`, `hybrid` ou `undecided` com fonte e decisão efetiva. Externa/híbrida: o que buscar; interna: o que construir; indefinida: dependências abertas. Rota não valida solução.
6. Confira relatório/cards/fontes; indique decisões, dados e autorizações necessários ao próximo uso. `experimentacao-inovacao` pode detalhar protocolo/analisar resultados, mas o pacote funciona isoladamente.

## Exemplo

Entrada: “Consolide o 3E do Portal de Solicitações de Dados.”
Saída (trecho):
> Rota híbrida: decisão documentada, capacidades internas/externas distintas.
> TC-01: hipótese, teste, medida e critério prévios.
> Construção planejada não é evidência de eficácia.

## Checagem final

- [ ] Fontes, versão e cronologia preservadas
- [ ] Escopo, construção e lacunas explícitos
- [ ] Cards individuais com quatro campos e status correto
- [ ] Rota sustentada; aprovação não inferida
- [ ] Plano separado de evidências e próximos passos

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `three_e_report` e `test_card` por teste: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** reescrita de fonte metodológica RC6 (`compile-3e-report/`), com separação entre plano, execução e reconstrução posterior, sem restrição por fase.
