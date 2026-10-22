# Galeria de templates

Ferramenta local, de uso do mantenedor, para ver como sai cada entregável de cada skill com o
design system atual. Como o `_LAYOUT_STUDIO`, fica numa pasta com `_` e não é distribuída com
as skills.

## Como usar

1. A galeria é regenerada ao final de `python3 _TOOLS/sync_shared.py` (exceto com `--check`,
   `--dry-run` ou `--no-gallery`). Para gerá-la sozinha, rode `python3 _GALERIA/gerar.py` na raiz do
   repositório. O gerador renderiza as amostras fictícias de
   `_SAMPLES_ENTREGAVEIS/<tipo>/input.json` com `_DESIGN_SYSTEM/scripts/render.py` em
   `_GALERIA/saida/<tipo>/` (HTML, PDF, Markdown, DOCX e, na apresentação, PPTX) e grava
   `_GALERIA/index.html`.
2. Abra `_GALERIA/index.html` no navegador (duplo clique; não precisa de servidor).
3. Na lateral, escolha a skill e o entregável. Veja HTML e PDF lado a lado, só um deles ou baixe
   Markdown, DOCX e PPTX. Um `!` na lista indica que algum formato não foi gerado; o motivo
   aparece no topo.

Sincronize ou rode o gerador de novo sempre que mudar `_DESIGN_SYSTEM` (tokens, renderizador ou um layout salvo no
Layout Studio): a galeria mostra o estado da pasta, mesmo antes do commit, e indica quando há
alterações locais no design system.

`saida/` e `index.html` são gerados e ficam fora do git. A lista de entregáveis de cada skill está em
`SKILLS`, no topo de `gerar.py`; atualize-a quando uma skill passar a gerar outro tipo.
