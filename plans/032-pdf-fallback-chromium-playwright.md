# Plan 032: Chromium (Playwright) como motor de PDF **de reserva**, só quando WeasyPrint/Pango não estiver disponível

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**: `git diff --stat 0278ae7..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/requirements.txt _DESIGN_SYSTEM/tests/test_render.py`
> Se algum arquivo no escopo mudou desde que este plano foi escrito, compare
> os trechos de "Estado atual" abaixo contra o código real antes de prosseguir;
> em caso de divergência, trate como condição de STOP.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: MED
- **Depends on**: none (independente do Plano 031, que está BLOCKED por um motivo não relacionado — posicionamento por `layout.json`, não motor de PDF)
- **Category**: dx + dependências
- **Planned at**: commit `0278ae7`, 2026-10-05

## Por que isso importa — e por que este plano **não** é a substituição total que foi pedida

O operador pediu a implementação da "Opção B" discutida antes: trocar o WeasyPrint por um motor autocontido (Chromium via Playwright), para eliminar a dependência de bibliotecas nativas do sistema (Pango/Cairo/GDK-pixbuf) que hoje tornam o projeto frágil entre máquinas — principalmente Windows, onde instalar WeasyPrint exige o runtime do GTK3 ou MSYS2, um passo manual e uma fonte real de atrito.

**A investigação feita para escrever este plano encontrou um defeito concreto que muda a recomendação.** Rendei o HTML real de `executive_presentation` (gerado por `render_html()`, com as fontes variáveis Montserrat/Roboto incorporadas via `@font-face` em base64, igual ao que roda em produção) através do Playwright/Chromium (`page.pdf(print_background=True, prefer_css_page_size=True)`) e comparei com o PDF equivalente gerado por WeasyPrint:

- **WeasyPrint**: `pdfplumber.extract_words()` lê o título corretamente: `['APRESENTAÇÃO', 'EXEMPLO', 'FICTÍCIO']`.
- **Chromium (Playwright)**: a mesma extração devolve texto corrompido: `['AAAAAAAPPPPPPPRRRRRRREEEEEEESSSSSSSEEEEEEENNNNNNNTTTTTTTAAAAAAAÇÇÇÇÇÇÇÃÃÃÃÃÃÃOOOOOOO', ...]` — cada caractere repetido ~7 vezes. `pdfplumber`/`pdfminer` também emitiram `Could not get FontBBox from font descriptor` repetidamente durante a leitura.

Tirei um screenshot do mesmo HTML renderizado no navegador (não do PDF) e o texto aparece visualmente correto e legível — então **não é um bug visual**, é a camada de texto do PDF (o "text layer" usado por seleção, copiar/colar, leitores de tela e qualquer extração programática de texto) que sai corrompida especificamente quando o Chromium exporta PDF com essas fontes variáveis incorporadas. Esse é exatamente o mecanismo que este projeto usa em `PdfIdempotencyTests` (Plano 028) e em toda a verificação de fidelidade feita nesta sessão — ou seja, **um PDF gerado por Chromium hoje passaria na checagem visual mas falharia silenciosamente em qualquer verificação de texto**, incluindo a futura, se alguém reaproveitar esse padrão para os outros 17 tipos.

Diante disso, **este plano implementa Chromium como motor de reserva (fallback), não substituição**: WeasyPrint continua sendo o motor principal e roda exatamente como hoje em qualquer máquina onde já funciona (nenhuma re-certificação visual dos 18 tipos é necessária, porque a saída deles não muda). O Chromium só entra quando `import weasyprint` falhar (`ImportError`/`OSError` — o mesmo gatilho que hoje produz "PDF indisponível"), dando a uma máquina sem Pango (tipicamente Windows sem o runtime do GTK3) um PDF funcional em vez de nenhum, com a corrupção da camada de texto documentada como limitação conhecida do caminho de reserva — não um bloqueador, mas algo que precisa aparecer no aviso emitido e no manifest, para quem usar esse PDF saber que a camada de texto pode não ser confiável. Investigar a causa raiz (provavelmente relacionada a fontes variáveis — um teste futuro com fontes estáticas, não variáveis, ajudaria a isolar) fica fora de escopo deste plano.

