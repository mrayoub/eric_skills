---
name: relatorio-4d
description: "Compila ou revisa o Relatório 4D a partir dos registros de D1 a D4 (mural, notas, transcrições, votos, snapshot D2): diagnóstico, alternativas, priorização com denominadores, dissensos, temas transversais, síntese analítica, hipótese de solução para o 3E e conclusão, além da Apresentação 4D, devolutiva curta para gestores. Use quando houver material de um workshop 4D ou fontes equivalentes e o usuário quiser o relatório, a síntese para o BP1, a apresentação ou a revisão de um relatório existente. Não use para preparar ou facilitar o encontro (use workshop-4d)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.2.0"
---

# Compilar o Relatório 4D

Consolida registros de D1 a D4; playbook e referências visuais não fornecem resultados de uma execução.

## Leia primeiro

- [Playbook 4D](references/4d-workshop-playbook.md): sequência metodológica.
- [Análise, hipótese e conclusão](references/analise-e-conclusao-4d.md): orientação da autora do playbook; temas transversais, síntese analítica, hipótese de solução, acabativa e Apresentação 4D.
- [Layout de cards](references/relatorio-4d-layout.md): grades tabuladas e comparações citadas.
Para conferir a fonte: [transcrição](<assets/Modelo 4D de Aprofundamento.transcricao.md>), [DOCX](<assets/Modelo 4D de Aprofundamento.docx>), [divergências](references/fonte-4d-e-divergencias.md), [original RC6](assets/4d-workshop-playbook-original-rc6.md) e [PDF fictício de referência visual](assets/official-four-d-report.pdf). Preserve originais; registre diferenças e datas; não copie conteúdo de outro projeto.

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md) antes de sintetizar,
pontuar ou planejar, e reaplique-o a cada arquivo ou resposta novos. Em resumo: resolva
nos arquivos tudo que for pesquisável; pergunte só a fronteira de questões decisivas
cujas dependências já estão resolvidas; registre origem e localizador de cada resposta;
entregue versão parcial quando faltar suporte decisivo. Nunca pergunte a nota, o
resultado ou a conclusão desejada: isso não é dado, e contaminaria a avaliação.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Quando usar

A fase do projeto é contexto, não pré-requisito. Se o pedido vier antes do momento
usual, entregue preparação ou versão parcial; se vier depois, use o material posterior
com data e não apresente reconstrução como plano combinado previamente.

## Passos

1. Identifique etapas existentes, mesmo em datas/fases distintas. Snapshot D2 não substitui D3/D4; somente D1/D2 exige parcial. Fontes posteriores são atualizações datadas. Na compilação assíncrona, declare materiais substitutos e deliberações não inferíveis; BP1 não é pré-requisito.
2. Inventarie briefing, snapshot, mural, transcrições, dados, alternativas e votos. Distinga original/derivado; extraia páginas, linhas, timestamps e imagens. Pergunte só por documentos/decisões ausentes.
3. Organize D1 percepções/enquadramento, D2 jornada/diagnóstico, D3 alternativas ligadas às dores, D4 ranking/regras/dissensos/responsáveis, conclusão e próximos passos. Preserve participantes, votos, denominadores e fontes.
4. Distinga observação, relato, hipótese causal e interpretação; exponha contraevidências/conflitos. Dados de briefing e votos não validam eficácia, adoção ou impacto; voto prioriza investigação.
5. Registre desafio atual, suposições críticas, alternativas descartadas/razões e fontes/respondentes das lacunas. Se houve BP1, identifique a formulação submetida naquela data; recomendações devem apoiar-se no diagnóstico e escolhas documentadas.
6. **Análise e conclusão** (obrigatório, conforme [o guia](references/analise-e-conclusao-4d.md)): depois do D4, deixe a ordem das dinâmicas e cruze os registros. Monte a tabela de temas que atravessaram o 4D (tema, onde apareceu, evidências, força), a síntese analítica (padrões, temas mais fortes, contradições, comparação com o briefing, limitações), a hipótese de solução ("Acreditamos que / Porque o diagnóstico mostrou / Precisamos validar se", sem fechar tecnologia, com ações soltas agrupadas sob um conceito) e a conclusão do aprofundamento (o que entendemos, hipótese, limitações, o que o 3E precisa resolver, o que segue aberto), condensada também no Resumo. Você compõe essas seções a partir das fontes; não peça ao usuário que as escreva.
7. Entregue relatório editável no formato pedido, adaptando contratos sem mudar semântica. Use grades de cards e tabelas somente para categorias sustentadas; a referência visual não cria achados.

## Exemplo

Entrada: “Consolide o 4D do Portal de Solicitações de Dados.”
Saída (trecho):
> Votos: 95 registrados; 100 esperados por dez presentes.
> Lacuna: cinco créditos sem explicação; apuração pendente.
> Ranking não comprova impacto.

## Checagem final

- [ ] D1 a D4 em ordem, com etapas ausentes identificadas
- [ ] Texto/números, denominadores e fontes reconciliados
- [ ] Relatos, hipóteses, propostas e decisões separados
- [ ] Snapshot, BP1 e atualizações preservam cronologia
- [ ] Recomendações ligadas a achados e limites
- [ ] Temas transversais com critério de força, síntese analítica e contradições
- [ ] Hipótese de solução com as três partes, sem tecnologia, ligada ao diagnóstico e coerente com o D4
- [ ] Conclusão com acabativa e Resumo no início

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md), revise com o [guia de escrita](references/guia-de-escrita.md) e não use travessão no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `four_d_report` para o relatório e `four_d_presentation` para a Apresentação 4D (no máximo 6 slides de conteúdo, conforme [o guia](references/analise-e-conclusao-4d.md#duas-saídas-da-mesma-base)), as duas derivadas da mesma análise: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"`: nunca contorne o schema.

**Proveniência:** reescrita de fonte metodológica RC6 (`compile-4d-report/`); a ordem interna D1 a D4 foi preservada, sem transformar a fase de origem em condição de uso.
