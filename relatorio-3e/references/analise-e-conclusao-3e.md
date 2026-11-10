# Análise, rastreabilidade e conclusão do Relatório 3E

O 3E continua o 4D: transforma a hipótese priorizada no 4D numa solução concreta, com fluxo, responsáveis,
dependências e experimento. Desde a orientação da autora do playbook 4D (10/11/2026), o `relatorio-4d` termina numa
hipótese de solução em três partes e numa conclusão que diz o que o 3E precisa resolver. O Relatório 3E fecha esse
ciclo: mostra como a hipótese virou solução, se cada parte da solução responde a uma dor do diagnóstico, e o que a
experimentação precisa responder. Como no 4D, o relatório não pode parar na descrição de E1, E2 e E3: precisa
concluir.

## Duas saídas da mesma base

| | Relatório 3E | Apresentação 3E |
|---|---|---|
| Tipo no design system | `three_e_report` (documento) | `three_e_presentation` (slides 16:9) |
| Pergunta que responde | Como a hipótese virou solução, com que plano e que testes | Qual solução sai do 3E, por que ela responde ao diagnóstico e o que vem primeiro |
| Uso | Registro, base da construção e da experimentação | Gerência e diretoria, devolutiva ao grupo |
| Conteúdo | E1 a E3, rastreabilidade, rota, Test Cards, conclusão | Cinco slides de conteúdo, no máximo seis: solução, rastreabilidade, construir e testar primeiro, rota, próximos passos |

Faça a análise uma vez e derive as duas. Entregue a apresentação quando o usuário pedir algo para gestores, uma
devolutiva ou um resumo executivo; ofereça-a ao entregar o relatório.

### Estrutura da Apresentação 3E

| `section_key` | Slide | O que contém |
|---|---|---|
| `solution` | A solução | A solução em uma frase, a hipótese do 4D de onde veio e o que mudou no E1 |
| `traceability` | Por que responde ao diagnóstico | Componentes "precisa ter" ligados às dores do 4D, com status; o que ficou fora e por quê |
| `build_and_test` | Construir e testar primeiro | O que será construído primeiro e a suposição de maior risco a testar; plano não é evidência |
| `route` | Rota | Interna, externa, híbrida ou indefinida, e do que depende |
| `next_steps` | Próximos passos | O que segue aberto, responsáveis ou "a definir" |

Mesmas regras da Apresentação 4D: título que conclui, até 4 blocos e 140 palavras por slide, capa em até 35
palavras, **no máximo 6 slides de conteúdo**.

## Ordem do relatório completo

| `section_key` | Seção | O que contém |
|---|---|---|
| `executive_summary` | Resumo | A acabativa em um parágrafo: a solução em uma frase, o que será construído e testado primeiro, a rota, o que segue aberto |
| `e1` | Esclarecer | Hipótese do 4D, hipótese refinada no E1 e o que mudou; é, não é, resolve a dor de, gera valor para |
| `e2` | Estruturar | Componentes com ID em precisa ter, pode evoluir e fora do recorte; plano de construção |
| `traceability` | Do 4D à solução | Tabela de rastreabilidade (abaixo) |
| `e3` | Experimentar | Suposições priorizadas por risco e Test Cards |
| `route` | Rota | Interna, externa, híbrida ou indefinida, com fonte e decisão efetiva |
| `conclusion` | Conclusão da estruturação | As cinco respostas da acabativa (abaixo) |

As seções `executive_summary`, `traceability` e `conclusion` são obrigatórias, além de E1 a E3 e rota. A skill compõe
todas a partir das fontes; o grilling só pergunta o que o material não responde.

## Do 4D à solução: rastreabilidade

Cada componente "precisa ter" responde a uma dor ou tema do 4D. Monte a tabela:

| Componente | Classificação | Dor ou tema do 4D | Status |
|---|---|---|---|
| C01: Etapas padrão do projeto | Precisa ter | Previsibilidade (tema transversal; I02) | Sustentado |
| C02: Registro mínimo por etapa | Precisa ter | Registro abandonado (A01) | Sustentado |
| C03: Painel para a diretoria | Pode evoluir | Nenhuma dor do 4D | Sem evidência |

Exemplo ilustrativo; não reutilize.

Status: **sustentado** (a dor está no diagnóstico do 4D, com evidência), **parcial** (a dor aparece, mas com pouca
evidência ou numa só dinâmica), **sem evidência** (não há dor do 4D que justifique). Um componente "precisa ter" sem
evidência é sinal de escopo crescendo: diga isso e indique o que faria o componente subir ou sair do recorte.

Sem relatório 4D, diga de onde veio a solução candidata e trate a rastreabilidade como lacuna.

## Hipótese: do 4D ao 3E

No E1, compare a hipótese que chegou do 4D com a hipótese refinada pelo grupo. Registre o que mudou (público, escopo,
mecanismo) e por quê. As suposições de "Precisamos validar se" do 4D devem aparecer no E3: priorizadas, testadas ou
explicitamente adiadas, com o motivo.

## Conclusão da estruturação (acabativa)

Feche com cinco respostas curtas:

1. **A solução em uma frase**, e o que mudou em relação à hipótese do 4D.
2. **O que será construído primeiro** (componentes "precisa ter" e responsáveis).
3. **O que será testado primeiro** (suposições de maior risco e Test Cards).
4. **A rota** e do que ela depende.
5. **O que segue aberto** e de quem depende.

O mesmo conteúdo, condensado, abre o relatório no Resumo.

## Escrita

Use afirmação calibrada, separe plano de evidência ("a construção planejada não é evidência de eficácia") e
expectativa de resultado. Título de seção diz o conteúdo. Distinga fora do escopo por desenho, lacuna de registro e
ausência de dado; nenhuma é preenchida com dado inventado.
