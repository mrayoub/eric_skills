---
name: gerador-cdt
description: "Gera os dados para preencher no Jira um Cadastro de Demanda Tecnológica (CDT) de qualidade, a demanda que a área leva à Diretoria de Tecnologia, a partir dos entregáveis da esteira ERIC, campo a campo como no formulário (título, Descrição com problema, objetivo, públicos, processo atual, resultados, entregas essenciais, importantes e fora do escopo, regras e responsáveis, tema, regulatório, riscos, benefícios, simplificação, solicitante e LGPD), com fonte e natureza de cada dado, checklist do comunicado de escopo, pontos fortes e fracos e os dados a obter quando o material não basta. Use quando o usuário pedir para abrir, preencher, montar, revisar ou completar uma CDT, levar a demanda para a Tecnologia ou TI, ou organizar o escopo para o Jira. Não use para pedir a decisão da gestão (use relatorio-final-inovacao) nem para escrever a Entrevista Inicial ou o Briefing (use briefing-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX e PDF."
  author: "GEIN-CCEE"
  version: "1.0.0"
---

# Gerador de CDT

CDT é o Cadastro de Demanda Tecnológica, aberto no Jira. Esta skill transforma o que a esteira produziu em uma
demanda clara e verificável para a Tecnologia: o problema, o resultado esperado e o que será entregue, separados em
essencial, importante e fora do escopo. O entregável segue o formulário do Jira campo a campo (a Demanda é o padrão;
a Iniciativa, ticket pai, só quando ainda não existir) e vem acompanhado da origem de cada dado, do checklist do
comunicado de escopo, de uma avaliação crítica e da lista de dados a obter. Quem cola a CDT no Jira precisa saber,
para cada campo, de onde veio o dado e quão forte ele é.

## Leia primeiro

- [Publicação sobre escopo](references/publicacao-escopo-tecnologia.md): o comunicado que a CDT sempre segue.
- [Campos da CDT](references/campos-da-cdt.md): abas e campos do Jira, o que é da área e o que é da Tecnologia,
  seções da Descrição, insumos da esteira, lições dos exemplos e falhas comuns.
- [Qualidade e veracidade](references/qualidade-e-veracidade.md): estado, natureza e origem dos dados, checklist do
  comunicado, avaliação crítica e dados a obter.
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
Na CDT, cada campo do Jira é uma questão do registro: um campo sem fonte vira
"a confirmar" e entra nos dados a obter, nunca é completado por suposição.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Quando usar

A fase do projeto é contexto, não pré-requisito. O caso típico é depois do BP2, na implementação com rota interna ou
híbrida. Se o pedido vier cedo ou o material for insuficiente, entregue a CDT parcial: preencha o que as fontes
sustentam e assinale, campo a campo, os dados que precisam ser obtidos. Se a rota for externa, diga o que muda no
pedido à Tecnologia (integração, segurança, contratação) em vez de pedir construção.

## Passos

1. **Inventário.** Liste os entregáveis recebidos (Entrevista Inicial, Briefing, relatórios 4D, 3E e 5C, Test e
   Learning Cards, apresentação da experimentação, scorecard, relatório final) com data, versão e estado de leitura.
   Identifique o recorte vigente: em geral, a decisão mais recente documentada.
2. **Preencha cada campo.** Siga [os campos](references/campos-da-cdt.md) na ordem do formulário. Ligue cada
   afirmação a fonte e localizador e classifique sua natureza (medido, documentado, decidido, relatado, proposta,
   hipótese, a confirmar). Traduza o vocabulário da esteira para o leitor da Tecnologia. Comece pelo problema; a
   solução testada entra como referência validada (Protótipo e Evidências), não como especificação fechada. Em
   campos de lista, proponha a opção e justifique. Não preencha os campos que são da Tecnologia.
3. **Separe o escopo.** Classifique cada entrega em essencial, importante ou fora do escopo, com o motivo. O
   "precisa ter" do 3E confirmado no teste é o núcleo do essencial; item reprovado ou não testado não vira essencial.
