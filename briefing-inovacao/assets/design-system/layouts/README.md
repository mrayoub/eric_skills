# Layouts de estrutura visual (por deliverable_type)

Arquivos `<deliverable_type>.layout.json` desta pasta definem a estrutura/frame de cada
tipo de entregável: tamanho de página e os "slots" (zonas nomeadas com posição e tamanho
em mm) que compõem aquele layout. São gerados e editados com a ferramenta em
`../../_LAYOUT_STUDIO/` (fora do git de skills, só de uso do mantenedor).

Dois tipos já são desenhados a partir do `layout.json`:

- `executive_presentation`: HTML, PPTX e PDF posicionam logo, título, corpo e rodapé de cada slide nos slots.
- `briefing_one_page`: HTML e PDF desenham cada bloco no slot com o mesmo `section_key`, nas mesmas
  posições, e recusam blocos sem slot. Editar este layout no Studio muda os dois formatos.

Nos demais tipos, o arquivo ainda é só a definição visual: a estrutura continua decidida
pelo código em `render.py` e `pdf_reportlab.py` e pelas regras de `profiles.json`.

Convenção de nome de arquivo: `<deliverable_type>.layout.json`, mesmo valor de
`deliverable_type` usado nos schemas de `../contracts/`.
