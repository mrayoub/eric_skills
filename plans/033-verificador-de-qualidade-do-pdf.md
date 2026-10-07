# Plan 033: Reprovar todo PDF com defeito visual (texto fora da página, fonte abaixo do mínimo, sobreposição) e criar a folha de comparação entre motores

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 0eac9a9..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/requirements.txt _DESIGN_SYSTEM/README.md _TOOLS`
> O Plano 032 já terá mudado esses arquivos (é dependência). Confira que as
> mudanças descritas no 032 estão lá; qualquer outra divergência dos trechos
> abaixo é STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (o portão pode reprovar PDFs que hoje saem com defeito — é o objetivo, mas muda comportamento)
- **Depends on**: `plans/032-pdf-reportlab-portatil.md` (DONE) — usa o `reportlab` do `requirements.txt` e o `--pdf-engine reportlab`.
- **Category**: tests / qualidade dos entregáveis
- **Planned at**: commit `0eac9a9`, 2026-10-05

## Why this matters

O operador definiu que os entregáveis devem ter qualidade de apresentação
*state of the art*. Hoje nada impede um PDF com texto cortado, sobreposto ou miúdo
de ser entregue: a única checagem é a contagem de páginas dos layouts de página
única, e o Plano 031 mostrou que ela deixa passar sobreposição silenciosa. O próprio
design system já proíbe esses defeitos em `tokens.json` → `density`:

```json
"density": {"minimum_font_size": 7.5, "minimum_body_font_size": 8, "maximum_columns": 4,
            "overflow_strategy": ["paginate", "split_component", "switch_layout_variant"],
            "forbidden_strategy": ["clip", "overlap", "shrink_below_minimum"]}
