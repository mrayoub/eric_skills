# Layouts de estrutura visual (por deliverable_type)

Arquivos `<deliverable_type>.layout.json` desta pasta definem a estrutura/frame de cada
tipo de entregável: tamanho de página e os "slots" (zonas nomeadas com posição e tamanho
em mm) que compõem aquele layout. São gerados e editados com a ferramenta em
`../../_LAYOUT_STUDIO/` (fora do git de skills, só de uso do mantenedor).

Hoje estes arquivos são **só a definição visual** — `scripts/render.py` ainda não os lê.
A estrutura de cada entregável continua sendo decidida pelo código Python em `render.py`
(funções `render_html`, `render_docx`, `render_pptx`) e pelas regras de `profiles.json`.

Quando a integração for feita, a expectativa é: `render.py` passa a ler o
`layout.json` do tipo correspondente e encaixar os blocos do JSON canônico nos slots
definidos, em vez de ter a estrutura hardcoded por tipo espalhada no código — com um
mecanismo de verificação (comparação estrutural para DOCX/PPTX, comparação visual com
limiar para PDF — ver Plano 028 Fase 2) garantindo que a saída real não diverge do que
foi desenhado, até que o layout seja redefinido na ferramenta.

Convenção de nome de arquivo: `<deliverable_type>.layout.json`, mesmo valor de
`deliverable_type` usado nos schemas de `../contracts/`.
