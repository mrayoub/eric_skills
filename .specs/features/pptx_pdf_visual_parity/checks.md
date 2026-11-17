# Paridade PPTX/PDF checks

Mutations: 3
Build: `python3 -m compileall -q _DESIGN_SYSTEM/scripts _TOOLS`
Plan: `.specs/features/pptx_pdf_visual_parity/plan.md`

8 checks in 3 slices · 0 one-way doors · 0 open

## Checks

### S1 - Conteúdo e edição

**C1** - Os quatro tipos preservam contagem, ordem e multiplicidade de palavras por slide do PDF (AC 1)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_pptx_parity.py::PptxParityTests::test_four_samples_preserve_slide_content_and_order`

**C2** - Os quatro tipos mantêm texto editável e somente o logo como imagem; cards, callout e tabela são nativos (AC 2)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_pptx_parity.py::PptxParityTests::test_four_samples_remain_editable`
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_pptx_parity.py::PptxParityTests::test_cards_callout_and_table_are_native_and_use_pdf_colors`

**C3** - Famílias, tamanhos e cores seguem o PDF; capa tem barra de 6 mm; os cinco tons dos cards têm preenchimento e faixa; corpo 17 pt (AC 3)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_pptx_parity.py::PptxParityTests::test_all_sample_fonts_and_cover_geometry`
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_pptx_parity.py::PptxParityTests::test_cards_callout_and_table_are_native_and_use_pdf_colors`

**C4** - Todos os slides dos quatro tipos têm identidade e `n / N`; citações têm sobrescrito baseline 30000 (AC 4)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_pptx_parity.py::PptxParityTests::test_all_sample_identity_numbering_and_superscripts`

### S2 - Conteúdo extenso

