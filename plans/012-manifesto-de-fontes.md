# Plan 012: Registrar a proveniência das fontes metodológicas num manifesto único

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat 452dda4..HEAD -- '*/assets' '*/references/fonte-*' _TOOLS`
> Os originais em `assets/` não deveriam ter mudado; se mudaram, STOP.

## Status

- **Status:** DONE

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 001 (`_TOOLS/sync_shared.py`)
- **Category**: docs
- **Planned at**: commit `452dda4`, reconciliado em 2026-09-29

## Why this matters

As skills adaptam métodos de fontes diferentes (DOCX 4D/3E/5C fornecidos pelo usuário,
cópias históricas do RC6, PDFs oficiais da Strategyzer, rubricas IQB e de potencial). A
relação "original → transcrição → adaptação" e a **vigência institucional** (confirmada,
histórica ou desconhecida) hoje estão espalhadas em prosa (`VALIDACAO_SKILLS_2026-09-28.md`,
`references/fonte-*-divergencias.md`, linhas de Proveniência). Um manifesto único, com
hash dos originais, torna detectável qualquer alteração acidental de um original e deixa
explícito o que ainda não foi confirmado — sem fingir aprovação que não existe.

Escopo propositalmente pequeno: **um** manifesto na raiz (fonte) e uma página gerada por
skill só com as fontes que ela contém. Não se cria um registro manual por skill (seriam 11
cópias para manter).

## Current state

Originais e derivados relevantes (confira com `ls`):

| Arquivo (em cada skill onde aparece) | Skills |
|---|---|
| `assets/Modelo 4D de Aprofundamento.docx` + `.transcricao.md`; `assets/4d-workshop-playbook-original-rc6.md`; `references/4d-workshop-playbook.md` (adaptação); `references/fonte-4d-e-divergencias.md` | workshop-4d, relatorio-4d |
| `assets/official-four-d-report.pdf` | relatorio-4d |
| `assets/Modelo 3E Estruturacao da Solucao.docx` + `.transcricao.md`; `assets/3e-solution-structuring-playbook-original-rc6.md`; `references/3e-solution-structuring-playbook.md`; `references/fonte-3e-e-divergencias.md`; `assets/test-card.md` | workshop-3e, relatorio-3e |
| `assets/Playbook_Modelo_5C_Centralidade_Cliente.docx` + `.transcricao.md`; `references/metodo-5c.md` | workshop-5c, relatorio-5c |
| `assets/strategyzer-test-card-2023.pdf`, `assets/strategyzer-learning-card-2023.pdf` | experimentacao-inovacao |
| `assets/strategyzer-innovation-project-scorecard-2023.pdf` | scorecard-inovacao |
| `references/iqb-rubric.md`, `scripts/iqb.py` | avaliacao-briefing-iqb |
| `references/innovation-potential-rubric.md`, `scripts/score.py` | potencial-inovacao |
| `references/briefing_template.md` | briefing-inovacao |
| `references/eric-esteira.md` (de `_ERIC_CONTEXT/README.md`) | todas |

SHA-256 já registrados em `VALIDACAO_SKILLS_2026-09-28.md` (use para conferência):
4D DOCX `d5071f2ab0d62e153b8f0bb7e89108a10bca6980d807dbd43c90bbd80fd115e3`;
3E DOCX `530cc4691c6cf5b5f093ba972b05d08649b4000a1fd077ee6020c94b00637e34`;
5C DOCX `3b793187dccd6691e124e61b9a407e6f383513d55de255c1049deae31df4e3c7`.

Pendências de vigência conhecidas (do mesmo documento, seção "Insumos ainda solicitados"):
modelo oficial do briefing; norma aprovada do IQB; regra vigente do potencial; documento
vigente da esteira ERIC; autoria/aprovação dos DOCX 4D/3E; versão institucional genérica do 5C.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Gerar | `python3 _TOOLS/build_sources.py` | exit 0 |
| Checar | `python3 _TOOLS/build_sources.py --check` | exit 0 |

## Scope

**In scope**: `_FONTES/manifest.json` (criar); `_TOOLS/build_sources.py` (criar); `<skill>/references/fontes.md` (gerado); `_TOOLS/README.md` (1 parágrafo).

**Out of scope**: qualquer original em `assets/`; textos de adaptação; SKILL.md (no máximo, o plano 010 pode acrescentar um link para `references/fontes.md` na linha de Proveniência — não faça aqui).

## Git workflow

Branch `advisor/012-fontes`. Um commit.

## Steps

### Step 1: Manifesto

`_FONTES/manifest.json`: lista de objetos com
`id`, `titulo`, `tipo` (`original` | `transcricao` | `adaptacao` | `historico` | `rubrica` | `script`),
`arquivo` (caminho relativo à skill), `skills` (lista), `origem` (texto: "fornecido pelo usuário em 2026-09", "ERIC_RC6 sdd/…", URL Strategyzer…),
`autor` (ou `null`), `versao_declarada` (ou `null`), `data_importacao` (ou `null`),
`deriva_de` (id ou `null`), `vigencia` (`confirmada` | `historica` | `desconhecida`),
`notas`. **Não** inclua hash — o script calcula.

Use `vigencia: "desconhecida"` para tudo, exceto: cópias `*-original-rc6.md` → `historica`; PDFs Strategyzer → `confirmada` com `notas: "publicação oficial Strategyzer 2023; licença conforme o PDF"`. Metadado que você não sabe fica `null` — não preencha por suposição.

### Step 2: Script

`_TOOLS/build_sources.py` (só biblioteca padrão):
- Lê o manifesto; para cada entrada e cada skill listada, calcula SHA-256 de `<skill>/<arquivo>`; erro se o arquivo não existir.
- Erro se o mesmo `arquivo` tiver hashes diferentes entre skills (cópias divergiram).
- Gera `<skill>/references/fontes.md` com uma tabela: Fonte | Tipo | Arquivo | Deriva de | Vigência | SHA-256 (12 primeiros caracteres) | Notas; e no fim a lista "Vigência a confirmar" com as entradas `desconhecida`.
- `--check`: não escreve; sai 1 se algum `fontes.md` estiver desatualizado ou houver erro.
- Para os DOCX 4D/3E/5C, compare com os hashes registrados acima e falhe se divergirem.

**Verify**: `python3 _TOOLS/build_sources.py && python3 _TOOLS/build_sources.py --check; echo $?` → `0`; `ls */references/fontes.md | wc -l` → `11`.

### Step 3: Documentar

Em `_TOOLS/README.md`: "Ao importar ou substituir uma fonte, atualize `_FONTES/manifest.json` (nova entrada; a anterior vira `historica`) e rode `build_sources.py`. Nunca reescreva um original."

**Verify**: `grep -c build_sources _TOOLS/README.md` → `≥1`.

## Test plan

Verifique a divergência em uma cópia descartável da árvore mínima no diretório
temporário, sem modificar os originais do worktree: altere um byte de
`relatorio-3e/assets/test-card.md` nessa cópia e confirme que `--check` falha.
Verifique também página gerada desatualizada e hash de DOCX divergente na cópia.
Os checks negativos não podem reescrever originais nem páginas, e devem informar
o arquivo envolvido. Na árvore real, geração e `--check` devem passar.

Reconciliação em 29/09/2026: hashes dos três DOCX e suas cópias foram conferidos
e coincidem com os registros abaixo. Mudanças anteriores no design system são
geradas e não representam alterações dos originais metodológicos. Fonte oficial
publicada e vigência institucional são coisas distintas: para PDFs Strategyzer,
explique nas notas que a publicação é oficial mas adoção institucional não está
confirmada. Não inventar autoria, data de importação ou aprovação.

## Done criteria

- [ ] Manifesto cobre todos os arquivos da tabela de "Current state"
- [ ] 11 `references/fontes.md` gerados; `--check` → 0
- [ ] Hashes dos 3 DOCX conferem com os registrados
- [ ] Nenhum original alterado (`git diff --stat -- '*/assets'` vazio)
- [ ] `plans/README.md` atualizado

## STOP conditions

- Hash de um DOCX divergir do registrado — um original foi alterado; não atualize o manifesto, reporte.
- Encontrar fonte sem saber se é original ou adaptação — marque `tipo` pela evidência no próprio arquivo; se não houver, pergunte.

## Maintenance notes

- A confirmação institucional (mudar `desconhecida` → `confirmada`) depende do mantenedor obter os documentos; o manifesto só torna a pendência visível.

## Fechamento — 29/09/2026

Manifesto com 27 entradas e 11 páginas geradas. Revisor confirmou geração
idempotente, `--check` sem escrita e cinco negativos em cópia descartável:
fonte divergente, DOCX alterado, página desatualizada, fonte ausente e deriva_de
inexistente. Hashes originais preservados; `_TESTS`: 20 testes e 9 subtestes passaram.
Os planos 013–023 foram alinhados à manutenção das páginas geradas por 012:
fontes alteradas exigem regenerar suas páginas no mesmo commit, sem duplicação.
Nenhuma confirmação institucional foi inferida nem bateria de modelos executada.
