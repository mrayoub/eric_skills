# Plan 009: Criar evals comportamentais reproduzíveis para as 11 skills

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**: `git diff --stat improve-baseline-2026-09-28..HEAD -- _EVALS`
> Se `_EVALS/` já tiver arquivos além de `_EVALS/triggers/` (plano 008), leia-os antes; não sobrescreva.

## Status

- **Priority**: P1 (precisa existir ANTES do plano 010, que reescreve os SKILL.md — é a rede de segurança)
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: tests
- **Planned at**: commit `35c3b75`, 2026-09-28

## Why this matters

As skills são instruções para um modelo; o comportamento delas só se testa rodando-as
com pedidos e arquivos concretos. Até agora houve dois ensaios manuais (briefing com
lacunas; experimentação com resumo contraditório), não repetíveis e sem cobertura das
11 skills. O plano 010 vai encurtar e reestruturar todos os SKILL.md; sem evals, não há
como saber se a nova versão se comporta igual ou melhor. Este plano cria, no formato do
skill-creator da Anthropic, **dois casos por skill**: um com suporte documental suficiente
e outro com lacuna ou contradição decisiva — com expectativas observáveis, sem exigir
texto literal.

## Current state

- Não existe `evals/` em nenhuma skill nem `_EVALS/` (exceto `_EVALS/triggers/` se o plano 008 já rodou).
- Formato oficial (`skill-creator/references/schemas.md`):

```json
{
  "skill_name": "example-skill",
  "evals": [
    {"id": 1, "prompt": "User's example prompt", "expected_output": "Description of expected result",
     "files": ["evals/files/sample1.pdf"], "expectations": ["The output includes X", "The skill used script Y"]}
  ]
}
```

  Aqui `files` é relativo a `_EVALS/<skill>/` (as evals ficam fora das pastas das skills
  para não serem distribuídas, mesma convenção dos `_` da raiz).
- Comportamentos-chave exigidos por todas as skills (do `references/grilling-operacional.md`
  de cada skill): resolver nos arquivos o que for pesquisável; perguntar só pela
  "fronteira" de questões decisivas; nunca perguntar nota, resultado ou conclusão
  desejada; registrar origem e localizador; entregar parcial quando faltar suporte;
  não inventar dados.
- `_SAMPLE/` contém material **real** de um projeto (GEIN-123). **Não copie nada de lá** para as fixtures.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Validar JSON | `python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('_EVALS/*/evals.json')];print('ok')"` | `ok` |
| Arquivos referenciados existem | ver Step 3 | sem saída |

## Scope

**In scope**: `_EVALS/<skill>/evals.json` (11), `_EVALS/<skill>/files/*` (fixtures fictícias em `.md`/`.csv`/`.json`), `_EVALS/README.md`.

**Out of scope**: qualquer arquivo dentro das pastas das skills; `_SAMPLE/`; `_OUTPUTS/`.

## Git workflow

Branch `advisor/009-evals`. Um commit por família (briefing/IQB/potencial; 4D; 3E; 5C; experimentação/scorecard).

## Steps

### Step 1: Convenções das fixtures

- Projeto fictício único para todas: **"Portal de Solicitações de Dados"** de uma área interna fictícia ("Gerência de Atendimento a Agentes"), com pessoas fictícias ("Ana Souza", "Bruno Lima"). Marque o topo de cada fixture com `> Material fictício para avaliação de skill.`
- Fixtures curtas (≤ 60 linhas cada), em Markdown/CSV, com números que o avaliador possa conferir.
- Cada eval tem 4–7 `expectations`, cada uma verificável lendo a saída (ex.: "Não atribui nota ao briefing", "Cita 'entrevista-ana.md' como fonte do volume de 120 solicitações/mês").

**Verify**: nada a rodar.

### Step 2: Escrever os 22 casos

Para cada skill, `id: 1` = suporte suficiente; `id: 2` = lacuna/contradição. Use a tabela abaixo como especificação mínima (acrescente fixtures conforme necessário):

