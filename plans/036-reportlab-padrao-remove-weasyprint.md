# Plan 036: Tornar o ReportLab o motor único de PDF e remover WeasyPrint, Pango e `pydyf`

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat 8472652..HEAD -- _DESIGN_SYSTEM _TOOLS _SAMPLES_ENTREGAVEIS`
> Os Planos 032–035 terão mudado esses caminhos. Confira que o que eles
> descrevem está presente (`pdf_reportlab.py` cobrindo os 5 layouts, portão
> `pdf_quality.py`, `--pdf-engine`); qualquer outra divergência é STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (muda o padrão de todos os PDFs; aprovado tipo a tipo nos gates dos Planos 032–035)
- **Depends on**: `plans/035-apresentacao-executiva-soap.md` DONE, com as aprovações visuais do operador registradas nos Planos 032, 034 e 035.
- **Category**: dependências / portabilidade
- **Planned at**: commit `8472652`, 2026-10-05

## Why this matters

Depois dos Planos 032–035, o ReportLab gera os 18 tipos de entregável, passa no
portão de qualidade e foi aprovado visualmente. Manter o WeasyPrint como padrão
conserva todo o problema de origem (`plans/PROBLEMA_MOTOR_PDF_CROSS_PLATFORM.md`):
dependência de Pango/Cairo, `DYLD_LIBRARY_PATH` no macOS, GTK3 no Windows, conflito de
versão do `pydyf` que derruba a execução, avisos repetidos de "Pango ausente" e testes
de PDF que pulam na maioria das máquinas. Este plano remove o WeasyPrint de vez:
PDF passa a sair igual em qualquer sistema com `pip install -r requirements.txt`.

## Current state (depois de 032–035; confira)

- `render.py`, bloco de PDF de `main()`:
  ```python
          try:
              if args.pdf_engine == "reportlab":
                  render_pdf_reportlab(content, tokens, profile, path)
              else:
                  from weasyprint import HTML
                  HTML(string=source_html or "", base_url=str(ROOT)).write_pdf(str(path))
          except (ImportError, OSError) as exc:
              ...  # mensagem com "brew install pango" no ramo weasyprint
  ```
  e o argumento `--pdf-engine` com `choices=("weasyprint", "reportlab")`, `default="weasyprint"`; `REPORTLAB_LAYOUTS` com os 5 layouts; `source_html` gerado também para PDF quando o motor é WeasyPrint.
- `_DESIGN_SYSTEM/requirements.txt` com `weasyprint==61.2` e `pydyf==0.10.0` (só servem ao WeasyPrint), além de `reportlab==5.0.1` e `pdfminer.six==20260107`.
- `_DESIGN_SYSTEM/tests/test_render.py`: `pdf_available()` testa `import weasyprint` e é usada para pular testes; `test_missing_pdf_backend_still_renders_other_formats` e `test_pdf_write_failure_removes_partial_pdf` simulam um `weasyprint.py` falso; um teste exige "brew install pango" na mensagem; `test_oversized_card_remains_fatal` e `PdfIdempotencyTests` dependem do WeasyPrint.
- `_DESIGN_SYSTEM/README.md`, item 3: fala em "falta de bibliotecas nativas (WeasyPrint/pango)".
- Achado relacionado (verificado em 05/10/2026): exceções inesperadas do motor de PDF que não sejam `ImportError`/`OSError` (ex.: `TypeError` por versão incompatível de dependência) derrubam a execução inteira e nenhum outro formato é entregue, porque o PDF é gerado antes de MD/TXT/DOCX.

Grep de referência para achar o que remover: `grep -rn -i "weasyprint\|pango\|pydyf\|pdf_available" _DESIGN_SYSTEM`.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Ambiente limpo 3.12 | `uv venv -q -p 3.12 /tmp/v036-312 && uv pip install -q -p /tmp/v036-312/bin/python -r _DESIGN_SYSTEM/requirements.txt pytest` | exit 0 (se não houver `uv`: `python3 -m venv` + `pip install`) |
| Ambiente limpo 3.10 | o mesmo com `-p 3.10` em `/tmp/v036-310` | exit 0 |
| Testes | `/tmp/v036-312/bin/python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed`, **0 skipped** de PDF |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check && python3 _TOOLS/build_sources.py --check` | exit 0 |

