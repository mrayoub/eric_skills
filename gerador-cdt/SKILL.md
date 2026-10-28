---
name: gerador-cdt
description: "Gera, a partir dos entregáveis da esteira ERIC, um Cadastro de Demanda Tecnológica (CDT) de qualidade para a área abrir no Jira e levar à Diretoria de Tecnologia. Entrega dois arquivos: a CDT, só com os campos para copiar e colar (Rótulo Epic com título tecnológico, Descrição com as cinco perguntas do comunicado interno sobre escopo, Justificativa e Benefícios), e a Análise da CDT, com o checklist do comunicado em destaque, o que obter e analisar primeiro, pontos fortes e fracos e a origem dos dados. Conhece os 28 campos do formulário para raciocinar com coerência. Use quando o usuário pedir para abrir, preencher, montar, revisar ou completar uma CDT, levar a demanda para a Tecnologia ou TI, ou organizar o escopo para o Jira. Não use para pedir a decisão da gestão (use relatorio-final-inovacao) nem para escrever a Entrevista Inicial ou o Briefing (use briefing-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX e PDF."
  author: "GEIN-CCEE"
  version: "1.3.1"
---

# Gerador de CDT

CDT é o Cadastro de Demanda Tecnológica, aberto no Jira. Esta skill transforma o que a esteira produziu em dois
arquivos: a **CDT**, com os quatro campos que a pessoa copia e cola no Jira, e a **Análise da CDT**, que mostra se a
demanda está pronta para envio e o que falta obter. A CDT não é o relatório do projeto: é curta, direta e deixa o
detalhe para os anexos.

## Leia primeiro

- [Campos da CDT](references/campos-jira.md): o que cada arquivo traz, padrão de escrita, Rótulo Epic, Descrição,
  Justificativa e Benefícios, os 28 campos do formulário, coerência entre campos e insumos da esteira.
- [Publicação sobre escopo](references/publicacao-escopo-tecnologia.md): as cinco perguntas da Descrição e o
  checklist.
- [Qualidade e veracidade](references/qualidade-e-veracidade.md): a Análise da CDT, com estado, checklist, o que
  obter e analisar primeiro, avaliação crítica e origem dos dados.
- [Esteira ERIC](references/eric-esteira.md): o que é a CCEE, as etapas da esteira, BP1/BP2, rotas e relações entre
  entregáveis. Leia antes de interpretar qualquer insumo.
- [Grilling operacional](references/grilling-operacional.md) e o
  [levantamento documental](references/grilling-operacional.md#5-complementos-de-levantamento-documental):
  mapa afirmação → fonte → natureza → limite → campo afetado.

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md) antes de sintetizar,
pontuar ou planejar, e reaplique-o a cada arquivo ou resposta novos. Em resumo: resolva
nos arquivos tudo que for pesquisável; pergunte só a fronteira de questões decisivas
cujas dependências já estão resolvidas; registre origem e localizador de cada resposta;
entregue versão parcial quando faltar suporte decisivo. Nunca pergunte a nota, o
resultado ou a conclusão desejada: isso não é dado, e contaminaria a avaliação.
Na CDT, cada campo do Jira é uma questão do registro: o dado sem fonte que o usuário
não souber vira lacuna "[COMPLETAR: ...]" e entra na análise, nunca é completado por suposição.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Quando usar

A fase do projeto é contexto, não pré-requisito. O caso típico é depois do BP2, na implementação com rota interna ou
híbrida. Quem abre a CDT é a gerência que patrocinou a esteira, e a decisão de seguir já foi tomada. Com material
insuficiente, entregue a CDT mesmo assim, com lacunas "[COMPLETAR: ...]" no que falta. Se a rota for externa, diga o
que muda no pedido à Tecnologia em vez de pedir construção.

## Passos

1. **Inventário.** Liste os entregáveis recebidos com data, versão e estado de leitura e identifique a decisão
   vigente mais recente.
