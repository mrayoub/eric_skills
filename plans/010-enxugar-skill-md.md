# Plan 010: Enxugar e reestruturar os 11 SKILL.md (piloto em potencial-inovacao)

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- '*/SKILL.md' _SHARED _ERIC_CONTEXT`
> Esperado: mudanças só na linha `description:` (plano 008) e nas frases que citam
> `scripts/score.py` / `scripts/iqb.py` (planos 003/004). Qualquer outra mudança no corpo = STOP.

## Status

- **Priority**: P2
- **Effort**: L
- **Risk**: MED (muda o comportamento das skills; mitigado pelas evals do 009)
- **Depends on**: 001 (sync + `_SHARED/`), 003, 004 (frases de CLI), 007 (README do DS fala do fallback de PDF), 008 (descriptions), 009 (evals — rede de segurança)
- **Category**: tech-debt
- **Planned at**: commit `967749d`, 2026-09-28

## Why this matters

O corpo de um SKILL.md entra inteiro no contexto sempre que a skill é acionada. As boas
práticas de skills da Anthropic pedem: corpo conciso, passos em ordem (listas/checklists),
explicar o **porquê** em vez de empilhar proibições, exemplos concretos, e detalhes em
arquivos de referência carregados só quando necessários (divulgação progressiva).

Hoje, cada SKILL.md tem 735–2.686 palavras em ~45 linhas (parágrafos de 150–250 palavras).
Quatro blocos são copiados literalmente nas 11 skills (~450 palavras cada vez, quase metade
do corpo); o de arquivos repete o `assets/design-system/README.md`. Além disso, cada skill
manda ler **antes de começar** o `eric-esteira.md` (1.586 palavras) e o
`grilling-operacional.md` (1.000), e 9 delas também `levantamento-documental-e-grilling.md`
(384), que se sobrepõe ao grilling. Resultado: o workshop-4d exige ~6.700 palavras
(~11k tokens) antes de agir, e instruções específicas ficam enterradas em texto repetido.

## Current state

### Blocos repetidos (texto idêntico nas skills indicadas)

1. **"## Grilling obrigatório na leitura e na interação"** (11 skills; nas skills 5C e nos
   relatórios o título é o mesmo). Começa: "Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos…" (~110 palavras).
2. **"## Uso independente da fase"** (10 skills; ausente em `experimentacao-inovacao` e `scorecard-inovacao`; nas 5C há versão própria mais curta). Começa: "Ative esta skill pela tarefa solicitada e pelos insumos disponíveis…" (~130 palavras).
3. **"## Contexto institucional"** (11): "Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas…" (~60 palavras).
4. **"## Arquivos e padrão visual"** (11; nas 5C começa com "Siga o [sistema visual incluído]"): "Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json`… use o tipo `<tipo>`…" (~230 palavras). Única parte específica: o(s) `deliverable_type`.

### Tipos de entregável por skill (preservar!)

| Skill | deliverable_type(s) |
|---|---|
| briefing-inovacao | `briefing`, `briefing_one_page`, `briefing_improvement_questionnaire` |
| avaliacao-briefing-iqb | `briefing_validation` |
| potencial-inovacao | `innovation_potential_assessment` |
| workshop-4d | `four_d_workshop_record` |
| relatorio-4d | `four_d_report` |
| workshop-3e | `three_e_workshop_record` + `test_card` por teste |
| relatorio-3e | `three_e_report` + `test_card` por teste |
| workshop-5c | `five_c_workshop_record` |
| relatorio-5c | `five_c_report` |
| experimentacao-inovacao | `experiment_plan`, `test_card`, `learning_card`, `experiment_report`, `evidence_recommendation`, `executive_presentation` |
| scorecard-inovacao | `innovation_scorecard` |

### Inconsistências a corrigir junto

- `potencial-inovacao/SKILL.md`: as instruções centrais (linhas 10–14) vêm **antes** do bloco de grilling; nas demais, depois.
- `experimentacao-inovacao/SKILL.md`: sem seção de uso independente de fase e sem linha de Proveniência.
- `workshop-5c/SKILL.md` linha 8: linka a mesma transcrição duas vezes ("Leia primeiro a [transcrição integral do DOCX 5C](assets/…transcricao.md)" e depois "sua [transcrição textual](assets/…transcricao.md)"). O mesmo ocorre em `relatorio-5c/SKILL.md` linha 8.
- Várias skills 4D/3E mandam ler a transcrição integral **e** o playbook adaptado **e** o registro de divergências no início. Para executar, basta o playbook adaptado; transcrição/DOCX/divergências são para conferência.

### Tamanhos atuais (palavras, `wc -w`)

