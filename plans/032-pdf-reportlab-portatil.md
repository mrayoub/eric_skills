# Plan 032: Gerar PDF com ReportLab, sem Pango — prova em `test_card`, `learning_card` e `briefing_one_page`

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 8472652..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/requirements.txt _DESIGN_SYSTEM/README.md _DESIGN_SYSTEM/assets/fonts _TOOLS`
> Se algum desses arquivos mudou desde que este plano foi escrito, compare os
> trechos de "Estado atual" com o código real antes de prosseguir; em caso de
> divergência, trate como STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (código novo isolado atrás de uma opção; o caminho padrão WeasyPrint não muda)
- **Depends on**: nenhum. Independente do Plano 031 (BLOCKED), que trata posicionamento por `layout.json` no HTML — não use `layout.json` aqui.
- **Category**: dependências / portabilidade
- **Planned at**: commit `8472652`, 2026-10-05
- **Substitui**: a versão anterior deste plano (Chromium/Playwright como reserva), rejeitada pelo operador porque o Chromium corrompia a camada de texto do PDF.

## Por que isso importa

O PDF é um formato de entrega real das 11 skills, mas hoje só sai onde o WeasyPrint
consegue carregar bibliotecas nativas do sistema (Pango, Cairo). Em Windows isso exige
instalar GTK3/MSYS2; no macOS com Python do Anaconda exige `DYLD_LIBRARY_PATH`; em
ambientes compartilhados uma versão diferente de `pydyf` derruba a geração (detalhes em
`plans/PROBLEMA_MOTOR_PDF_CROSS_PLATFORM.md`). O ReportLab é Python puro (wheel
`py3-none-any`, só depende de `pillow` e `charset-normalizer`, que têm wheels para todos
os sistemas): instala com `pip` e gera PDF igual em Mac, Linux e Windows. Este plano
**prova** o ReportLab em 3 tipos de entregável, atrás da opção `--pdf-engine reportlab`,
sem mudar o motor padrão. Se a prova for aprovada pelo operador, um plano seguinte
migra os outros tipos e decide trocar o padrão.

### O que já foi verificado ao escrever este plano (não é suposição)

Num ambiente isolado (Python 3.12, `reportlab==5.0.1`, `fonttools==4.66.1`), fora do repo:

- Instâncias estáticas geradas das fontes variáveis do projeto com
  `fonttools varLib.instancer <Variable.ttf> wght=<peso> --static --update-name-table`
  saem com nome interno correto (`Montserrat-Bold` 700, `Roboto-Regular` 400,
  `Roboto-Bold` 700) e sem tabela `fvar`. **Sem** `--update-name-table`, a Montserrat
  sai com nome interno `Montserrat-Thin` — por isso a opção é obrigatória.
  Tamanhos: Montserrat-Bold ≈ 375 KB, Roboto-Regular ≈ 158 KB, Roboto-Bold ≈ 158 KB.
- Test Card da amostra em A4 retrato: 1 página, 210,0 × 297,0 mm; `pypdf` extrai o
  texto com acentos corretos ("FICTÍCIO", "solicitação"); `pdfplumber` extrai palavras
  inteiras (sem a repetição de caracteres vista no Chromium).
- Duas execuções com `BaseDocTemplate(..., invariant=1)` produziram **bytes idênticos**.
- Transbordo: conteúdo dentro de `KeepInFrame(..., mode="error")` maior que a página
  lança `reportlab.platypus.doctemplate.LayoutError`. Em layout de duas colunas
  (`Frame`s lado a lado), conteúdo excedente vira uma 2ª página — detectável.
  Ou seja: o ReportLab **não sobrepõe texto em silêncio**, o defeito que bloqueou o Plano 031.
- One-page da amostra em A4 paisagem com duas colunas e logo PNG: 1 página,
  297,0 × 210,0 mm, texto extraído corretamente.

## Estado atual

Arquivos relevantes:

- `_DESIGN_SYSTEM/scripts/render.py` — renderizador único (fonte; as 11 skills recebem cópias via sync).
- `_DESIGN_SYSTEM/tests/test_render.py` — testes (não são copiados para as skills).
- `_DESIGN_SYSTEM/requirements.txt` — dependências com versões exatas.
- `_DESIGN_SYSTEM/assets/fonts/` — hoje só `Montserrat-Variable.ttf`, `Roboto-Variable.ttf` e as licenças OFL (sem "Reserved Font Name" declarado; gerar instâncias é permitido).
- `_DESIGN_SYSTEM/assets/logo_ccee.png` — logo usado no cabeçalho.
- `_TOOLS/sync_shared.py` — copia `_DESIGN_SYSTEM/` (exceto `tests/`, `__pycache__`) para `<skill>/assets/design-system/` nas 11 skills.

### Geração de PDF hoje — `render.py:932-955`

```python
    unavailable: dict[str, str] = {}
    if "pdf" in requested:
        path = out / f"{stem}.pdf"
        try:
            from weasyprint import HTML
            HTML(string=source_html or "", base_url=str(ROOT)).write_pdf(str(path))
        except (ImportError, OSError) as exc:
            import sys

            path.unlink(missing_ok=True)
            unavailable["pdf"] = f"{type(exc).__name__}: {exc}"[:300]
            print(f"AVISO: PDF não gerado ({unavailable['pdf']}). No macOS: brew install pango; "
                  "no Debian/Ubuntu: apt-get install libpango-1.0-0 libpangoft2-1.0-0.", file=sys.stderr)
        else:
            if profile["layout"] in ("executive_one_page", "card_portrait"):
                try:
                    from pypdf import PdfReader
                except ImportError as exc:
                    raise RuntimeError("Verificação de página única requer pypdf: pip install pypdf") from exc
                count = len(PdfReader(str(path)).pages)
                if count != 1:
                    path.unlink(missing_ok=True)
                    raise ValueError(f"{profile['layout']} excedeu uma página ({count}); revise ou divida o conteúdo sem reduzir a fonte")
            files.append(path)
