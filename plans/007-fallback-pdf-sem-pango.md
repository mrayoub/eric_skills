# Plan 007: Entregar os demais formatos e avisar claramente quando o PDF não puder ser gerado

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat improve-baseline-2026-09-28..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tests/test_render.py _DESIGN_SYSTEM/README.md`
> Mudanças dos planos 002/005/006 são esperadas; confirme que o bloco `if "pdf" in requested:` de `main()` ainda é o citado abaixo. Senão, STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 001 (sync)
- **Category**: dx
- **Planned at**: commit `35c3b75`, 2026-09-28

## Why this matters

O PDF usa WeasyPrint, que depende da biblioteca nativa `pango`. Onde ela falta (foi o
caso no Mac do mantenedor em 2026-09-28, e é comum em sandboxes de execução de skills),
`render.py` morre com `OSError: cannot load library 'pango-1.0-0'` e **nenhum** formato é
gerado depois do PDF — nem DOCX/MD, que não precisam de `pango`. Dois dos cinco testes do
design system falham pelo mesmo motivo, mascarando falhas reais. Queremos: gerar o que for
possível, registrar no manifesto o que faltou e por quê, e os testes pularem (skip) em vez
de falharem quando o ambiente não tem `pango`.

## Current state

- `_DESIGN_SYSTEM/scripts/render.py` `main()` (linhas ~686-702 na linha de base):

```python
    if "pdf" in requested:
        try:
            from weasyprint import HTML
        except ImportError as exc:
            raise RuntimeError("PDF requer WeasyPrint: pip install weasyprint") from exc
        path = out / f"{stem}.pdf"
        HTML(string=source_html or "", base_url=str(ROOT)).write_pdf(str(path))
        if profile["layout"] in ("executive_one_page", "card_portrait"):
            ...
            if count != 1:
                path.unlink(missing_ok=True)
                raise ValueError(f"{profile['layout']} excedeu uma página ({count}); revise ou divida o conteúdo sem reduzir a fonte")
        files.append(path)
```

  O `OSError` do `pango` é levantado no `from weasyprint import HTML` (não é `ImportError`), por isso escapa do `except`.
- O manifesto (`{stem}.manifest.json`) é escrito no fim de `main()` com `files` = hashes dos arquivos gerados; o stdout é `{"manifest": ..., "files": [...]}`.
- `_DESIGN_SYSTEM/tests/test_render.py`: `test_portrait_and_landscape_and_semantic_identity` e `test_card_is_one_page_and_presentation_is_editable` usam PDF.
- `_DESIGN_SYSTEM/README.md` "Uso pelas skills", item 3, fala em instalar bibliotecas de `requirements.txt`; nada sobre `pango`.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Testes | `python3 -m pytest -q _DESIGN_SYSTEM/tests` | 0 failed (skips permitidos sem pango) |
| Checar pango | `python3 -c "import weasyprint" ; echo $?` | 0 com pango; ≠0 sem |

## Scope

**In scope**: `_DESIGN_SYSTEM/scripts/render.py` (bloco PDF de `main()` e o print final); `_DESIGN_SYSTEM/tests/test_render.py`; `_DESIGN_SYSTEM/README.md` (item 3 de "Uso pelas skills"); cópias via sync.

**Out of scope**: instalar `pango` na máquina; a regra de uma página (continua erro — conteúdo que não cabe NÃO é "indisponível").

## Git workflow

Branch `advisor/007-pdf-fallback`. Commit: `Gera demais formatos quando o PDF não está disponível`.

## Steps

### Step 1: Isolar a falha de ambiente

No bloco PDF: capture `(ImportError, OSError)` **apenas** em torno do `import` e do
`write_pdf`. Em caso de falha, não levante; guarde
`unavailable["pdf"] = f"{type(exc).__name__}: {exc}"[:300]`, imprima em stderr
`AVISO: PDF não gerado (<motivo>). No macOS: brew install pango; no Debian/Ubuntu: apt-get install libpango-1.0-0 libpangoft2-1.0-0.`
e siga para os demais formatos. A verificação de uma página só roda se o PDF foi gerado.
O `ValueError` de "excedeu uma página" continua sendo erro fatal.

No manifesto, acrescente `"unavailable": unavailable` (dict vazio quando nada faltou) e
inclua a mesma chave no JSON impresso no stdout. Código de saída: `0` se só faltou PDF
por ambiente (o stdout diz o que faltou).

**Verify** (em máquina sem pango): `python3 _DESIGN_SYSTEM/scripts/render.py _SAMPLES_ENTREGAVEIS/learning_card/input.json --out-dir "$TMPDIR/lc" --formats pdf,md,docx; echo $?` → stdout contém `"unavailable": {"pdf"`; `ls "$TMPDIR/lc"` mostra `.md` e `.docx`; exit `0`.
(Em máquina com pango: PDF gerado e `"unavailable": {}`.)

### Step 2: Testes que pulam sem pango

No topo de `test_render.py`:

```python
def pdf_available() -> bool:
    try:
        import weasyprint  # noqa: F401
        return True
    except (ImportError, OSError):
        return False
```

Decore os dois testes que usam PDF com `@unittest.skipUnless(pdf_available(), "WeasyPrint/pango indisponível")`.
Adicione `test_missing_pdf_backend_still_renders_other_formats`: rode o script via
subprocess com `env` contendo `PYTHONPATH` apontando para um diretório temporário com um
`weasyprint.py` falso que faz `raise OSError("pango ausente (simulado)")`; peça `pdf,md` e
confirme exit 0, `.md` criado e `"unavailable"` com `pdf` no stdout.

**Verify**: `python3 -m pytest -q _DESIGN_SYSTEM/tests` → `0 failed`.

### Step 3: Documentar

No `_DESIGN_SYSTEM/README.md`, item 3 de "Uso pelas skills", acrescente: "Se o PDF não
puder ser gerado por falta de bibliotecas nativas (WeasyPrint/pango), o renderizador
gera os demais formatos e registra `unavailable.pdf` no manifesto. Informe isso ao
usuário e ofereça DOCX; não declare que o PDF foi entregue."

Rode o sync.

**Verify**: `python3 _TOOLS/sync_shared.py --check; echo $?` → `0`.

## Test plan

- Novo teste de backend simulado (Step 2).
- Testes de PDF existentes: pulados sem pango, executados com pango.

## Done criteria

- [ ] `python3 -m pytest -q _DESIGN_SYSTEM/tests` → `0 failed`
- [ ] Sem pango: `--formats pdf,md,docx` gera MD e DOCX, exit 0, `unavailable.pdf` no manifesto
- [ ] Conteúdo que excede uma página continua dando erro (teste existente de card, quando há pango)
- [ ] `sync_shared.py --check` → 0
- [ ] `plans/README.md` atualizado

## STOP conditions

- O `import weasyprint` falhar por outro motivo que não `ImportError`/`OSError` (ex.: `AttributeError` de versão) — reporte a mensagem; não amplie o `except` para `Exception`.

## Maintenance notes

- Não transforme outros erros em "indisponível": só ausência de backend de PDF.
- Se um dia houver outro backend (ex.: Chromium headless), ele entra como alternativa nesse mesmo ponto.