## Scope

**In scope**: `_DESIGN_SYSTEM/scripts/render.py`, `_DESIGN_SYSTEM/requirements.txt`,
`_DESIGN_SYSTEM/README.md`, `_DESIGN_SYSTEM/tests/test_render.py`,
`_SAMPLES_ENTREGAVEIS/*/` (derivados regenerados; `input.json` intocado),
`.github/workflows/tests.yml` (criar), cópias do sync, `plans/README.md`.

**Out of scope**: `pdf_reportlab.py` e `pdf_quality.py` (salvo remover referências ao WeasyPrint em comentários); o HTML como formato (continua existindo, só deixa de gerar o PDF); DOCX/PPTX; `SKILL.md` (nenhum cita Pango — confirme com grep); `layout.json`; `plans/PROBLEMA_MOTOR_PDF_CROSS_PLATFORM.md` (documento do operador).

## Git workflow

Branch `advisor/036-reportlab-padrao`; um commit por passo; português no imperativo; sem push/merge.

## Steps

### Step 1: Motor único em `render.py`

- `--pdf-engine`: `choices=("reportlab",)`, `default="reportlab"`, ajuda "motor do PDF (só reportlab; opção mantida por compatibilidade)".
- Remova o ramo `weasyprint`, `REPORTLAB_LAYOUTS` (todos os layouts são suportados) e a checagem de layout não suportado.
- `source_html` só quando `"html" in requested`.
- Tratamento de erro do PDF:
  - `ImportError` → `unavailable["pdf"]` + aviso `"AVISO: PDF não gerado (...). Instale: pip install -r requirements.txt."`
  - `PdfOverflow`/`ValueError` (conteúdo que não cabe; portão de qualidade) → continuam fatais, como hoje.
  - Qualquer outra exceção → `path.unlink(missing_ok=True)`, `unavailable["pdf"] = f"{type(exc).__name__}: {exc}"[:300]` e aviso; a execução continua e entrega os demais formatos.
- O manifesto continua registrando `"pdf_engine": "reportlab"` quando há PDF.
- Mude `RENDERER_VERSION` para `"2.0.0"` (mudança de motor).

**Verify**: `grep -n -i "weasyprint\|pango" _DESIGN_SYSTEM/scripts/render.py` → nada.

### Step 2: Dependências

Remova `weasyprint==61.2` e `pydyf==0.10.0` de `requirements.txt`. Recrie os dois ambientes limpos (tabela de comandos).

**Verify**: `/tmp/v036-312/bin/python -c "import weasyprint"` → `ModuleNotFoundError`; o render da amostra do test card com `--formats pdf` → exit 0.

### Step 3: Testes

- `pdf_available()` passa a testar `import reportlab`; remova os testes duplicados que só existiam para o WeasyPrint (o equivalente ReportLab foi criado no 032: transbordo do card).
- Reescreva `test_missing_pdf_backend_still_renders_other_formats` simulando o ReportLab ausente: pasta com um pacote falso `reportlab/__init__.py` contendo `raise ImportError("reportlab ausente (simulado)")` no `PYTHONPATH` → exit 0, `unavailable["pdf"]` contém "reportlab ausente", MD e DOCX existem, nenhum PDF.
- Novo `test_unexpected_engine_error_keeps_other_formats`: pacote falso `reportlab/__init__.py` com `raise TypeError("versão incompatível (simulado)")` → exit 0, `unavailable["pdf"]` começa com `"TypeError"`, MD e DOCX existem.
- `PdfIdempotencyTests` e `test_identity_for_all_states_and_supported_profiles` passam a rodar sempre (sem pular).
- Remova as asserções de "brew install pango".