```

Este plano transforma essas regras em verificação automática executada **em todo PDF
gerado, por qualquer motor**, e cria a ferramenta de comparação visual que os
Planos 034–036 usam como etapa de aprovação do operador. Com o portão em vigor,
"funcionou" passa a significar "saiu sem defeito mensurável", não só "gerou um arquivo".

### Verificado ao escrever este plano (não é suposição)

O código do Passo 1 foi executado contra as 18 amostras atuais
(`_SAMPLES_ENTREGAVEIS/*/*.pdf`, geradas pelo WeasyPrint), contra PDFs do ReportLab e
contra um PDF propositalmente defeituoso:

- PDF defeituoso (texto saindo da página, fonte de 6 pt, duas linhas desenhadas uma
  sobre a outra): as 3 falhas detectadas.
- 17 das 18 amostras: nenhum problema; **zero falsos positivos de sobreposição**
  (o ajuste que ignora letras vizinhas na mesma linha é necessário: sem ele, o par
  "T-" de "OUT-01" na tabela do IQB, aproximado pelo kerning, era acusado como sobreposição).
- 1 defeito real encontrado: `sample-briefing-one-page-v1.0.0.pdf` tem texto de **7,2 pt**
  — são as citações sobrescritas (`<sup>`) dentro do conteúdo das seções (8,5 pt).
  O Passo 2 corrige o CSS.
- Tempo: 0,01–0,12 s por PDF.
- `pdfminer.six==20260107` instala de wheel (depende de `charset-normalizer` e `cryptography`, ambos com wheels para Windows, macOS e Linux).

## Current state

- `_DESIGN_SYSTEM/scripts/render.py` — renderizador. Depois do Plano 032, o bloco de PDF de `main()` tem esta forma (confira):
  ```python
      if "pdf" in requested:
          path = out / f"{stem}.pdf"
          try:
              if args.pdf_engine == "reportlab":
                  render_pdf_reportlab(content, tokens, profile, path)
              else:
                  from weasyprint import HTML
                  HTML(string=source_html or "", base_url=str(ROOT)).write_pdf(str(path))
          except (ImportError, OSError) as exc:
              ...
          else:
              if profile["layout"] in ("executive_one_page", "card_portrait"):
                  ...
                  count = len(PdfReader(str(path)).pages)
                  if count != 1:
                      path.unlink(missing_ok=True)
                      raise ValueError(f"{profile['layout']} excedeu uma página ({count}); revise ou divida o conteúdo sem reduzir a fonte")
              files.append(path)
  ```
- CSS em `render.py`, função `css()` (`render.py:343-429` no commit de planejamento): não há regra para `sup`; o navegador/WeasyPrint aplica `font-size: smaller`. Linha de referência para inserir a regra nova, logo depois de:
  ```python
  p, li {{ orphans: 2; widows: 2; }}
  ```
- Padrão de módulo vizinho carregado por caminho (os testes carregam `render.py` sem `scripts/` no `sys.path`), `render.py:183-188`:
  ```python
          import importlib.util

          spec = importlib.util.spec_from_file_location("deliverable_validators", ROOT / "scripts/validators/__init__.py")
          validators = importlib.util.module_from_spec(spec)
          spec.loader.exec_module(validators)
  ```
- Amostras: `_SAMPLES_ENTREGAVEIS/<deliverable_type>/input.json` (18 tipos, dados fictícios). Os PDFs já presentes nelas foram gerados por uma versão antiga do renderizador; **não** os regenere.
- Convenções: Python com `from __future__ import annotations`, mensagens em português; testes `unittest` rodados por `pytest`; testes de PDF chamam `render.py` via `subprocess` (ver `RenderTests.render` em `test_render.py`). Commits em português no imperativo.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Ambiente | `python3 -m venv /tmp/venv-033 && /tmp/venv-033/bin/python -m pip install -q -r _DESIGN_SYSTEM/requirements.txt pdfminer.six==20260107 pypdfium2 pytest` | exit 0 |
| Testes | `/tmp/venv-033/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |
| Fontes | `python3 _TOOLS/build_sources.py --check` | exit 0 |

Anote a contagem de testes **antes** de começar (linha de base).

## Scope

**In scope**:
- `_DESIGN_SYSTEM/scripts/pdf_quality.py` (criar)
- `_DESIGN_SYSTEM/scripts/render.py` (chamada do portão; regra CSS de `sup`)
- `_DESIGN_SYSTEM/requirements.txt` (`pdfminer.six==20260107`)
- `_DESIGN_SYSTEM/README.md` (documentar o portão)
- `_DESIGN_SYSTEM/tests/test_render.py`
- `_TOOLS/compare_pdf_engines.py` (criar) e `_TOOLS/README.md`
- Cópias geradas pelo sync; `plans/README.md` (status)

**Out of scope**:
- `pdf_reportlab.py` — se um PDF do ReportLab for reprovado pelo portão, STOP (é defeito do 032, não deste plano).
- Qualquer outra mudança visual no CSS além da regra de `sup`.
- `_SAMPLES_ENTREGAVEIS/` — não regenere.
- Verificar contraste de cores, acessibilidade (PDF marcado) e hifenização: fora deste portão.

## Git workflow

- Branch: `advisor/033-verificador-qualidade-pdf`
- Commits: módulo; integração+CSS; testes; ferramenta de comparação; docs+sync.
- Não faça push nem merge.

## Steps

### Step 1: Criar `_DESIGN_SYSTEM/scripts/pdf_quality.py`

Conteúdo (testado; mantenha a lógica, pode ajustar só estilo):

```python
"""Portão de qualidade dos PDFs: aplica as regras de density do tokens.json.

Reprova texto fora da página, fonte abaixo do mínimo e caracteres sobrepostos."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Iterator


def _chars(layout: Any) -> Iterator[Any]:
    from pdfminer.layout import LTChar

    stack = list(layout)
    while stack:
        item = stack.pop()
        if isinstance(item, LTChar):
            yield item
        elif hasattr(item, "__iter__"):
            stack.extend(item)


def check_pdf(path: Path, min_size: float = 7.5, tolerance: float = 0.5, overlap_ratio: float = 0.4) -> list[str]:
    from pdfminer.high_level import extract_pages

    problems: list[str] = []
    for number, page in enumerate(extract_pages(str(path)), 1):
        width, height = page.width, page.height
        chars = sorted((c for c in _chars(page) if c.get_text().strip()), key=lambda c: (-c.y1, c.x0))
        outside = [c for c in chars if c.x0 < -tolerance or c.x1 > width + tolerance
                   or c.y0 < -tolerance or c.y1 > height + tolerance]
        if outside:
            sample = "".join(c.get_text() for c in outside[:20])
            problems.append(f"página {number}: texto fora da página ({sample!r})")
        small = sorted({round(c.size, 1) for c in chars if c.size < min_size - 0.05})
        if small:
            problems.append(f"página {number}: fonte abaixo de {min_size} pt ({small})")
        grid: dict[tuple[int, int], list[int]] = defaultdict(list)
        hits = 0
        for i, c in enumerate(chars):
            for gx in range(int(c.x0 // 20), int(c.x1 // 20) + 1):
                for gy in range(int(c.y0 // 20), int(c.y1 // 20) + 1):
                    for j in grid[(gx, gy)]:
                        d = chars[j]
                        # Letras vizinhas da mesma linha podem se tocar por kerning ("T-").
                        if abs(d.y0 - c.y0) < 0.5 and abs(i - j) <= 2:
                            continue
                        ix = min(c.x1, d.x1) - max(c.x0, d.x0)
                        iy = min(c.y1, d.y1) - max(c.y0, d.y0)
                        smaller = min(c.width * c.height, d.width * d.height)
                        if ix > 0 and iy > 0 and smaller and ix * iy / smaller > overlap_ratio:
                            hits += 1
                    grid[(gx, gy)].append(i)
        if hits:
            problems.append(f"página {number}: {hits} pares de caracteres sobrepostos")
    return problems
```

**Verify**: `/tmp/venv-033/bin/python -c "import importlib.util as u;s=u.spec_from_file_location('q','_DESIGN_SYSTEM/scripts/pdf_quality.py');m=u.module_from_spec(s);s.loader.exec_module(m);print(m.check_pdf(__import__('pathlib').Path('_SAMPLES_ENTREGAVEIS/test_card/sample-test-card-v1.0.0.pdf')))"` → `[]`; e com `_SAMPLES_ENTREGAVEIS/briefing_one_page/sample-briefing-one-page-v1.0.0.pdf` → `['página 1: fonte abaixo de 7.5 pt ([7.2])']`.

### Step 2: Corrigir o tamanho das citações no CSS

Em `css()`, logo depois da linha `p, li {{ orphans: 2; widows: 2; }}`, acrescente:
```python
sup {{ font-size: {tokens['density']['minimum_font_size']}pt; line-height: 0; }}
```

**Verify** (só se o WeasyPrint funcionar nesta máquina; senão registre "não verificável aqui" e siga): renderizar `_SAMPLES_ENTREGAVEIS/briefing_one_page/input.json` com `--formats pdf` para `/tmp/o033` e rodar `check_pdf` no PDF → `[]`.

### Step 3: Ligar o portão em `render.py`

1. Função nova em `render.py`:
   ```python
   def check_pdf_quality(path: Path, tokens: dict[str, Any]) -> list[str]:
       import importlib.util

       spec = importlib.util.spec_from_file_location("pdf_quality", ROOT / "scripts/pdf_quality.py")
       module = importlib.util.module_from_spec(spec)
       spec.loader.exec_module(module)
       return module.check_pdf(path, min_size=float(tokens["density"]["minimum_font_size"]))
   ```
2. No ramo `else:` do bloco de PDF, **depois** da checagem de página única e **antes** de `files.append(path)`:
   ```python
               problems = check_pdf_quality(path, tokens)
               if problems:
                   path.unlink(missing_ok=True)
                   raise ValueError("PDF reprovado na verificação de qualidade: " + "; ".join(problems[:5])
                                    + ". Divida o conteúdo ou mude a variante; não reduza a fonte")
   ```
   Se `pdfminer` não estiver instalado, `ImportError` deve encerrar com mensagem clara: envolva a chamada para relançar `RuntimeError("Verificação de qualidade do PDF requer pdfminer.six: pip install pdfminer.six")`, no mesmo estilo de `render.py` para `pypdf`.
3. `_DESIGN_SYSTEM/requirements.txt`: acrescente `pdfminer.six==20260107`.

**Verify**:
```
/tmp/venv-033/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/test_card/input.json --out-dir /tmp/o033a --formats pdf --pdf-engine reportlab
/tmp/venv-033/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/briefing_one_page/input.json --out-dir /tmp/o033a --formats pdf --pdf-engine reportlab
```
→ os dois terminam com `"unavailable": {}` e PDF gerado. Se algum for reprovado, STOP (defeito do 032).

### Step 4: Testes

Em `test_render.py`, classe `PdfQualityTests`, pulando se `reportlab` ou `pdfminer` não estiverem disponíveis:

1. `test_detects_each_defect`: gere com `reportlab.pdfgen.canvas` um PDF A4 com (a) `drawString(580, 400, "Saindo da pagina")` em Helvetica 12, (b) `drawString(50, 100, "miudo")` em Helvetica 6, (c) `drawString(50, 700, "Texto sobreposto aqui")` e `drawString(55, 702, "Outra linha por cima")` em Helvetica 12. `check_pdf` devolve 3 problemas contendo "fora da página", "abaixo de 7.5" e "sobrepostos".
2. `test_kerning_is_not_overlap`: PDF com `drawString(50, 700, "OUT-01 AVA-02 TT-TT")` em Helvetica 8 → `[]`.
3. `test_reportlab_outputs_pass`: renderize via `subprocess` as amostras de `test_card`, `learning_card` e `briefing_one_page` com `--pdf-engine reportlab` → exit 0 (o portão já roda dentro do `render.py`).
4. `test_weasyprint_samples_pass` (pula sem `pdf_available()`): renderize as 18 amostras com o motor padrão → exit 0 em todas. Se alguma for reprovada além do caso do Passo 2, STOP e reporte o tipo e a mensagem.
5. `test_gate_removes_pdf_and_fails`: carregue `render.py` como módulo (padrão `importlib` do topo de `test_render.py`), use `unittest.mock.patch.object(module, "check_pdf_quality", return_value=["página 1: teste"])` e chame `module.main()` com `unittest.mock.patch.object(sys, "argv", [...])` para a amostra do test card com `--pdf-engine reportlab --formats pdf,md` → `ValueError` contendo "reprovado na verificação de qualidade"; o `.pdf` não existe na pasta de saída.

**Verify**: `/tmp/venv-033/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests/test_render.py -k PdfQuality` → passa (o caso 4 pode pular sem Pango). Suíte completa → `0 failed`.

### Step 5: Ferramenta de comparação visual `_TOOLS/compare_pdf_engines.py`

Ferramenta de manutenção (não vai para as skills; `pypdfium2` não entra no `requirements.txt`). Comportamento:

- Argumentos: `--out <pasta>` (obrigatório), `--types <lista separada por vírgula>` (padrão: todas as pastas de `_SAMPLES_ENTREGAVEIS` com `input.json`), `--engines weasyprint,reportlab` (padrão os dois).
- Para cada tipo e motor: roda `render.py` via `subprocess` com `--formats pdf --pdf-engine <motor>` numa subpasta `<out>/<motor>/`; registra exit code e stderr (motor indisponível ou tipo não suportado não interrompem a ferramenta).
- Rasteriza cada página com `pypdfium2` (`pdf[i].render(scale=100/72).to_pil()`) e monta, com Pillow, uma imagem `<out>/<tipo>.png` com as páginas do WeasyPrint à esquerda e as do ReportLab à direita, rótulo do motor no topo de cada coluna e fundo cinza claro.
- Gera `<out>/index.html` com, por tipo: a imagem, número de páginas por motor, resultado do `check_pdf` por motor e o stderr quando houve falha.

Acrescente ao `_TOOLS/README.md` um parágrafo explicando o uso (`pip install pypdfium2 pillow`) e que ela é o material das revisões visuais dos Planos 034–036.

**Verify**: `/tmp/venv-033/bin/python _TOOLS/compare_pdf_engines.py --out /tmp/cmp-033 --types test_card,learning_card,briefing_one_page` → exit 0; `ls /tmp/cmp-033/*.png | wc -l` → `3`; `grep -c "<img" /tmp/cmp-033/index.html` → `3`.

### Step 6: Documentação e sync

- `_DESIGN_SYSTEM/README.md`, item 3: "Todo PDF passa por uma verificação de qualidade (`scripts/pdf_quality.py`): texto fora da página, fonte abaixo de `density.minimum_font_size` ou caracteres sobrepostos reprovam o arquivo, que não é entregue. Corrija dividindo o conteúdo ou trocando a variante; nunca reduza a fonte."
- Rode sync e checagens (tabela de comandos).

**Verify**: `ls */assets/design-system/scripts/pdf_quality.py | wc -l` → `11`; `--check`s com exit 0.

## Test plan

- 5 testes novos em `PdfQualityTests` (Passo 4), modelados nos testes de `subprocess` de `RenderTests` e no uso de `unittest.mock.patch.object` de `PresentationLayoutJsonTests`.
- O caso 1 garante que o portão detecta cada defeito; o caso 2 protege contra o falso positivo de kerning; os casos 3 e 4 garantem que as saídas atuais passam; o caso 5 garante que um PDF reprovado não é entregue.

## Done criteria

- [ ] `pytest -k PdfQuality` sem falhas; suíte completa `0 failed`
- [ ] `grep -n "check_pdf_quality" _DESIGN_SYSTEM/scripts/render.py` → definição + 1 chamada
- [ ] `grep -c "pdfminer.six==20260107" _DESIGN_SYSTEM/requirements.txt` → `1`
- [ ] `/tmp/cmp-033/index.html` gerado com 3 tipos
- [ ] `sync_shared.py --check` e `build_sources.py --check` → exit 0
- [ ] `git status` só com arquivos do escopo (mais cópias do sync)
- [ ] Linha do Plano 033 em `plans/README.md` atualizada

## STOP conditions

- O Plano 032 não está DONE, ou `--pdf-engine reportlab` não existe.
- Algum PDF do ReportLab das 3 amostras é reprovado pelo portão.
- Alguma amostra do WeasyPrint, além do one-page antes do Passo 2, é reprovada.
- O teste do kerning (caso 2) acusa sobreposição: não aumente `overlap_ratio` por conta própria; reporte.
- O tempo do `check_pdf` passar de 2 s numa amostra.

## Maintenance notes

- O portão vale para todo PDF: uma mudança de CSS ou de `pdf_reportlab.py` que crie sobreposição ou fonte miúda passa a falhar o render, o que é intencional.
- Limites conhecidos: não verifica contraste de cores, texto cortado por `overflow: hidden` dentro da página (o texto continua no PDF), nem acessibilidade (PDF marcado). Candidatos a evolução.
- `overlap_ratio=0.4` e a regra de vizinhança foram calibrados nas 18 amostras; ao mudar, rode a ferramenta do Passo 5 em todos os tipos.
- A ferramenta de comparação é a base das aprovações visuais do operador nos Planos 034–036.