```

Argumentos de `main()` — `render.py:902-906`:

```python
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--formats", help="json,pdf,docx,md,txt; pptx só para apresentação; csv só para tabelas exportáveis")
```

Manifesto — `render.py:976-990` (dicionário `manifest` com `renderer_version`, `files`, `unavailable`, …). Versão atual: `RENDERER_VERSION = "1.3.1"` em `render.py:18`. Nenhum teste fixa esse número.

### Funções de `render.py` que o motor novo deve reaproveitar (não duplique a lógica)

- `DELIVERABLE_LABELS` (`render.py:19-38`): rótulo do tipo, ex. `"test_card": "Cartão de teste"`, `"briefing_one_page": "Resumo do briefing"`.
- `CARD_LABELS` (`render.py:49-62`): rótulos dos 4 campos dos cards, ex. `"hypothesis": "1. Acreditamos que — hipótese"`.
- `identity_line(content)` (`render.py:83-89`): `"ID <id> · versão <v> · <estado>"`.
- Rodapé do Learning Card (`render.py:589-591`):
  ```python
      footer_label = identity_line(content)
      if content["deliverable_type"] == "learning_card" and meta.get("test_card_id"):
          footer_label += f' · Test Card {meta["test_card_id"]} v{meta.get("test_card_version", "")}'
  ```
- `block_text(block)` (`render.py:195-213`): texto plano de qualquer bloco.
- `table_rows(block)` (`render.py:216-240`): `(cabeçalhos, linhas)` de um bloco `table`.
- Agrupamento de seções do HTML — `html_report_blocks` (`render.py:307-340`): cada bloco `heading` abre uma seção cujo título é `block_text(heading)`; blocos antes do primeiro heading formam uma seção intitulada `"Notas"`. **Use a mesma regra** no one-page.

### Padrão de carregamento de módulo vizinho — `render.py:183-188`

```python
    if effective_completeness == "complete":
        import importlib.util

        spec = importlib.util.spec_from_file_location("deliverable_validators", ROOT / "scripts/validators/__init__.py")
        validators = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validators)
```

Os testes carregam `render.py` com `spec_from_file_location`, sem `scripts/` no `sys.path`;
por isso o módulo novo **deve** ser carregado com esse mesmo padrão, não com `import`.

### Aparência atual a reproduzir (do CSS em `render.py:343-429` e variantes `render.py:565-576`)

| Elemento | Card (A4 retrato) | One-page (A4 paisagem) |
|---|---|---|
| Margens | `tokens.page.a4_portrait`: 16 mm | `tokens.page.a4_landscape`: 12 mm |
| Cabeçalho | rótulo do tipo em maiúsculas, Montserrat Bold 8 pt, cor `document_accent`, à esquerda; logo à direita (máx. 38 × 11 mm); linha inferior 1,5 pt `document_primary` | igual |
| Título | Montserrat Bold 30 pt, entrelinha 1,1, `document_primary` | 24 pt |
| Resumo | Roboto 10,5 pt, `text_strong` | igual |
| Corpo | Roboto 9,5 pt, entrelinha 1,35, `text_body` | 8,5 pt dentro das seções |
| Campo do card | caixa com borda 0,75 pt `border`, barra esquerda 3 pt `document_accent`, padding 12 pt, rótulo Montserrat Bold 13 pt `document_primary` | — |
| Seção | — | faixa `document_deep` com título em maiúsculas Montserrat Bold 9 pt branco; conteúdo com padding 5–7 pt; **duas colunas**, espaço 8 pt |
| Callout | fundo `document_deep`, texto `inverse`, barra esquerda 3 pt `document_accent` | igual |
| Tabela | cabeçalho fundo `document_primary`, texto `inverse`; borda 0,75 pt `border`; 8 pt | igual |
| Citações | sobrescrito `[ID]` após o texto; seção final "Fontes" com lista "ID — source_id, locator" | igual |
| Rodapé | `footer_label` em Roboto 7,5 pt `text_muted`, alinhado à direita, na margem inferior, em toda página | igual |

As cores vêm de `tokens["color"]` (ex.: `document_primary` `#193C8E`, `document_accent` `#4C73D1`, `document_deep` `#102661`, `text_body` `#30343B`, `text_muted` `#586EA4`, `border` `#D2D9E8`, `inverse` `#FFFFFF`). Leia sempre de `tokens`, nunca escreva hex no código.

