# Problema em aberto: motor de geração de PDF não é portátil entre ambientes

> Este documento resume um problema real, não resolvido, encontrado numa sessão de
> trabalho no repositório `my_skills` (design system `_DESIGN_SYSTEM/`). É escrito para
> ser lido por outra IA/sessão sem nenhum contexto da conversa original — todas as
> evidências citadas foram verificadas de fato (comandos rodados, resultados reais), não
> são suposições. Onde algo não foi verificado, isso está dito explicitamente.
>
> **Commit em que este documento foi escrito**: `8472652` (branch `main`).

## Resumo do problema

`_DESIGN_SYSTEM/scripts/render.py` gera PDF a partir de HTML usando **WeasyPrint**, que
por sua vez depende de **Pango/Cairo/GDK-pixbuf** — bibliotecas nativas do sistema
operacional, não pacotes Python puros. Isso torna a geração de PDF frágil e inconsistente
entre máquinas/ambientes diferentes. O objetivo é ter geração de PDF confiável em pelo
menos dois ambientes-alvo (ver seção "Pergunta em aberto" abaixo — os ambientes exatos
ainda não estão bem definidos):

1. **Claude Code rodando num Mac** (ambiente de desenvolvimento local, já testado nesta
   sessão).
2. **"Claude Web"** — mencionado pelo operador como alvo, mas **não especificado com
   precisão** nesta sessão. Pode significar coisas bem diferentes (ver seção final).

## Onde o código vive

```python
# _DESIGN_SYSTEM/scripts/render.py, dentro de main(), linhas ~932-955 (commit 8472652)
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
            from pypdf import PdfReader
            count = len(PdfReader(str(path)).pages)
            if count != 1:
                path.unlink(missing_ok=True)
                raise ValueError(f"{profile['layout']} excedeu uma página ({count}); revise ou divida o conteúdo sem reduzir a fonte")
        files.append(path)
```

`_DESIGN_SYSTEM/requirements.txt` (pins exatos, commit `8472652`):
```
jsonschema==4.26.0
referencing==0.36.2
weasyprint==61.2
pydyf==0.10.0
python-docx==1.1.2
python-pptx==1.0.2
pypdf==5.9.0
```

O código já trata a ausência de PDF graciosamente (não quebra o pipeline — produz os
outros formatos e marca `pdf` como indisponível no manifest/stderr). O problema não é
"o programa quebra"; é "o PDF, que é um formato de entrega real deste sistema, não sai em
várias máquinas sem intervenção manual".

## Problemas concretos encontrados e verificados nesta sessão

### 1. Pango "ausente" mesmo quando instalado (macOS, Homebrew)

Nesta máquina (macOS, Python do Anaconda em `/opt/anaconda3/bin/python3`), `import
weasyprint` falhava com:
```
OSError: cannot load library 'pango-1.0-0': dlopen(pango-1.0-0, 0x0002): tried:
'pango-1.0-0' (no such file), ... '/opt/anaconda3/bin/../lib/pango-1.0-0' (no such file),
'/usr/lib/pango-1.0-0' (no such file, not in dyld cache), ...
```
Mas o Pango **já estava instalado** via Homebrew:
```
$ brew list pango
/opt/homebrew/Cellar/pango/1.58.2/...
/opt/homebrew/lib/libpango-1.0.dylib
```
O problema é que `/opt/homebrew/lib` não está no caminho de busca de bibliotecas
dinâmicas do processo Python (que roda via Anaconda). A correção verificada:
```
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 -c "import weasyprint; print('OK')"
# -> OK
```
**Isso não é um problema do WeasyPrint nem do Pango — é puramente uma questão de
`DYLD_LIBRARY_PATH` não incluir o prefixo do Homebrew.** Resolvido manualmente nesta
sessão, não corrigido no código do projeto.

### 2. Conflito de versão `pydyf` quebra o WeasyPrint nesta máquina, mesmo com Pango achado

Mesmo com `DYLD_LIBRARY_PATH` correto, a geração de PDF falhava com:
```
TypeError: PDF.__init__() takes 1 positional argument but 3 were given
```
Causa raiz confirmada: a versão de `pydyf` **instalada globalmente** nesta máquina é
`0.12.1`, mas o `requirements.txt` do projeto pina `pydyf==0.10.0` — e a API do
`pydyf.PDF.__init__()` mudou de forma incompatível entre essas versões. O projeto nunca
foi instalado via `pip install -r requirements.txt` num ambiente isolado nesta máquina;
o Python usado tinha uma versão mais nova de `pydyf` de alguma outra instalação.

