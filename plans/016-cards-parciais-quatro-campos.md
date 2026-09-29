# Plan 016: Manter os quatro campos em cards parciais e inconclusivos

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/README.md`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** TODO
- **Prioridade:** P1
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** MED
- **Depende de:** 015; 001 e 005 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A04; seleção de todos os achados autorizada pelo operador

## Por que importa

O formato parcial dispensa o contrato completo, mas não deveria dispensar a forma do método. Hoje um Test Card parcial com apenas uma hipótese é aceito. Campos desconhecidos precisam aparecer como pendências, sem inventar critério, resultado ou evidência.

## Estado atual e convenções

`_DESIGN_SYSTEM/scripts/render.py:108`, dentro de `validate`:
```python
schema_file = profile.get("schema") if meta.get("completeness", "complete") == "complete" else None
schema = read_json(ROOT / "contracts" / schema_file) if schema_file else envelope
```
Test Card: hypothesis/test/measure/criteria. Learning Card: hypothesis/observations/learning/action, nessa ordem. Os contratos completos exigem exatamente quatro blocos; observações completas do Learning Card precisam de citação. Essas exigências de conteúdo completo não podem ser transplantadas integralmente para um rascunho.
`_DESIGN_SYSTEM/tests/test_render.py::test_complete_cards_require_four_fields_and_learning_evidence` é o padrão de teste; o helper `content()` começa como partial. A regra de quatro campos consta também de workshop-3e/SKILL.md e relatorio-3e/SKILL.md. Plano 011 é distinto: vínculo Learning↔Test Card.

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

- `_DESIGN_SYSTEM/scripts/render.py`
- `_DESIGN_SYSTEM/tests/test_render.py`
- `_DESIGN_SYSTEM/README.md`
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/assets/design-system/**` das onze skills: somente arquivos gerados pelo sync a partir das fontes listadas; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/016-cards-parciais-quatro-campos`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Cobrir estrutura por estado

Adicione `test_cards_keep_four_fields_for_all_states` para test_card/learning_card × complete/partial/inconclusive. Demonstre que partial com só hipótese passa atualmente. Inclua campo ausente, duplicado, invertido, extra e texto só com espaços. Prepare positivos parciais com “Pendente: definir medida antes da coleta” e “Não observado: coleta ainda não realizada”, mantendo os quatro campos.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k cards_keep_four_fields_for_all_states
```

**Esperado:** teste coletado e casos inválidos parciais denunciam a falha anterior.

### Passo 2: Aplicar somente a invariável de forma a todos os estados

Dentro de validate, após o envelope/contrato e antes de escrever arquivos, para test_card e learning_card confira exatamente quatro blocos, chaves na ordem listada, texto string não vazio após strip e tipos paragraph/callout/metric/heading, que exibem texto. Uma função curta local ou no mesmo módulo evita duplicação. Não aplicar o contrato completo a todos os parciais: isso exigiria citações ainda inexistentes e, futuramente, vínculo do plano 011. Preserve a checagem de IDs e referências desconhecidas, que já vale para parciais. Não preencher, ordenar ou corrigir a entrada automaticamente.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'cards_keep_four_fields or complete_cards'
```

**Esperado:** positivos nos três estados passam; inválidos falham antes de criar arquivos.

### Passo 3: Confirmar pendências visíveis e ausência de exigências indevidas

Adicione `test_partial_cards_preserve_pending_fields_in_exports`. Renderize os quatro textos em MD/HTML/DOCX e PDF quando disponível. Um Learning Card parcial sem citação e sem vínculo TC precisa passar; uma referência inexistente precisa falhar mesmo parcial. Documente forma mínima versus completude no README, sem alterar instruções metodológicas já corretas.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'partial_cards or complete_cards or cards_keep_four_fields'
```

**Esperado:** quatro campos e pendências aparecem; completos mantêm restrições atuais.

### Passo 4: Sincronizar a fonte compartilhada

Edite apenas a fonte do design system; suas cópias em `<skill>/assets/design-system/` são geradas. Depois de passar os testes direcionados, rode:

```bash
python3 _TOOLS/sync_shared.py --dry-run
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
```

**Esperado:** dry-run mostra somente distribuição das fontes alteradas; sync termina com exit 0; --check retorna exit 0 sem divergências. Schemas específicos em `references/` não são atualizados pelo sync: só alterá-los quando expressamente listados no escopo. Não distribuir testes nem caches.

## Plano de verificação

Cobrir os dois tipos e três estados. Default sem completeness continua sendo complete. Não inventar Test Card prospectivo a partir de resultados; não transformar inconclusivo em completo. Testar rejeição antes da saída e que o objeto de entrada não foi modificado.

## Critérios de conclusão

- [ ] Suíte final local passa; testes de regressão nomeados neste plano foram coletados e passam.
- [ ] `python3 _TOOLS/sync_shared.py --check` retorna exit 0, sem divergências.
- [ ] Os casos e resultados especificados acima foram conferidos e registrados no fechamento.
- [ ] `git diff --check` retorna exit 0.
- [ ] Revisão de `git status --short`/`git diff --name-only` confirma o escopo e preservação de alterações preexistentes.
- [ ] Linha deste plano em `plans/README.md` atualizada com evidências e limitações, sem marcar bateria de modelo como executada.

## Condições de parada

Pare e reporte se:

- Os trechos atuais divergirem sem explicação pelas dependências deste plano.
- Uma verificação falhar duas vezes após tentativa razoável de correção, fora da falha inicial esperada de regressão.
- Faltar ambiente necessário, a solução pedir instalação não autorizada ou mudança fora do escopo.
- Alguma amostra fictícia de card usar um tipo textual excluído ou estrutura diferente; exigir mudar vínculo TC/LC ou regras de inferência; a mudança impedir declarar informação ausente sem inventá-la.

## Manutenção

Ao executar 011 depois, preservar a aceitação de parcial sem vínculo e a invariável de quatro campos. Novos formatos de card precisam exibir os mesmos campos, com pendências explícitas.
