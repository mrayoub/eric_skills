# Paridade visual DOCX/PDF checks

Mutations: 3
Build: `/private/tmp/eric-docx-venv/bin/python -m compileall -q _DESIGN_SYSTEM/scripts _TOOLS`
Plan: `.specs/features/docx_pdf_visual_parity/plan.md`

11 checks in 3 slices · 0 one-way doors · 0 open

## Checks

### S1 - Composição por tipo

**C1** - Os 19 pares amostrais têm orientação A4 e a mesma quantidade de páginas após conversão do DOCX pelo LibreOffice (AC 1)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_all_sample_page_counts`

**C2** - O Briefing DOCX mostra os sete slots, com três cartões lado a lado, em uma página A4 paisagem (AC 2)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_one_page_briefing_geometry`

**C3** - Os relatórios e registros preservam ordem, faixas, cartões, tabelas e conteúdo dentro da área segura do PDF (AC 3)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_report_structure_and_safe_area`

**C4** - Test Card e Learning Card têm quatro campos em ordem, visíveis em uma página A4 retrato (AC 4)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_cards_one_page_and_order`

**C10** - O logo CCEE mantém a proporção visual da arte original nas 19 primeiras páginas convertidas, sem alterar a paginação (AC 10)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_all_sample_logos_uncropped`

**C11** - As faixas azuis têm recuo de 12 pt no DOCX; na CDT, a primeira faixa mantém o recuo e a altura visual do PDF sem página extra (AC 11)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_cdt_section_padding_matches_pdf`

### S2 - Edição e identidade

**C5** - Os 19 DOCX mantêm texto e tabelas editáveis, sem imagem de página inteira (AC 5)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_all_samples_editable`

**C6** - Os 19 pares preservam título, ID, versão, estado, blocos e citações aplicáveis (AC 6)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_all_samples_semantic_parity`

**C7** - Ausência de dependência ou fonte falha com mensagem explícita (AC 7)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_missing_font_fails_explicitly`

### S3 - Distribuição e prova

**C8** - As treze skills recebem o mesmo renderizador e a sincronização passa (AC 8)
Proof: `python3 _TOOLS/sync_shared.py --check`

**C9** - O comparador produz uma linha e uma imagem por tipo e reprova página diferente ou conteúdo cortado (AC 9)
Proof: `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_comparator_artifacts_and_failures`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| DOCX em `profiles.json` (19) | `briefing` C1/C5/C6 · `briefing_one_page` C1/C2/C5/C6 · `briefing_improvement_questionnaire` C1/C5/C6 · `briefing_validation` C1/C5/C6 · `innovation_potential_assessment` C1/C5/C6 · `four_d_workshop_record` C1/C3/C5/C6 · `four_d_report` C1/C3/C5/C6 · `three_e_workshop_record` C1/C3/C5/C6 · `three_e_report` C1/C3/C5/C6 · `innovation_scorecard` C1/C5/C6 · `experiment_plan` C1/C5/C6 · `test_card` C1/C4/C5/C6 · `learning_card` C1/C4/C5/C6 · `experiment_report` C1/C3/C5/C6 · `evidence_recommendation` C1/C3/C5/C6 · `five_c_workshop_record` C1/C3/C5/C6 · `five_c_report` C1/C3/C5/C6 · `cdt` C1/C5/C6 · `cdt_analysis` C1/C5/C6 | - |
| DOCX nos layouts (4) | `report_portrait` C1/C3 · `report_landscape` C1/C3 · `executive_one_page` C1/C2 · `card_portrait` C1/C4 | - |
| Fontes de indisponibilidade (2) | biblioteca ausente C7 · arquivo de fonte ausente C7 | - |
| Falhas do comparador (2) | páginas diferentes C9 · conteúdo cortado C9 | - |
| Skills sincronizadas (13) | `avaliacao-briefing-iqb` C8 · `briefing-inovacao` C8 · `experimentacao-inovacao` C8 · `gerador-cdt` C8 · `potencial-inovacao` C8 · `relatorio-3e` C8 · `relatorio-4d` C8 · `relatorio-5c` C8 · `relatorio-final-inovacao` C8 · `scorecard-inovacao` C8 · `workshop-3e` C8 · `workshop-4d` C8 · `workshop-5c` C8 | - |

C10 percorre os mesmos 19 tipos da primeira linha e mede o logo na primeira página convertida de cada um.

## Swept

- validation: C1, C3, C7, C9
- failure modes: C7, C9
- idempotency: existing - o manifesto do renderizador usa o mesmo JSON canônico, perfil e tokens para regenerar derivados
- authorization: n/a - geração local sem controle de acesso
- concurrency: n/a - cada execução usa um diretório temporário exclusivo
- data lifecycle: existing - amostras são regeneradas do `input.json` versionado
- dependency failure: C7
- state transitions: n/a - documentos estáticos, sem estados de execução persistidos
- observability: C9 - relatório de comparação com linha e imagem para cada tipo

## Handoff

- **Settled mid-build:** 2026-10-28 - user: "aprovado pode continuar e preciso que vc de prioridade a presevar a edicao"
- **Settled mid-build:** 2026-10-29 - user: "vc consegue resolver o problema do corte do logo da ccee?"
- **Settled mid-build:** 2026-10-29 - user: "ha como aplicar o padding nos blocos azuis de titulo no docx???"
- **Dispatched:** Verifier at `6d91edf` (returned; três achados corrigidos)
- **Boundary:** C1-C11 fechadas; 19 pares com páginas e orientação iguais, zero caractere cortado, edição preservada, logo inteiro e faixas azuis com recuo horizontal no DOCX convertido. A CDT iguala o recuo e a altura da primeira faixa do PDF. Evidência visual em `evidence/report.json` e nas 34 imagens lado a lado, atualizadas em 29/10/2026.
- **Abandoned:** none
- **Walked:** n/a - não há tela de aplicativo