Correção verificada: criar um `venv` isolado e instalar exatamente
`requirements.txt` resolve (`pydyf==0.10.0` + `weasyprint==61.2` juntos funcionam, com
`DYLD_LIBRARY_PATH` setado). **Isso é uma falha de isolamento de ambiente, não um bug no
código do projeto** — mas evidencia como é fácil este projeto ficar com geração de PDF
quebrada em qualquer máquina que não siga `requirements.txt` à risca num ambiente limpo.

### 3. Alternativa investigada (Chromium via Playwright) tem um defeito sério: camada de texto do PDF corrompida

Para tentar eliminar a dependência de biblioteca nativa do sistema por completo, foi
testado substituir/complementar o WeasyPrint por **Playwright + Chromium**
(`page.pdf(print_background=True, prefer_css_page_size=True)`), que não depende de
Pango/Cairo (confirmado: `import playwright` funciona sem `DYLD_LIBRARY_PATH`).

**O que funciona bem:**
- Respeita `@page { size: ...; margin: ... }` do CSS deste projeto (testado com
  `briefing_one_page`, perfil `a4_landscape`: saída 297.0mm × 209.9mm, 1 página —
  esperado 297×210mm, a diferença de 0.1mm é arredondamento interno do Chromium).
- `pypdf.PdfReader` consegue ler o PDF gerado normalmente (a checagem de "página única"
  do projeto, `render.py:946-954`, continua funcionando).
- Testado também com `executive_presentation` (perfil `presentation_16_9`): 338.7mm ×
  190.5mm, 2 páginas, como esperado para a amostra usada.

**O que não funciona — achado concreto, verificado, não é suposição:**

O HTML deste projeto incorpora fontes variáveis (`Montserrat-Variable.ttf`,
`Roboto-Variable.ttf`) via `@font-face` em base64 (ver `_DESIGN_SYSTEM/scripts/render.py`,
função `css()`). Ao gerar PDF desse HTML via Chromium, a **camada de texto** do PDF
resultante sai corrompida:

```python
# WeasyPrint, mesma amostra (executive_presentation):
pdfplumber.extract_words() -> ['APRESENTAÇÃO', 'EXEMPLO', 'FICTÍCIO']

# Chromium/Playwright, mesmo HTML de entrada:
pdfplumber.extract_words() -> ['AAAAAAAPPPPPPPRRRRRRREEEEEEESSSSSSSEEEEEEENNNNNNNTTTTTTTAAAAAAAÇÇÇÇÇÇÇÃÃÃÃÃÃÃOOOOOOO', ...]
```

Cada caractere do título aparece repetido ~7 vezes na camada de texto. `pdfminer`/
`pdfplumber` também emitiram repetidamente `Could not get FontBBox from font descriptor`
ao ler esse PDF.

Um screenshot do **mesmo HTML renderizado no navegador** (não o PDF, a página web em si)
mostra o texto visualmente correto e legível — ou seja, **não é um bug visual**. É
especificamente a exportação para PDF do Chromium que corrompe a camada de texto quando
há fontes variáveis incorporadas. Hipótese não testada: pode estar relacionada a como o
Chromium subsetiza/instancia fontes variáveis (`font-weight: 100 900` num único arquivo)
ao converter para PDF — trocar por fontes estáticas (um arquivo por peso) no lugar das
variáveis poderia isolar/resolver isso, mas **isso não foi testado nesta sessão**.

**Por que isso importa**: um PDF com camada de texto corrompida parece correto a olho nu
mas falha silenciosamente em qualquer uso que dependa de extrair/selecionar/copiar texto
— incluindo os próprios testes de fidelidade que este projeto já tem (`_DESIGN_SYSTEM/
tests/test_render.py`, testes de idempotência que comparam texto extraído de PDFs
gerados em execuções diferentes). Um plano (`plans/032-pdf-fallback-chromium-playwright.md`)
foi escrito propondo Chromium como motor de **reserva** (só quando WeasyPrint falhar), não
substituição — mas o operador rejeitou essa proposta porque, se o texto sai corrompido,
não resolve o caso de uso real (ex: Windows sem WeasyPrint recebendo um PDF "funcional"
mas com texto quebrado não é uma solução aceitável).

## O que já está documentado/decidido no projeto sobre este assunto

