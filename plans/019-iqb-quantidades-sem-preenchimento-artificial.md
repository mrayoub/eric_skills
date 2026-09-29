# Plan 019: Permitir até três forças e perguntas sem exigir preenchimento artificial

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- _DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json avaliacao-briefing-iqb/references/briefing-validation-report.schema.json avaliacao-briefing-iqb/SKILL.md _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/tests/test_validators.py`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** DONE
- **Prioridade:** P2
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 012 (fontes geradas); 014; 001 e 005 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A07; seleção de todos os achados autorizada pelo operador

## Por que importa

A skill pede até três perguntas, mas o contrato exige três; pontos fortes exigem pelo menos dois. Um briefing vazio pode ser avaliado integralmente sem possuir uma força comprovada. O documento precisa aceitar a quantidade real de achados, sem inventá-los para cumprir o schema.

## Estado atual e convenções

`_DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json:623`, `$defs.stringListBlock.properties.data.properties.items`, tem minItems=2/maxItems=3. strengthsBlock referencia essa definição. Em provocationsBlock, o allOf fixa minItems=3/maxItems=3. A referência específica `avaliacao-briefing-iqb/references/briefing-validation-report.schema.json` é hoje idêntica à fonte.
`avaliacao-briefing-iqb/SKILL.md:36`: “pontos fortes, lacunas priorizadas e até três provocações ao sponsor”.
O sync replica o design system para assets/design-system, mas **não** atualiza schemas específicos em references. Essa referência precisa ser atualizada explicitamente. Preserve as sete seções e a matriz de quarenta critérios. Convenção: usar amostra IQB fictícia em TemporaryDirectory, como BriefingValidationTests em test_validators.py.

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

- `_DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json`
- `avaliacao-briefing-iqb/references/briefing-validation-report.schema.json`
- `avaliacao-briefing-iqb/SKILL.md`
- `_DESIGN_SYSTEM/tests/test_render.py`
- `_DESIGN_SYSTEM/tests/test_validators.py`
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/references/fontes.md`: somente páginas geradas pelo plano 012 afetadas por uma fonte alterada neste plano; nenhuma edição manual.
- `<skill>/assets/design-system/**` das onze skills: somente arquivos gerados pelo sync a partir das fontes listadas; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/019-iqb-quantidades-sem-preenchimento-artificial`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Cobrir zero, uma e três entradas sem perder seções

Adicione `test_iqb_accepts_zero_to_three_strengths_and_questions` em test_render.py. A partir da amostra fictícia de briefing_validation, mantenha as seções strengths/provocations como listas e varie items entre [], um texto e três textos. Para zero, acrescente ao summary uma nota factual de ausência. Adicione `test_iqb_rejects_four_strengths_or_questions`. Os primeiros casos devem reproduzir a falha antiga.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'iqb_accepts_zero_to_three or iqb_rejects_four'
```

**Esperado:** casos coletados; versões antigas rejeitam zero/um.

### Passo 2: Alinhar as duas definições e a orientação da skill

No stringListBlock, minItems passa a 0, maxItems permanece 3. No provocationsBlock, minItems também passa a 0, mantendo maxItems=3. Confirme os consumidores da definição antes de editar; não mude gaps ou a matriz de respostas. Copie a fonte atualizada para a referência específica da skill. Na etapa 5 do SKILL.md, explicite “até três pontos fortes sustentados e até três provocações relevantes; declare a ausência no resumo quando não houver itens”. Não preencher a lista com um item fictício chamado ausência. Preserve frontmatter e linguagem simples.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/tests/test_validators.py -q -p no:cacheprovider -k 'iqb or BriefingValidation'
```

**Esperado:** quantidades 0–3 aceitas, quatro rejeitadas, cálculo e seções obrigatórias preservados.

### Passo 3: Conferir os dois schemas e a exportação de listas vazias

Renderize o caso com listas vazias em MD/DOCX/HTML; a nota no resumo precisa aparecer. Confirme a igualdade da fonte com references e teste briefing vazio com quarenta respostas false e notas explícitas de ausência. Não tratar diagnóstico incompleto como avaliação completa: aqui a ausência é conhecida e avaliada, não falta de acesso à fonte decisiva.

**Verificar**:

```bash
python3 -c "from pathlib import Path; assert Path('_DESIGN_SYSTEM/contracts/briefing-validation-report.schema.json').read_bytes() == Path('avaliacao-briefing-iqb/references/briefing-validation-report.schema.json').read_bytes(); print('ok: schemas IQB iguais')"
```

**Esperado:** ok: schemas IQB iguais; casos de exportação incluídos no teste direcionado.

### Passo 4: Sincronizar a fonte compartilhada

Edite apenas a fonte do design system; suas cópias em `<skill>/assets/design-system/` são geradas. Depois de passar os testes direcionados, rode:

```bash
python3 _TOOLS/sync_shared.py --dry-run
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
```

**Esperado:** dry-run mostra somente distribuição das fontes alteradas; sync termina com exit 0; --check retorna exit 0 sem divergências. Schemas específicos em `references/` não são atualizados pelo sync: só alterá-los quando expressamente listados no escopo. Não distribuir testes nem caches.

## Plano de verificação

Testar 0/1/2/3/4 itens, seção ausente versus seção presente vazia, nota de ausência visível e avaliação de briefing vazio usando o script real. Não alterar IQB, vetos ou classificação. Preservar o limite de 650 palavras do SKILL.md e seus links; `wc -w avaliacao-briefing-iqb/SKILL.md` deve indicar no máximo 650.

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
- stringListBlock tiver consumidores além de strengths/provocations que precisem conservar outra cardinalidade; perder uma seção obrigatória; a alteração exigir recalibrar notas ou ultrapassar o orçamento do SKILL.md.

## Manutenção

Schemas em references são documentos especializados e não fazem parte do sync atual; sua igualdade precisa ser revisada quando o contrato muda. Perguntas devem derivar das lacunas observadas, não de uma cota.

## Fechamento — 29/09/2026

Revisão independente aprovada: 81 testes e 437 subtestes passaram; listas de 0–3, rejeição de quatro e de seção ausente, nota de ausência e IQB real com 40 false verificados; schemas iguais, 602 palavras e sync/fontes consistentes..
Checks de escopo, fontes e diff passaram; nenhuma bateria de modelos executada.
