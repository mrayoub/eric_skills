# Plan 013: Calcular total e classe com as mesmas notas publicadas

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 32a103a..HEAD -- potencial-inovacao/scripts/score.py _DESIGN_SYSTEM/scripts/validators/innovation_potential_assessment.py _TESTS/potencial-inovacao/test_score.py _DESIGN_SYSTEM/tests/test_validators.py _DESIGN_SYSTEM/README.md`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** DONE
- **Prioridade:** P1
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** MED
- **Depende de:** 012 (fontes geradas); 003 e 005 (DONE)
- **Categoria:** bug
- **Planejado contra:** commit `32a103a`, 2026-09-29
- **Achado coberto:** A01; seleção de todos os achados autorizada pelo operador

## Por que importa

O script publica notas arredondadas, mas calcula o total com as notas originais. O validador usa as notas publicadas: o resultado do próprio script pode ser recusado e indicar uma classe diferente da sustentada pelas notas visíveis. A correção deve manter os pesos e os limites da rubrica.

## Estado atual e convenções

`potencial-inovacao/scripts/score.py:69–76`, em `calculate_innovation_score`:
```python
normalized_score: int | float = int(value) if value.is_integer() else round(value, 1)
# normalized[key]["score"] recebe normalized_score
weighted_total += value * criterion["weight"]
```
O total usa `round(weighted_total, 1)`. Os pesos, nesta ordem, são impacto 0,30; viabilidade 0,25; alinhamento 0,20; urgência 0,15; inovação 0,10. Classes: total ≥70 `priorizar`, ≥40 `monitorar`, abaixo de 40 `arquivar`.
`_DESIGN_SYSTEM/scripts/validators/innovation_potential_assessment.py:45` acumula as notas de `scores.rows` nessa mesma ordem. Na entrada 69.91, 69.91, 69.95, 70.04, 70.04, o script retorna 70.0/priorizar, mas as notas devolvidas sustentam 69.9/monitorar.
Convenção: `unittest`, importação por `importlib.util`, `self.subTest`; exemplos em `_TESTS/potencial-inovacao/test_score.py::test_classification_boundaries` e `_DESIGN_SYSTEM/tests/test_validators.py::PotentialValidationTests`.

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

- `potencial-inovacao/scripts/score.py`
- `_DESIGN_SYSTEM/scripts/validators/innovation_potential_assessment.py`
- `_TESTS/potencial-inovacao/test_score.py`
- `_DESIGN_SYSTEM/tests/test_validators.py`
- `_DESIGN_SYSTEM/README.md`
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/references/fontes.md`: somente páginas geradas pelo plano 012 afetadas por uma fonte alterada neste plano; nenhuma edição manual.
- `<skill>/assets/design-system/**` das onze skills: somente arquivos gerados pelo sync a partir das fontes listadas; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/013-potencial-precisao-consistente`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Registrar a falha de ponta a ponta

Em `test_score.py`, adicione `test_published_scores_drive_total_and_classification`. Em `test_validators.py`, adicione `test_returned_scores_roundtrip_precision`: execute o script, transforme **as notas retornadas**, não a entrada original, nas cinco linhas do bloco `scores` da amostra fictícia de potencial e copie total/classe retornados. Antes da correção, o primeiro teste deve denunciar a divergência e o segundo receber erro do validador. Mantenha a amostra original sem edição.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _TESTS/potencial-inovacao/test_score.py _DESIGN_SYSTEM/tests/test_validators.py -q -p no:cacheprovider -k 'published_scores_drive_total or returned_scores_roundtrip_precision'
```

**Esperado:** os dois casos são coletados; na versão anterior falham pelo arredondamento, sem erro de importação.

### Passo 2: Usar a precisão publicada no cálculo

Preserve a publicação com uma casa decimal; acumule `normalized_score * criterion["weight"]`. Preserve a ordem de acumulação, `round(..., 1)` para o total, as contribuições `weighted` com duas casas e as classes atuais. O validador deve continuar recalculando as notas declaradas: não afrouxe a comparação nem aceite uma classe inconsistente. Documente essa política em uma frase no README do design system. Atualize expectativas que dependiam da precisão invisível, explicando a mudança.

**Verificar**:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m pytest _TESTS/potencial-inovacao/test_score.py _DESIGN_SYSTEM/tests/test_validators.py -q -p no:cacheprovider
```

**Esperado:** todos passam; a reprodução retorna 69.9/monitorar e é aceita.

### Passo 3: Sincronizar a fonte compartilhada

Edite apenas a fonte do design system; suas cópias em `<skill>/assets/design-system/` são geradas. Depois de passar os testes direcionados, rode:

```bash
python3 _TOOLS/sync_shared.py --dry-run
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
```

**Esperado:** dry-run mostra somente distribuição das fontes alteradas; sync termina com exit 0; --check retorna exit 0 sem divergências. Schemas específicos em `references/` não são atualizados pelo sync: só alterá-los quando expressamente listados no escopo. Não distribuir testes nem caches.

## Plano de verificação

Cubra notas com duas e três casas, zero e 100, resultados nos limites 40/70 e imediatamente abaixo/acima, notas ausentes e justificativa ausente. O teste integrado deve usar `calculate_innovation_score` e o validador real; adulterar total/classe precisa continuar falhando. Não exigir que a soma das contribuições individualmente arredondadas seja idêntica ao total: o total é arredondado uma única vez após acumular as notas publicadas.

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
- O ajuste exigir mudar pesos, limites ou inventar campos de precisão; surgirem entradas de outra unidade; o resultado integrado ainda não for exportável após a correção.

## Manutenção

Revisões da rubrica devem atualizar cálculo e validador em conjunto. A classificação de entradas com precisão adicional pode mudar; registre esse efeito no fechamento, sem recalcular entregas históricas.

## Fechamento — 29/09/2026

Revisão independente aprovada: 65 testes e 54 subtestes passaram; precisão e exportação consistentes; sync e fontes verificados.
Checks de escopo, fontes e diff passaram; nenhuma bateria de modelos executada.
