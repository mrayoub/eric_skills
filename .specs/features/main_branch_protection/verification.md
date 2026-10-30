# Proteção do main verification

**Verdict**: PASS
**Mutations**: 3 - probed C1, C2, C3; all killed after C3 fix
**Proofs**: `proofs.md` at 16e6841
**Verifier**: independent sub-agent (author != verifier)

## Findings

| Finding | Evidence | Fix | Closed |
| --- | --- | --- | --- |
| C3 can pass even when deletion protection is never checked | Mutation `exclusão consulta force push duas vezes` survived its original proof. The original test asserted only a total of three errors. | Test each field independently and assert its specific error. | `8ea4256` - C3 proof checks each field |

## Mutation evidence

The standard `mutate.py` runner could not create `.git/tlc-mutation-journal.json` in the sandbox (`PermissionError`). The same three mutations were applied to copies of the policy, script, workflow, and test in a temporary directory. Each narrow proof passed on the unmutated copy before its mutation ran. No production or test file in the repository was changed.

| Mutation | Narrow proof | Result |
| --- | --- | --- |
| PR ausente deixa de ser detectado | C1 | killed by assertion |
| strict invertido | C2 | killed by assertion |
| exclusão consulta force push duas vezes | C3 | killed after `8ea4256` |

## Own examples

At 16e6841, `problems()` reports `quantidade de aprovações obrigatórias divergente` when the remote approval count is 2, and `checks obrigatórios diferem de versionamento e testes` when the remote contexts include an extra `lint` job. Both examples pass. The read-only GitHub API response also matches the recorded policy: PR with zero required approvals, strict checks `versionamento` and `testes`, admin enforcement, and disabled force push and deletion.
