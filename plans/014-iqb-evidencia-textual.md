# Plan 014: Rejeitar evidências nulas ou de tipo inadequado no IQB

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- avaliacao-briefing-iqb/scripts/iqb.py _TESTS/avaliacao-briefing-iqb/test_iqb.py`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** DONE
- **Prioridade:** P1
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 012 (fontes geradas); 004 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A02; seleção de todos os achados autorizada pelo operador

## Por que importa

Quarenta respostas podem passar pela validação com evidência nula. A entrada precisa trazer texto de suporte ou uma descrição explícita de ausência, antes de qualquer nota ser calculada. Essa verificação é de preenchimento, não de qualidade da evidência.

## Estado atual e convenções

`avaliacao-briefing-iqb/scripts/iqb.py:215`, em `_validate_complete_evaluations`:
```python
if not str(item.get("evidence", "")).strip():
    raise ValueError(f"{item['criterion_id']}: evidence or an explicit absence note is required")
```
`str(None)` gera texto não vazio. O mesmo vale para números, listas e objetos. A função pública `calculate_iqb_from_evaluations` chama essa verificação.
`_TESTS/avaliacao-briefing-iqb/test_iqb.py` usa `answers(True/False)` para produzir CLA/EVI/OUT/ACT-01…10. Siga `test_empty_evidence_is_rejected` e `test_cli_success_and_missing_item_error`.

## Comandos necessários

Os comandos partem da raiz do repositório. O Python com dependências que passou na auditoria foi:

```bash
PLAN_PYTHON='/private/tmp/claude-945238751/-Users-mayoub-Desktop-workspaces-my-skills/609c5081-03a7-4c59-8e06-7671f031a322/scratchpad/venv/bin/python'
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -c 'import pytest, jsonschema, referencing, docx, pptx, pypdf; print("ok: dependências locais")'
```

Se esse ambiente temporário não existir, use `PLAN_PYTHON=python3` **somente se o comando de importação acima passar**. Não instalar dependências automaticamente nem invocar Claude. O backend PDF pode estar indisponível; nesse caso somente testes de PDF podem pular, com motivo explícito. Baseline da auditoria: 59 testes e 28 subtestes passaram. Não usar a contagem antiga como alvo: novos testes precisam ser coletados e passar.

| Finalidade | Comando | Resultado esperado |
| --- | --- | --- |
| Suíte final local | `PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _TESTS _DESIGN_SYSTEM/tests -q -p no:cacheprovider` | Nenhuma falha; testes novos executados |
| Espaços/diff | `git diff --check` | Exit 0 |
| Escopo | `git status --short` e `git diff --name-only` | Somente arquivos permitidos, descontando alterações preexistentes |

## Escopo

**Arquivos que podem mudar:**

- `avaliacao-briefing-iqb/scripts/iqb.py`
- `_TESTS/avaliacao-briefing-iqb/test_iqb.py`
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/references/fontes.md`: somente páginas geradas pelo plano 012 afetadas por uma fonte alterada neste plano; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/014-iqb-evidencia-textual`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Cobrir tipos inválidos pela API e CLI

Adicione `test_evidence_requires_nonempty_string` parametrizando ausência da chave, None, False, True, 0, 10, [], {}, string vazia e espaços/quebras de linha. Adicione `test_cli_null_evidence_is_error`, usando arquivo e stdin conforme o padrão existente. Modifique somente uma resposta por caso para isolar a causa.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _TESTS/avaliacao-briefing-iqb/test_iqb.py -q -p no:cacheprovider -k 'evidence_requires_nonempty_string or cli_null_evidence'
```

**Esperado:** os casos são coletados; antes da correção os tipos indevidos revelam a falha.

### Passo 2: Exigir texto sem converter o tipo

Leia o valor de `evidence`; rejeite se não for `str` ou se `.strip()` estiver vazio. Preserve o `ValueError` com ID do critério e a exigência de evidência ou nota de ausência. Não remova texto válido nem transforme ausência em resposta positiva. Inclua um caso aceito com answer=False e “Não há fonte disponível para este critério”.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _TESTS/avaliacao-briefing-iqb/test_iqb.py -q -p no:cacheprovider
```

**Esperado:** todos passam; CLI inválida retorna status error, código 2 e nenhuma nota final.

## Plano de verificação

A mesma entrada inválida precisa falhar na função pública e na CLI. Texto de ausência deve continuar aceito. Preservar resultados todos-true/todos-false, vetos e anti-clustering. Não escrever um avaliador automático da qualidade do texto.

## Integração com o manifesto de fontes (plano 012)

Quando uma fonte listada em `_FONTES/manifest.json` mudar neste plano, execute
`python3 _TOOLS/build_sources.py` depois da alteração/sync para atualizar somente
as páginas geradas afetadas. Não mudar metadados de aprovação nem hashes fixados
dos originais para fazer a checagem passar. Inclua as páginas alteradas no mesmo
commit da correção. Se nenhuma fonte listada mudar, não regenere páginas.

**Verificar:** `python3 _TOOLS/build_sources.py --check` → exit 0, sem divergências.
Mudanças anteriores geradas por 012 são esperadas na conferência de deriva.

## Critérios de conclusão

- [x] `python3 _TOOLS/build_sources.py --check` retorna exit 0; páginas afetadas atualizadas no mesmo commit.
- [x] Suíte final local passa; testes de regressão nomeados neste plano foram coletados e passam.
- [x] Os casos e resultados especificados acima foram conferidos e registrados no fechamento.
- [x] `git diff --check` retorna exit 0.
- [x] Revisão de `git status --short`/`git diff --name-only` confirma o escopo e preservação de alterações preexistentes.
- [x] Linha deste plano em `plans/README.md` atualizada com evidências e limitações, sem marcar bateria de modelo como executada.

## Condições de parada

Pare e reporte se:

- Os trechos atuais divergirem sem explicação pelas dependências deste plano.
- Uma verificação falhar duas vezes após tentativa razoável de correção, fora da falha inicial esperada de regressão.
- Faltar ambiente necessário, a solução pedir instalação não autorizada ou mudança fora do escopo.
- A função pública não passar pela validação citada; a mudança exigir alterar a rubrica ou o esquema de resposta; a CLI produzir nota antes do erro.

## Manutenção

Novos caminhos de entrada devem reutilizar esta validação. O texto preenchido não prova que a evidência sustenta a resposta; essa avaliação continua sendo tarefa da skill.

## Fechamento — 29/09/2026

Revisão independente aprovada: 68 testes e 87 subtestes passaram; API e CLI rejeitam evidência inválida; fontes e sync verificados.
Checks de escopo, fontes e diff passaram; nenhuma bateria de modelos executada.
