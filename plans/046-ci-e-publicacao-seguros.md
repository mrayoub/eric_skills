# Plan 046: Publicar pacotes só depois dos testes, com publicação idempotente e cadeia de dependências fixada

> **Executor instructions**: Siga passo a passo; rode cada verificação; pare nas STOP conditions; atualize `plans/README.md`.
>
> **Drift check**: `git diff --stat 595f3b0..HEAD -- .github _TOOLS/publish_releases.py _TOOLS/check_channels.py _DESIGN_SYSTEM/requirements.txt _TESTS/requirements-dev.txt`

## Status

- **Priority**: P1 · **Effort**: S · **Risk**: LOW · **Depends on**: 041 · **Category**: dx / security
- **Planned at**: commit `595f3b0`, 2026-10-09

## Why this matters

Verificado no histórico de execuções: às 17:46:14 de 2026-10-09 o workflow "Publicar pacotes" publicou as Releases
`*-v1.1.1` a partir do commit `7b1d5f4` enquanto o "Testes" do mesmo push foi **cancelado** e a matriz do mesmo commit
**falhou** (Windows). `release.yml` dispara no push que muda `catalog.json` sem esperar os testes; `tests.yml` tem
`cancel-in-progress: true` por ref, então um `workflow_dispatch` cancela a execução do push. Uma Release de versão é
imutável: o que sair quebrado fica publicado.

Problemas relacionados, todos verificados:
- `_TOOLS/publish_releases.py` decide o que é novo pelas tags **locais** (`git tag --list`); as tags criadas pelo `gh`
  só existem no remoto, então `--dry-run` local mente e uma execução local falha na primeira Release existente, sem
  mostrar o stderr do `gh` (`run(..., check=True)` com `capture_output`).
- A Release fixa `pacotes` é criada uma vez, sem `--target` (a tag fica no commit antigo), e só recebe
  `upload --clobber`: pacotes de skill renomeada/removida nunca saem; as notas dizem "Os 13 pacotes" fixo.
- `_TOOLS/check_channels.py:31` roda `npx -y skills` **sem versão** e lê nomes por uma regex sobre o desenho da tela
  (`^│ {4}…`); uma mudança de saída do CLI quebra todo PR com "descobre []".
- Actions fixadas por tag (`@v4`, `@v5`), não por SHA; `contents: write` no nível do workflow de release.
- `_DESIGN_SYSTEM/requirements.txt` (o arquivo que o usuário final instala) tem pins exatos `==`, que podem rebaixar
  pacotes do Python do usuário; os pins exatos deveriam ficar só no ambiente de CI/teste.

## Steps

1. **Release só após testes:** troque o gatilho de `release.yml` para `workflow_run` do workflow "Testes"
   (`types: [completed]`, `branches: [main]`) com `if: github.event.workflow_run.conclusion == 'success' &&
   github.event.workflow_run.event == 'push'`, faça checkout de `github.event.workflow_run.head_sha` e publique só se
   `catalog.json` mudou nesse commit (`git diff --name-only HEAD~1 HEAD`). Mantenha `workflow_dispatch`.
2. **Não cancelar o push:** em `tests.yml`, `concurrency.group: tests-${{ github.ref }}-${{ github.event_name }}`.
3. **Publicação idempotente** (`publish_releases.py`): tags existentes vindas de `git ls-remote --tags origin`
   (e/ou `gh release list --json tagName`); em falha do `gh`, imprima o stderr e saia com 1; `pacotes`: apague assets
   que não estão em `_DIST/`, mova a tag para o HEAD (`gh release edit pacotes --target <sha>` ou recrie) e gere as
   notas com o número real de skills.
4. **npx fixado:** `npx -y skills@<versão atual, ex.: 1.7.2> add … --list`; parse vazio vira "não foi possível ler a
   saída do npx skills", não divergência de catálogo.
5. **Cadeia:** fixe as actions por SHA (comentário com a tag ao lado) e acrescente `.github/dependabot.yml` para
   `github-actions` e `pip`; `permissions: contents: write` só no job de publicação.
6. **Requisitos:** `_DESIGN_SYSTEM/requirements.txt` com faixas compatíveis (`reportlab>=5,<6` etc.) e um
   `_TESTS/requirements-lock.txt` com os pins exatos usados pela CI (atualize `_TESTS/requirements-dev.txt` para
   incluí-lo). Confirme que a suíte passa com o lock.
7. Testes: `publish_releases.py --dry-run` com tags remotas simuladas (mock de `run`); parse vazio do npx; YAML válido.

## Done criteria

- [x] O push `c0b2939` falhou nos testes e a publicação `37981661152` foi ignorada · [x] `--dry-run` local lista 0 Releases pendentes após a publicação · [x] `pacotes` tem 13 `.skill` + catálogo + checksums, e a tag aponta para o HEAD validado `6123e99` · [x] suíte `0 failed` (202 testes, 1.511 subtestes; CI do commit `6123e99` passou)

## STOP conditions

- `workflow_run` não estiver disponível para o repositório privado ou exigir segredo extra.
- Fixar actions por SHA exigir token com escopo além do `GITHUB_TOKEN`.