4. **Confira contra o comunicado.** Marque os seis itens do checklist como atendido, parcial ou ausente e responda
   às cinco perguntas de "Comece pelo problema" ([qualidade](references/qualidade-e-veracidade.md)).
5. **Critique.** Escreva os pontos fortes e fracos e as perguntas que a Tecnologia deve fazer, mesmo que todos os
   campos estejam preenchidos. Liste os dados a obter, com motivo, responsável, pergunta pronta e se impedem o
   envio. Pergunte ao usuário só o que for decisivo e estiver na fronteira do grilling.
6. **Verifique e entregue.** Rode `python3 scripts/checar_cdt.py cdt.json`; corrija até o código 0 ou declare a
   versão parcial. Mostre no chat o estado, os campos prontos para colar na ordem do formulário, os pontos fracos e
   os dados a obter, e gere os arquivos.

## Exemplo

Entrada: "Monte a CDT do portal de solicitações com o relatório 3E, os Learning Cards e o relatório final."
Saída (trecho):
> **Estado: Parcial.** 2 de 19 campos a confirmar; o responsável pela validação impede o envio.
>
> **Informações Gerais: Descrição**, entregas essenciais: formulário guiado com campos obrigatórios por tipo de
> solicitação (medido: 7 de 8 analistas preencheram sem ajuda no teste com protótipo, LC-01).
>
> **Ponto fraco:** a meta de 10% de devoluções é proposta do sponsor, sem estudo; a Tecnologia pode questionar o
> indicador. Fortalecer com a linha de base de 25% (jul. a set. 2026) e prazo de apuração.
>
> **Dado a obter:** quem valida as entregas (Descrição: responsáveis). Perguntar ao sponsor: "Quem homologa as
> entregas com a Tecnologia?" Impede o envio: sim.

## Checagem final

- [ ] Todo campo do Jira tem fonte, natureza e localizador, ou "a confirmar" listado em dados a obter
- [ ] Nenhum campo da Tecnologia preenchido; opções de lista sugeridas com justificativa
- [ ] Problema antes da solução, sem jargão da esteira sem explicação; escopo em três grupos, com motivo
- [ ] Checklist do comunicado com os seis itens e as cinco perguntas respondidas
- [ ] Pontos fortes, pontos fracos e perguntas da Tecnologia presentes, mesmo com todos os campos preenchidos
- [ ] `scripts/checar_cdt.py` sem erros e estado igual em `readiness`, no chat e em `metadata.completeness`

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de Energia Elétrica). A CCEE
viabiliza a comercialização de energia elétrica no Brasil; "agente" pode ser uma organização participante do
mercado, não uma pessoa. Consulte [a esteira](references/eric-esteira.md) para interpretar etapas, BP1/BP2, rotas e
relações entre entregáveis; a CDT costuma nascer na etapa 8 (implementar).

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) e sem travessão no chat e nos arquivos; siga
[o design system](assets/design-system/README.md) com `deliverable_type` `cdt`: um bloco `paragraph` por campo, com
`data.section_key` e `data.text`, precedido de um `heading` no formato `Aba: campo` (as seções da Descrição usam
`Descrição: ...`). Abra com `readiness` e feche com `publication_checklist`, `quality_review`, `data_to_obtain` e
`traceability`; os dois últimos são seguidos de uma tabela sem `section_key`. Monte o JSON canônico, rode o
`checar_cdt.py`, depois `python3 assets/design-system/scripts/render.py entrada.json --out-dir saida`, e entregue o
JSON junto dos derivados. O MD e o TXT servem para colar no Jira; o PDF e o DOCX, para revisão e registro. Se a
validação falhar, corrija o conteúdo ou marque `metadata.completeness: "partial"`: nunca contorne o schema.

**Proveniência:** estrutura adaptada de publicação interna da CCEE sobre definição de escopo
(`references/publicacao-escopo-tecnologia.md`, anonimizada), da estrutura de CDTs reais observadas no Jira
(anonimizadas) e da metodologia ERIC deste repositório.
