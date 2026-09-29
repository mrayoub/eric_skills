# Plan 023: Distinguir critério local atingido de aprovação para expansão

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- experimentacao-inovacao/references/analise-da-execucao.md experimentacao-inovacao/references/base-metodologica.md _EVALS/experimentacao-inovacao/casos-criterio-local.json _EVALS/experimentacao-inovacao/files/sessoes-criterio-atingido.md _EVALS/experimentacao-inovacao/files/plano-sem-criterio.md _EVALS/experimentacao-inovacao/files/sessoes-coleta-incompleta.md _EVALS/README.md`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** TODO
- **Prioridade:** P2
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 009 (DONE); 016 recomendado antes de exportar os cards
- **Categoria:** docs
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A11; seleção de todos os achados autorizada pelo operador

## Por que importa

A orientação atual pode fazer o executor deixar inconclusivo um critério local previamente definido e efetivamente observado, por confundi-lo com aprovação geral. A ambiguidade foi encontrada documentalmente; seu efeito em uma execução de modelo não foi medido. Esclarecer o alcance da conclusão e preparar casos fictícios permite avaliar o comportamento depois, com custo separado.

## Estado atual e convenções

`experimentacao-inovacao/references/analise-da-execucao.md:7`:
> não infira taxa populacional, ganho causal ou aprovação formal de um Test Card.
`references/base-metodologica.md:9` permite “Status do critério original, se o teste efetivamente produziu a evidência exigida”.
`_EVALS/experimentacao-inovacao/evals.json`, caso 1, exige declarar o critério de quatro entre cinco não atingido, pois somente três concluíram sem ajuda. `files/plano-previo.md` fixa cinco sessões elegíveis, um gabarito e limiar quatro de cinco antes da coleta; não há autorização de expansão. `files/sessoes.md` contém três sucessos, uma falha e um sucesso com ajuda, sem exclusões.
O conjunto original tem dois casos; `_EVALS/README.md` valida exatamente dois por skill. Crie um conjunto adicional separado; não quebrar a checagem dos 22 casos originais. Todas as fixtures começam com marcador de material fictício e têm até 60 linhas.

## Comandos necessários

Os comandos partem da raiz do repositório e usam `python3`, biblioteca padrão e `rg`. Não há instalação, geração de binários ou chamada de modelo. Não adicionar testes que apenas espelhem o texto do documento. A validação estrutural não comprova compreensão pelo modelo.

| Finalidade | Comando | Resultado esperado |
| --- | --- | --- |
| Espaços/diff | `git diff --check` | Exit 0 |
| Escopo | `git status --short` e `git diff --name-only` | Somente arquivos permitidos, descontando alterações preexistentes |

## Escopo

**Arquivos que podem mudar:**

- `experimentacao-inovacao/references/analise-da-execucao.md`
- `experimentacao-inovacao/references/base-metodologica.md`
- `_EVALS/experimentacao-inovacao/casos-criterio-local.json` (criar)
- `_EVALS/experimentacao-inovacao/files/sessoes-criterio-atingido.md` (criar)
- `_EVALS/experimentacao-inovacao/files/plano-sem-criterio.md` (criar)
- `_EVALS/experimentacao-inovacao/files/sessoes-coleta-incompleta.md` (criar)
- `_EVALS/README.md`
- `plans/README.md` (somente status e evidências de conclusão deste plano)

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/023-experimentacao-criterio-local-e-limites`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Esclarecer o alcance da avaliação

Na etapa 4 de analise-da-execucao.md, substitua a proibição genérica de aprovação por instrução explícita: um critério **local, definido antes da coleta**, pode ser declarado atingido/não atingido quando a execução produziu as observações exigidas; isso não demonstra taxa populacional, causalidade nem autoriza expansão. Se amostra, protocolo, gabarito ou observações forem insuficientes para decidir, declare inconclusivo e explique a falta. Na base-metodologica.md, acrescente um exemplo curto de quatro sucessos em cinco sessões elegíveis, mantendo limites. Nunca reutilize uma medida descoberta após a coleta para reescrever o limiar original. Preserve a prioridade das decisões vigentes do 3E e as evidências contrárias.

**Verificar**:

```bash
rg -n 'critério local|atingido|não atingido|inconclusivo|expansão' experimentacao-inovacao/references/analise-da-execucao.md experimentacao-inovacao/references/base-metodologica.md
```

**Esperado:** as referências explicitam critério local e os três estados; expansão continua separada.

### Passo 2: Criar quatro casos adicionais sem mudar os dois originais