2. **Raciocine com o formulário inteiro.** Percorra os 28 campos ([campos](references/campos-jira.md#os-28-campos-do-formulário))
   para saber se há risco de não implementar, qual benefício é mensurável, se a demanda é regulatória e se as
   respostas se contradizem. Esses campos não são entregues; o que faltar vai para a análise.
3. **CDT, quatro blocos, nesta ordem.** Rótulo Epic: uma linha que nomeia a tecnologia (plataforma, sistema,
   ferramenta, integração, interface) e o que ela faz, sem nada que sugira uma pessoa. Descrição: um bloco só, com as
   cinco perguntas do comunicado como subtítulos em negrito, sempre respondidas, cada uma a partir da sua fonte
   principal (Briefing, todo o material, Relatório 4D, Relatório 3E, Relatório 3E; o Relatório final em todas;
   [de/para](references/campos-jira.md#fonte-principal-de-cada-pergunta)). Nada contradiz o Relatório final.
   Justificativa: os riscos de não implementar, um por linha. Benefícios: o principal com número na primeira linha.
   Markdown só na Descrição; nenhuma fonte no texto.
4. **Voz da gerência.** Escreva como a gerência que abre a CDT: primeira pessoa do plural ("nossa equipe",
   "aprovamos"), frases afirmativas e diretas, sem perguntas fora dos subtítulos, sem "a confirmar" e sem expressões
   de texto gerado por IA ([padrão de escrita](references/campos-jira.md#padrão-de-escrita)). O que faltar vira
   lacuna "[COMPLETAR: o dado]".
5. **Corte.** Cada fato aparece uma vez; siglas por extenso na primeira menção de cada campo; nada de narrar o
   método da esteira. Limites: 16 palavras no Rótulo Epic, 150 por pergunta da Descrição, 80 na Justificativa e nos
   Benefícios.
6. **Análise da CDT.** Estado; em destaque, o checklist do comunicado (regras e responsáveis respondidos na linha) e
   o que obter e analisar primeiro, em ordem de prioridade; depois avaliação crítica e origem dos dados, com as
   fontes ([qualidade](references/qualidade-e-veracidade.md)). Rode `python3 scripts/checar_cdt.py cdt.json
   analise.json` até o código 0; com lacunas, os dois arquivos são `partial`.
7. **Entregue.** No chat: o estado, onde estão os arquivos, as lacunas a preencher e o principal ponto fraco. Não
   repita a CDT no chat.

## Exemplo

Entrada: "Monte a CDT do formulário de pedidos de dados com o briefing, os relatórios 4D e 3E e o relatório final."
Saída (CDT, para colar no Jira):

```
Rótulo Epic

Formulário web com protocolo automático para pedidos de dados históricos no portal de atendimento

Descrição

**Qual problema queremos resolver?**
Queremos que os pedidos de dados históricos cheguem completos na primeira tentativa. Hoje recebemos esses pedidos por
e-mail, sem padrão: cerca de 4 em cada 10 voltam ao agente para complemento.
...
**O que é prioridade neste momento?**
**Essencial**
- Formulário com campos obrigatórios por tipo de pedido.

Justificativa

Retrabalho contínuo: os pedidos incompletos continuam consumindo horas da nossa equipe de atendimento.

Benefícios

Reduz de [COMPLETAR: horas mensais gastas hoje] para 15 as horas mensais da nossa equipe com complementos.
```

## Checagem final

- [ ] CDT com só Rótulo Epic, Descrição, Justificativa e Benefícios, nesta ordem, sem fonte e sem cabeçalho no MD e no TXT
- [ ] Rótulo Epic tecnológico, sem termo que sugira pessoa
- [ ] Descrição num bloco só, com as cinco perguntas na ordem e respondidas; Markdown só nela
- [ ] Texto da gerência em primeira pessoa, direto, sem perguntas, sem "a confirmar" e sem contradizer o Relatório final
- [ ] O que falta como "[COMPLETAR: ...]", com cada lacuna listada na análise
- [ ] Análise com estado, checklist e prioridades em destaque, avaliação crítica com pontos fracos e fontes na origem dos dados
- [ ] `scripts/checar_cdt.py` sem erros; mesmo estado nos dois arquivos, em `readiness` e no chat

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de Energia Elétrica). A CCEE
viabiliza a comercialização de energia elétrica no Brasil; "agente" pode ser uma organização participante do
mercado, não uma pessoa. Consulte [a esteira](references/eric-esteira.md) para interpretar etapas, BP1/BP2, rotas e
relações entre entregáveis; a CDT costuma nascer na etapa 8 (implementar).

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md), revise com o [guia de escrita](references/guia-de-escrita.md) e não use travessão no chat e nos arquivos; siga
[o design system](assets/design-system/README.md). Monte dois JSON canônicos:

- `deliverable_type` `cdt`: um `heading` e um `paragraph` para cada campo, com `data.section_key` `jira_title`,
  `description`, `justification` e `benefits`, nessa ordem, e `citation_ids` em cada parágrafo.
- `deliverable_type` `cdt_analysis`: `readiness`, `publication_checklist`, `data_to_obtain` (seguido da tabela de
  prioridades), `quality_review` e `traceability` (seguido da tabela de fontes).

Rode o `checar_cdt.py` com os dois, depois `python3 assets/design-system/scripts/render.py <arquivo>.json --out-dir
saida` para cada um, e entregue os JSON junto dos derivados. Da CDT, o MD e o TXT trazem só os campos, prontos para
colar no Jira; o PDF e o DOCX servem para revisão. Com lacunas, marque `metadata.completeness: "partial"`
nos dois arquivos; se a validação falhar, corrija o conteúdo: nunca contorne o schema.

**Proveniência:** estrutura adaptada de publicação interna da CCEE sobre definição de escopo
(`references/publicacao-escopo-tecnologia.md`, anonimizada), do formulário da CDT no Jira levantado com o usuário em
23/10/2026 e de uma CDT real usada como padrão de escrita (anonimizada), e da metodologia ERIC deste repositório.
