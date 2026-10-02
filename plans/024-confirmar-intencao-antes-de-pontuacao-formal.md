# Plan 024: Confirmar intenção antes de gravar pontuação formal (IQB, potencial, scorecard)

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat 2cb5c96..HEAD -- avaliacao-briefing-iqb/SKILL.md potencial-inovacao/SKILL.md scorecard-inovacao/SKILL.md`
> Se algum desses três arquivos mudou desde que este plano foi escrito, compare
> os trechos de "Current state" abaixo com o arquivo atual antes de prosseguir;
> em caso de divergência, trate como condição de STOP.

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `2cb5c96`, 2026-10-02

## Por que isto importa (e por que a ideia original mudou)

Uma auditoria cruzada com 7 repositórios externos de skills (`mattpocock/skills` entre
eles) sugeriu originalmente usar um campo `disable-model-invocation` no frontmatter para
impedir que `avaliacao-briefing-iqb`, `potencial-inovacao` e `scorecard-inovacao` —
as três únicas skills deste conjunto que calculam uma pontuação/classificação formal e
gravam um entregável "oficial" — disparassem por engano a partir de uma menção casual.

Essa ideia **não se aplica aqui**: o validador já usado neste repositório
(`quick_validate.py`, chamado nos planos 008/010) define
`ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}`
— `disable-model-invocation` não está nessa lista, e adicioná-lo faria o validador
rejeitar a skill com "Unexpected key(s) in SKILL.md frontmatter". Confirmado em
`$SC/scripts/quick_validate.py` (ver `$SC` abaixo).

O risco real de disparo acidental já é baixo — as três descriptions exigem linguagem
bem específica ("pedir nota, IQB, validação", "priorizar, ranquear, triar", "perguntar
quão validado ou maduro está um projeto") — mas o custo de um disparo indevido é real:
rodar o pipeline completo (grilling + script determinístico + render do design system)
a partir de um pedido ambíguo como "esse projeto tá indo bem?" produziria um artefato
com aparência de avaliação oficial sem o usuário ter pedido isso deliberadamente.

Correção de escopo, validadora pelo schema real: em vez de um campo de frontmatter,
adicionar uma frase curta no Passo 1 de cada uma das três skills, pedindo confirmação
quando o pedido não deixar claro que o usuário quer a nota/pontuação formal.

## Current state

| Skill | Arquivo | Linha | Palavras atuais | Orçamento | Folga |
|---|---|---|---|---|---|
| avaliacao-briefing-iqb | `avaliacao-briefing-iqb/SKILL.md` | 32 | 602 | 650 | 48 |
| scorecard-inovacao | `scorecard-inovacao/SKILL.md` | 33 | 832 | 900 | 68 |
| potencial-inovacao | `potencial-inovacao/SKILL.md` | 33 | 648 | 650 | **2 — sem folga prática** |

Trechos atuais (Passo 1 de cada skill):

`avaliacao-briefing-iqb/SKILL.md:32`:
```
1. Identifique briefing, versão, HMW, sete campos e fontes/localizadores. Transcrição é reconstrução, não aprovação; pergunte apenas por fontes, versões ou definições decisivas. Intenção não substitui evidência.
```

`scorecard-inovacao/SKILL.md:33`:
```
1. Identifique projeto, pergunta decisória, fase, data de corte, versão, público, escopo e responsáveis pela análise/gate. Preserve retratos anteriores; compare versões sem alterar notas passadas com evidências novas.
```

`potencial-inovacao/SKILL.md:33`:
```
1. Delimite oportunidade, público, versão e decisão de priorização. Registre a fase como contexto.
```

Orçamento de palavras por `SKILL.md` e comando de verificação: `plans/010-enxugar-skill-md.md:154,213,267`
(≤650 para a maioria, ≤900 para `scorecard-inovacao`, ≤1.400 para `experimentacao-inovacao`
— esta última não faz parte do escopo deste plano, pois não calcula pontuação/classificação).

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Validador do skill-creator | `SC=/Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator && python3 "$SC/scripts/quick_validate.py" <skill>` | `Skill is valid!` |
| Orçamento de palavras | `wc -w <skill>/SKILL.md` | `≤ 650` (ou `≤ 900` para scorecard-inovacao) |
| Sincronização (não deveria haver divergência nestes arquivos — eles não são cópia sincronizada) | `python3 _TOOLS/sync_shared.py --check` | código 0 (ou só divergências pré-existentes alheias a este plano — ver nota abaixo) |

**Nota sobre o `sync_shared.py --check` atual**: no momento em que este plano foi escrito,
`python3 _TOOLS/sync_shared.py --check` já retorna `DIVERGE relatorio-3e/assets/design-system/scripts/__pycache__`
(cache de bytecode, não relacionado a este plano). Isso é pré-existente — não é uma
regressão deste plano, e não deve ser corrigido aqui (fora de escopo). Confirme apenas que
nenhuma **nova** linha de divergência aparece além dessa.

## Scope

**In scope** (os únicos arquivos a modificar):
- `avaliacao-briefing-iqb/SKILL.md` (linha 32, Passo 1)
- `scorecard-inovacao/SKILL.md` (linha 33, Passo 1)
- `potencial-inovacao/SKILL.md` (linha 33, Passo 1) — **somente se** o Step 3 abaixo
  encontrar uma forma de caber sem estourar o orçamento; caso contrário, PARE neste
  arquivo e siga para o relatório final sem editá-lo.

**Out of scope** (não toque, mesmo que pareça relacionado):
- `scripts/iqb.py`, `scripts/score.py` — nenhuma mudança na lógica de cálculo.
- As outras 8 skills (`briefing-inovacao`, `experimentacao-inovacao`, `relatorio-3e`,
  `relatorio-4d`, `relatorio-5c`, `workshop-3e`, `workshop-4d`, `workshop-5c`) — nenhuma
  delas grava uma pontuação/classificação numérica formal; não fazem parte do problema
  que este plano resolve.
- Qualquer campo de frontmatter (`name`, `description`, `license`, `metadata`) — a mudança
  é só no corpo (Passo 1), não no frontmatter.
- `_SHARED/`, `_DESIGN_SYSTEM/`, `_TOOLS/` — nada aqui é sincronizado a partir de fonte
  compartilhada; é texto específico de cada skill.

## Git workflow

- Branch: `advisor/024-confirmar-intencao-pontuacao`
- Um commit por skill editada (até 2 ou 3 commits), mensagem no estilo observado em
  `git log` deste repositório (ex. `Plano 024: confirmar intenção antes da nota do IQB`).
- Não dar push nem abrir PR.

## Steps

### Step 1: `avaliacao-briefing-iqb/SKILL.md`

Na linha 32, ao final do Passo 1 (depois de "Intenção não substitui evidência."),
acrescente a frase (29 palavras):

```
Se o pedido não deixar claro que o usuário quer a nota formal do IQB, e não apenas uma leitura geral, confirme isso antes de aplicar os 40 critérios.
```

**Verify**: `wc -w avaliacao-briefing-iqb/SKILL.md` → ≤ 650 (deve ficar em torno de 631);
`SC=/Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator && python3 "$SC/scripts/quick_validate.py" avaliacao-briefing-iqb` → `Skill is valid!`

### Step 2: `scorecard-inovacao/SKILL.md`

Na linha 33, ao final do Passo 1 (depois de "evidências novas."), acrescente a frase
(36 palavras):

```
Se o pedido não deixar claro que o usuário quer o retrato formal do Scorecard, e não apenas uma opinião geral sobre o progresso, confirme isso antes de aplicar as dimensões e gravar o retrato datado.
```

**Verify**: `wc -w scorecard-inovacao/SKILL.md` → ≤ 900 (deve ficar em torno de 868);
validador → `Skill is valid!`

### Step 3: `potencial-inovacao/SKILL.md` — só se houver espaço

Este arquivo tem 648/650 palavras — **2 palavras de folga, insuficiente** para a mesma
frase (que tem ~27-30 palavras nas outras skills). Duas saídas possíveis, nessa ordem de
preferência:

1. Condense outra frase do Passo 1 ou do Passo 2 em até ~30 palavras para abrir espaço,
   **sem remover conteúdo normativo** (regras de pontuação, proibição de zerar lacunas,
   etc.) — só compactar redundância de estilo, se houver. Se não encontrar nada compactável
   sem perda de conteúdo, não invente corte.
2. Se não houver nada compactável, **não edite este arquivo**. Registre no relatório final
   que `potencial-inovacao` ficou de fora por falta de orçamento, e que a decisão de
   levantar o teto de 650 para esta skill (como já existe para `scorecard-inovacao` e
   `experimentacao-inovacao`) cabe ao operador, não ao executor.

**Verify (se editado)**: `wc -w potencial-inovacao/SKILL.md` → ≤ 650; validador →
`Skill is valid!`

## Test plan

Não há teste automatizado de comportamento para esta mudança (ela ajusta uma instrução de
prosa, não lógica de script). Validação é estrutural:
- Os 3 (ou 2) arquivos editados passam no `quick_validate.py`.
- Nenhum arquivo fica acima do próprio orçamento de palavras.
- `git diff` mostra apenas a frase adicionada em cada arquivo, nada mais.

## Done criteria

Machine-checkable. TODAS devem valer para os arquivos efetivamente editados:

- [ ] `wc -w avaliacao-briefing-iqb/SKILL.md` ≤ 650
- [ ] `wc -w scorecard-inovacao/SKILL.md` ≤ 900
- [ ] `wc -w potencial-inovacao/SKILL.md` ≤ 650 (ou arquivo não tocado, com nota no relatório)
- [ ] `quick_validate.py` retorna `Skill is valid!` para cada skill editada
- [ ] `git status` não mostra nenhum arquivo fora da lista em "Scope"
- [ ] `plans/README.md` com a linha deste plano atualizada

## STOP conditions

Pare e reporte (não improvise) se:
- O texto nas linhas citadas em "Current state" não bater com o arquivo atual (deriva
  desde que este plano foi escrito).
- `potencial-inovacao/SKILL.md` não tiver nenhuma frase seguramente compactável sem perda
  de conteúdo normativo (siga a Opção 2 do Step 3, não force um corte).
- `quick_validate.py` falhar por qualquer motivo além do que este plano antecipa.
- Você perceber que `briefing-inovacao`, `experimentacao-inovacao` ou qualquer relatório/
  workshop também grava uma pontuação numérica formal (contradizendo a premissa deste
  plano) — nesse caso, pare e reporte antes de estender o escopo sozinho.

## Maintenance notes

- Se, no futuro, o teto de `potencial-inovacao` for levantado (como já aconteceu com
  `scorecard-inovacao` e `experimentacao-inovacao` no plano 010), revisite o Step 3 e
  aplique a frase pendente.
- Esta mudança é só textual/comportamental — não cria nenhum mecanismo que realmente
  impeça o disparo da skill (isso exigiria suporte de uma `allowed-tools`/campo de
  invocação que o schema atual não tem). Se a Anthropic adicionar um campo real de
  invocação restrita ao schema do Agent Skills no futuro, isto pode ser revisitado.
- Não confundir com o Plano 008 (descriptions/acionamento) — aquele mede se a skill
  dispara nos casos certos; este plano trata do que a skill faz depois de disparada.
