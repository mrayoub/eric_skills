# Plan 021: Separar natureza da mudança e complexidade no mural 4D

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 32a103a..HEAD -- workshop-4d/references/mural-board-4d-template.md`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** TODO
- **Prioridade:** P2
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 012 (fontes geradas); nenhuma
- **Categoria:** docs
- **Planejado contra:** commit `32a103a`, 2026-09-29
- **Achado coberto:** A09; seleção de todos os achados autorizada pelo operador

## Por que importa

A natureza da mudança não determina seu esforço. O mural atual sugere automaticamente baixo esforço para incremental e alto esforço para radical, contrariando o playbook, que avalia complexidade por proposta. O ajuste melhora a facilitação sem mudar o método nem a classificação histórica.

## Estado atual e convenções

`workshop-4d/references/mural-board-4d-template.md:120–122`:
```text
| Zona Incrementais | Area | Melhorias continuas, baixo esforco |
| Zona Estruturais | Area | Mudancas de processo/modelo, medio esforco |
| Zona Radicais | Area | Inovacoes disruptivas, alto esforco |
```
`workshop-4d/references/4d-workshop-playbook.md:161` pede “Complexidade (baixa/média/alta)” por proposta, junto de dor, eliminação e simplificação. Preserve as três naturezas e os tempos D1–D4. Este template específico não é cópia compartilhada e não precisa de sync.

## Comandos necessários

Os comandos partem da raiz do repositório e usam `python3`, biblioteca padrão e `rg`. Não há instalação, geração de binários ou chamada de modelo. Não adicionar testes que apenas espelhem o texto do documento. A validação estrutural não comprova compreensão pelo modelo.

| Finalidade | Comando | Resultado esperado |
| --- | --- | --- |
| Espaços/diff | `git diff --check` | Exit 0 |
| Escopo | `git status --short` e `git diff --name-only` | Somente arquivos permitidos, descontando alterações preexistentes |

## Escopo

**Arquivos que podem mudar:**

- `workshop-4d/references/mural-board-4d-template.md`
- `plans/README.md` (somente status e evidências de conclusão deste plano)
- `<skill>/references/fontes.md`: somente páginas geradas pelo plano 012 afetadas por uma fonte alterada neste plano; nenhuma edição manual.

**Fora do escopo:** todos os outros arquivos, mudanças na rubrica não especificadas, frontmatter das skills, _SAMPLE/, _OUTPUTS/, .claude/, registros históricos e regeneração ampla de amostras. Use somente dados fictícios em memória ou diretório temporário. Preserve linguagem simples e a regra vigente de prioridade das decisões do 3E. Não executar baterias de acionamento/comportamento nem consumir chamadas de modelo.

## Fluxo de git

- Preserve alterações preexistentes; registre `git status --short` antes de trabalhar.
- Branch sugerida para execução: `advisor/021-4d-natureza-separada-do-esforco`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Confirmar os dois instrumentos

Leia a subseção 4.2 do mural e a consolidação D3 do playbook. Confirme a associação automática no primeiro e a complexidade separada no segundo. Não revisar o playbook inteiro nem reclassificar ideias existentes.

**Verificar**:

```bash
rg -n 'Zona Incrementais|Zona Estruturais|Zona Radicais|Complexidade' workshop-4d/references/mural-board-4d-template.md workshop-4d/references/4d-workshop-playbook.md
```

**Esperado:** as três zonas e a exigência de complexidade do playbook são encontradas.

### Passo 2: Retirar a estimativa automática e adicionar campo por proposta

Remova “baixo/medio/alto esforco” das linhas das zonas, preservando suas descrições de natureza. Após a tabela, escreva uma instrução curta: natureza e complexidade são avaliadas separadamente; registre “Complexidade (baixa/média/alta)” e justificativa por proposta; se não há suporte, marque pendente. Inclua um exemplo simples de mudança incremental complexa e radical simples, explicitamente ilustrativo, sem atribuir resultados ou escolhas ao projeto. Não mudar votação, quantidade de propostas nem duração.

**Verificar**:

```bash
python3 - <<'CHECK'
from pathlib import Path
text=Path('workshop-4d/references/mural-board-4d-template.md').read_text()
section=text.split('### Subsecao 4.2',1)[1].split('## Area 5',1)[0]
assert all(x in section for x in ['Zona Incrementais','Zona Estruturais','Zona Radicais','Complexidade (baixa/média/alta)'])
for row in section.splitlines():
    if any(x in row for x in ['Zona Incrementais','Zona Estruturais','Zona Radicais']):
        assert not any(x in row.lower() for x in ['baixo esforco','medio esforco','alto esforco','baixo esforço','médio esforço','alto esforço'])
print('ok: natureza e complexidade separadas')
CHECK
```

**Esperado:** ok: natureza e complexidade separadas.

## Plano de verificação

Conferência estrutural pelo comando acima e leitura da subseção resultante. Não criar testes que apenas reproduzam frases de um documento ou rodar bateria de modelo para esta alteração textual. A verificação local prova o ajuste no instrumento, não a compreensão do facilitador.

Verificação local específica:

```bash
python3 - <<'CHECK'
from pathlib import Path
text=Path('workshop-4d/references/mural-board-4d-template.md').read_text()
section=text.split('### Subsecao 4.2',1)[1].split('## Area 5',1)[0]
assert all(x in section for x in ['Zona Incrementais','Zona Estruturais','Zona Radicais','Complexidade (baixa/média/alta)'])
for row in section.splitlines():
    if any(x in row for x in ['Zona Incrementais','Zona Estruturais','Zona Radicais']):
        assert not any(x in row.lower() for x in ['baixo esforco','medio esforco','alto esforco','baixo esforço','médio esforço','alto esforço'])
print('ok: natureza e complexidade separadas')
CHECK
```

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
- A natureza da mudança for definida pelo esforço em uma decisão metodológica vigente; precisar alterar votação, schema ou registros reais; exemplo não puder ser mantido como ilustração sem dados reais.

## Manutenção

Não voltar a usar esforço como sinônimo de incremental/radical ao criar novos modelos. O plano 022 mexe em outra subseção do mesmo arquivo: execute em sequência para evitar conflitos.
