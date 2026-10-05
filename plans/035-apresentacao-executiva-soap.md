# Plan 035: Apresentação executiva 16:9 em nível *state of the art* — PDF em ReportLab, regras de conteúdo e tipografia de slide nos tokens

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 8472652..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/scripts/pdf_reportlab.py _DESIGN_SYSTEM/tokens.json _DESIGN_SYSTEM/layouts/executive_presentation.layout.json _DESIGN_SYSTEM/scripts/validators _DESIGN_SYSTEM/tests/test_render.py experimentacao-inovacao/references/entregaveis.md _SAMPLES_ENTREGAVEIS/executive_presentation`
> Os Planos 032–034 terão mudado parte desses arquivos. Em especial, confira o
> `layout.json` da apresentação (ver STOP conditions).

## Status

- **Priority**: P1
- **Effort**: L
- **Risk**: MED (regras novas de conteúdo podem recusar apresentações que hoje passam — é o objetivo)
- **Depends on**: `plans/034-pdf-reportlab-relatorios.md` DONE com aprovação visual do operador.
- **Category**: qualidade dos entregáveis
- **Planned at**: commit `8472652`, 2026-10-05

## Why this matters

O operador pediu entregáveis *state of the art*, e a apresentação executiva é o
entregável mais visível. Hoje ela tem dois problemas:

1. **Conteúdo**: os títulos dos slides são rótulos de tema ("Contexto", "Método",
   "Achados"), não a mensagem do slide; nada limita a quantidade de texto por slide.
   Em apresentações executivas de alto nível, cada slide tem um **título-mensagem**
   (a conclusão em uma frase), uma ideia por slide e pouco texto.
2. **PDF**: só sai pelo WeasyPrint (depende do Pango), e o caminho HTML com
   `position: absolute` (Plano 030) pode sobrepor texto sem erro — defeito que
   bloqueou o Plano 031. O ReportLab, com uma área por `Frame` e `KeepInFrame(mode="error")`,
   recusa o slide que não cabe em vez de sobrepor.

Além disso, PDF e PPTX usam tamanhos de fonte diferentes e literais no código
(PPTX: título 28 pt, corpo 17 pt, rodapé 10 pt em `render_pptx`). Este plano põe a
tipografia de slide nos tokens e faz os dois formatos lerem dali.

## Current state

### Slot do layout (versão commitada em `8472652`)

`_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` — tela 338,66 × 190,5 mm, coordenadas a partir do **topo**:

| Slot | x | y | largura | altura |
|---|---|---|---|---|
| `logo` | 281,94 | 8,89 | 43,18 | 16,19 |
| `titulo_slide` | 12,7 | 12,7 | 261,62 | 20,32 |
| `corpo_slide` | 15,24 | 39,37 | 307,34 | 135,89 |
| `rodape_slide` | 15,24 | 178,31 | 307,34 | 8,38 |

Atenção: no momento do planejamento o operador tinha uma alteração **não commitada**
nesse arquivo. Use o que estiver commitado quando você executar; leia os slots por nome
com `load_presentation_layout(deliverable_type)` (`render.py:471-479`), que devolve
`{nome: {"x","y","width","height",...}}` em mm. No ReportLab, `y` cresce de baixo para
cima: `y_reportlab = altura_da_página - y - height`.

Cálculo que define a tipografia de título: o slot de título tem 20,32 mm. Montserrat
Bold 24 pt com entrelinha 1,1 ocupa 9,3 mm por linha → **2 linhas cabem**; a 28 pt
(valor atual do PPTX) só cabe 1 linha (10,9 mm por linha).

### Como os slides são compostos hoje

`render_html`, ramo `presentation` (`render.py:490-543`) e `render_pptx` (`render.py:793-878`)
seguem a mesma composição: **capa** (título do documento + `summary`); **um slide por
seção** — cada `heading` abre uma seção cujo título é o texto do heading, e os blocos
seguintes até o próximo heading formam o corpo; **slide "Fontes"** com as citações.
Rodapé de cada slide: `identity_line(content)`.

Tamanhos literais no PPTX (`render.py:824`, `836`, `843`): `Pt(28)` título, `Pt(17)` corpo, `Pt(10)` rodapé.

### Amostra e contrato

`_SAMPLES_ENTREGAVEIS/executive_presentation/input.json`: headings "Contexto", "Método",
"Achados", "Recomendação", "Próximos passos" (section_keys `*_heading`), cada um com um
parágrafo de 14–20 palavras (section_keys `context`, `method`, `findings`,
`recommendation`, `next_steps`, exigidos pelo schema `contracts/executive-presentation.schema.json`).

Validadores semânticos: `_DESIGN_SYSTEM/scripts/validators/<deliverable_type>.py` com
`def validate(content) -> list[str]`, rodados só para versões `complete`. Exemplo do padrão
(`validators/learning_card.py`):

```python
"""Verifica o vínculo estrutural ao Test Card executado, sem julgar evidências."""
from __future__ import annotations

