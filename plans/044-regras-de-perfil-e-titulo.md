# Plan 044: Tornar confiáveis a regra do título e os perfis de conteúdo, e alinhar as instruções das skills a elas

> **Executor instructions**: Siga passo a passo; rode cada verificação; pare nas STOP conditions; atualize `plans/README.md`.
>
> **Drift check (rode primeiro)**: `git diff --stat 595f3b0..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/content-profiles.json _DESIGN_SYSTEM/tests/test_render.py experimentacao-inovacao relatorio-final-inovacao`

## Status

- **Priority**: P1 · **Effort**: S · **Risk**: LOW · **Depends on**: none · **Category**: bug
- **Planned at**: commit `595f3b0`, 2026-10-09 (auditoria pós-planos 033–043)

## Why this matters

Duas regras novas do renderizador (`_DESIGN_SYSTEM/scripts/render.py`, função `validate`) têm furos verificados, e as
instruções das skills que as usam induzem o agente a falhar nelas:

1. **Título sem o tipo do entregável** usa substring sem limite de palavra: "Debriefing das operações de liquidação"
   (tipo `briefing`) é recusado por conter "briefing"; "Relatorio 4D …" (sem acento) passa e "Relatório 4D …" não.
2. **Perfil de conteúdo** (`metadata.content_profile`):
   - é ignorado quando `metadata.completeness` falta, embora o resto da validação trate ausência como completa;
   - aceita seções vazias e títulos sem corpo como se fossem a seção exigida.
3. **Instruções** (`experimentacao-inovacao`, `relatorio-final-inovacao`) não dizem que a apresentação também exige as
   cinco seções do schema (`context`, `method`, `findings`, `recommendation`, `next_steps`) nem que o título de cada
   slide precisa ter de 4 a 12 palavras e dizer a conclusão (validador `validators/executive_presentation.py`); um guia
   (`pitch-canvas-executivo.md`) chega a dizer que "não há número fixo de slides ou palavras".
4. **Cabeçalho × nome do entregável**: com perfil, o cabeçalho mostra o rótulo do tipo ("Plano de experimentação",
   "Evidências e recomendação") e não o nome que a skill usa ("Modelo de experimentação", "Relatório final").

## Current state

- `render.py:130` — `effective_completeness = meta.get("completeness") or "complete"` (usado na validação do schema).
- `render.py:136-153` — bloco do perfil:
  ```python
  content_profile = meta.get("content_profile")
  ...
  if meta.get("completeness") == "complete":          # <- ignora ausência (bug)
      present = {block.get("data", {}).get("section_key") for block in content.get("blocks", [])
                 if block.get("type") != "page_break" and block_text(block).strip()}   # <- heading e vazio contam
  ```
  `block_text` (por volta da linha 245) devolve `json.dumps(data)` quando não há texto, então nunca é vazio.
- `render.py:155-160` — regra do título:
  ```python
  title_key = " ".join(str(content.get("title", "")).casefold().split())
  for name in (DELIVERABLE_LABELS.get(kind, ""), kind.replace("_", " ")):
      if name and name.casefold() in title_key:
          raise ValueError(...)
  ```
- `_DESIGN_SYSTEM/content-profiles.json` — perfis `experimentation_model`, `experimentation_presentation`, `final_report`, cada um com `label` e `required_sections`.
- Cabeçalho: `DELIVERABLE_LABELS[content["deliverable_type"]]` em `render_html` (eyebrow), `render_docx`, `render_pptx` e no `deliverable_label` passado ao `pdf_reportlab.render_pdf` (`render_pdf_reportlab`, perto de `render.py:1024`).
- Instruções: `experimentacao-inovacao/SKILL.md` (tabela "Entrega em arquivo"), `experimentacao-inovacao/references/avaliacao-do-mvp.md:26`, `relatorio-final-inovacao/references/pitch-canvas-executivo.md:27`, `relatorio-final-inovacao/references/relatorio-final.md:16`.
- Convenção: mensagens de erro em português dizendo como corrigir; testes em `_DESIGN_SYSTEM/tests/test_render.py`, classe `ContentProfileTests` como modelo.

## Steps

1. **Completude:** no bloco do perfil, troque `meta.get("completeness") == "complete"` por `effective_completeness == "complete"`.
2. **Seção presente de verdade:** conte só blocos que não sejam `heading`/`page_break` e tenham conteúdo real: `text`,
   `description`, `value` ou `content` não vazios, ou `items`/`rows`/`cards` com elementos. Não use `block_text`.
3. **Título:** compare em texto sem acento (NFD, sem marcas) e em minúsculas, com limite de palavra
   (`re.search(rf"(?<!\w){re.escape(nome)}(?!\w)", titulo)`), para o rótulo e para o nome do tipo.
4. **Cabeçalho com perfil:** crie `header_label(content)` que devolve `content-profiles.json[perfil]["label"]` quando
   houver perfil válido, senão `DELIVERABLE_LABELS[tipo]`; use nos quatro renderizadores e no PDF. A regra do título
   passa a comparar também com o rótulo do perfil.
5. **Instruções:**
   - `experimentacao-inovacao/SKILL.md` e `avaliacao-do-mvp.md`: a apresentação traz as cinco seções do schema e as duas do perfil; `direction` vem depois de `recommendation` e `next_steps` e não as substitui; cada slide tem título-mensagem de 4 a 12 palavras (exemplo: "O MVP funcionou, mas a economia de tempo não foi medida"); a `section_key` vai no bloco de conteúdo.
   - `pitch-canvas-executivo.md:27` e `relatorio-final.md:16`: troque "não há número fixo… de palavras" e "podem receber títulos narrativos" pelas regras do validador (capa ≤ 35 palavras; título 4–12 palavras; ≤ 4 blocos e ≤ 60 palavras por slide).
6. **Testes** (classe `ContentProfileTests` e uma nova `TitleRuleTests`): completeness ausente com perfil → erro;
   seção só com heading → erro; seção com `text: ""` → erro; "Debriefing das operações" (briefing) → aceito;
   "Relatorio 4D do portal" (four_d_report) → recusado; cabeçalho do PDF/HTML de um `experiment_plan` com perfil mostra
   "Modelo de experimentação". Cada teste deve falhar no código antigo (`git stash` só de `render.py`).
7. Sync, fontes, `build_catalog.py --bump` (minor nas skills cujo texto mudou; patch nas demais), suíte.

## Commands

| Purpose | Command | Expected |
|---|---|---|
| Testes | `python -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` (use `_TESTS/requirements-dev.txt`) | `0 failed` |
| Checagens | `python _TOOLS/sync_shared.py --check && python _TOOLS/build_sources.py --check && python _TOOLS/build_catalog.py --check && python _TOOLS/check_channels.py` | exit 0 |

## Done criteria

- [x] Os 6 casos do Step 6 passam e falhavam antes · [x] as 18 amostras renderizam · [x] suíte `0 failed` (189 testes, 1.511 subtestes) · [x] catálogo em dia

## STOP conditions

- Alguma amostra de `_SAMPLES_ENTREGAVEIS` passa a ser recusada pela regra do título corrigida.
- O cabeçalho com perfil exigiria mudar schemas.