avaliacao-briefing-iqb 863 · briefing-inovacao 1013 · experimentacao-inovacao 2686 · potencial-inovacao 735 · relatorio-3e 996 · relatorio-4d 1006 · relatorio-5c 897 · scorecard-inovacao 1367 · workshop-3e 993 · workshop-4d 1030 · workshop-5c 927.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Validar skill | `python3 $SC/scripts/quick_validate.py <skill>` (`SC=/Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator`) | `Skill is valid!` |
| Links | script do Step 6 | sem saída |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |
| Evals | ver `_EVALS/README.md` (plano 009) | sem regressão |

## Scope

**In scope**: corpo dos 11 `SKILL.md` (frontmatter intocado); `_SHARED/grilling-operacional.md`; `_SHARED/levantamento-documental-e-grilling.md` (remoção, Step 5); `_TOOLS/sync_shared.py` (só o mapa de sincronização, Step 5); `experimentacao-inovacao/references/` (novos arquivos para conteúdo movido, Step 4); cópias via sync.

**Out of scope**: `description:` (plano 008); `eric-esteira.md` e demais referências metodológicas (conteúdo); assets/originais/transcrições; design system.

## Git workflow

Branch `advisor/010-skill-md`. Um commit para o piloto; um commit por skill no rollout (facilita reverter uma só).

## Steps

### Step 1: Textos padrão que substituem os blocos repetidos

Use exatamente estes blocos (troque `<tipos>` pela coluna da tabela acima, com crases):

```markdown
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

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Para PDF, DOCX, MD, TXT ou PPTX, siga [o design system](assets/design-system/README.md)
com `deliverable_type` <tipos>: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.
```

Em `experimentacao-inovacao` e `scorecard-inovacao`, **acrescente** "Quando usar" (hoje ausente).

### Step 2: Estrutura-alvo de cada SKILL.md

```
---(frontmatter intacto)---
# <Título>
<1–2 frases: o que produz e o que NÃO é (ex.: "não é o Scorecard da Strategyzer")>

## Leia primeiro        ← só o que é necessário para executar (1–3 links)
## Grilling             ← bloco padrão
## Quando usar          ← bloco padrão (+ 1 frase específica, se houver)
## Passos               ← lista numerada; cada passo curto, com o porquê quando não for óbvio
## Exemplo              ← 1 exemplo curto de entrada → saída (5–15 linhas)
## Checagem final       ← checklist de 4–7 itens "- [ ]"
## Contexto ERIC        ← bloco padrão
## Entrega em arquivo   ← bloco padrão
**Proveniência:** 1 linha
```

Regras de reescrita:
- **Preserve toda regra específica** do método (ex.: "voto indica prioridade do grupo, não comprova efeito", "Test Card individual com quatro campos", "snapshot D2 não é diagnóstico final"). Cortar = cortar repetição e prosa, não regras.
- Converta cadeias de proibições em instrução positiva + razão (ex.: em vez de "Não converta ausência em zero e não emita…", escreva "Marque `não pontuável` quando faltar base — zero é uma avaliação sustentada, não um marcador de lacuna, e trocá-los muda a classe calculada.").
- Links para transcrição integral, DOCX original e registro de divergências vão para uma linha "Para conferir a fonte:" dentro de "Leia primeiro" — não como leitura obrigatória.
- Orçamento: ≤ 650 palavras por SKILL.md; `experimentacao-inovacao` ≤ 1.400 e `scorecard-inovacao` ≤ 900.

### Step 3: Piloto — `potencial-inovacao/SKILL.md`

Substitua o corpo (tudo depois do frontmatter) por:

```markdown
# Potencial de inovação

Pontua uma dor ou oportunidade em cinco critérios e aplica pesos e faixas da rubrica
interna do ERIC. Não é o Innovation Project Scorecard da Strategyzer (maturidade de
evidências) nem mede o resultado de um experimento.

## Leia primeiro

- [Rubrica de potencial](references/innovation-potential-rubric.md) — critérios, pesos, faixas e a regra de ausência.
- [Levantamento documental](references/levantamento-documental-e-grilling.md) — como montar o mapa afirmação → fonte.

<bloco Grilling>

<bloco Quando usar>

## Passos

1. Delimite oportunidade, público, versão avaliada e a decisão de priorização que a nota vai informar. Registre a fase apenas como contexto.
2. Para cada critério (impacto, viabilidade, alinhamento, urgência, novidade), registre: afirmação, evidência a favor e contra, fonte com localizador, limite e nota 0–100 justificada. Distinga impacto esperado de medido, viabilidade percebida de recurso comprometido e urgência documentada de preferência do sponsor — cada par muda a nota em direções diferentes.
3. Se faltar base para um critério, marque `não pontuável` e investigue a fonte ou o responsável. Zero é uma avaliação sustentada, não um marcador de lacuna; trocá-los muda a classe.
4. Com as cinco notas justificadas, grave-as em JSON (formato no topo de `scripts/score.py`) e rode `python3 scripts/score.py notas.json`. Use o total e a classe do resultado sem ajuste editorial. Se o status vier `incomplete`, entregue a avaliação como parcial, sem classe.
5. Mostre notas, fontes, pesos, total, classe, sensibilidades (que nota mudaria a classe) e os próximos dados capazes de mudar a leitura. Registre a decisão de priorização efetivamente tomada separada da recomendação calculada.

## Exemplo

Entrada: "Classifique a oportunidade 'triagem guiada de solicitações' com a planilha de volumes e a ata do comitê."
Saída (trecho):
| Critério | Nota | Fonte | Limite |
|---|---|---|---|
| Impacto | 60 | planilha-volumes.xlsx, aba 2, C4: 120 solicitações/mês com retrabalho | redução não medida |
| Viabilidade | não pontuável | — | sem estimativa de custo; responsável: TI (a confirmar) |
Status do script: `incomplete` → sem classe; próximo dado: estimativa de custo da TI.

## Checagem final

- [ ] Cada nota tem justificativa e fonte com localizador
- [ ] Nenhuma lacuna virou zero
- [ ] Total e classe vieram de `scripts/score.py`
- [ ] Recomendação calculada separada da decisão tomada
- [ ] Sensibilidades e próximos dados listados

<bloco Contexto ERIC>

<bloco Entrega em arquivo, com `innovation_potential_assessment`>

**Proveniência:** rubrica e algoritmo adaptados do RC6 (`calculate-innovation-potential/`), revistos para preservar incompletude em vez de classificar faltas como zero.
```

(Substitua os `<bloco …>` pelos textos do Step 1. Se o plano 005 já rodou, acrescente ao
bloco de entrega: "O bloco `scores` exige as cinco linhas com `criterion`, `score`, `weight`, `justification`, além de `overall_score` e `classification` iguais ao resultado do script.")

**Verify**:
- `wc -w potencial-inovacao/SKILL.md` → ≤ 650
- `quick_validate.py potencial-inovacao` → `Skill is valid!`
- Rode os 2 evals de `_EVALS/potencial-inovacao/` na versão nova e na da tag `improve-baseline-2026-09-28` (com autorização do operador — custa chamadas de modelo). Esperado: todas as expectativas que passavam continuam passando.

**Pare aqui e peça revisão do operador ao piloto antes do rollout.** Registre no status: "piloto pronto para revisão".

### Step 4: Rollout nas outras 10 skills

Uma skill por commit, nesta ordem: `avaliacao-briefing-iqb`, `briefing-inovacao`,
`workshop-4d`, `relatorio-4d`, `workshop-3e`, `relatorio-3e`, `workshop-5c`,
`relatorio-5c`, `scorecard-inovacao`, `experimentacao-inovacao`. Para cada uma:

1. Liste as regras específicas do corpo atual (uma por linha, num rascunho fora do repo).
2. Reescreva na estrutura do Step 2, com os blocos do Step 1.
3. Confira que toda regra da lista está no texto novo **ou** num arquivo de referência já linkado. Nenhuma regra some.
4. Exemplo curto e realista (projeto fictício "Portal de Solicitações de Dados").

Notas por skill:
- **avaliacao-briefing-iqb**: manter "ausência ou ambiguidade contam `no`", reauditoria quando a amplitude das notas finais ≤ 1, "comparar versões calculando cada uma separadamente" e a frase do plano 004 com `python3 scripts/iqb.py`.
- **briefing-inovacao**: os três modos viram subseções curtas de "Passos" ("Modo briefing", "Modo one-page", "Modo perguntas"); manter limite de 12 perguntas, "nova versão, não sobrescreve", one-page A4 paisagem de uma página.
- **workshop-4d / workshop-3e / workshop-5c**: os passos D1–D4 / E1–E3 / C1–C5 continuam numerados, um parágrafo curto cada. Blueprint Mural/board = opcional, uma linha.
- **relatorio-4d / relatorio-3e / relatorio-5c**: manter a estrutura numerada do relatório; "Condição de entrada" vira passo 1.
- **scorecard-inovacao**: os três primeiros parágrafos (instrumento oficial, grilling ancorado, extração documental) viram "Leia primeiro" com 3 links; a seção de entrevista (~250 palavras) vai para `references/entrevista-e-documentos.md` **somente se** esse arquivo ainda não contiver o mesmo conteúdo (confira antes; provavelmente já contém — então só remova do SKILL.md).
- **experimentacao-inovacao**: mova "## Analise a execução" (5 itens) para `references/analise-da-execucao.md` e o detalhamento de "## Planeje ou reconstrua os testes" para `references/planejamento-dos-testes.md`; no SKILL.md fique um passo de 2–3 linhas para cada, com link e a regra-chave (Test Card individual de 4 campos; Learning Card só após execução; critério prévio nunca preenchido depois). Acrescente "Quando usar" e a linha de Proveniência: "**Proveniência:** skill própria desta pasta; cards seguem os modelos oficiais Strategyzer 2023 em `assets/`."
- **workshop-5c / relatorio-5c**: remover o link duplicado da transcrição.