from typing import Any


def validate(content: dict[str, Any]) -> list[str]:
    metadata = content.get("metadata", {})
    if metadata.get("test_card_id") == metadata.get("artifact_id"):
        return ["metadata.test_card_id: o Learning Card não pode apontar para si mesmo"]
    return []
```

Orientação de conteúdo para a skill que produz a apresentação:
`experimentacao-inovacao/references/entregaveis.md`, seção "## Relatório e apresentação"
(narrativa `problema e hipótese → pergunta → método e amostra → evidências → status dos cards → recomendação → próximo gate`; "3 a 5 achados principais").

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Ambiente | `python3 -m venv /tmp/venv-035 && /tmp/venv-035/bin/python -m pip install -q -r _DESIGN_SYSTEM/requirements.txt pypdfium2 pytest` | exit 0 |
| Testes | `/tmp/venv-035/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` |
| Comparação | `/tmp/venv-035/bin/python _TOOLS/compare_pdf_engines.py --out /tmp/cmp-035 --types executive_presentation` | exit 0 |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check && python3 _TOOLS/build_sources.py --check` | exit 0 |

## Scope

**In scope**: `_DESIGN_SYSTEM/tokens.json` (estilos de slide), `_DESIGN_SYSTEM/scripts/render.py`
(`render_pptx` lê os tokens de slide; `REPORTLAB_LAYOUTS`), `_DESIGN_SYSTEM/scripts/pdf_reportlab.py`,
`_DESIGN_SYSTEM/scripts/validators/executive_presentation.py` (criar),
`_DESIGN_SYSTEM/tests/test_render.py`, `_DESIGN_SYSTEM/tests/test_validators.py`,
`_DESIGN_SYSTEM/README.md`, `experimentacao-inovacao/references/entregaveis.md`,
`_SAMPLES_ENTREGAVEIS/executive_presentation/` (input e derivados), cópias do sync, `plans/README.md`.

**Out of scope**: `layout.json` (não edite: é do operador); o ramo HTML `presentation`
e o Plano 031; outros tipos; `SKILL.md` (orçamento de palavras do Plano 010 — a orientação vai na referência).

## Git workflow

Branch `advisor/035-apresentacao-soap`; um commit por passo; português no imperativo; sem push/merge.

## Steps

### Step 1: Tipografia de slide nos tokens

Em `tokens.json` → `typography.styles`, acrescente (sem alterar os existentes):

```json
"slide_cover_title": {"family": "font_brand", "size": 36, "weight": 700, "line_height": 1.05},
"slide_title": {"family": "font_brand", "size": 24, "weight": 700, "line_height": 1.1},
"slide_body": {"family": "font_body", "size": 17, "weight": 400, "line_height": 1.3},
"slide_metric": {"family": "font_brand", "size": 40, "weight": 700, "line_height": 1.0},
"slide_footer": {"family": "font_body", "size": 10, "weight": 500, "line_height": 1.1}
```

Mude `profile_version` de `"1.0.0"` para `"1.1.0"`.

Em `render_pptx`, troque `Pt(28)`, `Pt(17)` e `Pt(10)` por `Pt(tokens["typography"]["styles"]["slide_title"]["size"])`, `["slide_body"]` e `["slide_footer"]`.

**Verify**: `grep -n "Pt(28)\|Pt(17)\|Pt(10)" _DESIGN_SYSTEM/scripts/render.py` → nada; suíte completa `0 failed` (se algum teste fixar 28 pt, STOP).

### Step 2: Regras de conteúdo (validador semântico)