**Verify**: suíte nos dois ambientes limpos (3.10 e 3.12) → `0 failed` e nenhum teste pulado por falta de PDF (`pytest -rs` não lista "pango" nem "weasyprint").

### Step 4: Regenerar as amostras

Para cada pasta `_SAMPLES_ENTREGAVEIS/<tipo>/` com `input.json`, rode o render com os formatos padrão do perfil para a própria pasta.

**Verify**: `grep -L '"pdf_engine": "reportlab"' _SAMPLES_ENTREGAVEIS/*/*.manifest.json` → nada; `git diff --stat -- '_SAMPLES_ENTREGAVEIS/*/input.json'` → nada.

### Step 5: Documentação

`_DESIGN_SYSTEM/README.md`: PDF gerado pelo ReportLab, instalado só com `pip install -r requirements.txt`, sem bibliotecas do sistema, em Windows, macOS e Linux; remova Pango/WeasyPrint; mantenha a descrição do portão de qualidade; diga que o HTML é um formato de entrega à parte. Em `plans/README.md`, registre que o problema de `PROBLEMA_MOTOR_PDF_CROSS_PLATFORM.md` foi resolvido por 032–036.

**Verify**: `grep -rn -i "weasyprint\|pango\|pydyf" _DESIGN_SYSTEM --include=*.md --include=*.py --include=*.txt` → nada.

### Step 6: Verificação em três sistemas (CI)

Crie `.github/workflows/tests.yml`: em `push` e `pull_request`, matriz `os: [ubuntu-latest, macos-latest, windows-latest]` × `python: ["3.10", "3.12"]`; passos: checkout, setup-python, `python -m pip install -r _DESIGN_SYSTEM/requirements.txt pytest`, `python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS`, `python _TOOLS/sync_shared.py --check`. Não faça push: o operador decide quando ativar (o GitHub Actions pode cobrar minutos em repositório privado).

**Verify**: `python3 -c "import yaml,sys;d=yaml.safe_load(open('.github/workflows/tests.yml'));print(sorted(d['jobs']))"` → lista com o job criado.

### Step 7: Sync e pacotes

Sync e checagens (tabela). Informe ao operador que os pacotes `.skill` em `_DIST/` precisam ser regerados.

**Verify**: `ls */assets/design-system/requirements.txt | xargs grep -l weasyprint` → nada.

## Test plan

Testes reescritos/novos do Passo 3; a suíte inteira passa a exercitar PDF em qualquer máquina. A CI do Passo 6 é a prova de Windows, que nenhum executor local consegue dar.

## Done criteria

- [ ] `grep -rn -i "weasyprint\|pango\|pydyf" _DESIGN_SYSTEM` → nada
- [ ] Suíte `0 failed` e sem skips de PDF em Python 3.10 e 3.12 limpos
- [ ] Amostras regeneradas com `pdf_engine: reportlab`; `input.json` intocados
- [ ] `.github/workflows/tests.yml` criado e válido
- [ ] Sync e `build_sources --check` → exit 0; status atualizado em `plans/README.md`

## STOP conditions

- Alguma aprovação visual (032, 034, 035) não está registrada.
- Algum tipo de amostra falha no render ou no portão de qualidade com o ReportLab.
- Algum `SKILL.md` ou referência de skill cita WeasyPrint/Pango (o grep do escopo diz que não; se disser, reporte antes de editar).
- Algum teste só passa reintroduzindo o WeasyPrint.

## Maintenance notes

- Daqui em diante, mudanças visuais no PDF são feitas em `pdf_reportlab.py`; o CSS só afeta o formato HTML. Avalie depois se o HTML deve seguir o mesmo desenho do PDF ou virar uma prévia simples.
- O Plano 031 (BLOCKED) tratava sobreposição no PDF gerado do HTML; com o PDF fora do HTML, reavalie se ele ainda é necessário só para o formato HTML.
- Robustez ainda pendente (fora deste plano): sem `python-docx`/`python-pptx` a execução inteira falha; `score.py`/`iqb.py` quebram no terminal do Windows com caracteres fora do cp1252 e recusam JSON com BOM.
