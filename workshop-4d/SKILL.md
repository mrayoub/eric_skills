---
name: workshop-4d
description: "Prepara, conduz ao vivo ou organiza de forma assíncrona o workshop 4D de aprofundamento de um desafio: D1 descongelar percepções, D2 diagnosticar (jornada e barco da inovação: ventos, âncoras, icebergs, porto), D3 desenhar alternativas e D4 decidir com créditos de votação. Use para montar roteiro, pauta, board colaborativo, perguntas de facilitação ou para registrar o que aconteceu em cada D. Não use para escrever o relatório consolidado depois do encontro (use relatorio-4d)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.3"
---

# Facilitar o 4D

Prepara, conduz ou registra D1–D4 em sequência lógica; resultados posteriores atualizam contexto, não recriam votações.

## Leia primeiro

- [Playbook 4D](references/4d-workshop-playbook.md) — tempos e dinâmicas.
Para conferir a fonte: [transcrição](<assets/Modelo 4D de Aprofundamento.transcricao.md>), [DOCX](<assets/Modelo 4D de Aprofundamento.docx>), [divergências](references/fonte-4d-e-divergencias.md), [original RC6](assets/4d-workshop-playbook-original-rc6.md). Preserve originais; registre diferenças e datas.
[Blueprint Mural](references/mural-board-4d-template.md) opcional: board autorizado ou registros físicos/conversacionais.

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

Prepare briefing/HMW, dados, entrevistas e decisões; se D1/D2 existirem, confira diagnóstico e lacunas. Pergunte só por objetivo, público, presença, acesso e restrições ausentes; distinga dados, percepções e hipóteses sem confirmar causas preferidas.

1. **D1 — Descongelar:** apresente desafio/dados citados; recolha anonimamente elefante na sala e sentimento dominante; preserve dissensos.
2. **D2 — Diagnosticar:** jornada antes/durante/depois; barco com ventos, âncoras, icebergs e porto. Registre relator, evidência, contraexemplos e verificações pendentes. Salve snapshot D2: intermediário, não diagnóstico final ou aprovação.
3. **D3 — Desenhar:** brainwriting individual para eliminar, simplificar e mudar a lógica; agrupe alternativas incrementais/estruturais/radicais ligadas à dor.
4. **D4 — Decidir:** aplique créditos combinados antes do voto; registre ranking, razões, dissensos, riscos e responsáveis que aceitaram investigar. Voto indica prioridade, não efeito ou adesão.

Em cada D, registre objetivo, tempo, pergunta e saída; adapte duração e documente desvios. Não invente participação/votos/dinâmicas. Sem D3/D4, entregue parcial; em modo assíncrono, indique substituições documentais. Registro por dimensão deve incluir fontes, participantes, versão, decisões e lacunas para `relatorio-4d`. Se houver BP1, seu insumo é o relatório concluído, não snapshot D2.

## Exemplo

Entrada: “Prepare o 4D do Portal de Solicitações de Dados.”
Saída (trecho):
> D2: investigar devoluções; snapshot ainda provisório.
> D4: combinar dez créditos por presente antes de votar.
> Nenhuma preferência é impacto já validado.

## Checagem final

- [ ] D1–D4 rastreáveis e lacunas explícitas
- [ ] Objetivo, duração, pergunta e registro por etapa
- [ ] Snapshot intermediário e voto distinguidos de validação
- [ ] Participação, decisões e responsáveis sustentados

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `four_d_workshop_record`: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** reescrita de fonte metodológica RC6 (`facilitate-4d-workshop/`). A sequência interna D1–D4 foi preservada; o vínculo do RC6 com fase e BP1 é apenas contexto histórico da fonte.