Crie `validators/executive_presentation.py` com `validate(content) -> list[str]`, aplicando só a versões completas (o runner já garante). Regras, com mensagens em português que digam como corrigir:

1. **Capa**: `content["summary"]` existe e tem até 35 palavras → senão `"summary: a capa precisa da mensagem principal em até 35 palavras"`.
2. **Título-mensagem**: cada bloco `heading` tem de 4 a 12 palavras e não é só um rótulo genérico (compare sem acento e em minúsculas com: `contexto`, `metodo`, `método`, `achados`, `resultados`, `recomendacao`, `recomendação`, `proximos passos`, `próximos passos`, `conclusao`, `conclusão`, `introducao`, `introdução`, `resumo`, `fontes`, `conteudo`, `conteúdo`) → `"<id>: título de slide deve dizer a conclusão do slide (4 a 12 palavras), não só o tema"`.
3. **Uma ideia por slide**: entre dois headings, no máximo 4 blocos e no máximo 60 palavras somando `text`, `title`, `description` e `items` → `"<id do heading>: slide com N palavras/blocos; divida em mais slides"`.

Conte palavras com `len(texto.split())`.

**Verify**: `test_validators.py` (Passo 6) passa.

### Step 3: Atualizar a amostra e a orientação da skill

- Em `_SAMPLES_ENTREGAVEIS/executive_presentation/input.json`, troque **só o `text` dos 5 headings** por títulos-mensagem fictícios coerentes com os parágrafos (mantenha `section_key`, IDs e parágrafos). Exemplo para o heading de achados: "A orientação reduziu dúvidas, mas o efeito real não foi medido".
- Em `experimentacao-inovacao/references/entregaveis.md`, no fim da seção "## Relatório e apresentação", acrescente um parágrafo: capa com a mensagem principal em até 35 palavras; cada slide com título-mensagem de 4 a 12 palavras que diga a conclusão; uma ideia por slide (até 4 blocos e 60 palavras); números-chave em bloco `metric`; detalhes e evidências completas no relatório ou apêndice. Diga que o renderizador recusa versões completas fora dessas regras.

**Verify**: `/tmp/venv-035/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/executive_presentation/input.json --out-dir /tmp/o035 --formats md` → exit 0. Uma cópia da amostra original (headings "Contexto" etc.) com `completeness: complete` → exit ≠ 0 com "título de slide deve dizer a conclusão".

### Step 4: Slides em ReportLab

Em `pdf_reportlab.py`, `render_presentation(...)` despachado quando `profile["layout"] == "presentation"`:

- Página 338,66 × 190,5 mm (`tokens.page.presentation_16_9`: 13,333 × 7,5 in).
- Leia os slots com `load_presentation_layout` (receba a função por parâmetro, como `block_text`). Se faltar algum dos 4 slots, `ValueError("layout.json da apresentação sem o slot <nome>")`.
- Composição idêntica à do PPTX: capa, um slide por seção, slide "Fontes".
- **Capa**: faixa vertical de 6 mm `document_accent` à esquerda; rótulo do tipo (`cover_eyebrow`) e título do documento (`slide_cover_title`, `document_primary`) na área do título ampliada até o topo do corpo; `summary` em `slide_body` `text_strong` como mensagem principal; logo no slot `logo`.
- **Slides de seção**: título (`slide_title`) dentro do slot `titulo_slide` com `KeepInFrame(..., mode="error")`; corpo no slot `corpo_slide` com `KeepInFrame(..., mode="error")`; blocos: `paragraph` em `slide_body`; `metric` em `slide_metric` `document_primary` com o texto de apoio abaixo em `slide_body`; `callout` como caixa `document_deep`/`inverse`; `list` com "•" em `slide_body`; `table` com 12 pt mínimo nas células; `card_grid` em até 3 colunas.
- **Fontes**: citações em `slide_body` reduzido não abaixo de 12 pt; se não couberem num slide, continue em "Fontes (cont.)".
- **Rodapé** no slot `rodape_slide`: `identity_line` à esquerda e `N / total` à direita, `slide_footer` `text_muted` (use o canvas numerado do Plano 034).
- Transbordo de título ou corpo → `PdfOverflow(f"slide {n} ({título}) excede a área; divida o conteúdo em mais slides")`.
- `REPORTLAB_LAYOUTS` e `SUPPORTED_LAYOUTS` passam a incluir `presentation`.

