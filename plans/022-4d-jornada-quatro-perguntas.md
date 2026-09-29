# Plan 022: Manter quatro perguntas em cada fase da jornada 4D

> **Instruções ao executor:** leia o plano inteiro, execute os passos na ordem e confira os resultados. Na fase de regressão, a falha antiga esperada deve ser demonstrada; depois da correção todos os casos devem passar. Se ocorrer uma condição de parada, reporte o impedimento e não amplie o escopo. Atualize apenas a linha deste plano em `plans/README.md` ao concluir.
>
> **Conferência inicial de versão:** `git diff --stat 3404a5c..HEAD -- workshop-4d/references/mural-board-4d-template.md`. Compare os trechos abaixo com os arquivos atuais. Alterações das dependências declaradas são esperadas: confira os trechos e registre seu novo commit-base. Diferenças de comportamento não explicadas exigem parar e reportar.

## Status

- **Status:** TODO
- **Prioridade:** P2
- **Esforço:** S (S = horas; M = cerca de um dia)
- **Risco da correção:** LOW
- **Depende de:** 012 (fontes geradas); 021 (mesmo arquivo; execução sequencial)
- **Categoria:** docs
- **Planejado contra:** commit `3404a5c`, 2026-09-29
- **Achado coberto:** A10; seleção de todos os achados autorizada pelo operador

## Por que importa

O playbook pede acontecimentos, dores, valor e retrabalho em cada fase da jornada. O mural faz perguntas diferentes em antes/durante/depois e pode deixar dimensões sem registro. As quatro perguntas precisam aparecer nas três colunas, sem preencher respostas pelo grupo.

## Estado atual e convenções

`workshop-4d/references/mural-board-4d-template.md:81–83`:
```text
| Coluna Antes | Area de post-its | Pergunta: "Como era antes? Quem faz o que?" |
| Coluna Durante | Area de post-its | Pergunta: "O que acontece no momento critico? Onde estao as dores?" |
| Coluna Depois | Area de post-its | Pergunta: "Qual o resultado? O que melhora ou piora?" |
```
`workshop-4d/references/4d-workshop-playbook.md:73–81`: para cada fase, perguntar “O que acontece?”, “Onde dói?”, “Onde gera valor?”, “Onde há retrabalho?”. Preserve antes/durante/depois, duração e uso de post-its. A edição do plano 021 é esperada apenas na subseção 4.2; confira essa diferença, sem tratá-la como deriva desconhecida.

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
- Branch sugerida para execução: `advisor/022-4d-jornada-quatro-perguntas`; se houver trabalho não relacionado, use checkout isolado em vez de misturar alterações.
- Um commit lógico, seguindo mensagens descritivas em português do histórico (exemplo: `Experimentação: explicita prioridade das decisões vigentes do 3E`). Commit/merge/push seguem a autorização do operador; a criação deste plano não os executa nem autoriza publicação.
- Não restaurar ou apagar alterações alheias, nem remover branches como parte desta correção.

## Passos

### Passo 1: Confirmar a jornada vigente

Leia a subseção 3.1 do mural e o passo 2 da jornada no playbook. Confirme que não há uma instrução vigente substituindo as quatro perguntas. Preserve as perguntas adicionais sobre atores, resultado e momento crítico como complementos.

**Verificar**:

```bash
rg -n 'Coluna Antes|Coluna Durante|Coluna Depois|O que acontece|Onde dói|Onde gera valor|Onde há retrabalho' workshop-4d/references/mural-board-4d-template.md workshop-4d/references/4d-workshop-playbook.md
```

**Esperado:** três colunas localizadas e as quatro perguntas presentes no playbook.

### Passo 2: Incluir as mesmas quatro perguntas nas três colunas

Nas linhas Coluna Antes/Durante/Depois da tabela, inclua explicitamente as quatro perguntas, com redação simples e igual à do playbook. Perguntas antigas úteis podem ficar após “Complemento:”. Não sugerir respostas, métricas ou jornadas do caso real. Não mudar barco da inovação, tempos ou decisão D4; preserve a separação natureza/complexidade adicionada em 021.

**Verificar**:

```bash
python3 - <<'CHECK'
from pathlib import Path
text=Path('workshop-4d/references/mural-board-4d-template.md').read_text()
section=text.split('### Subsecao 3.1',1)[1].split('### Subsecao 3.2',1)[0]
for phase in ['Coluna Antes','Coluna Durante','Coluna Depois']:
    rows=[row for row in section.splitlines() if phase in row]
    assert len(rows)==1,phase
    assert all(question in rows[0] for question in ['O que acontece?','Onde dói?','Onde gera valor?','Onde há retrabalho?']),phase
print('ok: quatro perguntas nas três fases')
CHECK
```

**Esperado:** ok: quatro perguntas nas três fases.

## Plano de verificação

Use a checagem estrutural abaixo, seguida da leitura da tabela para assegurar que as três colunas continuam compreensíveis. Não adicionar teste que espelhe frases de Markdown nem chamar modelo. Não concluir que uma jornada histórica foi reavaliada.

Verificação local específica:

```bash
python3 - <<'CHECK'
from pathlib import Path
text=Path('workshop-4d/references/mural-board-4d-template.md').read_text()
section=text.split('### Subsecao 3.1',1)[1].split('### Subsecao 3.2',1)[0]
for phase in ['Coluna Antes','Coluna Durante','Coluna Depois']:
    rows=[row for row in section.splitlines() if phase in row]
    assert len(rows)==1,phase
    assert all(question in rows[0] for question in ['O que acontece?','Onde dói?','Onde gera valor?','Onde há retrabalho?']),phase
print('ok: quatro perguntas nas três fases')
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
- A jornada passar a usar fases diferentes por decisão metodológica posterior; necessidade de alterar outros instrumentos ou preencher resultados; a edição sobrescrever o ajuste de 021.

## Manutenção

Ao adaptar jornada para outro contexto, conserve as quatro dimensões por fase. Perguntas adicionais complementam o diagnóstico, não substituem valor e retrabalho.
