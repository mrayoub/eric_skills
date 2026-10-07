# Plan 008: Reescrever as descriptions para acionar a skill certa e medir o acionamento

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- '*/SKILL.md'`
> Mudanças em SKILL.md vindas dos planos 003/004 (uma frase no corpo) são esperadas.
> Se alguma `description:` do frontmatter mudou desde a linha de base, STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW (texto; reversível)
- **Depends on**: none (pode rodar antes do 010; o 010 preserva o frontmatter daqui)
- **Category**: dx
- **Planned at**: commit `967749d`, 2026-09-28

## Why this matters

Um agente decide qual skill carregar lendo **apenas** `name` + `description` de cada uma.
Esta pasta tem 11 skills irmãs muito parecidas (três pares workshop/relatório, três
instrumentos de avaliação — IQB, potencial, scorecard — e experimentação que se sobrepõe
ao E3). As descriptions atuais descrevem o conteúdo, mas quase não trazem as palavras
que o usuário usa ("nota do briefing", "one-page", "ranquear dores", "Learning Card"),
repetem "Use em qualquer momento" (não é gatilho) e só uma delas diz quando **não** usar.
O guia oficial do skill-creator da Anthropic recomenda descriptions que digam o que a skill
faz **e** em que contextos usar, um pouco "insistentes" (modelos tendem a subacionar), e
testadas com um conjunto de consultas que devem e que não devem disparar — sobretudo
quase-acertos de skills vizinhas.

## Current state

Descriptions atuais (frontmatter, linha 3 de cada `SKILL.md`), resumidas:

| Skill | Problema principal |
|---|---|
| briefing-inovacao | Sem gatilhos ("one-page", "HMW", "transcrição"); sem fronteira com IQB |
| avaliacao-briefing-iqb | Bom conteúdo; sem fronteira explícita com briefing/potencial/scorecard |
| potencial-inovacao | "Use … em qualquer momento"; sem "ranquear/triar"; sem fronteira |
| workshop-4d / workshop-3e / workshop-5c | Sem "Não use para compilar o relatório" |
| relatorio-4d / relatorio-3e / relatorio-5c | "Use em qualquer momento"; sem fronteira com o workshop |
| experimentacao-inovacao | "Conduz a **fase** de experimentação" contradiz o princípio de uso independente de fase; sem fronteira com o E3 |
| scorecard-inovacao | "sem depender de outras skills" é irrelevante para acionamento; sem fronteira com IQB/potencial |

Regras de formato (validadas por `quick_validate.py` do skill-creator): `description` ≤ 1024
caracteres, sem `<` nem `>`. Mantenha entre aspas duplas como hoje. Não mude `name`.

Validador: `/Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py`
Eval de acionamento: `.../skill-creator/scripts/run_eval.py` (mesma pasta). Ele cria um
comando temporário em `<projeto>/.claude/commands/` e roda `claude -p` com cada consulta
3 vezes; o "projeto" é o primeiro diretório acima do `cwd` que contém `.claude/`.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Validar skill | `python3 $SC/scripts/quick_validate.py <skill>` (onde `SC=/Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator`) | `Skill is valid!` |
| Eval de acionamento | `cd "$EVALPROJ" && PYTHONPATH="$SC" python3 -m scripts.run_eval --eval-set <json> --skill-path <skill> --model claude-opus-5-5 --runs-per-query 3` | JSON com taxa por consulta |

## Scope

**In scope**: linha `description:` dos 11 `SKILL.md`; `_EVALS/triggers/<skill>.json` (criar, 11 arquivos); `_EVALS/triggers/README.md` e `_EVALS/triggers/resultados.md` (criar).

**Out of scope**: corpo dos SKILL.md (plano 010); `name`; qualquer outro arquivo.

## Git workflow

Branch `advisor/008-descriptions`. Commits: (1) conjuntos de eval; (2) linha de base medida; (3) novas descriptions + medição.

## Steps

### Step 1: Criar os conjuntos de eval de acionamento

Para cada skill, crie `_EVALS/triggers/<skill>.json` no formato do skill-creator:

```json
[{"query": "…", "should_trigger": true}, {"query": "…", "should_trigger": false}]
```

16 consultas por skill: 8 `true`, 8 `false`. Parta das sementes abaixo (Step 3) e
complete com variações realistas em português do Brasil: registros formais e casuais,
com contexto concreto (nomes de área, datas, arquivos), algumas sem citar o nome do
método. Os `false` devem ser **quase-acertos** — pedidos que pertencem a uma skill vizinha
desta pasta — nunca pedidos obviamente alheios ("escreva um poema"). Consultas devem ser
tarefas substanciais (um agente não aciona skill para pedidos triviais de um passo).

**Verify**: `python3 -c "import json,glob;[print(f, len(json.load(open(f))), sum(q['should_trigger'] for q in json.load(open(f)))) for f in sorted(glob.glob('_EVALS/triggers/*.json'))]"` → 11 linhas, cada uma `16 8`.

### Step 2: Medir a linha de base (descriptions atuais)

Crie um projeto de avaliação **fora** da pasta das skills, com as 11 skills instaladas como
irmãs para que a competição entre elas seja real:

```bash
SC=/Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator
EVALPROJ="$TMPDIR/skills-trigger-eval"; mkdir -p "$EVALPROJ/.claude/skills"
for s in avaliacao-briefing-iqb briefing-inovacao experimentacao-inovacao potencial-inovacao relatorio-3e relatorio-4d relatorio-5c scorecard-inovacao workshop-3e workshop-4d workshop-5c; do ln -sfn "/Users/mayoub/Desktop/workspaces/my_skills/$s" "$EVALPROJ/.claude/skills/$s"; done
```

Para cada skill: `cd "$EVALPROJ" && PYTHONPATH="$SC" python3 -m scripts.run_eval --eval-set /Users/mayoub/Desktop/workspaces/my_skills/_EVALS/triggers/<skill>.json --skill-path /Users/mayoub/Desktop/workspaces/my_skills/<skill> --model claude-opus-5-5 --runs-per-query 3 > "$TMPDIR/base-<skill>.json"`

Isto consome chamadas de modelo (11 × 16 × 3 ≈ 528). **Peça confirmação ao operador antes.**
Se o operador recusar, pule para o Step 3 e registre "linha de base não medida".

Registre em `_EVALS/triggers/resultados.md` uma tabela: skill | acertos `true` | acertos `false` | consultas erradas (texto).

**Verify**: `resultados.md` tem 11 linhas de dados (ou a nota de pulo).

### Step 3: Aplicar as novas descriptions

Substitua o valor de `description:` de cada `SKILL.md` exatamente pelo texto abaixo
(entre aspas duplas; uma linha só).

#### `briefing-inovacao` (652 caracteres)

```
Cria, reconstrói ou atualiza o briefing de sete campos de um desafio de inovação da CCEE (título, HMW, problema, relevância, resultados esperados, responsável, sponsor) e, quando pedido, gera a síntese executiva de uma página (one-page) ou perguntas para fechar lacunas do briefing. Use sempre que o usuário quiser escrever, preencher, revisar, versionar ou resumir um briefing, transformar entrevista ou transcrição em briefing, formular um 'how might we', montar uma one-page ou perguntas ao sponsor, mesmo sem dizer 'briefing'. Não use para dar nota ao briefing (use avaliacao-briefing-iqb) nem para priorizar oportunidades (use potencial-inovacao).
```

Sementes de acionamento — deve disparar:
- "Transforma essa transcrição da conversa com a área de adimplemento num briefing do desafio"
- "Preciso de uma one-page do briefing v2 pra levar pro comitê amanhã"
- "Quais perguntas eu deveria mandar pro sponsor pra fechar as lacunas desse briefing?"

Não deve disparar (quase-acertos):
- "Dá uma nota IQB pra esse briefing"
- "Entre essas três dores, qual devemos priorizar?"
- "Escreve um e-mail convidando os clientes pro workshop 5C"

#### `avaliacao-briefing-iqb` (606 caracteres)

```
Avalia a qualidade de um briefing de inovação pela rubrica IQB do ERIC: 40 critérios binários em clareza, evidências, resultados e acionabilidade, com vetos, nota por dimensão, IQB de 1 a 5 e classificação calculados por script. Use quando o usuário pedir nota, IQB, validação, auditoria, checklist ou comparação de versões de um briefing, ou perguntar se o briefing está bom o suficiente para seguir. Não use para escrever ou melhorar o briefing (use briefing-inovacao), para priorizar a oportunidade (use potencial-inovacao) nem para medir a maturidade das evidências do projeto (use scorecard-inovacao).
```

Sementes de acionamento — deve disparar:
- "Esse briefing está bom o suficiente pra seguir pro aprofundamento? Avalia pela rubrica"
- "Compara a versão 1 e a 2 do briefing e diz se a qualidade melhorou"
- "Roda o checklist dos 40 critérios nesse briefing"

Não deve disparar (quase-acertos):
- "Melhora a redação do HMW desse briefing"
- "Quão validado está o projeto de adimplemento hoje?"
- "Pontua essa oportunidade em impacto, viabilidade e urgência"

#### `potencial-inovacao` (623 caracteres)

```
Pontua e classifica o potencial de uma dor ou oportunidade de inovação com a rubrica interna do ERIC (impacto 30%, viabilidade 25%, alinhamento estratégico 20%, urgência 15%, novidade 10%), resultando em priorizar, monitorar ou arquivar, com justificativa e fonte por critério e cálculo por script. Use quando o usuário quiser priorizar, ranquear, triar ou comparar oportunidades, ideias ou dores, decidir se vale investir nelas ou revisar uma priorização já feita. Não use para dar nota a um briefing (use avaliacao-briefing-iqb) nem para avaliar a força das evidências de um projeto em andamento (use scorecard-inovacao).
```

Sementes de acionamento — deve disparar:
- "Temos 5 dores levantadas no garimpo, me ajuda a ranquear qual atacar primeiro"
- "Vale a pena investir nessa ideia de triagem automática? Classifica o potencial"
- "Revisa a priorização que fizemos mês passado com os dados novos"

Não deve disparar (quase-acertos):
- "Qual é o IQB desse briefing?"
- "O projeto tem evidência pra passar no gate de piloto?"
- "Monta os Test Cards para essa hipótese"

#### `workshop-4d` (480 caracteres)

```
Prepara, conduz ao vivo ou organiza de forma assíncrona o workshop 4D de aprofundamento de um desafio: D1 descongelar percepções, D2 diagnosticar (jornada e barco da inovação: ventos, âncoras, icebergs, porto), D3 desenhar alternativas e D4 decidir com créditos de votação. Use para montar roteiro, pauta, board colaborativo, perguntas de facilitação ou para registrar o que aconteceu em cada D. Não use para escrever o relatório consolidado depois do encontro (use relatorio-4d).
```

Sementes de acionamento — deve disparar:
- "Monta o roteiro do aprofundamento 4D de sexta com as perguntas de cada D"
- "Como facilito o barco da inovação no D2 com 12 pessoas remotas?"
- "Vamos fazer o 4D de forma assíncrona, organiza as etapas"

Não deve disparar (quase-acertos):
- "Com essas fotos do mural e a planilha de votos, escreve o relatório 4D"
- "Prepara o workshop 5C com os clientes"
- "Planeja o E3 do workshop de estruturação"

#### `relatorio-4d` (445 caracteres)

```
Compila ou revisa o Relatório 4D a partir dos registros de D1 a D4 (mural, notas, transcrições, votos, snapshot D2): diagnóstico, alternativas, priorização com denominadores, dissensos, evidências e lacunas rastreáveis. Use quando houver material de um workshop 4D ou fontes equivalentes e o usuário quiser o relatório, a síntese para o BP1 ou a revisão de um relatório existente. Não use para preparar ou facilitar o encontro (use workshop-4d).
```

Sementes de acionamento — deve disparar:
- "Tenho o mural, a transcrição e os votos do D4, compila o relatório"
- "Revisa esse relatório 4D antes de ir pro BP1"
- "Só fizemos D1 e D2, consegue consolidar o que temos?"

Não deve disparar (quase-acertos):
- "Quais perguntas uso para abrir o D1 amanhã?"
- "Escreve o relatório do encontro com clientes de ontem (5C)"
- "Avalia o briefing pelo IQB"

#### `workshop-3e` (501 caracteres)

```
Prepara, conduz ou registra o workshop 3E de estruturação da solução: E1 esclarecer hipótese e escopo, E2 estruturar componentes (precisa ter, pode evoluir, fora do recorte) e E3 planejar experimentos com Test Cards individuais da Strategyzer. Use para montar pauta, perguntas, board ou registrar as decisões do grupo sobre a solução candidata. Não use para compilar o relatório 3E (use relatorio-3e) nem para planejar em detalhe ou analisar uma rodada de experimentação (use experimentacao-inovacao).
```

Sementes de acionamento — deve disparar:
- "Prepara a pauta do workshop de estruturação da solução E1 a E3"
- "Como conduzo a classificação precisa ter / pode evoluir / fora do recorte?"
- "Registra o que o grupo decidiu no E2 hoje"

Não deve disparar (quase-acertos):
- "Compila o relatório 3E com os Test Cards"
- "Analisa os resultados do piloto que rodou em agosto"
- "Roteiro do workshop 4D"

#### `relatorio-3e` (496 caracteres)

```
Compila ou revisa o Relatório 3E: solução e escopo, plano de construção com responsáveis e prazos, Test Cards individuais prospectivos e decisão de rota (interna, externa, híbrida ou indefinida), separando plano de evidência observada. Use quando houver registros de E1 a E3 ou material equivalente e o usuário quiser o relatório ou os Test Cards consolidados. Não use para facilitar o workshop (use workshop-3e) nem para analisar resultados de testes já executados (use experimentacao-inovacao).
```

Sementes de acionamento — deve disparar:
- "Com as notas do E1-E3, monta o relatório 3E e a decisão de rota"
- "Revisa o relatório 3E e confere se cada Test Card tem os quatro campos"
- "A rota ficou híbrida; compila o relatório com o plano de construção"

Não deve disparar (quase-acertos):
- "Facilita o E1 comigo agora"
- "Gera os Learning Cards dos testes que rodamos"
- "Escreve o relatório 4D"

#### `workshop-5c` (434 caracteres)

```
Prepara, facilita ou reconstrói um workshop 5C de cocriação com clientes: C1 contextualizar, C2 compreender a experiência atual, C3 confirmar a experiência desejada, C4 cocriar propostas e C5 conduzir com pitches e créditos de votação. Use para montar roteiro, convite, regras de voto, dinâmicas ou o registro de um encontro com clientes ou agentes. Não use para escrever o relatório consolidado depois do encontro (use relatorio-5c).
```

Sementes de acionamento — deve disparar:
- "Vamos receber 8 agentes de mercado para cocriar, monta o roteiro 5C"
- "Como faço a votação de créditos no C5?"
- "Prepara as perguntas do C2 sobre a experiência atual"

Não deve disparar (quase-acertos):
- "Escreve o relatório do 5C de ontem com base nas notas"
- "Planeja o workshop 4D"
- "Monta a pauta do E1-E3"

#### `relatorio-5c` (413 caracteres)

```
Compila ou revisa o Relatório 5C de um encontro de cocriação com clientes, ligando C1 a C5 a falas, votos com denominador, critérios de experiência, propostas, dissensos e próximos passos. Use quando houver registros de um workshop 5C (notas, mural, gravação, votos, ata) e o usuário quiser o relatório, a síntese ou a devolutiva aos participantes. Não use para preparar ou facilitar o encontro (use workshop-5c).
```

Sementes de acionamento — deve disparar:
- "Aqui está a gravação e a ata do encontro 5C, faz o relatório"
- "Consolida os votos do C2 e do C5 e escreve a devolutiva aos clientes"
- "Revisa esse relatório 5C: os totais batem?"

Não deve disparar (quase-acertos):
- "Monta o roteiro do encontro 5C da semana que vem"
- "Compila o relatório 4D"
- "Analisa as sessões de think aloud"

#### `experimentacao-inovacao` (603 caracteres)

```
Planeja e analisa experimentos de inovação com pessoas ou operação: escolhe o método pela hipótese (entrevista, think aloud, MVP manual, piloto, comparação A/B e outros), escreve Test Cards e protocolo antes da coleta e, depois da execução, produz Learning Cards, síntese de evidências, recomendação, relatório e apresentação rastreáveis. Use quando o usuário falar em testar uma hipótese, piloto, MVP, teste de usabilidade, análise de sessões, resultados de experimento, Test Card ou Learning Card. Não use para testes automatizados de software nem apenas para o E3 de um workshop 3E (use workshop-3e).
```

Sementes de acionamento — deve disparar:
- "Quero testar se o formulário guiado reduz devoluções; qual método e quais Test Cards?"
- "Rodamos 5 sessões de think aloud, analisa e gera os Learning Cards"
- "O piloto terminou, faz a síntese de evidências e a recomendação"

Não deve disparar (quase-acertos):
- "Escreve testes unitários pro módulo de cobrança"
- "Compila o relatório 3E"
- "Quão maduro está o projeto no scorecard?"

#### `scorecard-inovacao` (544 caracteres)

```
Avalia a maturidade das evidências de um projeto de inovação com o Innovation Project Scorecard da Strategyzer, oficial ou em adaptação institucional declarada, gerando um retrato datado, sem média geral, com lacunas decisivas e próximos testes. Use quando o usuário perguntar quão validado ou maduro está um projeto, se há evidência suficiente para passar um gate, ou quiser comparar retratos ao longo da esteira. Não use para dar nota a um briefing (use avaliacao-briefing-iqb) nem para priorizar oportunidades novas (use potencial-inovacao).
```

Sementes de acionamento — deve disparar:
- "Quão validado está o projeto de adimplemento? Usa o scorecard da Strategyzer"
- "Temos evidência suficiente pra passar pro piloto?"
- "Compara o retrato de maturidade de junho com o de hoje"

Não deve disparar (quase-acertos):
- "Pontua o potencial dessa oportunidade"
- "Dá nota IQB no briefing"
- "Gera Learning Cards dos testes"

**Verify**: para cada skill, `quick_validate.py` → `Skill is valid!`; e
`python3 -c "import re,glob;[print(f,len(re.search(r'^description: \"(.*)\"$',open(f).read(),re.M).group(1))) for f in sorted(glob.glob('*/SKILL.md'))]"` → 11 linhas, todos ≤ 1024.

### Step 4: Medir de novo e ajustar

Repita o Step 2 (se autorizado) salvando em `$TMPDIR/novo-<skill>.json` e acrescente as
colunas "depois" em `resultados.md`. Meta: ≥ 7/8 nos `true` e ≥ 7/8 nos `false` por skill.
Para skills abaixo da meta, ajuste a description **à mão** mirando as consultas que
falharam (acrescente o termo que faltou ou a fronteira que confundiu) — no máximo 2
rodadas. Opcional: `python -m scripts.run_loop` do skill-creator pode propor texto, mas
**não** aceite sugestões que removam a frase "Não use para … (use <skill>)".

**Verify**: `resultados.md` mostra antes/depois para as 11 skills.

## Test plan

Os 11 conjuntos em `_EVALS/triggers/` são o teste. Crie `_EVALS/triggers/README.md`
explicando como rodar (os comandos do Step 2) e que devem ser rodados de novo sempre que
uma description mudar.

## Done criteria

- [ ] 11 arquivos `_EVALS/triggers/<skill>.json`, 16 consultas cada (8/8)
- [ ] 11 descriptions substituídas; todas as skills passam em `quick_validate.py`
- [ ] Toda description contém "Não use" e o nome de pelo menos uma skill irmã: `grep -c "Não use" */SKILL.md` → 11 linhas com `1`
- [ ] `grep -n "fase de experimentação" experimentacao-inovacao/SKILL.md | head -1` não está na linha 3
- [ ] `_EVALS/triggers/resultados.md` existe (com medições ou nota de pulo)
- [ ] `plans/README.md` atualizado

## STOP conditions

- `run_eval` falhar por não achar `claude` no PATH ou por autenticação — registre e pare os Steps 2/4 (os Steps 1 e 3 continuam válidos).
- Uma skill ficar abaixo de 5/8 em qualquer lado depois de 2 rodadas de ajuste — reporte as consultas que falham; pode indicar sobreposição real de escopo entre skills (decisão do mantenedor).

## Maintenance notes

- Ao criar uma 12ª skill, acrescente sua fronteira nas descriptions das vizinhas e consultas quase-acerto nos conjuntos delas.
- O acionamento depende também das skills instaladas no ambiente do usuário; a medição aqui só cobre a competição entre estas 11.
