# Plan 020: Alinhar o contrato da one-page à orientação paisagem

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- _DESIGN_SYSTEM/contracts/briefing-one-page.schema.json briefing-inovacao/references/briefing-one-page.schema.json _DESIGN_SYSTEM/tests/test_render.py`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** TODO
- **Prioridade:** P2
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 001 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A08; seleção de todos os achados autorizada pelo operador

## Por que importa

Quem segue o schema pode construir uma one-page em retrato, mas o perfil e o renderizador rejeitam essa orientação. A decisão vigente é A4 paisagem. A correção deve deixar esse formato claro nas duas versões do contrato, sem alterar os outros modos do briefing.

## Estado atual e convenções

Nos dois schemas, metadata.orientation tem:
```json
{"enum":["portrait","landscape"],"description":"Retrato por padrão (UXR-17); landscape aceito para compatibilidade com one-pages persistidas anteriormente."}
```
`briefing-inovacao/SKILL.md:41` determina A4 paisagem, uma página e fonte mínima preservada. `_DESIGN_SYSTEM/profiles.json` define paper=a4_landscape para briefing_one_page. `render.py:101` rejeita metadata.orientation incompatível com o perfil. Preserve essa decisão; não implementar retrato como variante nova.
O sync não copia schemas de references; atualize esse arquivo explicitamente. Siga `test_rejects_wrong_orientation` e `test_portrait_and_landscape_and_semantic_identity` em test_render.py.

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

- `_DESIGN_SYSTEM/contracts/briefing-one-page.schema.json`
- `briefing-inovacao/references/briefing-one-page.schema.json`
- `_DESIGN_SYSTEM/tests/test_render.py`
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/assets/design-system/**` das onze skills: somente arquivos gerados pelo sync a partir das fontes listadas; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/020-one-page-paisagem-consistente`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Testar o schema antes do perfil

Adicione `test_one_page_contract_only_accepts_landscape`: valide a amostra fictícia one-page diretamente contra cada schema com o registry do envelope, sem depender da rejeição antecipada de orientation em render.validate. Paisagem deve passar e portrait deve falhar no próprio contrato. Ausência de orientation pode continuar usando o perfil: não a torne obrigatória se hoje não é.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k one_page_contract_only_accepts_landscape
```

**Esperado:** teste coletado; portrait denuncia aceitação indevida nos schemas anteriores.

### Passo 2: Fixar paisagem e conferir os três modos

Troque enum por const landscape ou enum de um único item landscape; reescreva a descrição como “A4 paisagem, conforme o perfil executive_one_page”. Faça a mesma alteração na referência específica. Preserve layout_variant/page_size, sete campos, briefing_version_id e citações. Adicione `test_briefing_modes_keep_supported_orientation`, cobrindo briefing e questionnaire em portrait e one-page em landscape. Quando PDF disponível, uma one-page curta deve continuar tendo uma página e largura maior que altura.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _DESIGN_SYSTEM/tests/test_render.py -q -p no:cacheprovider -k 'one_page_contract or briefing_modes or wrong_orientation'
```

**Esperado:** três modos preservados; retrato recusado pelo contrato one-page.

### Passo 3: Conferir igualdade das referências

Confirme que fonte e referência especializada têm os mesmos bytes. A orientação ausente deve renderizar usando o perfil atual. Não regenere entregas reais nem renomeie versões históricas para ocultar incompatibilidades.

**Verificar**:

```bash
python3 -c "from pathlib import Path; assert Path('_DESIGN_SYSTEM/contracts/briefing-one-page.schema.json').read_bytes() == Path('briefing-inovacao/references/briefing-one-page.schema.json').read_bytes(); print('ok: schemas one-page iguais')"
```

**Esperado:** ok: schemas one-page iguais.

### Passo 4: Sincronizar a fonte compartilhada

Edite apenas a fonte do design system; suas cópias em `<skill>/assets/design-system/` são geradas. Depois de passar os testes direcionados, rode:

```bash
python3 _TOOLS/sync_shared.py --dry-run
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
```

**Esperado:** dry-run mostra somente distribuição das fontes alteradas; sync termina com exit 0; --check retorna exit 0 sem divergências. Schemas específicos em `references/` não são atualizados pelo sync: só alterá-los quando expressamente listados no escopo. Não distribuir testes nem caches.

## Plano de verificação

Positivo landscape nos dois schemas; negativo portrait; ausência de orientação quando permitida; integração dos três modos com suas amostras fictícias; orientação e página do PDF quando backend disponível. Rejeição deve ocorrer antes de gerar arquivos.

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
- A orientação vigente tiver mudado desde o commit-base; surgir requisito real de suportar retrato; precisar modificar perfil ou fonte mínima para passar o teste.

## Manutenção

Uma nova orientação requer perfil e testes próprios. Não anunciar compatibilidade no schema que o renderizador não fornece.