Crie casos-criterio-local.json no mesmo formato skill_name/evals, IDs 1–4. Caso 1 reutiliza plano-previo.md+sessoes.md: 3/5, critério não atingido. Caso 2 usa plano-previo.md+sessoes-criterio-atingido.md: P01/P02/P03/P04 corretos sem ajuda, P05 com ajuda, logo 4/5, critério local atingido; sem taxa populacional, ganho de tempo, causalidade ou decisão de escala. Caso 3 usa plano-sem-criterio.md+sessoes-criterio-atingido.md: plano exploratório sem limiar anterior; resultados descritivos, sem inventar aprovação. Caso 4 usa plano-previo.md+sessoes-coleta-incompleta.md: somente P01/P02/P04 observados com sucesso, P03/P05 sem registros; não trocar o denominador planejado cinco por três nem concluir se quatro de cinco ocorreu. Use nomes/área fictícios já existentes. Cada caso tem 4–7 expectativas: ligação ao plano, denominador, critério, fontes, limites e ação. Não executar os casos nesta implementação.

**Verificar**:

```bash
python3 - <<'CHECK'
import json
from pathlib import Path
root=Path('_EVALS/experimentacao-inovacao')
data=json.loads((root/'casos-criterio-local.json').read_text())
assert data['skill_name']=='experimentacao-inovacao'
assert [case['id'] for case in data['evals']]==[1,2,3,4]
for case in data['evals']:
    assert case['prompt'] and case['expected_output']
    assert 4 <= len(case['expectations']) <= 7
    for name in case['files']:
        path=root/name
        assert path.is_file(),path
        text=path.read_text()
        assert text.startswith('> Material fictício para avaliação de skill.')
        assert len(text.splitlines())<=60,path
original=json.loads((root/'evals.json').read_text())
assert [case['id'] for case in original['evals']]==[1,2]
print('ok: quatro casos adicionais; conjunto original preservado')
CHECK
```

**Esperado:** ok: quatro casos adicionais; conjunto original preservado.

### Passo 3: Documentar execução posterior e limites da validação local

Em _EVALS/README.md, adicione seção do conjunto complementar e caminho explícito. Mantenha intacta a checagem dos 11 conjuntos/22 casos originais. Informe que a validação acima confere só estrutura e insumos; comportamento requer execução posterior, com autorização específica de custo. Descreva comparação da versão-base 3404a5c e versão corrigida com os mesmos casos, em contextos novos e sem fornecer expectativas ao agente. Não criar benchmark fictício nem marcar comportamento como aprovado.

**Verificar**:

```bash
git diff --check && git diff -- _EVALS/experimentacao-inovacao/evals.json _EVALS/experimentacao-inovacao/files/plano-previo.md _EVALS/experimentacao-inovacao/files/sessoes.md
```

**Esperado:** exit 0; nenhum diff nos três arquivos originais.

## Plano de verificação

Execute a checagem estrutural abaixo. Recalcule manualmente 3/5 e 4/5 com as cinco linhas das fixtures; no caso incompleto, três observações não substituem as cinco sessões planejadas. Revisão documental deve confirmar que critério local não virou autorização de escala nem validação populacional. Execução comportamental fica registrada como NÃO RODADA até haver autorização de custo.

Verificação local específica:

```bash
python3 - <<'CHECK'
import json
from pathlib import Path
root=Path('_EVALS/experimentacao-inovacao')
data=json.loads((root/'casos-criterio-local.json').read_text())
assert data['skill_name']=='experimentacao-inovacao'
assert [case['id'] for case in data['evals']]==[1,2,3,4]
for case in data['evals']:
    assert case['prompt'] and case['expected_output']
    assert 4 <= len(case['expectations']) <= 7
    for name in case['files']:
        path=root/name
        assert path.is_file(),path
        text=path.read_text()
        assert text.startswith('> Material fictício para avaliação de skill.')
        assert len(text.splitlines())<=60,path
original=json.loads((root/'evals.json').read_text())
assert [case['id'] for case in original['evals']]==[1,2]
print('ok: quatro casos adicionais; conjunto original preservado')
CHECK
```

## Critérios de conclusão

- [ ] Checagem estrutural específica passa; avaliação com modelo registrada como não rodada.
- [ ] Os casos e resultados especificados acima foram conferidos e registrados no fechamento.
- [ ] `git diff --check` retorna exit 0.
- [ ] Revisão de `git status --short`/`git diff --name-only` confirma o escopo e preservação de alterações preexistentes.
- [ ] Linha deste plano em `plans/README.md` atualizada com evidências e limitações, sem marcar bateria de modelo como executada.

## Condições de parada

Pare e reporte se:

- Os trechos atuais divergirem sem explicação pelas dependências deste plano.
- Uma verificação falhar duas vezes após tentativa razoável de correção, fora da falha inicial esperada de regressão.
- Faltar ambiente necessário, a solução pedir instalação não autorizada ou mudança fora do escopo.
- O critério original do fixture tiver mudado; uma referência permitir pós-definir sucesso com dados já vistos; exigir expandir o conjunto original ou chamar modelo para concluir a tarefa estrutural; os casos dependerem de material real.

## Manutenção

Novos métodos devem separar critério de decisão local, inferência estatística e decisão de expansão. Não generalizar este exemplo para limiares populacionais que a amostra pequena não permite avaliar. Manter eval complementar separado até revisão explícita da organização dos conjuntos.
