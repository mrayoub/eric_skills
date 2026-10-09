# Template Mural — Workshop 3E de Estruturacao da Solucao

## Índice

- [Visao geral do board](#visao-geral-do-board)
- [Area 1 — Abertura](#area-1--abertura)
- [Area 2 — E1: Esclarecer](#area-2--e1-esclarecer)
- [Area 3 — E2: Estruturar](#area-3--e2-estruturar)
- [Area 4 — E3: Experimentar](#area-4--e3-experimentar)
- [Area 5 — Fechamento](#area-5--fechamento)
- [Convencoes visuais](#convencoes-visuais)
- [Notas de implementacao](#notas-de-implementacao)

> **Nota:** este template nao utiliza emojis, em conformidade com a politica zero emojis do ERIC (ADR-012). As etapas sao identificadas por codigos de cor e nomes.

Este documento descreve a estrutura do board Mural a ser criado automaticamente pela skill `facilitate_3e_workshop`. O board segue a metodologia 3E e serve como suporte visual e colaborativo para o workshop.

Use o board em qualquer fase, registrando datas e versões. O E3 prepara critérios quando o teste ainda não ocorreu; resultados e aprendizados reais podem ser anexados após a execução, mesmo fora de `experimentation`.

---

## Visao geral do board

O board e dividido em **5 areas** principais, dispostas em fluxo horizontal (da esquerda para a direita):

```
+----------+  +----------+  +----------+  +----------+  +----------+
| ABERTURA |  | E1       |  | E2       |  | E3       |  |FECHAMENTO|
| Solucao  |->|ESCLARECER|->|ESTRUTURAR|->|EXPERIMENT|->| Outputs  |
| Candidata|  | 20-30min |  | 70-90min |  | 40-50min |  |          |
+----------+  +----------+  +----------+  +----------+  +----------+
```

---

## Area 1 — Abertura

**Cor:** Cinza claro (#E0E0E0)
**Posicao:** Canto superior esquerdo

### Elementos

| Elemento | Tipo | Conteudo |
|---|---|---|
| Titulo do board | Texto grande | "Workshop 3E: [nome da solucao]" |
| Solucao candidata | Texto | Resumo da solução candidata com fonte e versão |
| Desafio de origem | Texto | Referência ao desafio e, se houver, à decisão BP1 |
| Participantes | Lista | Nomes ou quantidade |
| Timer | Widget | 3 horas |

---

## Area 2 — E1: Esclarecer

**Cor:** Amarelo (#FFF3CD)
**Posicao:** Apos abertura
**Tempo:** 20-30 min

### Subsecao 2.1 — Definicao da Solucao

| Elemento | Tipo | Conteudo |
|---|---|---|
| Titulo da secao | Texto | "[E1] Esclarecer" |
| Problema | Post-it | "Qual dor especifica esta solucao resolve?" |
| Resultado esperado | Post-it | "O que queremos alcancar?" |
| Limites | Post-it | "O que esta dentro e fora do escopo?" |
| Valor | Post-it | "Qual o valor esperado para a CCEE?" |

### Subsecao 2.2 — Criterios de Sucesso

| Elemento | Tipo | Conteudo |
|---|---|---|
| Instrucao | Texto | "Como saberemos se deu certo?" |
| Zona de criterios | Area de post-its | Participantes escrevem indicadores de sucesso |
| Criterio 1 | Post-it | Exemplo: "Reduzir o tempo de processo; fechar limiar com linha de base antes da coleta" |
| Criterio 2 | Post-it | (em branco) |
| Criterio 3 | Post-it | (em branco) |

---

## Area 3 — E2: Estruturar

**Cor:** Azul claro (#CCE5FF)
**Posicao:** Centro
**Tempo:** 70-90 min

### Subsecao 3.1 — Matriz de Priorizacao

| Elemento | Tipo | Conteudo |
|---|---|---|
| Titulo da secao | Texto | "[E2] Estruturar" |
| Instrucao | Texto | "Classifique o que a solucao precisa ter" |
| **Precisa ter (MVP)** | Area verde | Funcionalidades minimas para funcionar |
| **Pode evoluir depois** | Area amarela | Funcionalidades desejaveis |
| **Nao entra agora** | Area vermelha | Fora de escopo neste momento |

### Subsecao 3.2 — Levantamento

| Elemento | Tipo | Conteudo |
|---|---|---|
| Instrucao | Texto | "O que ja existe vs. o que precisa ser desenvolvido?" |
| Coluna "Ja existe" | Area | O que ja temos internamente que pode ser aproveitado |
| Coluna "Precisa criar" | Area | O que precisamos construir ou contratar |

### Subsecao 3.3 — Plano de Acao

| Elemento | Tipo | Conteudo |
|---|---|---|
| Instrucao | Texto | "Defina acoes, responsaveis e prazos" |
| Tabela de acoes | Grid com colunas | **O que fazer** / **Responsavel** / **Apoios** / **Prazo** |
| Linha 1 | Post-it | (acao 1) |
| Linha 2 | Post-it | (acao 2) |
| Zona de prazos | 3 colunas | 0-30 dias / 30-60 dias / 60+ dias |

---

## Area 4 — E3: Experimentar

**Cor:** Verde claro (#D4EDDA)
**Posicao:** Centro-direita
**Tempo:** 40-50 min

### Subsecao 4.1 — Principal Incerteza

| Elemento | Tipo | Conteudo |
|---|---|---|
| Titulo da secao | Texto | "[E3] Experimentar" |
| Maior risco | Post-it | "Qual a maior duvida que ainda temos?" |

### Subsecao 4.2 — Test Card

| Elemento | Tipo | Conteudo |
|---|---|---|
| Titulo | Texto | "Test Card" |
| Hipótese | Post-it | "Acreditamos que..." |
| Teste | Post-it | "Para verificar, vamos... (público, método e duração)" |
| Medida | Post-it | "Vamos observar ou medir... (unidade e fonte)" |
| Critério | Post-it | "Estaremos certos se... (definido antes da coleta)" |

### Subsecao 4.3 — plano de evidências futuras

| Elemento | Tipo | Conteudo |
|---|---|---|
| Titulo | Texto | "Evidências a coletar" |
| Fonte e localizador | Post-it | "Onde registraremos observações e medidas?" |
| Vínculo | Post-it | "Como cada registro apontará ao Test Card?" |
| Decisão futura | Post-it | "Que pergunta os dados permitirão responder?" |

---

## Area 5 — Fechamento

**Cor:** Cinza escuro (#D3D3D3)
**Posicao:** Canto inferior direito

### Elementos

| Elemento | Tipo | Conteudo |
|---|---|---|
| Titulo | Texto | "[FIM] Resumo do Workshop" |
| Outputs consolidados | Texto automatico | Lista de todos os outputs gerados |
| Proximos passos | Texto | "Acionar compile_3e_report para gerar o relatorio de estruturacao" |

---

## Convencoes visuais

| Etapa | Cor | Codigo |
|---|---|---|
| Abertura | Cinza | ABERT |
| E1 — Esclarecer | Amarelo | E1 |
| E2 — Estruturar | Azul | E2 |
| E3 — Experimentar | Verde | E3 |
| Fechamento | Cinza escuro | FIM |

## Notas de implementacao

- O board deve ser criado via `mcp.mural.write.create_board` com confirmacao do usuario.
- As secoes e subsecoes devem ser criadas via `mcp.mural.write.create_section`.
- Post-its modelo e fixos sao criados via `mcp.mural.write.create_sticky_note`.
- O Test Card é preparado antes da coleta; o board reserva espaço para o plano de evidências, sem Learning Card preenchido antecipadamente.
- Ao final, outputs sao extraidos via `mcp.mural.read.get_sticky_notes` e `mcp.mural.read.get_board`.
- Em caso de indisponibilidade do Mural, a skill opera apenas em modo conversacional.
