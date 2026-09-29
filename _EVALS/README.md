# Avaliações das skills de inovação

Os conjuntos comportamentais do plano 009 usam somente o projeto fictício
**Portal de Solicitações de Dados**, da **Gerência de Atendimento a Agentes**.
Ana Souza, Bruno Lima e os identificadores de participantes também são fictícios.
Nenhum insumo foi copiado de material real. Cada fixture tem no máximo 60 linhas
e começa com `> Material fictício para avaliação de skill.`

## Pastas e cobertura

| Pasta | Objeto avaliado |
| --- | --- |
| `briefing-inovacao/` | Sete campos, rastreabilidade, sponsor ausente e meta não aprovada |
| `avaliacao-briefing-iqb/` | Quarenta critérios, cálculo por script e veto de evidências |
| `potencial-inovacao/` | Cinco notas, cálculo ponderado e ausência de viabilidade |
| `workshop-4d/` | Preparação D1–D4 e registro de D4 não realizado |
| `relatorio-4d/` | Denominadores, dissensos e créditos divergentes |
| `workshop-3e/` | Método pelo risco, cards individuais e baseline ausente |
| `relatorio-3e/` | Rota híbrida, cards prospectivos e reconstrução retrospectiva |
| `workshop-5c/` | Preparação C1–C5, agenda adaptada e presença ausente |
| `relatorio-5c/` | Falas, apuração e conflito entre ata e votação |
| `experimentacao-inovacao/` | Critério não atingido, Learning Card e plano sem dados |
| `scorecard-inovacao/` | Estados de evidência, limites de entrevistas e ausência de média geral |
| `triggers/` | Seleção da skill pelo pedido; conjunto distinto do teste comportamental |

Cada pasta comportamental contém `evals.json` e `files/`. São dois casos por
skill: `id: 1` com suporte para a tarefa; `id: 2` com lacuna ou contradição decisiva.
Os casos têm de quatro a sete expectativas verificáveis na saída; não exigem
copiar uma resposta-modelo nem escolher uma nota previamente desejada.

O cálculo pode ser determinístico e verificável sem fixar as notas atribuídas
pelo avaliador: confira o total e a classe contra as notas efetivamente justificadas.
Identificadores, números, datas e HMW originais são dados que devem ser preservados;
o restante da redação é livre, desde que cumpra o comportamento esperado.

## Validar a estrutura sem chamadas de modelo

Na raiz do repositório:

```bash
python3 - <<'PY'
import json
from pathlib import Path

root = Path('_EVALS')
paths = sorted(root.glob('*/evals.json'))
assert len(paths) == 11
for path in paths:
    data = json.loads(path.read_text(encoding='utf-8'))
    assert data['skill_name'] == path.parent.name
    assert [case['id'] for case in data['evals']] == [1, 2]
    for case in data['evals']:
        assert case['prompt'] and case['expected_output']
        assert 4 <= len(case['expectations']) <= 7
        for name in case['files']:
            fixture = path.parent / name
            assert fixture.is_file(), fixture
            text = fixture.read_text(encoding='utf-8')
            assert text.startswith('> Material fictício para avaliação de skill.')
            assert len(text.splitlines()) <= 60, fixture
print('ok: 11 conjuntos, 22 casos')
PY
```

Essa checagem valida os casos e seus insumos. Ela não executa as skills nem prova
que um modelo cumpre as expectativas.

## Conjunto complementar: critério local da experimentação

[`experimentacao-inovacao/casos-criterio-local.json`](experimentacao-inovacao/casos-criterio-local.json) acrescenta quatro casos fictícios aos dois casos originais: critério prévio não atingido (3/5), atingido localmente (4/5), plano exploratório sem limiar e coleta incompleta. O conjunto original `experimentacao-inovacao/evals.json` e a checagem de 11 conjuntos/22 casos acima continuam independentes.

Para conferir a estrutura sem chamadas de modelo, carregue esse JSON, exija `skill_name: experimentacao-inovacao`, IDs 1–4, quatro a sete expectativas por caso e verifique que cada arquivo listado existe, começa com o marcador de material fictício e tem no máximo 60 linhas. Isso confere os insumos; **não mede o comportamento**. A execução comportamental permanece **não rodada** e exige autorização específica de custo.

