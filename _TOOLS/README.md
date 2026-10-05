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
O levantamento documental foi incorporado ao protocolo comum de grilling.
A sincronização também remove as cópias aposentadas dessa referência, mantendo
`grilling-operacional.md` como fonte única nas onze skills.

As fontes em `_DESIGN_SYSTEM/assets/fonts/static/` são geradas a partir das fontes
variáveis por `python3 _TOOLS/make_static_fonts.py` (requer `fonttools` apenas na
manutenção). Regenere as instâncias quando as fontes variáveis mudarem.

Ao importar ou substituir uma fonte, atualize `_FONTES/manifest.json` (nova entrada; a anterior vira `historica`) e rode `python3 _TOOLS/build_sources.py`. Nunca reescreva um original. O gerador confere as cópias e os hashes fixados dos DOCX 4D/3E/5C antes de produzir as páginas `references/fontes.md`; `python3 _TOOLS/build_sources.py --check` verifica tudo sem escrever e retorna código 1 para fonte ausente, divergente ou página desatualizada. Metadados desconhecidos ficam nulos; publicação oficial não confirma adoção institucional.
