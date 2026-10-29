---
name: potencial-inovacao
description: "Pontua e classifica o potencial de uma dor ou oportunidade de inovação com a rubrica interna do ERIC (impacto 30%, viabilidade 25%, alinhamento estratégico 20%, urgência 15%, novidade 10%), resultando em priorizar, monitorar ou arquivar, com justificativa e fonte por critério e cálculo por script. Use quando o usuário quiser priorizar, ranquear, triar ou comparar oportunidades, ideias ou dores, decidir se vale investir nelas ou revisar uma priorização já feita. Não use para dar nota a um briefing (use avaliacao-briefing-iqb) nem para avaliar a força das evidências de um projeto em andamento (use scorecard-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.26"
---

# Potencial de inovação

Pontua oportunidades pela rubrica interna do ERIC.
Não avalia maturidade de evidências (Scorecard da Strategyzer) nem resultados experimentais.

## Leia primeiro

- [Rubrica de potencial](references/innovation-potential-rubric.md): critérios, pesos, faixas e a regra de ausência.
- [Levantamento documental](references/grilling-operacional.md#5-complementos-de-levantamento-documental): mapa afirmação → fonte.

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md) antes de sintetizar,
pontuar ou planejar, e reaplique-o a cada arquivo ou resposta novos. Em resumo: resolva
nos arquivos tudo que for pesquisável; pergunte só a fronteira de questões decisivas
cujas dependências já estão resolvidas; registre origem e localizador de cada resposta;
entregue versão parcial quando faltar suporte decisivo. Nunca pergunte a nota, o
resultado ou a conclusão desejada: isso não é dado, e contaminaria a avaliação.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Quando usar

A fase do projeto é contexto, não pré-requisito. Se o pedido vier antes do momento
usual, entregue preparação ou versão parcial; se vier depois, use o material posterior
com data e não apresente reconstrução como plano combinado previamente.

## Passos

1. Delimite oportunidade, público, versão e decisão de priorização. Registre a fase como contexto.
2. Para impacto, viabilidade, alinhamento, urgência e novidade, registre afirmação, evidência favorável/contrária, fonte/localizador, limite e nota 0 a 100 justificada. Distinga impacto esperado/medido, viabilidade percebida/recurso comprometido e urgência documentada/preferência do sponsor; essas diferenças afetam a nota.
3. Sem base, marque `não pontuável` e investigue fonte ou responsável. Zero exige avaliação sustentada; usá-lo para lacunas muda a classe.
4. Grave as cinco notas justificadas em JSON (formato no topo de `scripts/score.py`); rode `python3 scripts/score.py notas.json`. Use total e classe sem ajuste editorial; com status `incomplete`, entregue avaliação parcial, sem classe.
5. Mostre notas, fontes, pesos, total, classe, sensibilidades (limiares de classe) e próximos dados. Registre a decisão tomada separada da recomendação calculada.

## Exemplo

Entrada: "Classifique a oportunidade 'triagem guiada de solicitações' com a planilha de volumes e a ata do comitê."
Saída (trecho):
| Critério | Nota | Fonte | Limite |
|---|---|---|---|
| Impacto | 60 | planilha-volumes.xlsx, aba 2, C4: 120 solicitações/mês com retrabalho | redução não medida |
| Viabilidade | não pontuável | não se aplica | sem estimativa de custo; responsável: TI (a confirmar) |
Status do script: `incomplete` → sem classe; próximo dado: estimativa de custo da TI.

## Checagem final

- [ ] Cada nota tem justificativa e fonte com localizador
- [ ] Nenhuma lacuna virou zero
- [ ] Total e classe vieram de `scripts/score.py`
- [ ] Recomendação calculada separada da decisão tomada
- [ ] Sensibilidades e próximos dados listados

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md), revise com o [guia de escrita](references/guia-de-escrita.md) e não use travessão no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `innovation_potential_assessment`: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"`: nunca contorne o schema.

Na versão completa, o bloco `table` com `data.section_key = "scores"` exige as cinco linhas com `criterion`, `score`, `weight`, `justification`, além de `overall_score` e `classification` iguais ao resultado do script.

**Proveniência:** rubrica e algoritmo adaptados do RC6 (`calculate-innovation-potential/`), revistos para preservar incompletude em vez de classificar faltas como zero.
