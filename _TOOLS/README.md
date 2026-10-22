# Manutenção das fontes compartilhadas

As fontes são `_DESIGN_SYSTEM/` (design system), `_ERIC_CONTEXT/README.md`
(contexto ERIC) e `_SHARED/` (referências comuns). As versões em
`<skill>/assets/design-system/` e as referências comuns em `<skill>/references/`
são cópias geradas. Os testes ficam na fonte e não são distribuídos nas skills.

Edite só a fonte e rode `python3 _TOOLS/sync_shared.py`. Ao final, ele também regenera a galeria de
templates (`_GALERIA/`); use `--no-gallery` para pular. Uma falha da galeria só gera aviso. Antes de distribuir,
rode `python3 _TOOLS/sync_shared.py --check`: código 0 confirma a sincronização;
código 1 lista as divergências. Para visualizar as ações sem alterar arquivos,
use `python3 _TOOLS/sync_shared.py --dry-run`.

A sincronização remove arquivos excedentes do design system e lixo dos pacotes.
O levantamento documental foi incorporado ao protocolo comum de grilling.
A sincronização também remove as cópias aposentadas dessa referência, mantendo
`grilling-operacional.md` como fonte única nas treze skills.

As fontes em `_DESIGN_SYSTEM/assets/fonts/static/` são geradas a partir das fontes
variáveis por `python3 _TOOLS/make_static_fonts.py` (requer `fonttools` apenas na
manutenção). Regenere as instâncias quando as fontes variáveis mudarem.

Para a revisão visual dos motores de PDF, instale `pypdfium2` e `pillow` no
ambiente de manutenção e rode `python3 _TOOLS/compare_pdf_engines.py --out /tmp/comparacao-pdf`.
Use `--types test_card,learning_card` para limitar os tipos. O `index.html`
gerado reúne as páginas lado a lado, o resultado do verificador e os erros de
renderização. Ele serve às aprovações visuais dos Planos 034–036.

Ao importar ou substituir uma fonte, atualize `_FONTES/manifest.json` (nova entrada; a anterior vira `historica`) e rode `python3 _TOOLS/build_sources.py`. Nunca reescreva um original. O gerador confere as cópias e os hashes fixados dos DOCX 4D/3E/5C antes de produzir as páginas `references/fontes.md`; `python3 _TOOLS/build_sources.py --check` verifica tudo sem escrever e retorna código 1 para fonte ausente, divergente ou página desatualizada. Metadados desconhecidos ficam nulos; publicação oficial não confirma adoção institucional.

## Licença e material de terceiros

`LICENSE` (Licença de Uso Restrito CCEE) vale só para o conteúdo da CCEE. O inventário
de terceiros, `THIRD_PARTY_NOTICES.md`, é gerado por `build_sources.py` a partir de três
campos obrigatórios de cada entrada do manifesto: `titular` (`"CCEE"`, o terceiro, ou `null`
quando a confirmar), `licenca` e `distribuido`. O `sync_shared.py` copia `LICENSE` e
`THIRD_PARTY_NOTICES.md` para cada skill, que pode ser instalada sozinha.

Material de terceiros cuja licença não permite redistribuição entra no manifesto com
`distribuido: false` e `arquivo` apontando para a URL oficial — nunca como arquivo. Os
PDFs da Strategyzer (Test Card, Learning Card, Innovation Project Scorecard) estão na lista
`RETIRED` de `build_sources.py`: se voltarem a qualquer skill, a verificação falha. Material
produzido por empregados da CCEE no exercício da função tem `titular: "CCEE"`.

## Versões e pacotes

`catalog.json` (raiz) guarda a versão (`metadata.version` do `SKILL.md`) e o hash do conteúdo
distribuível de cada skill. `python3 _TOOLS/build_catalog.py --check` falha se o conteúdo de uma skill
mudou sem subir a versão; `--bump [patch|minor|major]` sobe a versão de quem mudou e regrava o catálogo.
`python3 _TOOLS/build_dist.py` roda as checagens, valida o frontmatter (só `name`, `description`,
`license`, `allowed-tools` e `metadata`) e gera `_DIST/<skill>.skill` reprodutíveis, `catalog.json` e
`SHA256SUMS`. O pacote tem exatamente os arquivos que entram no hash, os mesmos que o `npx skills` instala.
O verificador para usuários fica em `_DESIGN_SYSTEM/scripts/check_updates.py` e é copiado para
`<skill>/scripts/check_updates.py` nas treze skills, inclusive `esteira-eric`.

## CI e publicação

`python3 _TOOLS/check_channels.py` confere os três canais: o `npx skills` descobre exatamente as skills do
catálogo; o pacote `.skill` tem os mesmos arquivos que o git distribui; nenhum link sai da pasta da skill; os
pacotes são reprodutíveis; e o `check_updates.py` reconhece todas como atualizadas (`--sem-npx` pula o npx).
`.github/workflows/tests.yml` roda, em todo push e pull request, as checagens de versionamento e canais e a suíte
em Linux; a matriz Windows/macOS/Linux x Python 3.10/3.12 roda toda segunda e sob demanda.
`.github/workflows/release.yml` roda depois que o workflow `Testes` conclui com sucesso no push ao
`main` e o `catalog.json` mudou: gera os pacotes e, com `_TOOLS/publish_releases.py`, cria uma Release
por versão nova e atualiza a Release fixa `pacotes` (`--dry-run` mostra o que faria).
As dependências distribuídas usam faixas em `_DESIGN_SYSTEM/requirements.txt`; o CI instala os pins de
`_TESTS/requirements-lock.txt` por `_TESTS/requirements-dev.txt`.
Recomendação: em Settings → Branches, exigir o check `versionamento` antes do merge no `main`.