### Evidências adicionais confirmadas nesta sessão (não é suposição)

- Playwright/Chromium **não precisa de Pango**: `import playwright` funciona neste ambiente sem `DYLD_LIBRARY_PATH` nenhum definido (ao contrário de WeasyPrint, que precisa dele aqui). Isso é esperado — Chromium traz seu próprio motor de renderização e não depende de Pango/Cairo do sistema em nenhuma plataforma.
- `page.pdf(print_background=True, prefer_css_page_size=True)` respeita o `@page { size: ...; margin: ...; }` do CSS deste projeto: testei com `briefing_one_page` (perfil `a4_landscape`) e o PDF saiu com 297.0mm × 209.9mm (esperado 297×210mm, diferença de 0.1mm por arredondamento interno do Chromium — não é um bug, é esperado) e exatamente 1 página.
- Testei também `executive_presentation` (perfil `presentation_16_9`, usa o branch `"presentation"` de `render_html`, já mesclado via Plano 030, com `position:absolute`/`@page margin:0`): saiu com 338.7mm × 190.5mm e 2 páginas (slide de título + 1 seção de conteúdo), consistente com o esperado para essa amostra.
- `pypdf.PdfReader` lê normalmente um PDF gerado por Chromium (confirmado via os dois testes acima) — a checagem de página única em `render.py:946-954` (`profile["layout"] in ("executive_one_page", "card_portrait")`) deve continuar funcionando sem alteração.
- Tamanho real do binário do Chromium baixado por `playwright install chromium` nesta máquina: 359MB (`~/Library/Caches/ms-playwright/chromium-<rev>`). Isso é por máquina, uma vez só (cache), não por execução.
- `playwright==1.63.0` foi a versão instalada ao rodar `pip install playwright` nesta sessão (sem pin explícito — decida se quer fixar essa versão exata no `requirements.txt`, mesmo padrão de pin estrito que o resto do arquivo já usa para `weasyprint`/`pydyf`/etc.).

## Estado atual

### 1. Onde o PDF é gerado hoje (`_DESIGN_SYSTEM/scripts/render.py:932-955`)

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

Esse bloco inteiro fica dentro de `main()` (não é uma função separada hoje — `render_html`/`render_docx`/`render_pptx`/`render_md` são funções, mas a geração de PDF é inline em `main`). **Este plano extrai essa lógica para uma função nova** (ex: `render_pdf(source_html: str, path: Path) -> str` — devolve o nome do motor usado, ex: `"weasyprint"` ou `"chromium"`, ou levanta exceção se nenhum funcionar), para poder tentar WeasyPrint e cair para Chromium sem duplicar a estrutura `try/except` e a checagem de página única.

### 2. `pdf_available()` em `_DESIGN_SYSTEM/tests/test_render.py:32-37`

```python
def pdf_available() -> bool:
    try:
        import weasyprint
        return True
    except (ImportError, OSError):
        return False
```

Usado como guarda de `@unittest.skipUnless(pdf_available(), ...)` em 4 lugares (linhas 409, 427, 449, 545) e checado diretamente em outros 5 (linhas 215, 657, 733, 742, 822, 984) para decidir se `pdf` entra na lista de formatos testados. **Depois deste plano, `pdf_available()` continua testando só WeasyPrint** (não precisa saber sobre Chromium) — os testes existentes continuam cobrindo o caminho principal exatamente como hoje. Um teste **novo**, separado, cobre o caminho de reserva via Chromium (Passo 4 abaixo), gated por uma função nova `chromium_available()`.

### 3. `_DESIGN_SYSTEM/requirements.txt` (atual, completo)

```
jsonschema==4.26.0
referencing==0.36.2
weasyprint==61.2
pydyf==0.10.0
python-docx==1.1.2
python-pptx==1.0.2
pypdf==5.9.0
```

