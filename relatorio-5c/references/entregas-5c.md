# Relatório e apresentação do 5C

O 5C tem duas entregas. As duas saem da **mesma análise** e das mesmas fontes, mas servem a leitores e usos
diferentes. Faça a análise uma vez e derive as duas; nunca deixe que uma diga algo que a outra contradiga.

| | Relatório 5C | Apresentação 5C |
|---|---|---|
| Tipo no design system | `five_c_report` (documento) | `five_c_presentation` (slides 16:9) |
| Pergunta que responde | O que aconteceu em cada etapa, com que evidência, e o que fica registrado | O que aprendemos sobre o problema e o que muda na nossa leitura |
| Leitor | Equipe do projeto, quem audita ou retoma o trabalho, quem decide com base em registro | Gestores, áreas envolvidas e participantes na devolutiva |
| Organização | Por etapa: Resumo, Escopo, C1 a C5, Divergências, Hipóteses | Por insight: ponto de partida, formato, dores, mapa, menções, diagnóstico × escuta, propostas, priorização, próximos passos |
| Densidade | Texto completo, tabelas por participante ou tema, fonte por achado | Título que conclui, três evidências e uma linha de leitura por slide; detalhe fica no relatório |
| Fontes | Localizador por achado e lista completa | Linha "Fontes:" por slide e slide final de fontes |

Quando o usuário pedir só "o relatório" ou só "a apresentação", entregue o que foi pedido e ofereça a outra. Quando
pedir "a devolutiva", "o material para os gestores" ou "o que apresentar", entregue a apresentação. Quando pedir o
registro do encontro, a síntese completa ou algo para arquivar, entregue o relatório.

## A base comum da análise

Antes de redigir qualquer entrega, monte a base. Ela não é um arquivo a entregar, mas tudo das duas entregas vem dela.

1. **Linha de base:** objetivo, diagnóstico prévio (volume, período, temas com peso), perguntas que o 5C deve
   responder e o que mudou entre o diagnóstico e o encontro (por exemplo, uma melhoria que entrou em operação).
2. **Sessões:** data, formato, profundidade (curta ou completa), etapas cobertas, participantes presentes e
   convidados separados, unidade de contagem.
3. **Relatos por bloco da jornada e por sessão**, com localizador.
4. **Fichas de dor** (D01, D02...): categoria, constatação em uma frase, o que foi relatado, impacto a examinar e os
   localizadores que a sustentam. Uma ficha junta relatos de sessões diferentes sobre a mesma dor.
5. **Contagens:** regra (voto, crédito ou menção codificada), total, exclusões (duplicados, vazios) e resultado.
6. **Triangulação** com o diagnóstico, quando houver: tema, base, leitura e evidência, com os status definidos abaixo.
7. **Propostas do C4:** grupo, proposta, o que propõe, benefício esperado, dependências.
8. **Priorização do C5:** créditos, ranking e razões, ou a lacuna registrada.
9. **Divergências e hipóteses a testar.**

## Triangulação: do diagnóstico à escuta

Quando houver diagnóstico prévio (chamados, voz do cliente, dados do serviço), compare cada tema com o que o 5C
trouxe. Use estes status e defina-os na própria entrega:

| Status | Quando usar |
|---|---|
| Corroborado | A escuta confirma o diagnóstico |
| Corroborado com ressalva | Confirma, mas com uma condição (por exemplo, uma melhoria recente ainda sem avaliação de uso) |
| Aprofundado | A escuta amplia causas, efeitos ou atores |
| Reorientado | A escuta muda a leitura do tema |
| Integrado à jornada | A dor se mostra parte de outro fluxo |
| Transversal | O tema aparece em todos os fluxos |
| Emergente | O tema não estava no diagnóstico |

Diga sempre que o diagnóstico mede frequência histórica e o workshop traz evidência qualitativa e prioridades
percebidas, e que a triangulação não representa validação de eficácia. No relatório, a triangulação entra como
seção depois do C3; na apresentação, como slide próprio.

## Estrutura da apresentação

Seções obrigatórias do `five_c_presentation`, nesta ordem. Cada uma começa com um `heading` (título do slide) e um
`paragraph` com o mesmo `section_key`, seguido de cards ou tabela quando couber.

| `section_key` | Slide | O que contém |
|---|---|---|
| `starting_point` | Ponto de partida | Objetivo, base do diagnóstico, dores com peso, perguntas a validar, o que mudou desde o diagnóstico |
| `format` | Formato | Sessões, profundidade, etapas cobertas, participantes (presentes e convidados separados), unidade de contagem |
| `pains` | Dores relatadas | Por bloco da jornada e por sessão: título que conclui, três evidências, linha de leitura |
| `pain_map` | Mapa das dores | Fichas com ID, categoria, constatação e impacto a examinar (cards, até 4 por slide) |
| `mentions` | O que mais foi indicado | Contagem com regra, total e exclusões; "são menções, não votos" quando for o caso |
| `diagnosis_check` | Do diagnóstico à escuta | Tabela de triangulação; sem diagnóstico prévio, diga isso em uma frase |
| `proposals` | Propostas cocriadas | Grupo, proposta, benefício esperado; ressalva de hipótese cocriada |
| `prioritization` | Priorização | Créditos e ranking do C5, ou a lacuna registrada |
| `next_steps` | Próximos passos | Hipóteses a testar, responsáveis ou "a definir" |

Regras de cada slide:

- **Título que conclui**, de 4 a 14 palavras: "No presencial, as mesmas dores aparecem como falhas de execução", não
  "Dores do presencial". O renderizador recusa título genérico.
- **No máximo 4 blocos e 140 palavras por slide.** Se não couber, divida: um mapa com 15 dores vira quatro slides.
- **Mensagem da capa** (`summary`) em até 35 palavras.
- **Tabela abre slide próprio**: o parágrafo da seção fica no slide anterior. Escreva-o para funcionar sozinho.
- Ressalva de método no próprio slide, curta: "São menções, não votos do C5.", "Não representa validação de eficácia."

Uma etapa sem registro vira slide com a lacuna ("O resultado da distribuição de créditos ainda não foi registrado"),
nunca um slide omitido nem preenchido com dado inventado.

Veja o [exemplo de referência](exemplos/5c-oficial-sessao-coletiva-apresentacao.md), feito pela autora do playbook.
