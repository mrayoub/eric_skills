---
name: briefing-inovacao
description: "Cria, reconstrói ou atualiza a Entrevista Inicial de sete campos de um desafio de inovação da CCEE (título, HMW, problema, relevância, resultados esperados, responsável e sponsor). A partir dela, produz o Briefing de uma página ou Perguntas para fechar lacunas. Use para organizar entrevistas e transcrições, formular um 'como poderíamos', revisar a Entrevista Inicial, preparar o Briefing ou levantar perguntas ao sponsor. Não use para dar nota IQB (use avaliacao-briefing-iqb) nem para priorizar oportunidades (use potencial-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.14"
---

# Entrevista Inicial, Briefing e Perguntas para fechar lacunas

Produz Entrevista Inicial de sete campos, Briefing de uma página ou Perguntas para fechar lacunas conforme solicitado; a criação não atribui nota IQB a si própria.

## Leia primeiro

- [Sete campos](references/briefing_template.md) — estrutura da Entrevista Inicial.
- [Schema](references/briefing.schema.json) — integração JSON.

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

1. Leia entrevistas, CDT, dados, versões e decisões. Separe problema, interpretação, causas supostas e soluções; pergunte apenas por lacunas que mudem a saída.

### Entrevista Inicial de sete campos

2. Preencha título, HMW, problema/oportunidade, relevância, resultados, responsável e sponsor. Preserve HMW original; reformulação separada. Resultados são mudanças, não funcionalidades. Números exigem fonte, período e unidade; hipótese não vira fato. Marque campos pendentes e quem/dado pode resolvê-los.
3. Para melhorar, crie nova versão da mesma Entrevista Inicial, ligada à base e aos novos insumos; não sobrescreva nem invente outro tipo. Em conversa, mantenha conteúdo e linhagem.

### Briefing

4. Condense a versão identificada da Entrevista Inicial em um Briefing de uma página, sem acrescentar evidência ou impacto. Se ausente, reconstrua uma versão provisória rotulada. Preserve nuances, lacunas, `briefing_version_id` (identificador técnico da versão da Entrevista Inicial) e fontes adicionais. Use [schema](references/briefing-one-page.schema.json), variante `executive_one_page`: A4 paisagem, uma página, fonte mínima preservada.

### Perguntas para fechar lacunas

5. Use a Entrevista Inicial identificada/provisória e o IQB disponível. Priorize lacunas verificáveis, depois exploração; indique campo, fonte consultada, razão e respondente. Remova duplicatas; limite inicial de 12 perguntas, novas fronteiras após respostas. IQB alto não impede investigação. Use [schema](references/briefing-improvement-questionnaire.schema.json); não invente respostas.

## Exemplo

Entrada: “Gere a Entrevista Inicial do Portal de Solicitações de Dados.”
Saída (trecho):
> Sponsor: pendente — entrevista-ana.md não identifica designação.
> Meta de 30%: proposta não aprovada, conforme email-meta-proposta.md.
> Pergunta: quem foi designado sponsor?

## Checagem final

- [ ] Saída solicitada entregue, completa ou parcial
- [ ] Fatos rastreáveis; responsáveis sustentados
- [ ] HMW e versão-base preservados; nenhum arquivo sobrescrito
- [ ] Briefing e perguntas vinculados à Entrevista Inicial correta
- [ ] Sem gerar automaticamente os três modos

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `briefing` (Entrevista Inicial de sete campos), `briefing_one_page` (Briefing) ou
`briefing_improvement_questionnaire` (Perguntas para fechar lacunas): monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** adaptação das três skills homônimas das fontes metodológicas do RC6, com a estrutura de briefing do ERIC_RC1 preservada nos recursos locais. Funciona sem infraestrutura da iniciativa de origem.