### 4. Plano 031 — fora de escopo, não mexa

`plans/031-render-html-offset-fix-e-one-page-card-layout-json.md` está **BLOCKED** (ver `plans/README.md`) por uma regressão real no posicionamento `position:absolute`/`layout.json` de `render_html`, nada a ver com qual motor converte HTML→PDF. Este plano 032 não desbloqueia, não reavalia e não depende do 031. Se notar que a saída do Chromium para os tipos afetados pelo Plano 030 (`executive_presentation`, branch `"presentation"`) difere visualmente do WeasyPrint além do já documentado (corrupção da camada de texto), registre como nota, não tente corrigir aqui.

## Comandos que você vai precisar

| Propósito | Comando | Esperado no sucesso |
|---|---|---|
| Instalar Playwright | `pip install playwright` (a partir de `_DESIGN_SYSTEM/`, no ambiente usado para testar) | instala sem erro |
| Baixar o Chromium | `playwright install chromium` | baixa ~360MB (uma vez, fica em cache); sem erro |
| Testes (sem Pango/PDF via WeasyPrint) | `python3 tests/test_render.py` (rodar o arquivo direto, NÃO `python3 -m unittest tests.test_render` — colide com um pacote `tests` do Anaconda no `site-packages`) | todos passam; skips de WeasyPrint continuam esperados se Pango não estiver disponível no ambiente |
| Sync para as 11 skills | `python3 ../_TOOLS/sync_shared.py` (a partir de `_DESIGN_SYSTEM/`) depois `python3 ../_TOOLS/sync_shared.py --check` | segundo comando sai com código 0 |

**Importante sobre este ambiente de execução específico**: Pango está instalado (Homebrew) mas só é encontrado com `DYLD_LIBRARY_PATH=/opt/homebrew/lib` definido manualmente, e há um conflito de versão entre `pydyf` instalado globalmente e o pinado em `requirements.txt` que quebra o WeasyPrint nesta máquina fora de um ambiente isolado com as versões corretas. Isso é um problema de ambiente local, não deste plano — **não tente corrigir isso como parte da execução**. Rode os testes que dependem de WeasyPrint só se `pdf_available()` já der `True` naturalmente no seu ambiente; trate skips como esperados, não como falha. Chromium/Playwright, ao contrário, não deveria precisar de nenhuma dessas variáveis — se precisar, isso é uma descoberta nova, pare e reporte.

## Escopo

**Em escopo** (únicos arquivos a modificar):
- `_DESIGN_SYSTEM/scripts/render.py` — extrai a geração de PDF de `main()` para uma função `render_pdf()`, adiciona a tentativa de fallback via Chromium.
- `_DESIGN_SYSTEM/requirements.txt` — adiciona `playwright`.
- `_DESIGN_SYSTEM/tests/test_render.py` — novos testes, nova função `chromium_available()`.
- `_DESIGN_SYSTEM/README.md` — documenta o novo passo de instalação (`playwright install chromium`) e o comportamento de fallback.

**Fora de escopo** (não toque, mesmo parecendo relacionado):
- `render_html`, `render_docx`, `render_pptx`, `render_md` — nenhuma dessas funções muda; elas continuam gerando a MESMA string/arquivo de entrada que hoje é passada para o WeasyPrint. Este plano só muda o que acontece depois (qual motor converte HTML→PDF), nunca o HTML/CSS em si.
- O Plano 031 e qualquer coisa em `_DESIGN_SYSTEM/layouts/` — não relacionado.
- `_LAYOUT_STUDIO/` — não relacionado.
- Investigar ou corrigir a corrupção da camada de texto do Chromium com fontes variáveis — documentada como limitação conhecida (ver "Por que isso importa"), não corrigida aqui. Se quiser investigar depois, a hipótese mais provável é trocar `Montserrat-Variable.ttf`/`Roboto-Variable.ttf` por instâncias estáticas (um arquivo por peso) só no caminho do Chromium, para isolar se o problema é a variação de peso dentro de um único arquivo de fonte.
- Trocar o motor principal de WeasyPrint para Chromium — explicitamente rejeitado por este plano (ver "Por que isso importa"). Se o operador quiser isso mesmo assim depois de ler a limitação encontrada, é uma decisão para uma conversa separada, não uma correção deste plano.

