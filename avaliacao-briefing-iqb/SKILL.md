---
name: avaliacao-briefing-iqb
description: "Avalia pelo IQB do ERIC a qualidade da Entrevista Inicial de sete campos ou do Briefing de uma página: 40 critérios binários de clareza, evidências, resultados e acionabilidade, com vetos, notas por dimensão, IQB de 1 a 5 e classificação calculados por script. Use para nota, auditoria, checklist ou comparação de versões desses documentos, inclusive quando perguntarem se estão bons para seguir. Identifique qual documento foi avaliado e suas fontes. Não use para escrevê-los ou melhorá-los (use briefing-inovacao), priorizar a oportunidade (use potencial-inovacao) ou medir a maturidade das evidências do projeto (use scorecard-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.9"
---

# Avaliação IQB da Entrevista Inicial ou do Briefing

Avalia a qualidade da Entrevista Inicial de sete campos ou do Briefing de uma página pela rubrica interna IQB; não mede maturidade do projeto pelo Scorecard da Strategyzer.

## Leia primeiro

- [Rubrica IQB](references/iqb-rubric.md) — critérios, vetos e reauditoria.
- [Schema do relatório](references/briefing-validation-report.schema.json) — saída estruturada opcional.

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

1. Identifique se o documento avaliado é a Entrevista Inicial de sete campos ou o Briefing de uma página, sua versão, HMW, sete campos identificáveis e fontes/localizadores. No Briefing, os campos podem estar condensados; não presuma conteúdo omitido a partir da Entrevista Inicial sem citá-la como fonte. Transcrição é reconstrução, não aprovação; pergunte apenas por fontes, versões ou definições decisivas. Intenção não substitui evidência. Se o pedido não deixar claro que o usuário quer a nota formal do IQB, e não apenas uma leitura geral, confirme isso antes de aplicar os 40 critérios.
2. Responda `yes`/`no` aos dez itens de cada família `CLA`, `EVI`, `OUT`, `ACT`, inclusive vetos. Ausência ou ambiguidade contam `no`; registre lacuna, evidência e localização, sem inventar itens. No relatório estruturado, indique `initial_interview` quando a evidência vem da Entrevista Inicial e `briefing` quando vem do Briefing.
3. Grave as 40 respostas booleanas justificadas em JSON (formato em `scripts/iqb.py`); rode `python3 scripts/iqb.py respostas.json`. Copie contagens, notas brutas/finais, tetos, média e classificação; não recalcule nem ajuste editorialmente.
4. Com amplitude das quatro notas finais ≤1, reaudite cada resposta e evidência. Notas próximas podem estar corretas; não force dispersão.
5. Entregue matriz citada, vetos, IQB, classificação, até três pontos fortes sustentados, lacunas priorizadas e até três provocações relevantes ao sponsor. Declare a ausência no resumo quando não houver itens. Fonte decisiva inacessível exige diagnóstico parcial antes da nota final. Compare versões calculando cada uma separadamente; IQB alto não aprova projeto ou experimento.

## Exemplo

Entrada: “Avalie pelo IQB a Entrevista Inicial do Portal de Solicitações de Dados.”
Saída (trecho):
> EVI-06: no — briefing.md, Evidências: somente suposições.
> Veto: evidências limitadas a 1; números derivados de `scripts/iqb.py`.
> Próximo dado: registro que demonstre ocorrência do problema.

## Checagem final

- [ ] 40 critérios, respostas e fontes/localizadores registrados
- [ ] Ausências, vetos e notas brutas/finais expostos
- [ ] Cálculo copiado do script; reauditoria quando amplitude ≤1
- [ ] Versões comparadas independentemente; lacunas priorizadas

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `briefing_validation`: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.
O campo técnico `briefing_version_id` identifica a versão do documento avaliado;
indique no texto se ela é da Entrevista Inicial ou do Briefing.

**Proveniência:** rubrica, schema e cálculo adaptados de fonte metodológica RC6 (`validate-briefing/`); o cálculo foi endurecido para impedir pontuação com itens ausentes.