A meta não é igualdade de pixels com o WeasyPrint; é a mesma hierarquia e conteúdo,
uma página, texto extraível. A comparação visual é feita pelo operador no Passo 8.

### Convenções do repositório

- Python com `from __future__ import annotations`, type hints, funções pequenas, mensagens de erro em português (veja `render.py`).
- Tests em `unittest`, executados com `pytest`; testes de PDF usam `subprocess` contra `SCRIPT` e pulam quando a dependência falta — padrão `pdf_available()` em `test_render.py:32-37`:
  ```python
  def pdf_available() -> bool:
      try:
          import weasyprint
          return True
      except (ImportError, OSError):
          return False
  ```
- Simulação de motor ausente: `test_missing_pdf_backend_still_renders_other_formats` (`test_render.py:470-492`) cria um `weasyprint.py` falso numa pasta e a põe no `PYTHONPATH`. Use o mesmo truque.
- Commits em português, imperativo, assunto curto. Exemplos do `git log`: "Corrige canvas de test_card/learning_card.layout.json e escreve plano 031", "render_pptx lê posição de layouts/<tipo>.layout.json com fallback".

## Commands you will need

Crie um ambiente isolado (não use o Python global — foi justamente a causa do problema 2 do documento de origem):

| Purpose | Command | Expected on success |
|---|---|---|
| Ambiente | `python3 -m venv /tmp/venv-032 && /tmp/venv-032/bin/python -m pip install -q -r _DESIGN_SYSTEM/requirements.txt reportlab==5.0.1 fonttools==4.66.1 pytest pdfplumber` | exit 0 |
| Testes | `/tmp/venv-032/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` (skips de WeasyPrint são esperados se não houver Pango) |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |
| Fontes | `python3 _TOOLS/build_sources.py --check` | exit 0 |
| Validador | `for s in */; do [ -f "$s/SKILL.md" ] && python3 ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py "$s"; done` | 11 × "Skill is valid!" (se o caminho não existir, pule e registre) |

**Linha de base (antes de mudar qualquer coisa)**:
```
/tmp/venv-032/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS | tail -1
/tmp/venv-032/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/learning_card/input.json --out-dir /tmp/h0 --formats html
/tmp/venv-032/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/briefing_one_page/input.json --out-dir /tmp/h0 --formats html
```
Anote a contagem de testes. Os dois HTML em `/tmp/h0` servem para provar, no fim, que o caminho padrão não mudou.

## Scope

**In scope** (os únicos arquivos que você deve criar ou modificar):
- `_TOOLS/make_static_fonts.py` (criar)
- `_TOOLS/README.md` (uma seção curta)
- `_DESIGN_SYSTEM/assets/fonts/static/Montserrat-Bold.ttf`, `Roboto-Regular.ttf`, `Roboto-Bold.ttf` (gerar)
- `_DESIGN_SYSTEM/scripts/pdf_reportlab.py` (criar)
- `_DESIGN_SYSTEM/scripts/render.py`
- `_DESIGN_SYSTEM/requirements.txt`
- `_DESIGN_SYSTEM/README.md`
- `_DESIGN_SYSTEM/tests/test_render.py`
- As cópias geradas pelo sync em `<skill>/assets/design-system/` (só via `_TOOLS/sync_shared.py`, nunca à mão)
- `plans/README.md` (linha de status)

**Out of scope** (não toque):
- O caminho WeasyPrint e o HTML (`render_html`, `css`): a saída padrão não pode mudar.
- O motor padrão: `--pdf-engine` continua com padrão `weasyprint` neste plano.
- `_DESIGN_SYSTEM/layouts/*.layout.json` e qualquer leitura deles — é assunto do Plano 031.
- Os outros 15 tipos de entregável no ReportLab (relatórios, apresentação, etc.) — plano seguinte, se a prova for aprovada.
- `SKILL.md` das skills — só mudam quando o padrão mudar.
- `_SAMPLES_ENTREGAVEIS/` — não regenere amostras.
- Os arquivos `*-Variable.ttf` — continuam sendo usados pelo HTML.
- `_DESIGN_SYSTEM/layouts/executive_presentation.layout.json` pode estar com alteração não commitada do operador na cópia de trabalho principal: não inclua nem reverta.

