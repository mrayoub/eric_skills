# Layouts de estrutura visual (por deliverable_type)

Arquivos `<deliverable_type>.layout.json` desta pasta definem a estrutura/frame de cada
tipo de entregável: tamanho de página e os "slots" (zonas nomeadas com posição e tamanho
em mm) que compõem aquele layout. São gerados e editados com a ferramenta em
`../../_LAYOUT_STUDIO/` (fora do git de skills, só de uso do mantenedor).

Dois tipos já são desenhados a partir do `layout.json`:

- `executive_presentation`: HTML, PPTX e PDF posicionam logo, título, corpo e rodapé de cada slide nos slots.
- `briefing_one_page`: HTML e PDF desenham cada bloco no slot com o mesmo `section_key`, nas mesmas
  posições, e recusam blocos sem slot. Editar este layout no Studio muda os dois formatos.

- `innovation_potential_assessment`: HTML e PDF leem a ordem e as colunas. Os slots são lidos de cima
  para baixo (depois da esquerda para a direita); dois slots com o mesmo topo formam uma linha de duas
  colunas, e um slot mais estreito que 60% do maior ocupa meia largura. A altura não é fixa: o conteúdo
  flui entre páginas. O modo de exibição define o componente: "Título e conteúdo" é um card com faixa,
  "Somente conteúdo" é a caixa escura (com o título como etiqueta pequena interna) e "Listagem tabular"
  mostra o painel de notas (`scores`). Blocos sem slot seguem no fim, no estilo comum.

Nos demais tipos, o arquivo ainda é só a definição visual: a estrutura continua decidida
pelo código em `render.py` e `pdf_reportlab.py` e pelas regras de `profiles.json`.

Convenção de nome de arquivo: `<deliverable_type>.layout.json`, mesmo valor de
`deliverable_type` usado nos schemas de `../contracts/`.