**C5** - Um parágrafo de 220 palavras numeradas continua sem perda, repetição ou quebra de palavras (AC 5)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py::PptxTablesAndWrapTests::test_long_text_is_split_between_words`

**C6** - Tabela de 20 linhas preserva ordem e repete cabeçalhos; células longas cabem na área útil (AC 6)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py::PptxTablesAndWrapTests::test_table_is_native_with_repeated_header`
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_render.py::FormatParityTests::test_long_table_cells_fit_in_pptx_area`

### S3 - Aparência e publicação

**C7** - Os 36 slides dos quatro tipos correspondem visualmente aos PDFs, sem corte ou sobreposição; dimensões diferem no máximo 0,2 pt e diferença RGB média por página é no máximo 12/255 (AC 7)
Proof: `python3 .specs/features/pptx_pdf_visual_parity/compare.py`

O teste numérico detecta regressões amplas; o julgamento independente das capturas abaixo confere conteúdo e composição, sem confundir limiar numérico com aparência comprovada:

- `captures/executive_presentation-01.png`
- `captures/executive_presentation-02.png`
- `captures/executive_presentation-03.png`
- `captures/executive_presentation-04.png`
- `captures/executive_presentation-05.png`
- `captures/executive_presentation-06.png`
- `captures/executive_presentation-07.png`
- `captures/five_c_presentation-01.png`
- `captures/five_c_presentation-02.png`
- `captures/five_c_presentation-03.png`
- `captures/five_c_presentation-04.png`
- `captures/five_c_presentation-05.png`
- `captures/five_c_presentation-06.png`
- `captures/five_c_presentation-07.png`
- `captures/five_c_presentation-08.png`
- `captures/five_c_presentation-09.png`
- `captures/five_c_presentation-10.png`
- `captures/five_c_presentation-11.png`
- `captures/five_c_presentation-12.png`
- `captures/five_c_presentation-13.png`
- `captures/five_c_presentation-14.png`
- `captures/four_d_presentation-01.png`
- `captures/four_d_presentation-02.png`
- `captures/four_d_presentation-03.png`
- `captures/four_d_presentation-04.png`
- `captures/four_d_presentation-05.png`
- `captures/four_d_presentation-06.png`
- `captures/four_d_presentation-07.png`
- `captures/three_e_presentation-01.png`
- `captures/three_e_presentation-02.png`
- `captures/three_e_presentation-03.png`
- `captures/three_e_presentation-04.png`
- `captures/three_e_presentation-05.png`
- `captures/three_e_presentation-06.png`
- `captures/three_e_presentation-07.png`
- `captures/three_e_presentation-08.png`

**C8** - Sincronização das 13 skills com renderer, fontes, versões, pacotes e os 14 canais do catálogo passam (AC 8)
Proof: `python3 _TOOLS/sync_shared.py --check`
Proof: `python3 _TOOLS/build_sources.py --check`
Proof: `python3 _TOOLS/build_catalog.py --check`
Proof: `python3 _TOOLS/build_dist.py --check`
Proof: `python3 _TOOLS/check_channels.py --sem-npx`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Tipos (4) | `executive_presentation` C1/C2/C3/C4/C7 · `five_c_presentation` C1/C2/C3/C4/C7 · `four_d_presentation` C1/C2/C3/C4/C7 · `three_e_presentation` C1/C2/C3/C4/C7 | - |
| Elementos editáveis (4) | texto C2 · card_grid C2 · callout C2 · table C2/C6 | - |
| Tons de card (5) | blue C3 · neutral C3 · red C3 · green C3 · yellow C3 | - |
| Paginação (3) | 220 palavras C5 · 20 linhas C6 · 9 linhas com células longas C6 | - |
| Capturas (36) | `executive_presentation-01.png` C7 · `executive_presentation-02.png` C7 · `executive_presentation-03.png` C7 · `executive_presentation-04.png` C7 · `executive_presentation-05.png` C7 · `executive_presentation-06.png` C7 · `executive_presentation-07.png` C7 · `five_c_presentation-01.png` C7 · `five_c_presentation-02.png` C7 · `five_c_presentation-03.png` C7 · `five_c_presentation-04.png` C7 · `five_c_presentation-05.png` C7 · `five_c_presentation-06.png` C7 · `five_c_presentation-07.png` C7 · `five_c_presentation-08.png` C7 · `five_c_presentation-09.png` C7 · `five_c_presentation-10.png` C7 · `five_c_presentation-11.png` C7 · `five_c_presentation-12.png` C7 · `five_c_presentation-13.png` C7 · `five_c_presentation-14.png` C7 · `four_d_presentation-01.png` C7 · `four_d_presentation-02.png` C7 · `four_d_presentation-03.png` C7 · `four_d_presentation-04.png` C7 · `four_d_presentation-05.png` C7 · `four_d_presentation-06.png` C7 · `four_d_presentation-07.png` C7 · `three_e_presentation-01.png` C7 · `three_e_presentation-02.png` C7 · `three_e_presentation-03.png` C7 · `three_e_presentation-04.png` C7 · `three_e_presentation-05.png` C7 · `three_e_presentation-06.png` C7 · `three_e_presentation-07.png` C7 · `three_e_presentation-08.png` C7 | - |
| Skills com renderer (13) | avaliacao-briefing-iqb C8 · briefing-inovacao C8 · experimentacao-inovacao C8 · gerador-cdt C8 · potencial-inovacao C8 · relatorio-3e C8 · relatorio-4d C8 · relatorio-5c C8 · relatorio-final-inovacao C8 · scorecard-inovacao C8 · workshop-3e C8 · workshop-4d C8 · workshop-5c C8 | - |
| Canais (3) | npx C8 · .skill C8 · clone C8 | - |

## Swept

- validation: C1, C3, C6; existing - contratos e validadores sem alteração
- failure modes: C5, C6; existing - teste de biblioteca PPTX ausente e validação do renderizador
- idempotency: existing - manifestos e build_dist --check comparam derivados das fontes versionadas
- authorization: existing - AD-001 exige PR e checks versionamento/testes antes de main; usuário autorizou push e merge
- concurrency: n/a - geração local com diretórios temporários exclusivos; CI controla concorrência de seus jobs
- data lifecycle: C1, C2; arquivos editáveis e amostras derivados de JSON, sem dados de produção
- dependency failure: existing - erro explícito se python-pptx ausente; compare.py falha se LibreOffice ausente
- state transitions: n/a - documentos estáticos
- observability: C7 - índice com hash das referências, página, tamanho e diferença RGB

## Handoff

- **Settled mid-build:** 2026-11-13 - user: "entao se estiver validado de acordo com o /tlc-spec-lean execute commit, push, PR e merge!"
- **Dispatched:** none
- **Boundary:** implementação anterior preparada; verificações retomadas nesta sessão
- **Abandoned:** none
- **Walked:** documentos estáticos convertidos pelo LibreOffice com fontes do repositório; rasterização na mesma escala; tela de aplicativo e navegação não se aplicam