## Git workflow

- Branch: `advisor/032-pdf-reportlab`
- Um commit por passo lógico (fontes; módulo; integração; testes; docs+sync). Assunto em português no imperativo.
- Não faça push nem merge.

## Steps

### Step 1: Gerar as fontes estáticas com um script reproduzível

Crie `_TOOLS/make_static_fonts.py`:

```python
#!/usr/bin/env python3
"""Gera instâncias estáticas das fontes variáveis do design system (motor ReportLab).

Requer fontTools só na manutenção: pip install fonttools. Não é dependência das skills."""
from __future__ import annotations

from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "_DESIGN_SYSTEM/assets/fonts"
INSTANCES = [("Montserrat", 700, "Bold"), ("Roboto", 400, "Regular"), ("Roboto", 700, "Bold")]


def main() -> None:
    target = FONTS / "static"
    target.mkdir(exist_ok=True)
    for family, weight, style in INSTANCES:
        font = TTFont(FONTS / f"{family}-Variable.ttf")
        static = instantiateVariableFont(font, {"wght": weight}, static=True, updateFontNames=True)
        static.save(target / f"{family}-{style}.ttf")
        print(f"OK {family}-{style}.ttf")


if __name__ == "__main__":
    main()
```

Se `updateFontNames=True` lançar erro, STOP (o nome interno ficaria errado — ver "O que já foi verificado").

Acrescente ao `_TOOLS/README.md` um parágrafo: as fontes em `_DESIGN_SYSTEM/assets/fonts/static/` são geradas por `python3 _TOOLS/make_static_fonts.py` (requer `pip install fonttools`) a partir das variáveis; regenere se as variáveis mudarem.

**Verify**:
```
/tmp/venv-032/bin/python _TOOLS/make_static_fonts.py
/tmp/venv-032/bin/python -c "
from fontTools.ttLib import TTFont
for n in ('Montserrat-Bold','Roboto-Regular','Roboto-Bold'):
    f=TTFont(f'_DESIGN_SYSTEM/assets/fonts/static/{n}.ttf'); print(n, f['name'].getDebugName(6), f['OS/2'].usWeightClass, 'fvar' in f)"
```
→ três linhas `OK …`; depois `Montserrat-Bold Montserrat-Bold 700 False`, `Roboto-Regular Roboto-Regular 400 False`, `Roboto-Bold Roboto-Bold 700 False`.

### Step 2: Criar o módulo `_DESIGN_SYSTEM/scripts/pdf_reportlab.py`

Interface (load-bearing — `render.py` e os testes dependem dela):

```python
"""Motor de PDF em ReportLab: só pip, sem Pango/Cairo. Plano 032: prova para
os layouts card_portrait e executive_one_page."""
from __future__ import annotations

import html
import io
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts" / "static"
SUPPORTED_LAYOUTS = ("card_portrait", "executive_one_page")


class PdfOverflow(ValueError):
    """O conteúdo não cabe na página única exigida pelo layout."""


def render_pdf(content: dict[str, Any], tokens: dict[str, Any], profile: dict[str, Any], path: Path, *,
               deliverable_label: str, footer_label: str, field_labels: dict[str, str] | None,
               block_text: Callable[[dict[str, Any]], str],
               table_rows: Callable[[dict[str, Any]], tuple[list[str], list[list[str]]]]) -> None:
    ...
```

Regras de implementação:

