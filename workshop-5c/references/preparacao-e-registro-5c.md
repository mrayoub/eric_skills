# Preparar e registrar o 5C pensando nas entregas

O 5C gera duas entregas na skill `relatorio-5c`: o Relatório 5C (registro por etapa) e a Apresentação 5C (devolutiva
por insight). As duas dependem do que foi registrado no dia. Num caso real, a devolutiva saiu sem os critérios do C3 e
sem os créditos do C5, e foi preciso perguntar depois à autora se isso tinha sido desenho da sessão ou falta de
registro. Era desenho: a sessão remota foi curta e objetiva. Deixe isso claro antes do encontro, para que fora do
escopo e lacuna de registro nunca se confundam. Os [exemplos](exemplos/README.md) mostram uma preparação feita pela autora do playbook.

## 1. Ponto de partida (antes do C1)

Monte com a equipe, a partir de briefing, diagnóstico e dados do serviço:

- **Objetivo** do encontro, em uma frase.
- **Linha de base:** a origem dos dados (chamados, voz do cliente, indicadores), o período, o volume e os temas com
  peso (por exemplo, "55% dos chamados sobre encerramento de contrato").
- **Perguntas que o 5C deve responder**, de 2 a 4. Por exemplo: que dores continuam atuais, onde estão as causas e os
  impactos, quais melhorias têm mais valor.
- **O que mudou desde o diagnóstico:** melhorias que entraram em operação, regras novas. Anote para verificar no
  encontro se a dor persiste.
- **Foco declarado:** problemas antes das soluções.

Esse ponto de partida é apresentado no C1 e vira a linha de base da triangulação "do diagnóstico à escuta" nas
entregas.

## 2. Formato, presença e regras de contagem

Defina e registre antes do encontro:

- **Formato e profundidade de cada sessão:** presencial ou remota, completa (C1 a C5) ou curta (C1 a C3, cerca de
  1h30). Uma sessão curta pode preceder a completa para ampliar a escuta; diga o que uma leva para a outra. A sessão
  curta é objetiva por desenho: o C3 usa só a confirmação por post-its, sem construir experiência desejada e
  critérios, e não há C4 nem C5. Declare isso no roteiro: o que ela não cobre fica fora do escopo, não é lacuna.
- **Adaptação do 5C oficial**, quando houver: etapa oficial, etapa aplicada, o que mudou e o motivo, conforme o
  [método](metodo-5c.md).
- **Convidados e presentes, separados.** Convidados nunca são denominador. Registre a organização e o perfil de cada
  presente.
- **Regra de cada contagem:** votos em C2, menções codificadas em C3 (post-its agrupados depois), créditos em C5. Para
  cada uma: unidade (pessoa ou organização), quantidade por pessoa, elegibilidade e o tratamento de duplicados, vazios
  e abstenções.

## 3. O que registrar em cada C

| Etapa | Registre no dia | Por que as entregas precisam |
|---|---|---|
| C1 Contextualizar | Ponto de partida apresentado, dúvidas e correções de enquadramento | Escopo, linha de base e validade temporal |
| C2 Compreender | Relatos por bloco temático da jornada, com o bloco numerado, relator ou perfil e um caso concreto; o que funciona; votos com a regra | Dores por sessão e fichas de dor D01, D02... |
| C3 Confirmar | Experiência desejada, situações a evitar e **critérios de sucesso** por dor priorizada, além dos post-its de confirmação | Critérios do C3 e contagem de menções; numa sessão completa, é o que mais se perde |
| C4 Cocriar | Ideias individuais e, por grupo, o mini-canvas: proposta, dor que atende, como funciona, **benefício esperado**, dependências, alternativas descartadas, composição do grupo | Propostas cocriadas com benefício esperado e ressalvas |
| C5 Conduzir | Pitches, **créditos por proposta e o total**, razões, objeções e encaminhamentos acordados com responsável | Priorização e próximos passos; também se perde com facilidade |

Antes de encerrar uma sessão completa, confira em voz alta com a equipe: os critérios do C3 e os créditos do C5 estão
anotados? Se algo não foi registrado, anote a lacuna no dia, com o motivo, em vez de reconstruir depois. Numa sessão
curta, confira só o que ela prevê (C1 a C3, com a confirmação por post-its).

## 4. Facilitação

- **Problemas antes das soluções:** no C2 e no C3, segure propostas e anote-as para o C4.
- **Espontâneo antes do induzido:** quando a CCEE tiver uma lista de opções (atributos, soluções candidatas), pergunte
  primeiro o que geraria valor e só depois mostre a lista. Registre o que surgiu antes e o que surgiu depois.
- **Organize os relatos pelos blocos da jornada** já usados no diagnóstico, para que a comparação fique direta.

## 5. Registro do encontro como base das entregas

O registro (`five_c_workshop_record`) segue a mesma base de análise que o `relatorio-5c` usa para as duas entregas:

| `section_key` | Conteúdo |
|---|---|
| `starting_point` | Objetivo, linha de base, perguntas a responder, o que mudou desde o diagnóstico |
| `sessions` | Sessões com data, formato, profundidade e etapas cobertas; presentes e convidados separados; adaptação declarada; regras de contagem |
| `c1` a `c5` | O que aconteceu em cada etapa, com os registros da tabela acima e fonte por item |
| `record_gaps` | O que não foi registrado, em que etapa, por quê e como obter; "nenhuma lacuna" quando for o caso |

Quanto mais completo o registro, menos o relatório precisa perguntar. Quando o registro já existir, o `relatorio-5c`
só redige.
