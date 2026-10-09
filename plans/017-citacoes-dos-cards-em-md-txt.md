# Plan 017: Preservar fontes individuais dos cards em Markdown e TXT

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 32a103a..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tests/test_render.py`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** DONE
- **Prioridade:** P1
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 012 (fontes geradas); 001 e 005 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `32a103a`, 2026-09-29
- **Achado coberto:** A05; seleção de todos os achados autorizada pelo operador

## Por que importa

A bibliografia final permanece, mas Markdown/TXT perde o vínculo entre cada card de uma grade e suas fontes. Duas afirmações podem ter fontes diferentes e o leitor precisa reconhecer essa diferença também nos formatos editáveis.

## Estado atual e convenções

`_DESIGN_SYSTEM/scripts/render.py:554–555`, em render_md:
```python
for card in block["data"]["cards"]:
    lines.append("| " + str(card["title"]).replace("|", "\\|") + " | " + card_text(card).replace("|", "\\|") + " |")
```
O conteúdo do card é escrito, mas `card.citation_ids` não é. HTML e DOCX já exibem citações por card. TXT é derivado do Markdown em `main`. `relatorio-4d/references/relatorio-4d-layout.md:16` exige fontes ligadas aos cards.
Siga `_DESIGN_SYSTEM/tests/test_render.py::test_md_escapes_pipes` e os testes de extração de conteúdo, usando TemporaryDirectory e F01/F02 fictícios.

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
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/references/fontes.md`: somente páginas geradas pelo plano 012 afetadas por uma fonte alterada neste plano; nenhuma edição manual.
- `<skill>/assets/design-system/**` das onze skills: somente arquivos gerados pelo sync a partir das fontes listadas; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/017-citacoes-dos-cards-em-md-txt`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Separar as fontes no teste

Adicione `test_card_grid_citations_survive_md_txt`. Use três cards: primeiro F01, segundo F02, terceiro sem fonte; bibliografia tem F01/F02. Verifique a fonte na linha do respectivo card, não apenas ocorrência em algum lugar do documento. A versão anterior deve falhar.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k card_grid_citations_survive_md_txt
```

**Esperado:** teste coletado e falha porque o vínculo individual não aparece.

### Passo 2: Acrescentar referências ao conteúdo da célula

Em render_md, depois de card_text(card), acrescente “Fontes: F01, F02” somente quando o card tiver citation_ids. Escape barras verticais depois de montar o texto; preserve quebras de linha de forma compatível com tabela Markdown. Mantenha citações do bloco e bibliografia geral. Não propague automaticamente a fonte de um card aos demais nem copie as fontes do bloco para todos. TXT deve herdar o vínculo pela conversão existente.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'card_grid_citations or md_escapes_pipes'
```

**Esperado:** vínculos corretos em MD/TXT, sem fonte inventada no terceiro card.

### Passo 3: Sincronizar a fonte compartilhada

Edite apenas a fonte do design system; suas cópias em `<skill>/assets/design-system/` são geradas. Depois de passar os testes direcionados, rode:

```bash
python3 _TOOLS/sync_shared.py --dry-run
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
```

**Esperado:** dry-run mostra somente distribuição das fontes alteradas; sync termina com exit 0; --check retorna exit 0 sem divergências. Schemas específicos em `references/` não são atualizados pelo sync: só alterá-los quando expressamente listados no escopo. Não distribuir testes nem caches.

## Plano de verificação

Cobrir card com uma e várias fontes, card sem fonte, texto/título com pipe e grade com fonte no bloco além das fontes individuais. Conferir que HTML e DOCX mantêm a associação e que referência desconhecida continua rejeitada. Não comparar arquivos binários por hash.

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
- [x] `python3 _TOOLS/sync_shared.py --check` retorna exit 0, sem divergências.
- [x] Os casos e resultados especificados acima foram conferidos e registrados no fechamento.
- [x] `git diff --check` retorna exit 0.
- [x] Revisão de `git status --short`/`git diff --name-only` confirma o escopo e preservação de alterações preexistentes.
- [x] Linha deste plano em `plans/README.md` atualizada com evidências e limitações, sem marcar bateria de modelo como executada.

## Condições de parada

Pare e reporte se:

- Os trechos atuais divergirem sem explicação pelas dependências deste plano.
- Uma verificação falhar duas vezes após tentativa razoável de correção, fora da falha inicial esperada de regressão.
- Faltar ambiente necessário, a solução pedir instalação não autorizada ou mudança fora do escopo.
- A conversão TXT apagar a fonte acrescentada; a solução exigir mudar o schema ou inventar uma referência; as citações atuais de HTML/DOCX desaparecerem.

## Manutenção

Futuras estruturas aninhadas precisam manter vínculo individual em cada formato. Este plano não julga se uma fonte suporta o achado: apenas conserva o vínculo declarado.

## Fechamento — 29/09/2026

Revisão independente aprovada: 74 testes e 387 subtestes passaram; fontes individuais preservadas em MD/TXT, associação HTML/DOCX e referências desconhecidas verificadas; sync, fontes e diff sem divergências..
Checks de escopo, fontes e diff passaram; nenhuma bateria de modelos executada.
