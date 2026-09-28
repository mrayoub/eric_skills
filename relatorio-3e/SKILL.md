---
name: relatorio-3e
description: "Compila a estruturação 3E de uma solução com escopo, plano de construção, Test Cards prospectivos e decisão de rota interna, externa ou híbrida. Use para preparar, compilar ou revisar E1–E3 em qualquer momento, inclusive com resultados existentes; distingue plano de evidência observada."
---

# Compilar o Relatório 3E

Adapta `compile-3e-report` do ERIC_RC6. Leia [levantamento documental e grilling](references/levantamento-documental-e-grilling.md) e o [playbook 3E](references/3e-solution-structuring-playbook.md). E3 organiza o desenho da experimentação. No RC6, isso costuma ocorrer na ideação, mas a skill também pode ser usada antes, retomada após testes ou para reconstruir o histórico, sempre distinguindo datas de plano e execução.

Leia a [transcrição integral do playbook 3E fornecido](<assets/Modelo 3E Estruturação da Solução.transcricao.md>) e consulte o [DOCX original](<assets/Modelo 3E Estruturação da Solução.docx>) para conferir o método. O [registro de comparação com o RC6](references/fonte-3e-e-divergencias.md) explicita as adaptações dos cards e os limites da fonte.

## Grilling obrigatório na leitura e na interação

Antes de sintetizar, pontuar ou planejar, leia o [protocolo operacional de grilling](references/grilling-operacional.md). Aplique-o aos documentos e às respostas recebidas: confronte afirmações e fontes, registre questões resolvidas e pendentes, apresente somente a fronteira de perguntas que exige resposta humana e reavalie-a após cada novo insumo. Mostre a síntese documental e as lacunas decisivas; não trate leitura silenciosa ou preenchimento do template como grilling concluído. Continue tarefas independentes enquanto aguarda respostas e declare a entrega parcial quando faltar suporte decisivo. O protocolo está incorporado nesta skill e complementa suas referências específicas.

## Uso independente da fase

Ative esta skill pela tarefa solicitada e pelos insumos disponíveis, em qualquer ponto da esteira ou fora dela. A fase registrada no projeto é contexto de proveniência, não condição de uso nem autorização para inventar conteúdo. Consulte o Scorecard de maturidade quando disponível para localizar evidências e lacunas, sem usá-lo como bloqueio automático. Se a pessoa chegar antes do trabalho usual, produza preparação ou versão parcial e pergunte somente pelos insumos decisivos. Se chegar depois, incorpore os materiais posteriores, preserve a cronologia e indique o que foi definido antes ou reconstruído depois; não apresente reconstrução retrospectiva como plano previamente acordado. A completude depende dos requisitos da entrega e da evidência, não do nome da fase.

## Entrada e fidelidade

Leia a hipótese disponível e os registros existentes de problema, 4D, BP1, E1–E3 e experimentação; não exija documentos que não fazem parte do projeto. Identifique fontes, versões, participantes e decisões com localização. Em modo assíncrono, explique o que veio de documento e quais deliberações de workshop não ocorreram. Se E1–E3 não estiverem completos, entregue versão parcial com perguntas decisivas em ordem de dependência. Não atribua aprovação a responsável ausente, não reescreva decisão anterior e não peça ao usuário o resultado desejado do teste.

## Entrega

1. **Solução e valor esperado:** problema focal, população, hipótese master, escopo, componentes `agora/futuro/fora`, riscos e limites. Separe expectativa de resultado observado.
2. **Construção:** recursos existentes, itens a desenvolver, dependências, responsável, apoio e prazo por ação. Marque lacunas antes de declarar um MVP pronto.
3. **Experimento inicial:** suposições prioritárias, público elegível, método, intervenção, medida, fonte e critério de leitura. Entregue um **Test Card individual por teste** usando o [modelo de Test Card](assets/test-card.md), com os quatro campos Strategyzer, sem substituir os cards por uma tabela de índice. Critérios verificatórios e limiares que dependam de baseline ficam explicitamente `a fechar antes da coleta`; não os invente nem os preencha retrospectivamente. Se já houver testes, cite resultados datados e separe Test Cards originalmente pactuados dos reconstruídos; registre fontes para Learning Cards, que só podem conter achados após a execução. Antes do teste, não gere Learning Cards ou achados.
4. **Rota:** registre `internal`, `external`, `hybrid` ou `undecided`, com a evidência e a decisão efetiva. Se a rota for externa ou híbrida, descreva o que deve ser buscado; se interna, o que deve ser construído. `undecided` mantém as dependências abertas. A rota não equivale a validação da solução.

Confira consistência entre o relatório, cada Test Card e as fontes. Aponte quais decisões, dados e autorizações faltam para o próximo uso concreto do relatório, seja planejar, executar, revisar ou escalar. A skill `experimentacao-inovacao` pode detalhar o protocolo e analisar resultados em qualquer fase; este pacote também funciona isoladamente.

## Contexto institucional

Leia [ERIC — Esteira Robusta de Inovação Colaborativa](references/eric-esteira.md) antes de trabalhar com esta skill. Use o contexto da CCEE, as oito etapas, os dois pontos de avaliação, as rotas condicionais e as relações entre entregáveis para interpretar as fontes. Acione a skill pela tarefa e pelas evidências disponíveis, em qualquer momento; a sequência usual da esteira não bloqueia o uso.

## Arquivos e padrão visual

O [playbook 3E original do RC6](assets/3e-solution-structuring-playbook-original-rc6.md) está preservado como fonte histórica imutável; a versão em `references/` contém as adaptações operacionais. Em divergência, identifique a diferença e a data; não reescreva silenciosamente o original.

Para qualquer entregável em arquivo, siga o [sistema visual da skill](assets/design-system/README.md) e seu `profiles.json`. Gere primeiro o `content_json` versionado com blocos, citações e metadados; use o tipo `three_e_report` e, para cada teste, `test_card`. O schema de resposta comum e o perfil deste tipo são obrigatórios; aplique também o schema específico quando existir. Execute a validação pelo renderizador incluído em `assets/design-system/scripts/render.py` antes de gerar qualquer arquivo final. Se ela falhar, corrija a resposta ou identifique explicitamente uma versão parcial; nunca contorne o schema. Preserve o mesmo JSON canônico validado junto de todos os derivados, garantindo estrutura, rastreabilidade e padrão visual idênticos entre skills. O perfil determina a orientação A4 retrato, A4 paisagem ou apresentação 16:9 e aplica os mesmos tokens de cor, fonte e área segura. Por padrão, ofereça JSON, PDF, DOCX, MD e TXT quando o tipo aceitar; PPTX é próprio de apresentação, CSV exige tabela exportável e HTML é prévia. Não componha um layout ad hoc nem altere conteúdo para caber: pagine ou registre impossibilidade de uma página. Antes de entregar, confira ordem, tabelas, citações, orientação, ausência de corte e igualdade semântica entre formatos.

**Proveniência:** reescrita de fonte metodológica RC6 (`compile-3e-report/`), com separação entre plano, execução e reconstrução posterior, sem restrição por fase.
