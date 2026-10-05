# Correção do Plano 033 após revisão (05/10/2026)

> **Para o executor**: este documento complementa `plans/033-verificador-de-qualidade-do-pdf.md`.
> Leia o plano original para contexto. Trabalhe no branch existente
> `advisor/033-verificador-qualidade-pdf`. Rode cada verificação e confirme o resultado
> antes de seguir. Se uma STOP condition ocorrer, pare e reporte. Não faça push nem merge
> no `main`.

## O que a revisão encontrou

O portão de qualidade funciona, mas o plano foi concluído **violando uma STOP condition**.
O plano dizia: "Alguma amostra do WeasyPrint, além do one-page antes do Passo 2, é
reprovada → STOP". A amostra `executive_presentation` foi reprovada ("texto fora da
página": o rodapé com a identificação sai abaixo da borda em todos os slides). Em vez de
parar, foi criado o teste `test_weasyprint_samples_gate_known_defect`, que aceita a falha.

Consequência se o branch for integrado assim: o PDF da apresentação executiva deixa de
ser gerado pelo motor padrão até o Plano 035.

O defeito é real e anterior ao 033 (vem do Plano 030). A causa e a correção já existem no
branch do Plano 031 (BLOCKED por outro motivo):

- `38d17de` — "Corrige offset de @page margin no branch presentation": acrescenta `@page { margin: 0; }` quando o layout de slots existe (1 linha em `render.py`).
- `d05eb02` — "Adiciona teste de regressão do offset de @page margin" (14 linhas em `test_render.py`).

O revisor verificou: os dois commits entram sem conflito em `advisor/033-verificador-qualidade-pdf`;
com eles, a apresentação passa no portão, o teste de regressão passa e o **único** teste que
falha é `test_weasyprint_samples_gate_known_defect` — exatamente o que deve ser invertido.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Ambiente | `python3 -m venv /tmp/venv-033c && /tmp/venv-033c/bin/python -m pip install -q -r _DESIGN_SYSTEM/requirements.txt pytest pypdfium2` | exit 0 |
| Testes com WeasyPrint | `/tmp/venv-033c/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check && python3 _TOOLS/build_sources.py --check` | exit 0 |

O WeasyPrint precisa do Pango. No macOS com Homebrew, se `import weasyprint` falhar com
`cannot load library 'pango-1.0-0'`, prefixe os comandos com `DYLD_LIBRARY_PATH=/opt/homebrew/lib`.
**Esta correção exige rodar com o WeasyPrint funcionando** — sem ele, os testes que provam
a correção pulam. Se não conseguir carregar o WeasyPrint, STOP.

## Scope

**In scope**: `_DESIGN_SYSTEM/scripts/render.py` (só o que vem do `38d17de`),
`_DESIGN_SYSTEM/tests/test_render.py`, cópias do sync.
**Out of scope**: `pdf_quality.py` (não afrouxe o portão); qualquer outra parte do branch do
Plano 031 (`d0248d6`, `77dd4d7`, `288b08a`, `cff0229` — são a parte BLOCKED); `layout.json`.

## Steps

### Step 1: Trazer as duas correções do Plano 031

```
git switch advisor/033-verificador-qualidade-pdf
git cherry-pick 38d17de d05eb02
```
**Verify**: `git log --oneline -2` mostra os dois commits; `git show --stat HEAD~1 HEAD` só toca `_DESIGN_SYSTEM/scripts/render.py` e `_DESIGN_SYSTEM/tests/test_render.py`. Conflito → STOP.

### Step 2: Inverter o teste que aceitava o defeito

Em `_DESIGN_SYSTEM/tests/test_render.py`, classe `PdfQualityTests`, substitua
`test_weasyprint_samples_gate_known_defect` por `test_weasyprint_samples_pass`:

- pula com `self.skipTest(...)` se `pdf_available()` for falso;
- para cada `_SAMPLES_ENTREGAVEIS/*/input.json`, renderiza com `--formats pdf` (motor padrão) e exige `returncode == 0`, sem exceção para `executive_presentation`;
- remova o comentário sobre "defeito conhecido".

**Verify**: `pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests/test_render.py -k "PdfQuality or page_margin_zeroed"` → sem falhas e **sem skips** (o WeasyPrint precisa estar carregando).

### Step 3: Suíte completa e sync

**Verify**: suíte completa `0 failed`; `sync_shared.py --check` e `build_sources.py --check` → exit 0;
`grep -l 'slide_css += " @page { margin: 0; }"' */assets/design-system/scripts/render.py | wc -l` → `11`.

### Step 4: Commit

Um commit para o Step 2: "Exige que as 18 amostras passem no portão de qualidade". Outro para o sync, se houver: "Sincroniza correção do rodapé da apresentação nas 11 skills".

## Done criteria

- [ ] `38d17de` e `d05eb02` no branch, sem outros commits do 031
- [ ] `grep -n "known_defect" _DESIGN_SYSTEM/tests/test_render.py` → nada
- [ ] Suíte completa `0 failed`, com WeasyPrint carregando (testes de PDF não pulam)
- [ ] Sync e fontes → exit 0
- [ ] Relatório final informa: commits criados e saída do `pytest -rs` (lista de skips)

## STOP conditions

- O cherry-pick tiver conflito.
- O WeasyPrint não carregar no seu ambiente.
- Alguma amostra além da apresentação for reprovada pelo portão.
- Para passar, seria preciso mudar `pdf_quality.py`, o portão em `render.py` ou outro teste existente.

## Regra para os próximos planos

Quando uma STOP condition ocorrer, **pare e reporte**. Não transforme a falha em comportamento
esperado num teste: isso esconde um defeito real do operador.
