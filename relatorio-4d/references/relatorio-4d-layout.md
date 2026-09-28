# Estrutura visual de cards para o Relatório 4D

Referência visual: `my_skills/_SAMPLE/GEIN-123 - Otimização da Jornada do Serviços de Adimplemento/Relatorio_4D_Adimplemento_2026-06-18.pdf` (8 páginas rasterizadas, A4 paisagem; SHA-256 `e9c86debaf32b40fb76fe2e6f0d7c19499c61cabf14206d97afb60a3f9185985`). Este guia descreve somente a composição; nomes, números, afirmações e conclusões do PDF não são modelos de conteúdo.

## Gramática visual

- Capa de contraste alto, título grande e metadados alinhados. Nas páginas internas, cabeçalho azul escuro para a seção D1–D4, fundo claro e rodapé consistente.
- Primeiro mostre a pergunta ou síntese em faixa horizontal. Distribua sinais e métricas em uma fileira de 3–4 cards; use tons diferentes apenas para codificar função semântica, com rótulos textuais.
- Para jornada, tabule etapas antes / durante / depois em colunas adjacentes e, se houver múltiplos atores, linhas separadas. Cada célula deve conter observações rastreáveis.
- Para barco da inovação, se essa dinâmica realmente ocorreu, disponha ventos, âncoras, icebergs e porto em cards; omita categorias não usadas, sem preenchimento inventado.
- Para ideação, use matriz de cards de ideias, seguida de agrupamento por natureza da mudança. Não transfira itens do caso de referência.
- Para síntese e priorização, combine chamada de conclusão com tabela de dimensão, observação, fonte e implicação. Registre denominadores, regras de voto e dissensos quando existirem.
- Cada página pode conter uma ou mais grades; a página não deve ser forçada a reproduzir o número de páginas do exemplo. Quebre antes de cortar ou diminuir fonte. Preserve citações ligadas aos cards e mantenha o JSON como fonte canônica.

## Composição no schema

Use `heading` com `data.section_key` exigida pelo relatório, `card_grid` com `data.columns` de 1 a 4 e `data.cards` (cada card tem `title`, `text` ou `items`, `tone` opcional e `citation_ids` opcional), `table` para comparações e `page_break` quando uma nova seção merecer página própria. O renderer compartilha esta estrutura entre PDF, HTML, DOCX, MD e TXT; tabelas continuam tabelas editáveis.

Tons permitidos: `blue`, `neutral`, `red`, `green`, `yellow`. `red` indica risco ou ausência, `green` resultado favorável observado, `yellow` hipótese ou atenção, `blue` informação principal. A cor nunca substitui o rótulo textual.
