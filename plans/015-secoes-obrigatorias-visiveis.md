# Plan 015: Exigir que seções obrigatórias apareçam nos arquivos entregues

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- _DESIGN_SYSTEM/contracts/four-d-workshop-record.schema.json _DESIGN_SYSTEM/contracts/three-e-workshop-record.schema.json _DESIGN_SYSTEM/contracts/three-e-report.schema.json _DESIGN_SYSTEM/contracts/five-c-workshop-record.schema.json _DESIGN_SYSTEM/contracts/five-c-report.schema.json _DESIGN_SYSTEM/contracts/innovation-scorecard.schema.json _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/README.md`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** TODO
- **Prioridade:** P1
- **Esforço:** M (S = horas; M = cerca de um dia)
- **Risco da correção:** MED
- **Depende de:** 012 (fontes geradas); 001 e 005 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A03; seleção de todos os achados autorizada pelo operador

## Por que importa

Seis contratos aceitam seções completas dentro de `page_break`. Esse bloco representa uma quebra de página: seu texto é descartado nos derivados. A presença do texto no JSON não pode ser suficiente para afirmar que uma entrega está completa.

## Estado atual e convenções

Nos seis contratos, `allOf[1].properties.blocks.allOf[].contains` usa este padrão (exemplo E1):
```json
{"type":"object","properties":{"data":{"type":"object","required":["section_key","text"],"properties":{"section_key":{"const":"e1"},"text":{"type":"string","minLength":1}}}}}
```
Não restringe `block.type`. Os contratos 5C também exigem `citation_ids` com pelo menos um item; conservar isso.
`_DESIGN_SYSTEM/scripts/render.py:405` retorna apenas uma div para page_break; `render_md:544` ignora o bloco. Table/list/card_grid tampouco exibem necessariamente `data.text` como síntese, mesmo sendo blocos visíveis.
Seções: 4D registro d1–d4; 3E registro e1–e3; 3E relatório e1–e3/route; 5C registro e relatório c1–c5; scorecard alignment_opportunity/risk_reduction/next_gate.
Modelo de teste: `_DESIGN_SYSTEM/tests/test_render.py::test_every_type_has_schema_and_complete_sections_are_enforced`, que hoje testa parágrafos e remoção de seção.

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

- `_DESIGN_SYSTEM/contracts/four-d-workshop-record.schema.json`
- `_DESIGN_SYSTEM/contracts/three-e-workshop-record.schema.json`
- `_DESIGN_SYSTEM/contracts/three-e-report.schema.json`
- `_DESIGN_SYSTEM/contracts/five-c-workshop-record.schema.json`
- `_DESIGN_SYSTEM/contracts/five-c-report.schema.json`
- `_DESIGN_SYSTEM/contracts/innovation-scorecard.schema.json`
- `_DESIGN_SYSTEM/tests/test_render.py`
- `_DESIGN_SYSTEM/README.md`
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/references/fontes.md`: somente páginas geradas pelo plano 012 afetadas por uma fonte alterada neste plano; nenhuma edição manual.
- `<skill>/assets/design-system/**` das onze skills: somente arquivos gerados pelo sync a partir das fontes listadas; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/015-secoes-obrigatorias-visiveis`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Demonstrar a perda para os seis tipos

Crie `test_required_sections_reject_hidden_block_types`: monte cada documento completo com textos fictícios únicos por seção e F01 quando necessário. Substitua uma seção de cada vez por page_break; cubra também list/table/card_grid com `data.text` mas conteúdos próprios diferentes. Antes da correção, pelo menos page_break será aceito. Não leia insumos reais. Liste os tipos de blocos nas amostras fictícias versionadas desses seis documentos para antecipar incompatibilidades.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k required_sections_reject_hidden_block_types
```

**Esperado:** teste coletado e reprodução anterior denuncia a aceitação indevida.

### Passo 2: Restringir as sínteses a tipos que exibem texto

Em cada `contains`, exigir `type` e `data`, limitando `type` a paragraph, heading, callout ou metric. Todos exibem `data.text` nos formatos suportados. Preserve chaves, minContains e citações existentes. Não proíba tabelas, grades ou quebras extras: elas continuam permitidas, mas não substituem a síntese obrigatória. Não altere o envelope global, o renderizador nem os contratos de outros tipos. Se uma amostra precisar de migração, pare e apresente o caso antes de ampliar o escopo.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'required_sections or complete_sections'
```

**Esperado:** tipos inadequados rejeitados; documentos com sínteses em parágrafos continuam aceitos.

### Passo 3: Verificar a entrega, não só a validação

Adicione `test_required_section_text_survives_exports`, cobrindo os seis tipos e os quatro tipos textuais permitidos. Renderize em diretório temporário; confirme textos únicos em HTML, MD, TXT e parágrafos/tabelas do DOCX; no PDF extraia texto quando o backend estiver disponível. Verifique que page_break adicional entre sínteses não invalida documento nem elimina conteúdo. Documente a restrição no README.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'required_section or complete_sections'
```

**Esperado:** todos passam; skips de PDF só por indisponibilidade do backend.

### Passo 4: Sincronizar a fonte compartilhada

Edite apenas a fonte do design system; suas cópias em `<skill>/assets/design-system/` são geradas. Depois de passar os testes direcionados, rode:

```bash
python3 _TOOLS/sync_shared.py --dry-run
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
```

**Esperado:** dry-run mostra somente distribuição das fontes alteradas; sync termina com exit 0; --check retorna exit 0 sem divergências. Schemas específicos em `references/` não são atualizados pelo sync: só alterá-los quando expressamente listados no escopo. Não distribuir testes nem caches.

## Plano de verificação

Para cada um dos seis tipos: positivo com todas as seções; negativo com seção faltante; negativo com texto em page_break/list/table/card_grid; positivo com quebra extra; citações 5C preservadas. Não comparar hashes binários. Não marcar como parcial um completo inválido para fazê-lo passar.

## Integração com o manifesto de fontes (plano 012)

Quando uma fonte listada em `_FONTES/manifest.json` mudar neste plano, execute
`python3 _TOOLS/build_sources.py` depois da alteração/sync para atualizar somente
as páginas geradas afetadas. Não mudar metadados de aprovação nem hashes fixados
dos originais para fazer a checagem passar. Inclua as páginas alteradas no mesmo
commit da correção. Se nenhuma fonte listada mudar, não regenere páginas.

**Verificar:** `python3 _TOOLS/build_sources.py --check` → exit 0, sem divergências.
Mudanças anteriores geradas por 012 são esperadas na conferência de deriva.

## Critérios de conclusão

- [ ] `python3 _TOOLS/build_sources.py --check` retorna exit 0; páginas afetadas atualizadas no mesmo commit.
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
- Uma seção das amostras fictícias depender de um tipo excluído; a implementação exigir alterar renderização ou tipos fora dos seis listados; alguma síntese permitida sumir de um formato; uma referência de schema não resolver.

## Manutenção

Adicionar um tipo visual não significa que ele pode cumprir uma seção textual. Novos contratos devem declarar tipos admissíveis e testar presença do texto nos derivados. Cards têm uma regra separada no plano 016.
