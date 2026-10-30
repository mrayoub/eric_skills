# Proteção do main checks

Mutations: 3
Build: none - script Python interpretado, sem compilação ou lint no repositório
Plan: `.specs/features/main_branch_protection/plan.md`

5 checks in 1 slice · 1 one-way door · 0 open, of which 0 block

## Checks

### S1 - Entrada protegida no main

**C1** - Política exige PR com zero aprovações obrigatórias e rejeita política sem PR (AC 1)
Proof: `python3 -m pytest -q _TESTS/test_branch_protection.py::MainProtectionTests::test_policy_requires_pr`

**C2** - Política exige exatamente `versionamento` e `testes`, ambos atuais em relação ao main (AC 2)
Proof: `python3 -m pytest -q _TESTS/test_branch_protection.py::MainProtectionTests::test_policy_requires_current_checks`

**C3** - Política aplica os checks a administradores e bloqueia force push e exclusão (AC 3)
Proof: `python3 -m pytest -q _TESTS/test_branch_protection.py::MainProtectionTests::test_policy_prevents_admin_force_delete`

**C4** - Ambos os checks obrigatórios são jobs ativos no evento `pull_request` (AC 2)
Proof: `python3 -m pytest -q _TESTS/test_branch_protection.py::MainProtectionTests::test_workflow_supplies_required_checks_on_pr`

**C5** - A API remota retorna todos os valores da política versionada após a aplicação (AC 4)
Proof: `python3 _TOOLS/check_main_protection.py`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Checks obrigatórios (2) | `versionamento` C2, C4, C5 · `testes` C2, C4, C5 | - |
| Política de entrada (5) | PR C1, C5 · checks atuais C2, C5 · admins C3, C5 · force push C3, C5 · exclusão C3, C5 | - |
| One-way door (1) | proteção de `main` C1-C5 | - |

## Swept

- validation: C1-C3
- failure modes: C5 - consulta ou divergência retorna exit 1
- idempotency: C5 - leitura sem escrita; PUT da mesma política é idempotente
- authorization: C3 - administradores não contornam; API PUT exige admin
- concurrency: C2 - branch atualizado antes do merge
- data lifecycle: n/a - apenas política remota, sem dados de usuário
- dependency failure: C5 - falha da API retorna exit 1
- state transitions: C5 - política aplicada e lida
- observability: C5 - diagnóstico de cada campo divergente

## Handoff

- **Settled mid-build:** user: "3" - escolheu PR + `versionamento` + `testes`
- **Dispatched:** none
- **Boundary:** pending
- **Abandoned:** none
- **Walked:** n/a - configuração sem tela própria
