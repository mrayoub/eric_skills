# Skills prontas versionadas verification

**Verdict**: PASS
**Mutations**: 3 - probed C1, C3, C4; all killed
**Proofs**: `proofs.md` at 155705a (8 pass, 0 fail; 3 mutations killed)
**Verifier**: independent sub-agent (author != verifier)

## Findings

| Finding | Evidence | Fix | Closed |
| --- | --- | --- | --- |
| C5 can pass when the `versionamento` job or its package check is disabled, leaving divergent packages unblocked on push or PR. | `_TESTS/test_distribution.py::ReleaseSafetyTests::test_versionamento_checks_checked_in_packages` only checked that the command string was present in the job's steps. Adding `if: false` to either left the proof green. | Assert the exact active job condition and absence of a step-level `if`. | `d219ad8` - C5 proof checks both guards |

## Own examples

- An empty ready directory produced exit 1, reported all three expected names, and stayed empty.
- Changing only `SHA256SUMS` by one newline produced exit 1, named that manifest, and left its bytes untouched.