## Git workflow

- Branch: `advisor/032-pdf-fallback-chromium`
- Um commit por etapa lógica, seguindo o padrão observado em `git log` (mensagens curtas, imperativas, em português, sem prefixo de tipo).
- Não dê push nem abra PR a menos que instruído.

## Passos

### Passo 1: Extrai a geração de PDF para uma função `render_pdf()`

Em `_DESIGN_SYSTEM/scripts/render.py`, adicione uma função nova (perto das outras funções `render_*`, ex: depois de `render_md`):

```python
class PdfUnavailable(Exception):
    """Nenhum motor de PDF disponível (nem WeasyPrint, nem Chromium)."""


def render_pdf(source_html: str, path: Path) -> str:
    """Gera o PDF em `path` a partir de `source_html`. Tenta WeasyPrint
    primeiro (motor principal, mantém a fidelidade visual já validada nos
    Planos 027/028); cai para Chromium via Playwright só se WeasyPrint não
    estiver disponível (import falha por biblioteca nativa ausente, ex:
    Pango no Windows sem runtime do GTK3). Devolve o nome do motor usado
    ("weasyprint" ou "chromium"). Levanta PdfUnavailable se nenhum funcionar.

    Limitação conhecida do caminho Chromium: a camada de texto do PDF sai
    corrompida com as fontes variáveis deste projeto (confirmado nesta
    sessão: texto duplicado letra a letra ao extrair com pdfplumber, embora
    o visual renderizado esteja correto) -- ver Plano 032. O PDF ainda é
    visualmente válido e a checagem de página única (abaixo, em main())
    continua funcionando, mas texto extraído/selecionado desse PDF não é
    confiável."""
    try:
        from weasyprint import HTML
        HTML(string=source_html or "", base_url=str(ROOT)).write_pdf(str(path))
        return "weasyprint"
    except (ImportError, OSError) as weasyprint_exc:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise PdfUnavailable(f"weasyprint: {weasyprint_exc}") from exc
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                # base_url equivalente: WeasyPrint recebe base_url=ROOT para resolver
                # recursos relativos; aqui escrevemos um arquivo temporário e navegamos
                # via file:// a partir de ROOT, para manter o mesmo comportamento de
                # resolução de caminhos relativos (fontes/imagens já vêm embutidas em
                # base64 no HTML gerado por render_html, então isso raramente importa,
                # mas mantenha para não divergir silenciosamente se algo mudar).
                tmp_html = path.with_suffix(".tmp.html")
                tmp_html.write_text(source_html or "", encoding="utf-8")
                try:
                    page.goto(f"file://{tmp_html.resolve()}")
                    page.pdf(path=str(path), print_background=True, prefer_css_page_size=True)
                finally:
                    tmp_html.unlink(missing_ok=True)
                browser.close()
            return "chromium"
        except Exception as chromium_exc:
            raise PdfUnavailable(f"weasyprint: {weasyprint_exc} | chromium: {chromium_exc}") from chromium_exc
```

**Verify**: `python3 -c "import ast; ast.parse(open('scripts/render.py').read())"` → sem `SyntaxError` (checagem rápida antes de integrar).

### Passo 2: Troca o bloco inline em `main()` para usar `render_pdf()`

Troque o bloco citado em "Estado atual" item 1 por:

