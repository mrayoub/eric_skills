# Entregáveis oficiais checks

Mutations: 3
Build: `python3 _TOOLS/sync_shared.py --check`; `python3 _TOOLS/build_catalog.py --check`; `python3 _TOOLS/build_dist.py --check`
Plan: `.specs/features/entregaveis_oficiais/plan.md`

18 checks em seis slices do plano, quatro contratos persistentes, nenhuma questão aberta. C18 acrescentado após o achado F1 do Verifier; preserva AC17/33 nas versões parciais e inconclusivas.

## Checks

**C1** - Seleção oficial padrão e acesso explícito aos depreciados (AC 1, 2, 3, 4)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_routing_guidance`

**C2** - Galeria oferece os quatro modelos por método e preserva Test Card (AC 5)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_gallery_catalog`

**C3** - Layout Studio configura e reabre etapas aplicadas (AC 6)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_studio_application`

**C4** - Receita do relatório exige texto e fonte em cada campo obrigatório (AC 7, 8, 9, 13, 14, 15, 16)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_report_recipe`

**C5** - Aplicação padrão preserva nomes, funções e ordem de cada playbook (AC 10, 11, 12)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_standard_methods`

**C6** - Receita da apresentação cobre as etapas e o fechamento em ordem (AC 19, 20, 24)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_presentation_recipe`

**C7** - Decisão condicional exige declaração explícita e conteúdo quando verdadeiro (AC 21, 22, 23)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_conditional_decision`

**C8** - Densidade limita cada slide sem impor seis slides ao deck (AC 27)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_slide_density`

**C9** - Pocket completa não exige fases excluídas por desenho (AC 17, 32, 33)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_pocket_scopes`

**C10** - Adaptações preservam significados e sessões de profundidades diferentes (AC 18, 34, 35, 36)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_adapted_and_mixed`

**C11** - Inventário rejeita cobertura ambígua e IDs repetidos (AC 18, 31, 33)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_application_validation`

**C12** - Seis JSONs geram todos os formatos previstos com conteúdo e geometria (AC 25, 26, 28)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_render_formats`

**C13** - Contratos anteriores continuam renderizáveis com rótulo depreciado (AC 3, 4, 30)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_legacy_compatibility`

**C14** - Tom comum fica disponível em cada skill e exemplos preservam evidências (AC 37, 38, 39, 40, 41)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_editorial_guidance`

**C15** - Entrada inválida falha antes de criar derivados finais (AC 16, 31)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_invalid_cli`

**C16** - Fontes distribuídas, versões e pacotes permanecem sincronizados (AC 29)
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_distribution`

**C17** - Configuração, exportação e reimportação das etapas funcionam pelos controles reais do Studio; a galeria abre os seis oficiais (AC 5, 6).
Proof: `node .specs/features/entregaveis_oficiais/walk-studio.cjs`

**C18** - Oficial parcial ou inconclusivo conserva inventário e receita ordenada; a seção sem registro exibe pendência explícita, sem exigir fonte inexistente nem aceitar afirmação sem fonte (AC 17, 33).
Proof: `python3 -m pytest -q _DESIGN_SYSTEM/tests/test_official_deliverables.py -k test_partial_recipe`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Tipos oficiais (6) | four_d_official_report C4 C12 · four_d_official_presentation C6 C12 · three_e_official_report C4 C12 · three_e_official_presentation C6 C12 · five_c_official_report C4 C12 · five_c_official_presentation C6 C12 | - |
| Métodos (3) | 4D C5 C9 C10 · 3E C5 C9 C10 · 5C C5 C9 C10 | - |
| Variantes por método (3) | standard C5 · adapted C10 · pocket C9 | - |
| Receita do relatório (8 grupos) | título e finalidade C4 C12 · introdução C4 · estruturação C4 · descrição C4 · execução C4 · desfecho C4 · conclusão C4 · recomendações C4 | - |
| Receita do pitch (7 grupos) | contextualização C6 · estruturação C6 · execução C6 · conclusão C6 · recomendações C6 · decisão C7 · call to action C6 | - |
| Decisão (4 estados) | true C7 · false C7 · ausente C7 · desconhecida C7 | - |
| Cobertura por sessão (4 estados) | integral C5 · pocket por desenho C9 · lacuna C9 C18 · sessões mistas C10 | - |
| Landing (4) | identificadores C12 C13 · receita dinâmica C4 C6 · decisão C7 · inventário C11 | - |
| Entidades (10) | SKILL C1 · TIPO_ENTREGAVEL C12 · CONTRATO C4 · PERFIL_VISUAL C12 · JSON_CANONICO C12 · APLICACAO_METODO C11 · SESSAO C10 · ETAPA_APLICADA C11 · ARQUIVO_DERIVADO C12 · PACOTE C16 | - |
| Leitores (7) | skills C1 C14 · renderer C12 · galeria C2 C17 · Studio C3 C17 · amostras C12 · catálogo C16 · pacotes C16 | - |
| Erro e formatos (2 resultados) | entrada válida código 0 C12 · entrada inválida código não zero sem derivados C15 | - |
| Tom (6) | 4D relatório C14 · 4D apresentação C14 · 3E relatório C14 · 3E apresentação C14 · 5C relatório C14 · 5C apresentação C14 | - |

## Swept

- validation: C4 C6 C7 C8 C11 C15
- failure modes: C9 C15; existing - manifesto registra dependência de exportação indisponível
- idempotency: existing - renderer usa artifact_id, content_version e JSON canônico; C12
- authorization: n/a - arquivos locais sem API externa
- concurrency: n/a - geração local explícita, sem serviço concorrente novo
- data lifecycle: C3 C13 C16; JSONs anteriores preservados
- dependency failure: existing - contrato de unavailable no manifesto e testes de renderização
- state transitions: C9 C11 para completo, parcial e inconclusivo no escopo
- observability: C15; existing - erros identificam campos e manifesto registra hashes

## Handoff

- **Settled mid-build:** user autorizou commit, merge e push ao GitHub após testes passarem; user: "aprovado" em 2026-11-17; padrão dos playbooks, adaptação/pocket nos três métodos e tom da autora nos seis oficiais confirmados na revisão anterior.
- **Dispatched:** Verifier final independente solicitado em 2026-11-17 no HEAD `f2553f5`, diff `e53a71c..f2553f5`, após `proofs.md` registrar 20 provas verdes. Revisão editorial preliminar concluída em `editorial-review.md`. Fontes visuais são inspiração, sem capturas vinculantes; controles reais do Studio e galeria provados por C17.
- **Boundary:** trabalho local concluído após retomada da sessão `01a1ea00-a992-7d32-bd43-030e69693142`: implementação `f2553f5`, quatro achados do Verifier corrigidos em `616653b`; suíte completa com 349 testes e 2.408 subtestes verdes; 21 provas verdes e três mutações mortas. Catálogo, pacotes e canais sincronizados. Próximo passo autorizado: push, PR, checks `versionamento`/`testes` e merge em main. As alterações preexistentes de `pptx_pdf_visual_parity` permanecem fora dos commits desta feature.
- **Abandoned:** nenhum.
- **Walked:** Chrome headless local: seleção dos três tipos de apresentação oficial, botão Configurar etapas aplicadas, prévia/exportação e importação por arquivo, desenho de slot e seleção de sua fonte; galeria abre HTML/PDF dos seis oficiais. Resultado PASS em evidence/walk.json; sem captura vinculante.