1. **Imports do ReportLab dentro de `render_pdf`** (ou de funções chamadas por ela), para que `ImportError` só ocorra ao gerar PDF.
2. **Fontes**: registre `Montserrat-Bold`, `Roboto-Regular`, `Roboto-Bold` com `pdfmetrics.registerFont(TTFont(nome, str(FONT_DIR / f"{nome}.ttf")))`, só se `nome not in pdfmetrics.getRegisteredFontNames()`. Se algum arquivo faltar, lance `FileNotFoundError("Fontes estáticas ausentes em assets/fonts/static; rode _TOOLS/make_static_fonts.py")`.
3. **Geometria**: `paper = profile["paper"]`; `page = tokens["page"][paper]`; tamanho `(page["width"]*mm, page["height"]*mm)`; margens `margin_*` do token. Se `profile["layout"] not in SUPPORTED_LAYOUTS`, lance `ValueError`.
4. **Estilos**: centralize numa função `make_styles(tokens, layout) -> dict[str, ParagraphStyle]`. Tamanho, entrelinha e família vêm de `tokens["typography"]["styles"]` sempre que o estilo existir lá (`cover_title` 30 pt/1,1; `cover_eyebrow` 8 pt; `section_title`; `body` 9,5 pt/1,35; `body_dense` 8 pt; `metric` 16 pt; `table_header` 8 pt; `table_body` 8 pt/1,3; `footer` 7,5 pt), com `leading = size * line_height`; `font_brand` → `Montserrat-Bold`, `font_body` → `Roboto-Regular` (ou `Roboto-Bold` quando `weight >= 600`). Use a tabela "Aparência atual a reproduzir" só para o que os tokens não definem (ex.: título de 24 pt no one-page, rótulo do campo de 13 pt). Cores sempre de `colors.HexColor(tokens["color"][...])`. Nenhum tamanho pode ficar abaixo de `tokens["density"]["minimum_font_size"]` (7,5). Todo texto vindo do conteúdo passa por `html.escape(...)` e `\n` vira `<br/>` (o `Paragraph` interpreta marcação).
5. **Citações**: depois do texto de um bloco, acrescente `"".join(f'<super size="7.5" rise="3">[{html.escape(i)}]</super>' for i in block.get("citation_ids", []))`. **O tamanho explícito é obrigatório**: um `<super>` sem `size` sai com 6,8 pt num corpo de 8,5 pt (verificado), abaixo do mínimo de 7,5 pt do design system. No fim do conteúdo, se `content["citations"]` não estiver vazio, uma seção "Fontes" com uma linha por citação: `"<b>{id}</b> — {source_id}"` + `", {locator}"` quando houver.
6. **Cabeçalho** (flowable no topo do conteúdo): `Table` de uma linha `[Paragraph(deliverable_label.upper(), eyebrow), Image(logo)]`, com o logo `ROOT / "assets/logo_ccee.png"` escalado para caber em 38 × 11 mm mantendo proporção (use `reportlab.lib.utils.ImageReader(...).getSize()`), linha inferior 1,5 pt `document_primary`. Depois o título (`Paragraph(content["title"])`) e, se houver, o resumo.
7. **Blocos → flowables** (uma função `block_flowables(block, ...)`):
   - `paragraph` e tipos sem regra própria: `Paragraph(block_text(block))`.
   - `callout`: `Table` de uma célula com fundo `document_deep`, texto `inverse`, `LINEBEFORE` 3 pt `document_accent`.
   - `metric`: `Paragraph` 16 pt negrito `document_primary` sobre `document_accent_soft`.
   - `list`: um `Paragraph` por item com marcador "•" (ou `ListFlowable`).
   - `table`: `headers, rows = table_rows(block)`; `Table([headers] + rows, repeatRows=1)` com colunas de largura igual, células como `Paragraph` 8 pt, cabeçalho `document_primary`/`inverse`, `GRID` 0,75 pt `border`.
   - `heading` e `page_break`: só usados no agrupamento do one-page (não viram flowable próprio).
   - `card_grid`, `image_ref`, `chart`, `canvas`: `Paragraph(block_text(block))` (simplificação aceita nesta prova).
8. **Card (`card_portrait`)**: um único `Frame` dentro das margens, deixando 10 mm livres embaixo para o rodapé. Para blocos cujo `data.section_key` está em `field_labels`, gere a caixa do campo (`Table` de duas linhas: rótulo e texto; `BOX` 0,75 pt `border`, `LINEBEFORE` 3 pt `document_accent`, padding 12 pt) seguida de `Spacer(1, 10)`. Embrulhe **toda** a história em `KeepInFrame(largura, altura, story, mode="error")`.
9. **One-page (`executive_one_page`)**: três `Frame`s na mesma página: cabeçalho de largura total no topo, com altura fixa de 40 mm (conteúdo em `KeepInFrame(..., mode="error")`), e duas colunas iguais abaixo, separadas por 8 pt, deixando 8 mm para o rodapé. História: `[KeepInFrame(cabeçalho), FrameBreak(), *seções]`. Seções agrupadas pela regra de `html_report_blocks` (título do heading ou "Notas"); cada seção é uma `Table` de duas linhas: faixa (`document_deep`, título em maiúsculas Montserrat Bold 9 pt branco) e conteúdo (lista de flowables do Passo 7, corpo 8,5 pt).
10. **Rodapé**: na função `onPage` do `PageTemplate`, `canvas.drawRightString(largura - margem_direita, margem_inferior / 2, footer_label)` em Roboto-Regular 7,5 pt `text_muted`. A mesma função incrementa um contador de páginas (lista mutável).
11. **Build e transbordo**: monte o documento num `io.BytesIO()` com `BaseDocTemplate(buffer, pagesize=..., pageTemplates=[...], title=content["title"], invariant=1)`. Capture `reportlab.platypus.doctemplate.LayoutError` e lance `PdfOverflow(f"{profile['layout']} excedeu uma página; revise ou divida o conteúdo sem reduzir a fonte")`. Se o contador de páginas for maior que 1, lance `PdfOverflow` com a mesma mensagem. **Só** escreva `path.write_bytes(buffer.getvalue())` depois do build sem erro — nunca deixe PDF parcial.