**Verify**: `/tmp/venv-035/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/executive_presentation/input.json --out-dir /tmp/o035 --formats pdf,pptx --pdf-engine reportlab` → exit 0; número de páginas do PDF = número de slides do PPTX.

### Step 5: Regenerar os derivados da amostra

```
/tmp/venv-035/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/executive_presentation/input.json --out-dir _SAMPLES_ENTREGAVEIS/executive_presentation --pdf-engine reportlab
```
**Verify**: `git status _SAMPLES_ENTREGAVEIS/executive_presentation` mostra só os arquivos daquela pasta; o manifesto tem `"pdf_engine": "reportlab"`.

### Step 6: Testes

`test_validators.py` — classe `ExecutivePresentationRulesTests`:
1. amostra nova completa → `[]`;
2. heading "Contexto" → erro de título-mensagem;
3. heading de 15 palavras → erro;
4. seção com 5 blocos ou 70 palavras → erro "divida em mais slides";
5. sem `summary` ou com 40 palavras → erro da capa;
6. a mesma apresentação com `completeness: partial` → o render não aplica as regras (exit 0).

`test_render.py` — classe `ReportLabPresentationTests` (pula sem `reportlab`):
1. páginas do PDF = slides do PPTX, tamanho 338,66 × 190,5 mm (± 0,5);
2. cada página contém a `identity_line` e `"{n} / {total}"`;
3. todos os títulos-mensagem e textos da amostra aparecem no PDF;
4. corpo que não cabe (um parágrafo de 60 palavras repetido em 4 blocos, `completeness: partial` para passar do validador) → exit ≠ 0 com "excede a área", sem PDF;
5. bytes idênticos em duas renderizações;
6. PPTX: o título usa `slide_title.size` (24 pt) e o corpo `slide_body.size` (17 pt).

**Verify**: `pytest -k "ExecutivePresentationRules or ReportLabPresentation"` sem falhas; suíte completa `0 failed`.

### Step 7: Revisão visual do operador (gate) e docs

- `_TOOLS/compare_pdf_engines.py --out /tmp/cmp-035 --types executive_presentation` e informe o caminho. Não marque DONE sem a aprovação do operador.
- `_DESIGN_SYSTEM/README.md`: regras de conteúdo da apresentação e `--pdf-engine reportlab` cobrindo os 18 tipos. Sync e checagens.

## Test plan

6 testes de validador + 6 de render (Passo 6). O portão de qualidade do 033 roda em cada PDF: fonte mínima, sobreposição e texto fora da página continuam garantidos.

## Done criteria

- [ ] Amostra renderiza com `--pdf-engine reportlab`; PDF com o mesmo número de páginas que os slides do PPTX
- [ ] Testes novos sem falhas; suíte completa `0 failed`
- [ ] `grep -n "Pt(28)\|Pt(17)\|Pt(10)" _DESIGN_SYSTEM/scripts/render.py` → nada
- [ ] `/tmp/cmp-035/index.html` aprovado pelo operador
- [ ] Sync e `build_sources --check` → exit 0; status atualizado em `plans/README.md`

## STOP conditions

- O `layout.json` da apresentação commitado não tem os slots `logo`, `titulo_slide`, `corpo_slide`, `rodape_slide`, ou o `titulo_slide` tem menos de 19 mm de altura (o título de 2 linhas a 24 pt não caberia).
- Algum teste existente fixa os tamanhos 28/17/10 do PPTX.
- O sample novo não passa no validador e a correção exigiria mudar parágrafos ou `section_key`s.
- O portão de qualidade reprova o PDF da amostra.
- Um passo falha duas vezes após tentativa razoável.

## Maintenance notes

- As regras de conteúdo valem só para versões completas; rascunhos parciais continuam livres.
- Os limites (35/12/4/60 palavras) são um ponto de partida; ajuste com o operador depois de ver apresentações reais, sempre com teste.
- O ramo HTML `presentation` (Plano 030) continua existindo para o formato `html`; o Plano 036 decide se ele segue.
- PPTX e PDF agora compartilham a tipografia de slide; mudanças vão no `tokens.json`.
