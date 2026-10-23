---
name: workshop-5c
description: "Prepara, facilita ou reconstrói um workshop 5C de cocriação com clientes: C1 contextualizar, C2 compreender a experiência atual, C3 confirmar a experiência desejada, C4 cocriar propostas e C5 conduzir com pitches e créditos de votação. Use para montar roteiro, convite, regras de voto, dinâmicas ou o registro de um encontro com clientes ou agentes. Não use para escrever o relatório consolidado depois do encontro (use relatorio-5c)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.20"
---

# Facilitar o workshop 5C

Prepara ou registra cocriação com clientes; playbook não determina serviço, empresas, participantes, responsáveis ou agenda de outros projetos.

## Leia primeiro

- [Método 5C](references/metodo-5c.md): condução adaptada.
Para conferir a fonte: [transcrição](assets/Playbook_Modelo_5C_Centralidade_Cliente.transcricao.md) e [DOCX](assets/Playbook_Modelo_5C_Centralidade_Cliente.docx).

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

Prepare briefing, diagnóstico, entrevistas, jornada e decisões; extraia desafio/evidências e perfis afetados sem copiar a aplicação original. Pergunte por público, acesso, objetivo, facilitadores, tempo, registro e condições decisivas ausentes. A amostra reúne perspectivas, sem representatividade automática. Combine presença, voto/créditos e preservação de ideias/dissensos antes de votar: três votos em C2 e dez créditos em C5 são referências adaptáveis com regra/data. Confira divergência entre duração declarada e intervalos do DOCX.

1. **C1 Contextualizar:** apresente desafio/origem/dúvidas e agenda; abra correções. Registre versão, fontes e dúvidas.
2. **C2 Compreender:** peça episódios, condições, consequências, acertos, fricções e oportunidades; registre relator/perfil/tema/evidência. Priorize pela regra combinada; preserve contagem, elegibilidade, abstenções e dissensos.
3. **C3 Confirmar:** construa experiência desejada, situações a evitar e critérios observáveis; são hipóteses a verificar, com desacordos preservados.
4. **C4 Cocriar:** ideias individuais antes de grupos diversos; vincule propostas a dor, funcionamento, benefícios alegados e dependências. Preserve origens, alterações de grupos e alternativas descartadas, sem forçar consenso.
5. **C5 Conduzir:** registre pitches; apure créditos/ranking reproduzível, razões e objeções. Separe preferência, decisão institucional e validação experimental. Encaminhamentos/responsáveis somente quando acordados.

Devolva síntese e próximos passos definidos. Em modo assíncrono, declare dinâmicas substituídas e decisões não reproduzidas; etapas ausentes mantêm parcial. Registro C1 a C5 para `relatorio-5c` exige sínteses/fontes, participantes/perfis, versão, regras, votos, decisões e lacunas. Relatos/votos não comprovam eficácia, escala, viabilidade ou impacto; proponha testes.

## Exemplo

Entrada: “Prepare o 5C do Portal de Solicitações de Dados.”
Saída (trecho):
> Agenda adaptada ao encontro real, regras antes dos votos.
> Convidados não são denominador de presentes elegíveis.
> Sem presença registrada, entrega parcial.

## Checagem final

- [ ] C1 a C5 separadas com síntese/fonte ou lacuna
- [ ] Regras, presença, elegibilidade e abstenções rastreáveis
- [ ] Ideias, falas e dissensos preservados
- [ ] Preferência separada de decisão e eficácia
- [ ] Agenda, adaptações e próximos passos documentados

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md), revise com o [guia de escrita](references/guia-de-escrita.md) e não use travessão no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `five_c_workshop_record`: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"`: nunca contorne o schema.

**Proveniência:** adaptação metodológica do playbook 5C fornecido pelo usuário. Esta skill não atribui origem externa certificada ao método.