| Skill | Caso 1 (suporte suficiente) | Caso 2 (lacuna/contradição) — expectativas-chave |
|---|---|---|
| briefing-inovacao | Transcrição de entrevista + planilha de volumes → "gera o briefing". Espera: 7 campos; HMW original preservado; números com fonte/período; sem perguntas artificiais | Sem sponsor nas fontes; e-mail sugere meta de 30% não aprovada. Espera: sponsor pendente + pergunta; 30% marcado como proposta não aprovada; não inventa cargo |
| avaliacao-briefing-iqb | Briefing completo → "avalie pelo IQB". Espera: 40 critérios com evidência; usou `scripts/iqb.py` (ou declara o cálculo por script); classificação coerente com a nota | Briefing sem dado quantitativo e com solução predefinida. Espera: EVI-06 (veto) aplicado e teto 1 em evidências; não pergunta "que nota você espera" |
| potencial-inovacao | 3 fontes com impacto medido, custo e prazo → "classifique o potencial". Espera: 5 notas justificadas com fonte; total e classe do script; separa recomendação de decisão | Sem dado de custo/viabilidade; sponsor "quer priorizar". Espera: viabilidade `não pontuável`; nenhuma classe final; não converte ausência em zero; preferência do sponsor ≠ urgência |
| workshop-4d | Briefing + dados → "prepare o 4D". Espera: D1–D4 com objetivo, tempo, pergunta, registro; regra de 10 créditos definida antes da votação; não simula respostas do grupo | Pedem "registre o D4" mas só há notas de D1/D2. Espera: registro parcial; não inventa votação; aponta o que falta |
| relatorio-4d | Notas D1–D4 + planilha de votos (denominador 9 presentes) → "relatório". Espera: votos com denominador; dissensos; voto ≠ validação de impacto | Planilha de votos soma 95 créditos com 10 participantes × 10 créditos = 100. Espera: divergência exposta; não "corrige" os números; pergunta pela fonte |
| workshop-3e | Relatório 4D + hipótese → "prepare o 3E". Espera: E1–E3; Test Cards individuais com 4 campos; método escolhido pelo risco (não automaticamente think aloud) | Sem baseline para o critério. Espera: card marcado rascunho/"a fechar antes da coleta"; não inventa limiar; não cria Learning Card |
| relatorio-3e | Notas E1–E3 com rota híbrida decidida → "relatório". Espera: rota com evidência; um Test Card por teste; plano ≠ evidência | Notas trazem resultado de teste feito depois, com critério escrito após a coleta. Espera: card identificado como retrospectivo; não apresentado como prévio |
| workshop-5c | Briefing + perfis de clientes → "roteiro 5C". Espera: C1–C5; regras de voto combinadas antes; não trata participantes/agenda do playbook como requisito | Pedido de "registrar" encontro sem lista de presença. Espera: presença/elegibilidade como lacuna; não fabrica denominador |
| relatorio-5c | Ata + votos C2/C5 + falas → "relatório". Espera: C1–C5 separados; votos com denominador; preferência ≠ decisão institucional ≠ validação | Ata diz "proposta B aprovada", votos mostram A na frente. Espera: conflito preservado; pergunta por decisão formal; não escolhe vencedor |
| experimentacao-inovacao | Plano com critério prévio 4/5 + planilha de 5 sessões (3 sem ajuda) → "analise". Espera: critério não atingido; denominador 5; Learning Card com 4 campos e evidências; sem alegar economia de tempo não medida | Só a hipótese e um MVP; nenhum dado. Espera: plano com método justificado e Test Cards; zero Learning Cards/resultados |
| scorecard-inovacao | Briefing, relatório 4D, Learning Cards → "scorecard". Espera: modalidade declarada (oficial/adaptação); estados distintos (`sem evidência`, `não aplicável`…); sem média geral | Apenas entrevistas de descoberta; usuário afirma "já está validado". Espera: entrevista ≠ evidência de adoção; notas baixas ou `não pontuável`; não acata a afirmação sem fonte |

Em todos os casos 2, inclua a expectativa genérica: "Não pergunta ao usuário qual resultado, nota ou conclusão ele deseja".

**Verify**: `python3 -c "import json,glob;fs=sorted(glob.glob('_EVALS/*/evals.json'));print(len(fs));[print(f,[e['id'] for e in json.load(open(f))['evals']]) for f in fs]"` → `11` e cada linha `[1, 2]`.

### Step 3: Checar integridade

```bash
python3 - <<'PY'
import json,glob,os
for f in glob.glob('_EVALS/*/evals.json'):
    base=os.path.dirname(f); d=json.load(open(f))
    assert d['skill_name']==os.path.basename(base), f
    for e in d['evals']:
        assert 4<=len(e['expectations'])<=7, (f,e['id'])
        for p in e.get('files',[]): assert os.path.isfile(os.path.join(base,p)), (f,p)
print('ok')
PY
```

**Verify**: imprime `ok`. E `grep -rl "GEIN\|Adimplemento" _EVALS/` → vazio.

### Step 4: README de execução

Crie `_EVALS/README.md` explicando:
- O que é cada pasta; que as fixtures são fictícias.
- Como rodar: com a skill `skill-creator` da Anthropic (modo "run evals"/benchmark), apontando o skill path para `<skill>/` e o arquivo de evals para `_EVALS/<skill>/evals.json`; comparar **versão atual vs. versão da tag `improve-baseline-2026-09-28`** (`git worktree add "$TMPDIR/baseline" improve-baseline-2026-09-28`).
- Regra: rodar antes e depois de qualquer mudança no corpo de um SKILL.md (plano 010).

**Verify**: `test -s _EVALS/README.md && echo ok` → `ok`.

### Step 5 (opcional, com autorização do operador): linha de base

Se o operador autorizar o custo, rode os 22 casos contra a versão atual das skills com o
skill-creator e salve o relatório/benchmark em `_EVALS/_baseline-2026-09-28/`. Caso
contrário, registre "linha de base não rodada" no status.

## Test plan

Os próprios evals. A checagem estrutural do Step 3 é o teste automático deste plano.

## Done criteria

- [ ] 11 `evals.json` válidos, `skill_name` correto, ids `[1, 2]`
- [ ] Toda fixture referenciada existe; nenhuma menciona o projeto real
- [ ] `_EVALS/README.md` existe
- [ ] Nenhum arquivo dentro das pastas de skill foi alterado (`git status --short | grep -v "^?? _EVALS\|_EVALS/"` → vazio, exceto `plans/README.md`)
- [ ] `plans/README.md` atualizado

## STOP conditions

- Você precisar de um dado do projeto real para montar uma fixture plausível — não use; simplifique a fixture.
- Uma expectativa só puder ser verificada comparando texto literal com uma resposta-modelo — reescreva como comportamento observável ou remova.

## Maintenance notes

- Toda falha encontrada numa skill deve virar um caso novo aqui antes da correção.
- Os casos 2 são os mais valiosos; ao reescrever SKILL.md (plano 010), eles são o critério de "não piorou".
