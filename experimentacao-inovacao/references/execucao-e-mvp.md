# Execução: modelo de experimentação, construção do MVP e realização dos testes

O bloco de execução começa pelo entregável **Modelo de experimentação** — o desenho que a equipe vai executar — e segue com o acompanhamento da construção do MVP e da realização dos testes. A equipe constrói e executa; a skill desenha, acompanha e registra. Resultados não são interpretados aqui — isso é do bloco de consolidação.

## Entregável: Modelo de experimentação

Um modelo executável por rodada, ligado aos Test Cards do bloco 1. Quem o recebe deve conseguir construir o MVP e rodar os testes sem perguntar o que fazer. Tipo do design system: `experiment_plan`.

| Seção | Conteúdo |
|---|---|
| `hypothesis` | hipótese master e Test Cards cobertos, por ID e versão |
| `method` | método de cada teste e por que produz a evidência necessária; o que não permite concluir |
| `population` | público, elegibilidade, recrutamento, amostra prevista e unidade observada |
| `measures` | medidas, numeradores, denominadores, janelas e critérios já fixados nos cards; registros e instrumentos de coleta |
| `protocol` | roteiro passo a passo de cada teste: preparação, exposição ou tarefa, moderação, registro, encerramento e desvios |
| `guardrails` | riscos, limites de exposição, monitoramento, regra de interrupção e quem decide |
| `mvp_build` | MVP a construir: componentes, critério de pronto, versão e responsáveis |
| `scope` | escopo da experimentação e o que fica fora |
| `schedule` | cronograma operacional: marcos de construção e de teste, datas e responsáveis |
| `start_gate` | gate de início: o que precisa estar pronto e quem autoriza |

Declare `metadata.content_profile: "experimentation_model"`: em versão completa, o renderizador recusa o modelo sem as quatro últimas seções.

Se algum card ainda não tiver critério decisivo, o modelo sai como parcial (`metadata.completeness: "partial"`) e o teste correspondente não entra no gate de início.

## Acompanhar a construção do MVP

- **Componentes:** liste cada componente a construir a partir do "precisa ter" do 3E e do escopo da experimentação. No modelo, registre para cada um a origem (decisão do 3E ou adaptação datada), critério de pronto verificável, responsável, estado (`planejado`, `em construção`, `pronto`, `adiado`, `fora do escopo`) e versão. "Pode evoluir" e "fora do recorte" não entram sem decisão registrada.
- **Critério de pronto:** descreva o que precisa funcionar para o teste previsto no Test Card acontecer — tarefa, fluxo, dado ou operação —, não uma qualidade genérica. Um componente pode estar pronto para o teste sem estar pronto para implantação.
- **Trabalho manual por trás:** em MVP manual, concierge ou simulação, registre o que é feito por pessoas, por quem e com que custo; isso limita conclusões sobre automação e escala.
- **Desvios:** toda diferença entre o planejado e o construído entra com data, motivo, responsável e efeito nos Test Cards afetados. Não reescreva o escopo para coincidir com o que foi entregue.
- **Prontidão para testar:** antes de expor pessoas ou operação, confira o gate de início — versão, componentes prontos, público elegível, medidas, fontes de dados, guardrails, regra de interrupção e quem autoriza. MVP que não atende ao protocolo não inicia o teste sem decisão registrada; registre também quando o teste começa com pendência aceita.

## Acompanhar a realização dos testes

- Execute conforme o protocolo de cada Test Card e registre cada execução: `execucao_id`, Test Card, data, método, unidade observada, perfil elegível, versão do MVP, procedimento ou tarefa, fontes com localização, desfecho bruto, desvios, intervenções e dados ausentes.
- Acompanhe elegibilidade, versão, adesão ao protocolo e qualidade dos registros durante a coleta. Adaptações entram datadas, ao lado do plano original, indicando se ocorreram antes ou depois de alguma coleta.
- Alimente o livro de evidências com IDs estáveis e localizadores verificáveis (página, evento, linha de dado ou tempo do vídeo). Em sessões moderadas, diferencie ajuda técnica, orientação e influência na decisão.
- Não calcule status de critério, não escreva Learning Card e não recomende neste bloco. Registre o que aconteceu; a leitura vem na consolidação.

## Registros da execução

Os registros da construção e dos testes — versão, componentes e estado, desvios, execuções por Test Card, livro de evidências e dados ausentes — ficam no [caderno](../assets/caderno-da-rodada.md) e são a entrada da consolidação. Se for pedido um relatório detalhado da execução, use `experiment_report` (seções `scope`, `method`, `evidence`, `results`, `limits`, `recommendation`), sem interpretar resultados antes da consolidação.
