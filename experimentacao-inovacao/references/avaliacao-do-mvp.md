# Avaliação do MVP

Na consolidação, avalie o MVP como produto, **separado da avaliação das hipóteses**. As duas leituras respondem perguntas diferentes: os Learning Cards dizem o que a evidência mostra sobre as hipóteses; a avaliação do MVP diz se o que foi construído funcionou, atendeu ao escopo e está pronto para seguir.

## Regras

- MVP que funciona não valida hipótese. Hipótese não sustentada não torna o MVP ruim — pode ser a proposta, não a construção.
- Cada dimensão leva evidência com ID e localizador, ou `não avaliado`. Não preencha por impressão nem pela vontade de avançar.
- Avalie a versão efetivamente testada, registrada no caderno durante a execução; não estenda a conclusão a versões futuras.
- Prontidão para teste não é prontidão para implantação. Implantação exige o que o BP2 pede: riscos, custo, dependências e responsáveis.

## Dimensões

| Dimensão | Pergunta | Evidências típicas |
|---|---|---|
| Aderência ao escopo | O MVP testado tinha os componentes "precisa ter" e respeitou o recorte? | registro de construção, desvios datados |
| Funcionamento | Os componentes fizeram o que o critério de pronto pedia durante os testes? | registros de execução, falhas, incidentes |
| Experiência de uso observada | Onde as pessoas tiveram fricção, erro ou ajuda? | sessões, livro de evidências, matriz de unidades |
| Viabilidade operacional e técnica | A operação e a tecnologia sustentariam o uso real? | trabalho manual, integrações, limites técnicos |
| Esforço e custo | Quanto custou construir e operar o MVP, e o que isso indica para a solução? | horas, custos, trabalho manual |
| Pendências | O que ficou incompleto, provisório ou adiado? | backlog, desvios, componentes adiados |
| Prontidão para implantação | O que falta para implantar, e quem decide? | condições do BP2, dependências, riscos |

## No entregável

Inclua a avaliação do MVP na **Apresentação da experimentação e direcionamento** como seção própria (`section_key: mvp_evaluation`), ao lado dos resultados das hipóteses, e termine com o direcionamento (`section_key: direction`). A versão completa também exige as seções do schema `context`, `method`, `findings`, `recommendation` e `next_steps`; `direction` vem depois de `recommendation` e `next_steps` e não as substitui. Use `metadata.content_profile: "experimentation_presentation"` e coloque cada `section_key` no bloco de conteúdo, não só no título. Cada slide deve ter um título-mensagem de 4 a 12 palavras, como "O MVP funcionou, mas a economia de tempo não foi medida". Use a avaliação no direcionamento: por exemplo, iterar o MVP quando a hipótese se sustentou mas a construção limitou a evidência, ou investigar quando a hipótese não se sustentou com um MVP que funcionou.
