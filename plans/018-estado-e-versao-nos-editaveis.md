# Plan 018: Mostrar estado, ID e versão em todos os formatos de leitura

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/README.md`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** TODO
- **Prioridade:** P1
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 017; 001 e 007 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A06; seleção de todos os achados autorizada pelo operador

## Por que importa

O receptor de um arquivo editável pode não receber o JSON nem o manifesto. Ele precisa saber se o documento é parcial, completo ou inconclusivo, além de reconhecer ID e versão. A identificação deve ser automática e estar no conteúdo visível.

## Estado atual e convenções

`render_md:536` começa com título e resumo; `render_docx:613` também; `render_pptx:698` monta título/corpo sem metadados. HTML/PDF já usa:
```python
completeness_label = COMPLETENESS_LABELS[meta.get("completeness") or "complete"]
```
`COMPLETENESS_LABELS` mapeia complete→Completo, partial→Parcial, inconclusive→Inconclusivo. O HTML tem rodapé com ID, versão e estado. Reutilize esse vocabulário e o timbre/tokens atuais, sem mudar os nomes canônicos do JSON.
Teste de referência: `test_reader_labels_are_portuguese_and_canonical_keys_are_preserved`, mais `test_card_is_one_page_and_presentation_is_editable`, em `_DESIGN_SYSTEM/tests/test_render.py`.

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
- Branch sugerida para execução: `advisor/018-estado-e-versao-nos-editaveis`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Definir uma linha comum de identificação

Adicione uma função curta no render.py que forme “ID <artifact_id> · versão <content_version> · <estado em português>”. Use os campos já validados, sem escrever no objeto content. Se metadata trouxer data identificada, preserve-a; não invente uma data de avaliação a partir da hora da exportação e não adicione exigência nova de data. Acrescente testes `test_editable_formats_show_identity_and_state`, primeiro demonstrando a ausência em MD/DOCX/PPTX.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k editable_formats_show_identity_and_state
```

**Esperado:** testes coletados e denunciam a ausência anterior.

### Passo 2: Apresentar identificação nos formatos editáveis

Em MD, inclua a linha após título; TXT herdará a linha. Em DOCX, use parágrafo discreto após título ou rodapé visível. No PPTX, inclua identificação legível na capa e rodapé dos slides, reutilizando fontes/tokens e sem sobrepor logo ou conteúdo. Preserve HTML/PDF existentes e o comportamento de PDF indisponível. Não imprimir estruturas internas, nomes de schema ou instruções técnicas ao usuário. Documente a identificação automática no README.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'editable_formats_show_identity or reader_labels or card_is_one_page or missing_pdf_backend'
```

**Esperado:** todos passam; texto extraído mostra ID, versão e estado nos formatos suportados.

### Passo 3: Verificar formatos e estados sem aumentar fonte nem cortar conteúdo

Nos testes, percorra partial/inconclusive/complete e ausência de completeness (default completo), usando documentos fictícios válidos para cada perfil. Extraia conteúdo com Document/Presentation/PdfReader, não apenas propriedades do arquivo. Cubra briefing, relatório, card e apresentação. A identificação não deve tornar um card curto maior que uma página ou cortar o corpo da apresentação. Não exigir PPTX de tipos que não o suportam.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider
```

**Esperado:** todos passam; um card curto continua uma página quando PDF disponível.

### Passo 4: Sincronizar a fonte compartilhada

Edite apenas a fonte do design system; suas cópias em `<skill>/assets/design-system/` são geradas. Depois de passar os testes direcionados, rode:

```bash
python3 _TOOLS/sync_shared.py --dry-run
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
```

**Esperado:** dry-run mostra somente distribuição das fontes alteradas; sync termina com exit 0; --check retorna exit 0 sem divergências. Schemas específicos em `references/` não são atualizados pelo sync: só alterá-los quando expressamente listados no escopo. Não distribuir testes nem caches.

## Plano de verificação

Positivos para os três estados e default, metadados visíveis em MD/TXT/DOCX/PPTX e preservação em HTML/PDF. Confirmar objeto JSON intacto e que não se chama de completo um parcial. O vínculo TC/LC do plano 011 é adicional e deve continuar aparecendo quando implementado.

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
- Necessidade de reduzir fonte abaixo do padrão, mudar orientação ou inventar data para acomodar metadados; identidade existente no HTML/PDF sumir; card curto ultrapassar uma página.

## Manutenção

As onze skills recebem o ajuste por sync. Critérios específicos de cada skill podem exigir mais informação no cabeçalho; esta linha é o mínimo compartilhado e não prova vigência das fontes, tratada em 012.
