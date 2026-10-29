# docx_pdf_visual_parity proofs

**HEAD**: c1d1a9e
**Tree**: clean
**Result**: 12 pass, 0 fail; mutations 3 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C2 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C3 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C4 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C10 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C11 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C5 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C6 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C7 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| C8 | `python3 _TOOLS/sync_shared.py --check` | count unknown | - | pass |
| C9 | `/private/tmp/eric-docx-venv/bin/python -m unittest _DESIGN_SYSTEM.tests.test_docx_parity.DocxParityTests.test_` | 1 | - | pass |
| Build | `/private/tmp/eric-docx-venv/bin/python -m compileall -q _DESIGN_SYSTEM/scripts _TOOLS` | - | - | pass |

## Mutations

| Mutation | Location | Killed |
| --- | --- | --- |
| C9 page size tolerance 0.2 -> 20 pt | `_TOOLS/check_docx_pdf_parity.py:98` | yes |
| C2 swap briefing card positions | `_DESIGN_SYSTEM/scripts/render.py:1350` | yes |
| C6 omit briefing source list | `_DESIGN_SYSTEM/scripts/render.py:1355` | yes |
