---
name: briefing-inovacao
description: "Cria, reconstrói ou atualiza o briefing de sete campos de um desafio de inovação da CCEE (título, HMW, problema, relevância, resultados esperados, responsável, sponsor) e, quando pedido, gera a síntese executiva de uma página (one-page) ou perguntas para fechar lacunas do briefing. Use sempre que o usuário quiser escrever, preencher, revisar, versionar ou resumir um briefing, transformar entrevista ou transcrição em briefing, formular um 'how might we', montar uma one-page ou perguntas ao sponsor, mesmo sem dizer 'briefing'. Não use para dar nota ao briefing (use avaliacao-briefing-iqb) nem para priorizar oportunidades (use potencial-inovacao)."
---

# Briefing de inovação

Produz briefing, one-page ou perguntas de melhoria conforme solicitado; a criação não atribui nota IQB a si própria.

## Leia primeiro

- [Sete campos](references/briefing_template.md) — estrutura do briefing.
- [Schema](references/briefing.schema.json) — integração JSON.

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

1. Leia entrevistas, CDT, dados, versões e decisões. Separe problema, interpretação, causas supostas e soluções; pergunte apenas por lacunas que mudem a saída.

### Modo briefing

2. Preencha título, HMW, problema/oportunidade, relevância, resultados, responsável e sponsor. Preserve HMW original; reformulação separada. Resultados são mudanças, não funcionalidades. Números exigem fonte, período e unidade; hipótese não vira fato. Marque campos pendentes e quem/dado pode resolvê-los.
3. Para melhorar, crie nova versão do mesmo briefing, ligada à base e aos novos insumos; não sobrescreva nem invente outro tipo. Em conversa, mantenha conteúdo e linhagem.

### Modo one-page

4. Condense versão identificada sem acrescentar evidência ou impacto. Se ausente, reconstrua versão provisória rotulada. Preserve nuances, lacunas, `briefing_version_id` e fontes adicionais. Use [schema](references/briefing-one-page.schema.json), variante `executive_one_page`: A4 paisagem, uma página, fonte mínima preservada.

### Modo perguntas

5. Use versão identificada/provisória e IQB disponível. Priorize lacunas verificáveis, depois exploração; indique campo, fonte consultada, razão e respondente. Remova duplicatas; limite inicial de 12 perguntas, novas fronteiras após respostas. IQB alto não impede investigação. Use [schema](references/briefing-improvement-questionnaire.schema.json); não invente respostas.

## Exemplo

Entrada: “Gere o briefing do Portal de Solicitações de Dados.”
Saída (trecho):
> Sponsor: pendente — entrevista-ana.md não identifica designação.
> Meta de 30%: proposta não aprovada, conforme email-meta-proposta.md.
> Pergunta: quem foi designado sponsor?

## Checagem final

- [ ] Saída solicitada entregue, completa ou parcial
- [ ] Fatos rastreáveis; responsáveis sustentados
- [ ] HMW e versão-base preservados; nenhum arquivo sobrescrito
- [ ] One-page/perguntas vinculadas ao briefing correto
- [ ] Sem gerar automaticamente os três modos

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Para PDF, DOCX, MD, TXT ou PPTX, siga [o design system](assets/design-system/README.md)
com `deliverable_type` `briefing`, `briefing_one_page` ou `briefing_improvement_questionnaire`: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** adaptação das três skills homônimas das fontes metodológicas do RC6, com a estrutura de briefing do ERIC_RC1 preservada nos recursos locais. Funciona sem infraestrutura da iniciativa de origem.
