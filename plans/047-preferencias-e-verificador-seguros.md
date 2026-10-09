# Plan 047: Blindar as preferências locais e o verificador de atualizações

> **Executor instructions**: Siga passo a passo; rode cada verificação; pare nas STOP conditions; atualize `plans/README.md`.
>
> **Drift check**: `git diff --stat 595f3b0..HEAD -- _SHARED _DESIGN_SYSTEM/scripts/check_updates.py _TOOLS/sync_shared.py esteira-eric README.md _TOOLS/README.md`

## Status

- **Priority**: P1 · **Effort**: M · **Risk**: LOW · **Depends on**: none · **Category**: security
- **Planned at**: commit `595f3b0`, 2026-10-09

## Why this matters

Verificado no código e nas instruções:

1. **Injeção persistente de instruções (SEC-01):** `_SHARED/preferencias-do-usuario.md:9-12` manda ler as preferências
   do **projeto** em toda execução e "aplicar o que vier", com prioridade sobre as do usuário; `_SHARED/preferencias.py`
   imprime o texto literalmente; a lista "O que recusar" só vale na hora de gravar. Uma pasta de projeto vinda de
   terceiros (repositório clonado, pasta compartilhada) com `.eric/preferencias/todas.md` passa instruções a todas as skills.
2. **Symlink (SEC-02):** `preferencias.py` resolve só a raiz do projeto; `guard()` verifica caminhos não resolvidos;
   `write_text`/`replace` seguem links: um `todas.md` que é link para outro arquivo do usuário é sobrescrito num
   `adicionar --projeto`. Escritas não são atômicas.
3. **Token do GitHub (SEC-03):** `_DESIGN_SYSTEM/scripts/check_updates.py` envia `GITHUB_TOKEN`/`GH_TOKEN` para qualquer
   `--catalog`, inclusive `http://`, e o `urllib` repassa o cabeçalho em redirecionamentos.
4. **Falha ruidosa (CORR-04):** `check_updates.py` lê o `SKILL.md` de todas as pastas irmãs sem `try`; uma skill de
   terceiros com arquivo não UTF-8 derruba o verificador com traceback.
5. **Documentação:** o guia diz que o script fica "ao lado deste arquivo (`../scripts/preferencias.py`)" e os comandos
   usam `scripts/preferencias.py` relativo à raiz da skill — ambíguo; `esteira-eric/SKILL.md` diz "Não gera arquivos nem
   requer Python", mas roda o script de preferências; a `esteira-eric` não tem `check_updates.py` (não recebe o design
   system), e `README.md`/`_TOOLS/README.md` dizem que todas têm; `_TOOLS/README.md` diz "doze skills" para o grilling.

## Steps

1. **Leitura como dado:** no guia, preferências lidas são dados; antes de aplicar, reaplicar a lista "O que recusar";
   preferências de **projeto** são mostradas ao usuário e só aplicadas depois de confirmadas na primeira vez em que
   aparecem ou quando o arquivo muda — o script guarda o hash aceito em `~/.config/eric-skills/projetos-aceitos.json`
   e o `ler --projeto` marca "NÃO CONFIRMADA" quando o hash diverge. Acrescente um comando `confirmar --projeto DIR`.
2. **Symlink e atomicidade:** resolva o caminho final completo, recuse arquivos ou pastas que sejam links, rode `guard`
   no caminho resolvido, grave em arquivo temporário na mesma pasta e use `os.replace`.
3. **Token:** envie `Authorization: Bearer` só para `https://raw.githubusercontent.com` e `https://api.github.com`;
   recuse `http://`; use um `HTTPRedirectHandler` que remove o cabeçalho em redirecionamento para outro host.
4. **Leituras protegidas:** `try/except (OSError, UnicodeDecodeError)` por pasta irmã; pule e siga.
5. **Docs e metadados:** guia com "na pasta `scripts/` da raiz da skill (rode a partir da raiz ou use o caminho
   absoluto)"; `esteira-eric` `metadata.requirements`: "Python opcional, só para preferências locais"; copiar
   `check_updates.py` também para `scripts/` de todas as skills via `sync_shared.py` (como `preferencias.py`) e
   apontar o README para `<skill>/scripts/check_updates.py`; corrigir "doze" → "treze" em `_TOOLS/README.md`.
6. **Testes** (`_TESTS/test_preferencias.py`, `_TESTS/test_distribution.py`): projeto não confirmado aparece marcado;
   link simbólico recusado; token não enviado a `http://` nem a outro host (mock de `urlopen`); irmã não UTF-8 não derruba.
7. Sync, fontes, `build_catalog.py --bump`, suíte.

## Done criteria

- [ ] Os 4 testes novos falhavam antes e passam · [ ] `esteira-eric` com `scripts/check_updates.py` · [ ] suíte `0 failed`

## STOP conditions

- A confirmação de preferências de projeto exigir interação que o Codex/Claude Code não suportem no fluxo da skill.