**Verify (por skill)**: `wc -w` dentro do orçamento; `quick_validate.py` ok; links do Step 6 ok; os 2 evals da skill sem regressão (se autorizados).

### Step 5: Fundir `levantamento-documental-e-grilling.md` no grilling

O conteúdo de `_SHARED/levantamento-documental-e-grilling.md` se sobrepõe ao
`_SHARED/grilling-operacional.md`. Leve para o grilling apenas o que não existe lá:
(a) o mapa `afirmação → fonte/localização → natureza → limite → campo afetado`;
(b) "cópias, resumos e apresentações derivados não são confirmações independentes";
(c) "em trabalho ao vivo, não interrompa uma dinâmica para perguntar algo checável depois; registre a lacuna". Acrescente-os como uma seção "## 5. Complementos de levantamento documental".
Depois: remova os links para `levantamento-documental-e-grilling.md` dos SKILL.md; apague
`_SHARED/levantamento-documental-e-grilling.md`; remova essa entrada do mapa em
`_TOOLS/sync_shared.py` e faça o sync apagar as 9 cópias.

**Verify**: `grep -rln "levantamento-documental-e-grilling" --include=*.md . | grep -v "^./plans/\|^./VALIDACAO\|^./MELHORIAS"` → vazio (se aparecer em outra referência, troque o link para `grilling-operacional.md`); `ls */references/levantamento-documental-e-grilling.md 2>/dev/null | wc -l` → `0`; `sync --check` → 0.

### Step 6: Checagens globais

```bash
python3 - <<'PY'
import re,os,glob
for sk in sorted(glob.glob('*/SKILL.md')):
    d=os.path.dirname(sk)
    for f in [sk]+glob.glob(d+'/references/*.md'):
        for m in re.finditer(r'\]\(<?([^)>]+)>?\)',open(f).read()):
            l=m.group(1)
            if l.startswith('http'): continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f),l.split('#')[0]))): print('QUEBRADO',f,l)
PY
for s in */SKILL.md; do printf "%s %s\n" "$(wc -w < $s)" "$s"; done
grep -c "^## Grilling$" */SKILL.md
```

**Verify**: nenhum `QUEBRADO`; palavras dentro dos orçamentos; 11 × `1`.

## Test plan

- Evals do plano 009 (2 por skill), versão nova vs. tag de linha de base — critério: nenhuma expectativa que passava passa a falhar.
- Checagens estruturais do Step 6.

## Done criteria

- [ ] 11 SKILL.md na estrutura do Step 2, dentro do orçamento de palavras
- [ ] `grep -c "Ative esta skill pela tarefa solicitada" */SKILL.md` → todos `0`
- [ ] `grep -c "Para qualquer entregável em arquivo, siga" */SKILL.md` → todos `0`
- [ ] 11 × `quick_validate.py` ok; nenhum link quebrado
- [ ] Nenhum `levantamento-documental-e-grilling.md` nas skills
- [ ] Evals sem regressão (ou registro de que não foram autorizados)
- [ ] `sync_shared.py --check` → 0
- [ ] `plans/README.md` atualizado

## STOP conditions

- O operador não aprovar o piloto (Step 3) — não faça o rollout.
- Um eval que passava na linha de base falhar na versão nova e o conserto exigir reintroduzir texto repetido — reporte o caso.
- Você não conseguir encaixar uma regra específica sem estourar o orçamento em mais de 20% — reporte a skill e a regra (não corte a regra).

## Maintenance notes

- Os blocos padrão do Step 1 vivem só nos SKILL.md; se mudarem, mude nos 11 (considere um check no `sync_shared.py` que compare os blocos).
- Novas regras devem entrar na skill onde se aplicam, como passo ou item de checagem, com o porquê — não como mais um parágrafo de proibições.