```python
unavailable: dict[str, str] = {}
if "pdf" in requested:
    path = out / f"{stem}.pdf"
    try:
        engine = render_pdf(source_html or "", path)
    except PdfUnavailable as exc:
        import sys

        path.unlink(missing_ok=True)
        unavailable["pdf"] = str(exc)[:300]
        print(f"AVISO: PDF não gerado ({unavailable['pdf']}). No macOS: brew install pango; "
              "no Debian/Ubuntu: apt-get install libpango-1.0-0 libpangoft2-1.0-0; "
              "ou instale o motor de reserva: pip install playwright && playwright install chromium.",
              file=sys.stderr)
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
        if engine == "chromium":
            print("AVISO: PDF gerado com motor de reserva (Chromium/Playwright) — "
                  "WeasyPrint indisponível neste ambiente. A camada de texto deste PDF "
                  "pode estar corrompida (ver Plano 032); o conteúdo visual é confiável.",
                  file=sys.stderr)
        files.append(path)
```

Note que `engine` precisa ficar registrado em algum lugar visível além do stderr, para rastreabilidade — decida se adiciona um campo `"pdf_engine": engine` no manifest (procure onde o manifest é montado em `main()`, provavelmente logo depois deste bloco ou no fim da função) **só quando `"pdf" in files`** (não adicione a chave quando PDF não foi gerado). Siga o padrão de nomes de chave já usado no manifest existente (leia como as outras chaves são montadas antes de decidir o nome exato).

**Verify**: a partir de `_DESIGN_SYSTEM/`, com WeasyPrint disponível no seu ambiente:
```bash
python3 scripts/render.py ../_SAMPLES_ENTREGAVEIS/briefing_one_page/input.json --out-dir /tmp/plan032-verify --formats pdf
python3 -c "import json; m = json.load(open('/tmp/plan032-verify/sample-briefing-one-page-v1.0.0.manifest.json')); print(m.get('pdf_engine'))"
```
Esperado: imprime `weasyprint` (ou o nome de chave que você escolheu — ajuste o comando de verificação de acordo, mas documente no commit qual chave usou).

### Passo 3: Simula "WeasyPrint indisponível" para provar que o fallback funciona

Use `unittest.mock.patch` para forçar a branch de exceção sem precisar desinstalar WeasyPrint de verdade. Em `_DESIGN_SYSTEM/tests/test_render.py`, adicione (próximo a outros testes de `render.py`, seguindo o padrão de `load_render_module()` já usado por `PresentationLayoutJsonTests`):

```python
def chromium_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:
        return False


class ChromiumPdfFallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render = load_render_module()

    @unittest.skipUnless(chromium_available(), "Playwright/Chromium indisponível")
    def test_falls_back_to_chromium_when_weasyprint_unavailable(self):
        content_doc = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_one_page/input.json").read_text(encoding="utf-8"))
        tokens = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))
        profile = json.loads((ROOT / "profiles.json").read_text(encoding="utf-8"))["types"]["briefing_one_page"]
        html_out = self.render.render_html(content_doc, tokens, profile)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.pdf"
            with unittest.mock.patch("builtins.__import__", side_effect=_block_weasyprint_import):
                engine = self.render.render_pdf(html_out, path)
            self.assertEqual(engine, "chromium")
            self.assertTrue(path.is_file())
            from pypdf import PdfReader
            self.assertGreaterEqual(len(PdfReader(str(path)).pages), 1)

    @unittest.skipUnless(chromium_available(), "Playwright/Chromium indisponível")
    def test_single_page_check_still_works_with_chromium(self):
        # mesmo cenário de test_oversized_card_remains_fatal (RenderTests), mas
        # forçando o caminho Chromium -- confirma que pypdf consegue ler um PDF
        # gerado por Chromium para a checagem de página única do main().
        content_doc = json.loads((ROOT.parent / "_SAMPLES_ENTREGAVEIS/test_card/input.json").read_text(encoding="utf-8"))
        tokens = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))
        profile = json.loads((ROOT / "profiles.json").read_text(encoding="utf-8"))["types"]["test_card"]
        html_out = self.render.render_html(content_doc, tokens, profile)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.pdf"
            with unittest.mock.patch("builtins.__import__", side_effect=_block_weasyprint_import):
                self.render.render_pdf(html_out, path)
            from pypdf import PdfReader
            self.assertEqual(len(PdfReader(str(path)).pages), 1)


_real_import = __import__


def _block_weasyprint_import(name, *args, **kwargs):
    if name == "weasyprint":
        raise ImportError("bloqueado pelo teste para simular ambiente sem WeasyPrint")
    return _real_import(name, *args, **kwargs)
```