- `plans/032-pdf-fallback-chromium-playwright.md` — plano escrito, **rejeitado pelo
  operador** pelo motivo acima. Contém o passo a passo de como a tentativa de fallback
  foi desenhada (útil como referência do que já foi tentado, não como solução pronta).
- `plans/031-render-html-offset-fix-e-one-page-card-layout-json.md` — **BLOCKED**, mas é
  um problema **diferente e não relacionado**: posicionamento `position:absolute` dentro
  do HTML via `layout.json`, não o motor que converte HTML→PDF. Não confundir os dois.
- `_DESIGN_SYSTEM/README.md` e o próprio aviso em `render.py` já orientam `brew install
  pango` (macOS) / `apt-get install libpango-1.0-0 libpangoft2-1.0-0` (Debian/Ubuntu) —
  mas **não há nenhuma orientação para Windows** no código ou documentação atual, e
  WeasyPrint no Windows exige o runtime do GTK3 ou MSYS2 — historicamente uma fonte
  conhecida de atrito para esse motor nessa plataforma (fama bem documentada no
  ecossistema WeasyPrint, não específica deste projeto).

## Pergunta em aberto — não resolvida nesta sessão, provavelmente o ponto de partida

O operador mencionou dois ambientes-alvo: **"Claude Web"** e **"Claude Code no Mac"**.
O segundo é razoavelmente claro (confirmado nesta sessão: funciona com os dois ajustes
da seção 1 e 2 acima). O primeiro **não foi esclarecido** — a pergunta de clarificação
feita ao operador sobre o que exatamente significa "Claude Web" foi interrompida antes de
uma resposta, então **isso permanece desconhecido e não deve ser assumido**. Possibilidades
que mudam a solução de forma significativa:

1. **O sandbox de execução de código do claude.ai** (ferramenta de Analysis/code
   execution que roda Python/Bash num container controlado pela Anthropic quando uma
   skill é acionada numa conversa no navegador). Se for isso: esse ambiente provavelmente
   **não tem acesso de rede irrestrito** para baixar os ~360MB do binário do Chromium via
   `playwright install chromium`, e não é claro se há permissão para `apt-get
   install`/instalar bibliotecas de sistema arbitrárias, nem é garantido que o container
   persista pacotes instalados entre execuções. **Isso precisa ser pesquisado/confirmado
   antes de assumir qualquer solução baseada em instalar algo nesse ambiente** — a
   abordagem pode precisar ser radicalmente diferente (ex: um motor 100% Python puro sem
   nenhuma dependência nativa, mesmo que com suporte a CSS mais limitado; ou gerar o PDF
   fora desse sandbox e só consumi-lo pronto).
2. **A ferramenta de code execution hospedada da API/Claude Agent SDK** — ambiente
   diferente do anterior, com suas próprias restrições (também não pesquisado aqui).
3. **Simplesmente alguém usando o claude.ai no navegador** sem execução de código
   automática — nesse caso o problema pode nem ser "qual motor de PDF rodar", mas outra
   coisa inteiramente (ex: como entregar o arquivo). Não investigado.

**Recomendação para quem continuar este trabalho**: antes de propor qualquer solução
técnica nova, esclarecer com o operador exatamente qual é o ambiente "Claude Web" (as
três opções acima, ou outra) — a resposta muda completamente o espaço de soluções
viáveis. Depois disso, as linhas de investigação mais promissoras parecem ser, em ordem
de risco crescente:

- Isolar e corrigir a causa raiz da corrupção de fontes variáveis no Chromium (testar
  fontes estáticas em vez de variáveis só no caminho de exportação para PDF) — se
  resolver, reabre a opção de Chromium como motor único, inclusive no "Claude Web" se
  esse ambiente permitir instalar o binário do Chromium.
- Pesquisar motores de PDF/HTML→PDF que sejam Python puro (sem biblioteca nativa do
  sistema) — nenhum foi pesquisado nesta sessão; vale investigar antes de assumir que não
  existe opção viável.
- Corrigir a instalação/empacotamento deste projeto para sempre instalar
  `requirements.txt` num ambiente isolado com as versões exatas pinadas (resolveria o
  problema 2 acima de forma sistemática, reduzindo a fragilidade mesmo mantendo
  WeasyPrint como motor único) — não resolve Windows nem o ambiente desconhecido do
  "Claude Web", mas é uma correção de higiene de dependências independente de qualquer
  outra decisão.
