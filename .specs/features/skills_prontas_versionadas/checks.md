# Skills prontas versionadas checks

Mutations: 3
Build: `python3 _TOOLS/build_dist.py --check`; `python3 _TOOLS/build_catalog.py --check`
Plan: `.specs/features/skills_prontas_versionadas/plan.md`

6 checks in 1 slice · 1 one-way door · 0 open, of which 0 block

## Checks

### S1 - Pacotes prontos no commit

**C1** - A construção grava exatamente 14 pacotes e dois manifestos em `_SKILLS_PRONTAS/` (AC 1)
Proof: `python3 -m pytest -q _TESTS/test_distribution.py::PackageTests::test_complete_build_has_exact_catalog_set`

**C2** - `--check` em checkout íntegro sai 0 e não altera os bytes nem os nomes da pasta (AC 2)
Proof: `python3 -m pytest -q _TESTS/test_distribution.py::PackageTests::test_checked_in_packages_are_current`

**C3** - `--check` sai 1 e nomeia arquivos alterados, ausentes e extras (AC 3)
Proof: `python3 -m pytest -q _TESTS/test_distribution.py::PackageTests::test_check_rejects_missing_changed_and_extra_files`

**C4** - Reconstrução remove pacote obsoleto e atualiza SHA256SUMS (AC 4)
Proof: `python3 -m pytest -q _TESTS/test_distribution.py::PackageTests::test_build_removes_obsolete_package`

**C5** - O job `versionamento` roda a checagem de pacotes em pull requests e push no main (AC 5)
Proof: `python3 -m pytest -q _TESTS/test_distribution.py::ReleaseSafetyTests::test_versionamento_checks_checked_in_packages`

**C6** - O workflow de Release e o publicador leem `_SKILLS_PRONTAS/`, sem referência ativa a `_DIST/` (AC 6)
Proof: `python3 -m pytest -q _TESTS/test_distribution.py::ReleaseSafetyTests::test_release_reads_ready_skills`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Pacotes por skill (14) | C1, table-driven over all 14 entries in catalog.json | - |
| Manifestos (2) | `catalog.json` C1, C2 · `SHA256SUMS` C1, C2, C4 | - |
| Desvios (3) | alterado C3 · ausente C3 · extra C3 | - |
| Caminho público (1) | `_SKILLS_PRONTAS/` C1, C5, C6 | - |

## Swept

- validation: C3
- failure modes: C3, C5
- idempotency: C2
- authorization: n/a - comandos locais e workflow já autorizado pelo GitHub
- concurrency: existing - workflow de Release usa grupo `release` sem cancelamento
- data lifecycle: C4
- dependency failure: existing - `run_checks()` retorna exit 1 quando sync, fontes ou catálogo divergem
- state transitions: C1-C4
- observability: C3 - diagnóstico nomeia arquivos divergentes

## Handoff

- **Settled mid-build:** none
- **Dispatched:** Verifier at `b17f456` - pending
- **Boundary:** C1-C6 closed at `b17f456`
- **Abandoned:** none
- **Walked:** n/a - sem interface gráfica