Isso exige `import tempfile` e `from pathlib import Path` já presentes em `test_render.py` (confira — provavelmente já estão, dado o uso de `tempfile.TemporaryDirectory()` em outros testes como `test_oversized_card_remains_fatal`). Se `unittest.mock.patch("builtins.__import__", ...)` se mostrar instável (pode interferir com imports de outras bibliotecas durante o teste), use uma abordagem mais cirúrgica: `unittest.mock.patch.object(self.render, "render_pdf", wraps=...)` não serve aqui porque o objetivo é testar `render_pdf` de verdade — considere em vez disso mockar especificamente `weasyprint.HTML` para levantar a exceção, ou renomear a importação dentro de `render_pdf` para facilitar o mock (ex: `import weasyprint as _weasyprint_module` no topo do arquivo, e mockar isso) — decida a forma mais limpa e documente a escolha no commit.

**Verify**: `python3 tests/test_render.py -v ChromiumPdfFallbackTests` → `OK` (ou `skipped` se Playwright/Chromium não estiver instalado no ambiente — não é falha).

### Passo 4: Atualiza `requirements.txt`

```
jsonschema==4.26.0
referencing==0.36.2
weasyprint==61.2
pydyf==0.10.0
python-docx==1.1.2
python-pptx==1.0.2
pypdf==5.9.0
playwright==1.63.0
```

(Confirme a versão exata do Playwright no momento da execução — `pip index versions playwright` ou `pip show playwright` depois de instalar — e ajuste se uma versão mais nova já tiver saído; não precisa ser exatamente `1.63.0`, só precisa ser pinada, seguindo o padrão do resto do arquivo.)

**Verify**: `pip install -r requirements.txt && playwright install chromium` → sem erro.

### Passo 5: Documenta no README

Em `_DESIGN_SYSTEM/README.md`, ache a seção que hoje documenta a instalação/dependências (ou o aviso sobre Pango/WeasyPrint, citado no erro: "No macOS: brew install pango; no Debian/Ubuntu: apt-get install..."). Adicione uma nota explícita:

> Geração de PDF: o motor principal é WeasyPrint (requer Pango/Cairo/GDK-pixbuf do sistema — ver instruções de instalação por SO). Se WeasyPrint não estiver disponível (comum no Windows sem o runtime do GTK3), `render.py` cai automaticamente para Chromium via Playwright (`pip install playwright && playwright install chromium`, baixa ~360MB uma vez). **Limitação conhecida do caminho Chromium**: a camada de texto do PDF gerado por ele pode sair corrompida com as fontes variáveis deste projeto (o PDF continua visualmente correto; texto extraído/copiado dele não é confiável) — ver Plano 032 para os detalhes.

**Verify**: leitura manual — confirme que a nota está no README e é encontrável por quem for instalar o projeto pela primeira vez.

### Passo 6: Suíte completa + sync

```bash
cd _DESIGN_SYSTEM
python3 tests/test_render.py
python3 ../_TOOLS/sync_shared.py
python3 ../_TOOLS/sync_shared.py --check
```
**Verify**: primeiro comando sai OK (skips de WeasyPrint e/ou Chromium são aceitáveis se nenhum dos dois estiver disponível no seu ambiente — mas pelo menos um dos dois precisa estar disponível para você verificar de verdade que o fallback funciona; se nenhum estiver, PARE e reporte, porque este plano não pode ser verificado sem pelo menos um motor de PDF funcionando). Segundo comando roda sem erro. Terceiro sai com código 0.

## Plano de testes