Em uma comparação futura, use os mesmos quatro casos e fixtures em contextos novos contra a versão-base `3404a5c` e a versão corrigida. Forneça ao agente somente o pedido e os arquivos do caso; guarde `expectations` para avaliação posterior. Registre versão, modelo, configuração, saída e evidência por expectativa antes de comparar. Não trate a existência dos casos como benchmark aprovado.

## Executar os casos e comparar versões

Use a skill **skill-creator da Anthropic**, no fluxo de execução de evals/benchmark.
Informe separadamente o caminho da skill (`<raiz>/<skill>/`) e o arquivo do
conjunto (`<raiz>/_EVALS/<skill>/evals.json`). Aqui, os caminhos de `files` são
relativos à pasta do conjunto, não à pasta da skill. Se o executor exigir
caminhos absolutos, converta-os em uma cópia temporária do JSON; preserve o
conjunto versionado e não instale `evals/` nos pacotes distribuídos.

Exemplo de instrução ao executor, após autorizar o custo:

> Use skill-creator para executar os casos de briefing-inovacao. Skill path:
> `<raiz>/briefing-inovacao/`; eval file:
> `<raiz>/_EVALS/briefing-inovacao/evals.json`; resolva os arquivos de entrada
> relativamente à pasta desse eval file. Execute em contexto novo, registre a
> saída e as evidências para cada expectativa e faça o benchmark por caso.

Compare a versão atual com a tag `improve-baseline-2026-09-28`. Prepare a cópia
de referência em um diretório temporário novo, sem alterar a árvore atual:

```bash
EVAL_TMPDIR=$(mktemp -d "${TMPDIR:-/private/tmp}/skills-evals.XXXXXX")
git worktree add "$EVAL_TMPDIR/baseline" improve-baseline-2026-09-28
```

A tag anterior ao plano 009 não contém esses conjuntos. Use os mesmos
`evals.json` e fixtures da árvore atual nas duas versões; altere apenas o
skill path para `"$EVAL_TMPDIR/baseline/<skill>/"` na execução da referência.
Registre o hash da versão atual e o da tag, modelo, configuração e data.
Para medir uma mudança específica, como o plano 010, preserve também uma cópia
do estado imediatamente anterior à mudança e compare antes/depois com ela.

Execute cada caso em contexto novo, sem fornecer as expectativas ao agente
que produz a entrega. Aplique as expectativas depois, lendo saída, arquivos
gerados e registro de execução; marque cada item como passou/falhou com evidência.
Falha técnica ou limite de uso deve ser registrada como execução inválida,
sem virar falha comportamental ou acerto artificial. Salve cada caso concluído
antes de iniciar outro e pare no primeiro erro técnico.

Peça autorização antes das chamadas de modelo. Comece sequencialmente por um
caso de lacuna, confira o procedimento e só amplie com um orçamento autorizado.
Uma execução completa usa 22 casos por versão; duas versões são 44 execuções,
mais eventuais chamadas de avaliação e turnos necessários. Não há promessa de
consumo fixo. Esses casos produzem entregáveis e podem custar mais por execução
que uma consulta de acionamento; não execute todos em paralelo automaticamente.

Guarde a linha de base atual em `_EVALS/_baseline-2026-09-28/` quando autorizada,
com saídas, registros por expectativa e benchmark. Execuções posteriores devem
ter pastas identificadas por versão/data, sem sobrescrever resultados anteriores.

## Regra de manutenção e status

Execute os casos comportamentais antes e depois de qualquer mudança no corpo
de um `SKILL.md`, em particular o piloto e a expansão do plano 010. O adiamento
do teste de acionamento em `triggers/` não substitui essa comparação de comportamento.
Qualquer falha nova deve virar um caso antes da correção; preservar o resultado
dos casos de lacuna é o critério de não piorar a skill.

**Linha de base não rodada.** Nesta implementação do plano 009 foram criados
e validados somente os conjuntos e as fixtures. Nenhuma chamada de modelo foi
feita e não há benchmark comportamental concluído.