**Verify**:
```
/tmp/venv-032/bin/python -c "
import importlib.util, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('m','_DESIGN_SYSTEM/scripts/pdf_reportlab.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.SUPPORTED_LAYOUTS, issubclass(m.PdfOverflow, ValueError))"
```
→ `('card_portrait', 'executive_one_page') True`

### Step 3: Integrar no `render.py` atrás de `--pdf-engine`

1. Constante perto de `RENDERER_VERSION`: `REPORTLAB_LAYOUTS = ("card_portrait", "executive_one_page")`. Mude `RENDERER_VERSION` para `"1.4.0"`.
2. Argumento: `parser.add_argument("--pdf-engine", choices=("weasyprint", "reportlab"), default="weasyprint", help="motor do PDF; reportlab dispensa Pango (prova: cards e one-page)")`.
3. Logo depois do `if invalid: raise ...` (`render.py:914-916`) e antes de `out.mkdir(...)` (`render.py:918`), para não gravar nenhum arquivo: se `"pdf" in requested and args.pdf_engine == "reportlab" and profile["layout"] not in REPORTLAB_LAYOUTS`, lance `ValueError(f"--pdf-engine reportlab ainda não suporta o layout {profile['layout']}; use weasyprint")`.
4. Função nova em `render.py`, `render_pdf_reportlab(content, tokens, profile, path)`: carrega `ROOT / "scripts/pdf_reportlab.py"` com o padrão `importlib.util` de `render.py:183-188`; monta `footer_label` com a mesma regra de `render.py:589-591`; chama `module.render_pdf(...)` passando `deliverable_label=DELIVERABLE_LABELS[...]`, `field_labels=CARD_LABELS.get(content["deliverable_type"])`, `block_text=block_text`, `table_rows=table_rows`. Para não duplicar a regra do rodapé, extraia-a para `def footer_label(content) -> str` e use-a também em `render_html` (`render.py:589-591`) — a saída do HTML deve ficar idêntica.
5. No bloco de PDF de `main()`, troque só a chamada do motor:
   ```python
           try:
               if args.pdf_engine == "reportlab":
                   render_pdf_reportlab(content, tokens, profile, path)
               else:
                   from weasyprint import HTML
                   HTML(string=source_html or "", base_url=str(ROOT)).write_pdf(str(path))
           except (ImportError, OSError) as exc:
   ```
   Dentro do `except`, mantenha a mensagem atual para `weasyprint` (um teste exige "brew install pango") e, para `reportlab`, use `f"AVISO: PDF não gerado ({unavailable['pdf']}). Instale: pip install reportlab."`. Não capture `PdfOverflow`: ele é `ValueError` e deve encerrar com erro, como hoje.
6. Em `source_html`: com `--pdf-engine reportlab`, o HTML só precisa ser gerado se `"html" in requested` (mude a condição de `render.py:926` para `"html" in requested or ("pdf" in requested and args.pdf_engine == "weasyprint")`).
7. Manifesto: quando o PDF entrar em `files`, acrescente `"pdf_engine": args.pdf_engine` ao dicionário `manifest`; sem PDF, não acrescente a chave.

**Verify**:
```
/tmp/venv-032/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/test_card/input.json --out-dir /tmp/o032 --formats pdf,md --pdf-engine reportlab
/tmp/venv-032/bin/python -c "import pypdf;r=pypdf.PdfReader('/tmp/o032/sample-test-card-v1.0.0.pdf');print(len(r.pages));print('Acreditamos que' in r.pages[0].extract_text())"
grep -c '"pdf_engine": "reportlab"' /tmp/o032/sample-test-card-v1.0.0.manifest.json
```
→ JSON com `"unavailable": {}`; `1`; `True`; `1`.

### Step 4: Provar que funciona sem WeasyPrint

```
mkdir -p /tmp/fake-wp && printf 'raise OSError("pango ausente (simulado)")\n' > /tmp/fake-wp/weasyprint.py
PYTHONPATH=/tmp/fake-wp /tmp/venv-032/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/briefing_one_page/input.json --out-dir /tmp/o032b --formats pdf --pdf-engine reportlab
```
**Verify**: saída com `"unavailable": {}` e o arquivo `/tmp/o032b/sample-briefing-one-page-v1.0.0.pdf` existe. Sem `--pdf-engine reportlab`, o mesmo comando deve continuar produzindo `"unavailable": {"pdf": "OSError: pango ausente (simulado)"}` (comportamento antigo preservado).

### Step 5: Testes

Em `_DESIGN_SYSTEM/tests/test_render.py`, crie `reportlab_available()` (mesmo formato de `pdf_available()`, importando `reportlab`) e a classe `ReportLabPdfTests(unittest.TestCase)` com `@unittest.skipUnless(reportlab_available(), "reportlab indisponível")`. Use `subprocess.run([sys.executable, str(SCRIPT), ..., "--pdf-engine", "reportlab"])` como nos testes existentes. Casos:

1. `test_test_card_sample_one_page_a4_portrait`: amostra `_SAMPLES_ENTREGAVEIS/test_card/input.json` → exit 0; 1 página; largura/altura da `mediabox` convertidas para mm = 210 ± 0,5 e 297 ± 0,5; o texto extraído (normalize espaços com `" ".join(text.split())`) contém o título, os 4 rótulos de `CARD_LABELS["test_card"]`, o texto de cada campo e a `identity_line`.
2. `test_learning_card_footer_links_test_card`: amostra do learning card → 1 página e o texto contém `"Test Card sample-test-card v1.0.0"`.
3. `test_one_page_sample_landscape`: amostra do one-page → 1 página, 297 × 210 mm (± 0,5), texto contém o HMW "Como podemos tornar as solicitações mais claras e rastreáveis?".
4. `test_oversized_card_fails_without_partial_files`: `content("test_card", "TC-big")` com `item["title"] = "Título longo para verificar o limite do card. " * 120` → exit ≠ 0, stderr contém "excedeu uma página", nenhum `.pdf` e nenhum `.manifest.json` na pasta.
5. `test_one_page_overflow_fails`: amostra do one-page com `item["blocks"] = item["blocks"] * 12` (ajuste IDs para ficarem únicos: `{**b, "id": f'{b["id"]}-{i}'}`) → exit ≠ 0, "excedeu uma página", sem `.pdf`. Se a validação do schema recusar a lista repetida, use `completeness: "partial"`; se ainda assim recusar, STOP.
6. `test_works_when_weasyprint_is_broken`: mesmo truque de `test_missing_pdf_backend_still_renders_other_formats` (pasta com `weasyprint.py` que lança `OSError`, no `PYTHONPATH`) → com `--pdf-engine reportlab`, exit 0, `unavailable == {}`, PDF existe.
7. `test_unsupported_layout_rejected_before_writing`: `content("briefing", "BR-1")` com `--formats pdf,md --pdf-engine reportlab` → exit ≠ 0, stderr contém "ainda não suporta", pasta de saída sem nenhum arquivo.
8. `test_deterministic_bytes`: renderizar a amostra do test card duas vezes em pastas diferentes → bytes do PDF idênticos.
9. `test_embeds_static_fonts`: no PDF do test card, os nomes em `/BaseFont` dos recursos de fonte incluem algum que termina em `Montserrat-Bold` e algum que termina em `Roboto-Regular`; nenhum contém `Thin` nem `Variable`.
10. `test_manifest_records_engine`: manifesto com `"pdf_engine": "reportlab"`; e um render sem PDF (`--formats md`) não tem a chave `pdf_engine`.

**Verify**: `/tmp/venv-032/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests/test_render.py -k ReportLab` → `10 passed`. Depois a suíte completa → `0 failed`, e o número de testes que passam é o da linha de base + 10.

### Step 6: Dependência e documentação

- `_DESIGN_SYSTEM/requirements.txt`: acrescente `reportlab==5.0.1` (mesmo estilo de versão exata do arquivo). Não acrescente `fonttools`.
- `_DESIGN_SYSTEM/README.md`, no item 3 (renderização): acrescente uma frase: "`--pdf-engine reportlab` gera o PDF sem Pango, só com `pip install reportlab`; nesta versão vale para Test Card, Learning Card e resumo do briefing (one-page). O padrão continua `weasyprint`." Na lista "Arquivos normativos", mencione `assets/fonts/static/` (instâncias estáticas usadas pelo ReportLab, geradas por `_TOOLS/make_static_fonts.py`).

**Verify**: `grep -c "reportlab==5.0.1" _DESIGN_SYSTEM/requirements.txt` → `1`; `grep -c "pdf-engine reportlab" _DESIGN_SYSTEM/README.md` → `1` ou mais.

### Step 7: Sincronizar para as 11 skills

```
python3 _TOOLS/sync_shared.py
python3 _TOOLS/sync_shared.py --check
python3 _TOOLS/build_sources.py --check
ls */assets/design-system/assets/fonts/static/Roboto-Regular.ttf | wc -l
ls */assets/design-system/scripts/pdf_reportlab.py | wc -l
```
**Verify**: os dois `--check` com exit 0; as duas contagens → `11`. Rode o validador de skills (tabela de comandos) → 11 válidas.

### Step 8: Material para a revisão visual do operador (gate)

