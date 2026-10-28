# Paridade visual DOCX/PDF dos entregáveis ERIC verification

**Verdict**: FAIL
**Mutations**: 3 - probed C9, C2, C6; 2 killed, 1 survived
**Proofs**: `proofs.md` at 6d91edf (10 passing checks before mutation; mutation run returned 1)
**Verifier**: independent sub-agent (author != verifier)

## Findings

| Finding | Evidence | Fix | Closed |
| --- | --- | --- | --- |
| C9 does not prove that changed page dimensions fail. | Mutation `C9 page size tolerance 0.2 -> 20 pt` survived. `test_comparator_artifacts_and_failures` checks only page count and clipping, not page size. | Assert a same-count pair whose width differs beyond 0.2 pt produces `page_size`; retain a near-boundary passing case. | |
| C3 and C9 accept visibly different composition on later report pages. | `evidence/report.json` gives `four_d_report` pages 2 and 3 blue-region IoU 0.0083 and 0.0838, mean RGB difference 43.702 and 48.059, yet `failures` is empty. `test_report_structure_and_safe_area` asserts blue overlap only on `pages[0]`. The `four-d-report-page-one.png` capture also shows shifted section placement and different card color/spacing against the PDF. | Align the DOCX layout with the PDF on all pages and add per-page visual acceptance bounds, with explicit review of intended differences. | |
| C6 does not hold the required state or absence of duplication. | `test_all_samples_semantic_parity` checks title, ID, version, source IDs and block text with `assertIn`, but never asserts `metadata.completeness`/the rendered state or occurrence counts. Duplicated content can pass. | Assert the rendered state and compare expected occurrence counts or structured block sequence in both formats. | |

## Own boundary examples

- C9: equal page counts, width 595.28 vs 595.49 pt (0.21 pt difference) produced `page_size`, as required.
- C2: deleting `identificacao_versao` from the seven-slot briefing layout raised `ValueError: executive_one_page: faltam slots do layout`.

The production files were restored byte-for-byte after mutation probes. The existing `proofs.md` was restored after the check script wrote its mutation result.
