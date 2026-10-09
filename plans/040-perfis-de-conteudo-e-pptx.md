# Plan 040: Perfis de conteúdo que exigem as seções novas, tabelas nativas no PPTX e quebra de texto por palavra

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat c71cb41..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/contracts experimentacao-inovacao relatorio-final-inovacao`

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW (validação só para documentos que declaram o perfil; PPTX muda a forma das tabelas, não o conteúdo)
- **Depends on**: 039 (entregáveis da experimentação), 036 (motor único)
- **Category**: qualidade dos entregáveis
- **Planned at**: commit `c71cb41`, 2026-10-09

## Why this matters

A revisão do design system de 2026-10-09 achou três lacunas que nenhum plano cobria:

1. **Contratos não exigem as seções novas.** Os entregáveis da experimentação (039) e do relatório final reusam
   tipos genéricos. O renderizador só valida as seções mínimas do tipo; faltar "MVP a construir" no Modelo de
   experimentação, "Avaliação do MVP" na apresentação ou a decisão no relatório final passa sem aviso.
2. **No PPTX, tabelas viram texto** (`Dimensão | Avaliação` dentro da caixa de texto do corpo).
3. **No PPTX, o texto é cortado a cada 650 caracteres** (`line[i:i+650]`), às vezes no meio de uma palavra.

## Current state (em `c71cb41`)

- `render.py`, `validate()`: schema do tipo + validadores semânticos; `metadata` aceita campos extras
  (`deliverable-content.schema.json`, `additionalProperties: true`).
- `render_pptx()`: acumula `block_text` dos blocos de cada seção em linhas; tabelas viram `" | ".join(...)`;
  `for chunk in [line[i:i+650] ...]` divide por caracteres; nova lâmina a cada 650 caracteres ou 8 linhas.
- `experimentacao-inovacao`: Modelo de experimentação = `experiment_plan` com "seções extras" (MVP a construir,
  escopo, cronograma, gate de início); Apresentação = `executive_presentation` com avaliação do MVP e direcionamento.
- `relatorio-final-inovacao`: relatório = `evidence_recommendation` com blocos adicionais (histórico, execução, decisão).

## Scope

**In scope**: `_DESIGN_SYSTEM/content-profiles.json` (novo), `render.py` (validação do perfil; PPTX),
`_DESIGN_SYSTEM/tests/test_render.py`, `_DESIGN_SYSTEM/README.md`, `experimentacao-inovacao` (SKILL.md e
referências: nomes dos perfis e `section_key`s), `relatorio-final-inovacao` (idem), cópias do sync, versões
(`build_catalog.py --bump`), `catalog.json`, `plans/README.md`.

**Out of scope**: novos `deliverable_type`; PDF (ReportLab); layouts.

## Steps

### Step 1: Perfis de conteúdo

`_DESIGN_SYSTEM/content-profiles.json`:

| Perfil (`metadata.content_profile`) | Tipo | Seções obrigatórias (`section_key`) |
|---|---|---|
| `experimentation_model` | `experiment_plan` | `mvp_build`, `scope`, `schedule`, `start_gate` |
| `experimentation_presentation` | `executive_presentation` | `mvp_evaluation`, `direction` |
| `final_report` | `evidence_recommendation` | `history`, `feasibility`, `decision` |

Em `validate()`: se `metadata.content_profile` existir, ele precisa estar no arquivo e ser do mesmo
`deliverable_type`; em versões `complete`, cada seção obrigatória precisa de ao menos um bloco com aquele
`section_key` e texto visível. Mensagem: `"<perfil>: falta a seção <key> (<rótulo>); acrescente-a ou marque a versão como parcial"`.
Sem o campo, nada muda.

### Step 2: Skills declaram o perfil

- `experimentacao-inovacao`: tabela "Entrega em arquivo" com o perfil e as `section_key`s; `execucao-e-mvp.md` e
  `avaliacao-do-mvp.md` citam as chaves.
- `relatorio-final-inovacao`: `relatorio-final.md` e "Entrega em arquivo" com `final_report` (histórico, viabilidade, decisão).

### Step 3: Tabelas nativas no PPTX

Em `render_pptx`, cada bloco `table` vira uma tabela do PowerPoint (`shapes.add_table`) na área do corpo: cabeçalho
com fundo `document_primary` e texto `inverse`, corpo `text_body`, fonte `slide_body` limitada a 12 pt mínimo.
Até 8 linhas de dados por lâmina; mais linhas continuam em lâminas "(continuação)" repetindo o cabeçalho. Legenda
(`data.title`/vista) acima da tabela. Texto antes da tabela sai na lâmina anterior.

### Step 4: Quebra por palavra

Troque o corte por caracteres por divisão em limites de palavra (nenhuma palavra partida entre lâminas);
mantenha o limite de 650 caracteres e 8 linhas por lâmina.

### Step 5: Testes

- Perfil: documento completo sem `mvp_build` falha com a mensagem; parcial passa; perfil de outro tipo falha;
  perfil desconhecido falha; documento sem perfil inalterado.
- PPTX: amostra com tabela gera um `GraphicFrame` com `has_table`, cabeçalho e linhas; tabela de 20 linhas ocupa
  3 lâminas com cabeçalho repetido.
- PPTX: parágrafo de 2.000 caracteres — todas as palavras íntegras ao juntar as lâminas.

### Step 6: Sync, versões e pacotes

`sync_shared.py`, `build_sources.py`, `build_catalog.py --bump` (as skills que mudaram), suíte completa,
`build_dist.py`.

## Done criteria

- [ ] `content-profiles.json` e validação; skills declaram os perfis
- [ ] Tabelas nativas no PPTX com continuação e cabeçalho repetido
- [ ] Nenhuma palavra partida entre lâminas
- [ ] Testes novos passam e falham no código anterior; suíte `0 failed`; catálogo e pacotes em dia

## STOP conditions

- A validação do perfil exigiria mudar o schema de algum tipo.
- Algum teste existente depende do texto `" | "` das tabelas no PPTX de forma que o conteúdo mude.