Gere, numa pasta fora do repo, os PDFs das 3 amostras com os dois motores (o WeasyPrint só se estiver disponível nesta máquina):
```
for t in test_card learning_card briefing_one_page; do
  /tmp/venv-032/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/$t/input.json --out-dir /tmp/revisao-032/reportlab --formats pdf --pdf-engine reportlab
  /tmp/venv-032/bin/python _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/$t/input.json --out-dir /tmp/revisao-032/weasyprint --formats pdf || true
done
ls /tmp/revisao-032/*/
```
**Verify**: 3 PDFs em `/tmp/revisao-032/reportlab/`. Registre no relatório final os caminhos e se os PDFs do WeasyPrint foram gerados. **Não** decida sozinho se a aparência está aceitável: isso é do operador.

## Test plan

- 10 testes novos em `ReportLabPdfTests` (Passo 5), modelados em `test_missing_pdf_backend_still_renders_other_formats` e `test_card_is_one_page_and_presentation_is_editable`.
- Diferente dos testes de WeasyPrint, estes **rodam sem Pango**: em qualquer máquina com `pip install -r requirements.txt` eles não devem pular.
- Regressão: a suíte completa precisa manter `0 failed`; os testes do caminho WeasyPrint (inclusive "brew install pango" na mensagem) não mudam.

## Done criteria

- [ ] `_DESIGN_SYSTEM/assets/fonts/static/` contém exatamente `Montserrat-Bold.ttf`, `Roboto-Regular.ttf`, `Roboto-Bold.ttf`, com nomes internos corretos (Passo 1)
- [ ] `/tmp/venv-032/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests/test_render.py -k ReportLab` → `10 passed`, nenhum skip
- [ ] Suíte completa → `0 failed`
- [ ] O HTML padrão não mudou: renderize as mesmas duas amostras da linha de base com `--out-dir /tmp/h1 --formats html` e `cmp /tmp/h0/sample-learning-card-v1.0.0.html /tmp/h1/sample-learning-card-v1.0.0.html && cmp /tmp/h0/sample-briefing-one-page-v1.0.0.html /tmp/h1/sample-briefing-one-page-v1.0.0.html` → exit 0
- [ ] `python3 _TOOLS/sync_shared.py --check` e `python3 _TOOLS/build_sources.py --check` → exit 0
- [ ] `grep -n "layout.json\|load_presentation_layout" _DESIGN_SYSTEM/scripts/pdf_reportlab.py` → nenhuma linha
- [ ] `git status` só mostra arquivos da lista "In scope" (mais as cópias do sync)
- [ ] PDFs do Passo 8 gerados e caminhos informados no relatório
- [ ] Linha do Plano 032 em `plans/README.md` atualizada

## STOP conditions

Pare e reporte, sem improvisar, se:

- O trecho de `render.py:932-955` não bater com o "Estado atual" (drift).
- `reportlab==5.0.1` não instalar no ambiente isolado, ou exigir compilação nativa.
- `updateFontNames=True` falhar ou o nome interno da Montserrat sair diferente de `Montserrat-Bold`.
- Algum caractere do português (á, ã, ç, ê, õ, —, ·) sair errado ou ausente no texto extraído do PDF: é exatamente o defeito que eliminou o Chromium.
- O transbordo não gerar erro (PDF com texto sobreposto ou cortado em uma página): é o defeito que bloqueou o Plano 031.
- Fazer passar um teste existente exigiria mudar o caminho WeasyPrint, o HTML ou um teste existente.
- Um passo falhar duas vezes após uma tentativa razoável de correção.

## Maintenance notes

- **Duas implementações de layout**: a partir daqui, mudanças visuais nos cards e no one-page precisam ser feitas no CSS (`render.py`) **e** em `pdf_reportlab.py`. O revisor deve cobrar as duas.
- **Próximo plano (se o operador aprovar a prova)**: estender `pdf_reportlab.py` aos relatórios (fluxo de várias páginas; ver regra de seções) e à apresentação 16:9; depois trocar o padrão de `--pdf-engine` para `reportlab`, atualizar `SKILL.md`/README e tornar o WeasyPrint opcional ou removê-lo.
- **Dependência**: `reportlab` traz `pillow` (wheels binárias para todos os sistemas). Em ambientes compartilhados que já tenham outra versão de `reportlab`, a versão exata pode conflitar; avaliar faixa de versões (`>=5,<6`) quando o ReportLab virar padrão.
- **Fontes**: se as variáveis forem trocadas, rode `_TOOLS/make_static_fonts.py`; o peso 500 do rodapé (`tokens.typography.styles.footer.weight`) é aproximado por Roboto-Regular nesta prova.
- **Tamanho dos pacotes**: as fontes estáticas acrescentam ≈ 0,7 MB a cada uma das 11 skills e aos `.skill` de `_DIST/`.
- **Plano 031**: o ReportLab detecta transbordo por construção (`KeepInFrame` / contagem de páginas), sem depender de `position: absolute`. Se o 031 for retomado, considere implementar os slots de `layout.json` no ReportLab (coordenadas em mm mapeiam direto em `Frame`s) em vez do HTML.
