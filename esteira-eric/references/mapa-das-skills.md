# Mapa das skills pela esteira

A ordem é a sequência usual da esteira (RC6). Qualquer skill pode ser usada fora dela; indique a que responde à
pergunta atual do projeto.

| Etapa | Pergunta | Skill | Entregável | Quando indicar |
|---|---|---|---|---|
| 1. Garimpar | Qual oportunidade merece atenção? | `potencial-inovacao` | Avaliação do potencial | Há dores ou ideias a priorizar, triar ou comparar |
| 2. Conhecer | O que vamos trabalhar? | `briefing-inovacao` | Briefing, one-page, perguntas de melhoria | Falta o briefing, ou ele precisa ser revisado ou resumido |
| 2. Conhecer | O briefing está bom o suficiente? | `avaliacao-briefing-iqb` | Avaliação IQB | Existe briefing e é preciso saber se ele sustenta o próximo passo |
| 3. Aprofundar | Qual problema queremos resolver? | `workshop-4d` | Roteiro e registro D1–D4 | Vai preparar, conduzir ou registrar o workshop 4D |
| 3. Aprofundar → BP1 | O desafio está estruturado? | `relatorio-4d` | Relatório 4D | Há registros do 4D e falta o relatório para o BP1 |
| 4. Gerar ideias | Como resolver? | `workshop-3e` | Roteiro e registro E1–E3, Test Cards | Há alternativa priorizada a tornar testável |
| 4–5. Gerar ideias e desenhar | Qual proposta testável e qual rota? | `relatorio-3e` | Relatório 3E, Test Cards, decisão de rota | Há registros do 3E e falta o relatório |
| 7. Experimentar → BP2 | O teste responde à pergunta crítica? | `experimentacao-inovacao` | Hipóteses com Test Cards, Modelo de experimentação, Apresentação e direcionamento | Há Test Cards a executar ou resultados a analisar |
| Qualquer etapa | Quão madura está a evidência? | `scorecard-inovacao` | Scorecard de evidências | Antes de um gate, ou para comparar a maturidade ao longo do tempo |
| Qualquer etapa (usual no BP2 e na implementação) | Que decisão pedir à gestão? | `relatorio-final-inovacao` | Relatório final e pitch executivo | A gestão precisa decidir avançar, iterar, investigar ou encerrar |
| Transversal | Como o cliente vive a experiência? | `workshop-5c` | Roteiro e registro C1–C5 | A experiência de clientes ou agentes é central e precisa de cocriação |
| Transversal | O que o encontro com clientes concluiu? | `relatorio-5c` | Relatório 5C | Há registros do 5C e falta o relatório |

Etapas sem skill própria — **5. Desenhar soluções**, **6. Buscar soluções externas** e **8. Implementar** — usam o
relatório 3E (rota) e o relatório final (decisão e plano). Diga isso ao usuário em vez de inventar uma skill.

## Sinais nos arquivos

- Briefing de sete campos, sem IQB → `avaliacao-briefing-iqb` antes do 4D, se a qualidade do briefing estiver em dúvida.
- Registros D1–D4 sem relatório → `relatorio-4d`.
- Relatório 4D com prioridade do D4 e sem 3E → `workshop-3e`.
- Test Cards prospectivos sem execução → `experimentacao-inovacao` (modelo de experimentação).
- Registros de sessões ou execução sem Learning Cards → `experimentacao-inovacao` (consolidação).
- Learning Cards e recomendação, sem decisão de gestão → `relatorio-final-inovacao` ou `scorecard-inovacao` antes do BP2.
