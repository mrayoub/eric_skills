# Avaliação de acionamento das skills

Cada JSON contém 16 consultas em português: oito devem acionar a skill e oito
não devem. As negativas testam fronteiras com skills vizinhas; as sementes do
plano 008 foram preservadas. As consultas são fictícias e não usam `_SAMPLE/`.

Os conjuntos de `briefing-inovacao` e das skills vizinhas agora usam os nomes
Entrevista Inicial de sete campos, Briefing e Perguntas para fechar lacunas.
As escolhas históricas em `resultados.md` foram registradas com consultas anteriores
à mudança de nomenclatura; devem ser medidas novamente antes de comparar taxas.

## Revisão local nesta implementação

Por instrução do operador, o plano 008 foi avaliado nesta sessão de Codex antes
e depois de editar as descriptions, sem chamadas ao Claude Opus. Consulte
[resultados.md](resultados.md) para as escolhas por consulta e os limites do método.

Para repetir essa revisão, apresente o catálogo de `name` e `description` das catorze
skills e cada consulta a um avaliador, peça uma escolha primária ou `nenhuma`,
registre todas as escolhas antes de compará-las com `should_trigger` e calcule
`(escolha == skill do conjunto) == should_trigger`. Salve a linha de base antes
de editar o catálogo e repita com as mesmas consultas após a mudança.

A revisão desta sessão não foi cega: o avaliador já tinha lido planos e rótulos.
Ela não reproduz invocações reais de skills nem as três tentativas por consulta
do `run_eval`. Uma nova avaliação independente deve ocultar os rótulos e o
resultado anterior do avaliador e usar contexto novo para cada consulta.

## Medição empírica com Claude CLI

**Procedimento suspenso após a auditoria de 28/09/2026.** Os comandos abaixo
documentam o procedimento original do plano; não os execute como uma bateria
até corrigir e validar o runner. Veja a auditoria em [resultados.md](resultados.md).
O `run_eval` observado trata limite, timeout e algumas falhas como ausência de
acionamento, o que produz acertos artificiais nas negativas. Ele também cria
um comando substituto, em vez de observar diretamente a skill nativa.

Para retomar, prepare um runner que:

- Instale as catorze skills nativas, incluindo a avaliada, sem um comando duplicado
  ou substituto. Registre o catálogo recebido por cada sessão e detecte o nome
  real em `Skill` ou a leitura do `SKILL.md` correspondente.
- Execute sequencialmente, começando com no máximo quatro chamadas autorizadas:
  uma positiva e uma negativa, nas versões anterior e posterior.
- Restrinja as ferramentas a leitura/seleção de skills, reduza o número de
  turnos e encerre após observar a seleção. Não execute os entregáveis pedidos
  por essas consultas: o objeto desta avaliação é apenas o acionamento.
- Separe `acionou`, `não acionou` e `erro`. Limite de uso, autenticação, timeout,
  processo malsucedido, catálogo incompleto e fluxo inválido são erros; não
  entram na taxa de acerto. Interrompa a rodada no primeiro erro.
- Grave cada tentativa imediatamente, com versão, modelo, consulta, catálogo,
  escolha observada e estado de execução, permitindo retomar sem repetir as
  tentativas válidas. Preserve stdout/stderr de falhas para diagnóstico.
- Só amplie a amostra após validar o diagnóstico e obter autorização para o
  novo número de chamadas. Não repita automaticamente a bateria de 1.056.

Compare as descriptions de `21cef5b` (antes) e `9ac08f3` (depois), sem alterar
a árvore de trabalho atual. Mesmo o diagnóstico de quatro chamadas não
substitui a comparação completa nem atende sozinho à meta por skill do plano.

Rode novamente estes conjuntos sempre que uma `description` mudar. O procedimento
empírico abaixo mede a competição entre estas catorze skills e exige Claude CLI autenticado.
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
