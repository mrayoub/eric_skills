---
name: gerador-cdt
description: "Gera os dados para preencher no Jira um Cadastro de Demanda Tecnológica (CDT) de qualidade, a demanda que a área leva à Diretoria de Tecnologia, a partir dos entregáveis da esteira ERIC. Preenche os 28 campos das abas Informações Gerais e Benefícios da Demanda, na ordem da tela e com as opções exatas das listas do Jira; a Descrição responde às cinco perguntas do comunicado interno sobre escopo (problema, quem é impactado, processo atual, resultado esperado e prioridade). Fora do Jira, traz o checklist do comunicado respondido, fontes, pontos fortes e fracos e os dados a obter quando o material não basta. Use quando o usuário pedir para abrir, preencher, montar, revisar ou completar uma CDT, levar a demanda para a Tecnologia ou TI, ou organizar o escopo para o Jira. Não use para pedir a decisão da gestão (use relatorio-final-inovacao) nem para escrever a Entrevista Inicial ou o Briefing (use briefing-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.0"
---

# Gerador de CDT

CDT é o Cadastro de Demanda Tecnológica, aberto no Jira. Esta skill transforma o que a esteira produziu nos campos do
formulário, prontos para copiar, mais uma parte fora do Jira que mostra se a demanda está pronta para envio. A CDT não
é o relatório do projeto: é curta, direta e deixa o detalhe para os anexos.

## Leia primeiro

- [Campos do Jira](references/campos-jira.md): os 28 campos, opções exatas, padrão de escrita, formato de cada campo,
  coerência entre campos e insumos da esteira.
- [Publicação sobre escopo](references/publicacao-escopo-tecnologia.md): as cinco perguntas da Descrição e o
  checklist.
- [Qualidade e veracidade](references/qualidade-e-veracidade.md): estado, pendência, campo vazio, checklist,
  avaliação crítica, dados a obter e origem dos dados.
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
"a confirmar:" e entra nos dados a obter, nunca é completado por suposição.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Quando usar

A fase do projeto é contexto, não pré-requisito. O caso típico é depois do BP2, na implementação com rota interna ou
híbrida. Com material insuficiente, entregue a CDT parcial: preencha o que as fontes sustentam e assinale os dados a
obter. Se a rota for externa, diga o que muda no pedido à Tecnologia em vez de pedir construção.

## Passos

1. **Inventário.** Liste os entregáveis recebidos com data, versão e estado de leitura e identifique a decisão
   vigente mais recente.
2. **Descrição.** Responda sempre às cinco perguntas do comunicado, nesta ordem: qual problema, quem é impactado,
   como funciona hoje, qual resultado e o que é prioridade (essencial, importante e fora do escopo). Markdown só
   aqui. Nada além das cinco perguntas.
3. **Demais campos, na ordem da tela.** Opção exata da lista na primeira linha e `Motivo:` em uma linha; Sim ou Não
   com a linha que sustenta a resposta; texto simples, sem Markdown. Release, Data de operação e a escala de 1 a 10
   nunca são preenchidos ([formato](references/campos-jira.md#formato-de-cada-campo-no-entregável)).
4. **Corte.** Cada fato aparece uma vez; siglas por extenso na primeira menção de cada campo; nada de narrar o
   método da esteira. Limites: 150 palavras por pergunta da Descrição, 60 nos demais campos, 12 no título.
5. **Fora do Jira.** Escreva estado, checklist (com regras e responsáveis na própria linha), avaliação crítica, dados
   a obter e origem dos dados ([qualidade](references/qualidade-e-veracidade.md)). Rode
   `python3 scripts/checar_cdt.py cdt.json` até o código 0 ou declare a versão parcial.
6. **Entregue.** No chat: o estado, onde estão os arquivos, o principal ponto fraco e os dados a obter. Não repita a
   CDT inteira no chat.

## Exemplo

Entrada: "Monte a CDT do formulário de pedidos de dados com o relatório 3E, os Learning Cards e o relatório final."
Saída (trecho do arquivo):

```
Descrição: O que é prioridade neste momento?
**Essencial**
- Formulário com campos obrigatórios por tipo de pedido.
**Fora do escopo**
- Extração automática dos dados.

Informações Gerais: Família / Serviços
Informações aos Clientes / Disponibilizar dados históricos sob demanda
Motivo: é o serviço que recebe os pedidos.

Informações Gerais: Release
Selecionar no Jira.
```

## Checagem final

- [ ] Descrição com as cinco perguntas, na ordem do comunicado, e nada mais; Markdown só nela
- [ ] Os 28 campos presentes, na ordem da tela, com a opção exata do Jira e sem contradição entre campos
- [ ] Todo campo com fonte, "a confirmar:" listado em dados a obter ou marcado para deixar vazio
- [ ] Checklist com os seis itens, regras e responsáveis respondidos na linha; avaliação crítica com pontos fracos
- [ ] `scripts/checar_cdt.py` sem erros; estado igual em `readiness`, no chat e em `metadata.completeness`

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de Energia Elétrica). A CCEE
viabiliza a comercialização de energia elétrica no Brasil; "agente" pode ser uma organização participante do
mercado, não uma pessoa. Consulte [a esteira](references/eric-esteira.md) para interpretar etapas, BP1/BP2, rotas e
relações entre entregáveis; a CDT costuma nascer na etapa 8 (implementar).

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md), revise com o [guia de escrita](references/guia-de-escrita.md) e não use travessão no chat e nos arquivos (as opções do Jira com hífen, como "PLD - Preço de Liquidação das Diferenças", são exceção); siga
[o design system](assets/design-system/README.md) com `deliverable_type` `cdt`: um bloco `paragraph` por campo, com
`data.section_key` e `data.text`, precedido de um `heading` com o título `Aba: Rótulo` (a Descrição usa
`Descrição: <pergunta>`; a parte fora do Jira usa `Fora do Jira: <seção>`). As chaves e a ordem estão em
`assets/design-system/response-sections.json`. Abra com `readiness` e feche com `publication_checklist`,
`quality_review`, `data_to_obtain` e `traceability`; os dois últimos são seguidos de uma tabela sem `section_key`.
Monte o JSON canônico, rode o `checar_cdt.py`, depois `python3 assets/design-system/scripts/render.py entrada.json
--out-dir saida`, e entregue o JSON junto dos derivados. O MD e o TXT servem para colar no Jira; o PDF e o DOCX, para
revisão. Se a validação falhar, corrija o conteúdo ou marque `metadata.completeness: "partial"`: nunca contorne o
schema.

**Proveniência:** estrutura adaptada de publicação interna da CCEE sobre definição de escopo
(`references/publicacao-escopo-tecnologia.md`, anonimizada), do formulário da CDT no Jira levantado com o usuário em
23/10/2026 e de uma CDT real usada como padrão de escrita (anonimizada), e da metodologia ERIC deste repositório.