- `ChromiumPdfFallbackTests.test_falls_back_to_chromium_when_weasyprint_unavailable` (Passo 3) — prova que o fallback dispara e produz um PDF válido quando WeasyPrint está bloqueado.
- `ChromiumPdfFallbackTests.test_single_page_check_still_works_with_chromium` (Passo 3) — prova que a checagem de página única (`render.py:946-954`, não modificada) continua funcionando com um PDF gerado por Chromium.
- Todos os testes existentes que usam `pdf_available()` continuam cobrindo o caminho WeasyPrint sem alteração — não precisam de mudança, porque `render_pdf()` tenta WeasyPrint primeiro e só cai para Chromium se ele faltar.
- Verificação: `python3 tests/test_render.py` → todos os testes passam (skips de PDF são aceitáveis só se NENHUM motor estiver disponível no ambiente).

## Done criteria

Todas devem valer:

- [ ] `python3 tests/test_render.py` sai OK
- [ ] `ChromiumPdfFallbackTests` passa (não só "skipped") em pelo menos um ambiente com Playwright/Chromium instalado, confirmando o fallback de verdade
- [ ] Gerar um PDF com WeasyPrint disponível produz `pdf_engine` (ou a chave escolhida) `"weasyprint"` no manifest
- [ ] Gerar um PDF com WeasyPrint bloqueado (mock) e Chromium disponível produz `pdf_engine` `"chromium"` no manifest E imprime o aviso de limitação da camada de texto em stderr
- [ ] `render_html`, `render_docx`, `render_pptx`, `render_md` não foram modificadas (`git diff` confirma)
- [ ] `_DESIGN_SYSTEM/README.md` documenta o passo `playwright install chromium` e a limitação conhecida
- [ ] `python3 ../_TOOLS/sync_shared.py --check` sai com código 0
- [ ] Nenhum arquivo fora do escopo foi modificado
- [ ] `plans/README.md` com a linha de status deste plano atualizada

## STOP conditions

Pare e reporte (não improvise) se:

- O código em `render.py`/`test_render.py` nas linhas citadas não bater com os trechos de "Estado atual" (drift desde que este plano foi escrito).
- Nem WeasyPrint nem Chromium funcionarem no seu ambiente de execução — você não consegue verificar nenhum dos dois caminhos de verdade; não finja que passou.
- `playwright install chromium` falhar por motivo de rede/ambiente (ex: firewall bloqueando o download) — isso não é algo para contornar, é uma condição real do ambiente de execução; reporte e pare.
- Você encontrar que a corrupção da camada de texto também afeta a checagem de página única de alguma forma (ex: `pypdf.PdfReader` lançar exceção ao abrir um PDF gerado por Chromium, não só retornar texto errado) — isso seria mais grave do que o confirmado nesta sessão e precisa ser investigado antes de prosseguir, não contornado.
- Um teste de verificação falhar duas vezes após uma tentativa razoável de ajuste.

## Notas de manutenção

- Se no futuro alguém quiser investigar a corrupção da camada de texto do Chromium, o ponto de partida mais plausível é testar com fontes estáticas (um arquivo `.ttf` por peso) em vez de `Montserrat-Variable.ttf`/`Roboto-Variable.ttf`, só no caminho Chromium — comparar antes/depois com `pdfplumber.extract_words()` no mesmo HTML.
- Se o operador decidir mais adiante que quer promover Chromium a motor principal (não mais fallback), isso exige uma re-certificação visual completa dos 18 tipos que geram PDF — não é uma extensão trivial deste plano, é um plano novo e maior, com a decisão explícita do operador documentada.
- `pdf_engine` no manifest (ou a chave escolhida no Passo 2) é um precedente novo — se outro plano futuro adicionar mais formatos/motores alternativos (ex: um motor de DOCX alternativo), considere seguir o mesmo padrão de registrar proveniência.
- Revisor: confira que `render_pdf()` realmente tenta WeasyPrint **primeiro** em todos os casos — a ordem importa para não regredir a fidelidade visual já validada em máquinas onde WeasyPrint funciona.
