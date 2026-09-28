# Manutenção das fontes compartilhadas

As fontes são `_DESIGN_SYSTEM/` (design system), `_ERIC_CONTEXT/README.md`
(contexto ERIC) e `_SHARED/` (referências comuns). As versões em
`<skill>/assets/design-system/` e as referências comuns em `<skill>/references/`
são cópias geradas. Os testes ficam na fonte e não são distribuídos nas skills.

Edite só a fonte e rode `python3 _TOOLS/sync_shared.py`. Antes de distribuir,
rode `python3 _TOOLS/sync_shared.py --check`: código 0 confirma a sincronização;
código 1 lista as divergências. Para visualizar as ações sem alterar arquivos,
use `python3 _TOOLS/sync_shared.py --dry-run`.

A sincronização remove arquivos excedentes do design system e lixo dos pacotes.
`levantamento-documental-e-grilling.md` é atualizado somente nas skills em que
já existe, preservando as ausências intencionais.
