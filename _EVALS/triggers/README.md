# Avaliação de acionamento das skills

Cada JSON contém 16 consultas em português: oito devem acionar a skill e oito
não devem. As negativas testam fronteiras com skills vizinhas; as sementes do
plano 008 foram preservadas. As consultas são fictícias e não usam `_SAMPLE/`.

Rode novamente estes conjuntos sempre que uma `description` mudar. A avaliação
mede somente a competição entre estas onze skills e exige Claude CLI autenticado.
Peça autorização antes das chamadas de modelo: cada medição completa usa
11 × 16 × 3 = 528 chamadas; antes e depois somam 1.056 chamadas.

Prepare um projeto temporário fora do repositório, com todas as skills instaladas
como irmãs:

```bash
SKILL_CREATOR_DIR=/Users/mayoub/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator
SKILLS_ROOT=/Users/mayoub/Desktop/workspaces/my_skills
EVALPROJ="${TMPDIR:-/private/tmp}/skills-trigger-eval"
mkdir -p "$EVALPROJ/.claude/skills"
for skill in avaliacao-briefing-iqb briefing-inovacao experimentacao-inovacao potencial-inovacao relatorio-3e relatorio-4d relatorio-5c scorecard-inovacao workshop-3e workshop-4d workshop-5c; do
  ln -sfn "$SKILLS_ROOT/$skill" "$EVALPROJ/.claude/skills/$skill"
done
```

Para cada skill, use o Python com as dependências do skill-creator instaladas:

```bash
cd "$EVALPROJ"
PYTHONPATH="$SKILL_CREATOR_DIR" python3 -m scripts.run_eval \
  --eval-set "$SKILLS_ROOT/_EVALS/triggers/briefing-inovacao.json" \
  --skill-path "$SKILLS_ROOT/briefing-inovacao" \
  --model claude-opus-5-5 --runs-per-query 3 \
  > "${TMPDIR:-/private/tmp}/base-briefing-inovacao.json"
```

Meça a linha de base antes de alterar as descriptions. Repita depois, salvando
como `novo-<skill>.json`, e registre os resultados em `resultados.md`. A meta
por skill é acertar pelo menos sete das oito consultas de cada lado. Falta de
autenticação ou do executável interrompe as medições; registre a pendência sem
interpretar falha de execução como erro de acionamento.
