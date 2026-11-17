---
name: relatorio-3e
description: "Compila ou revisa o Relatório oficial 3E e a Apresentação oficial 3E a partir dos registros da execução, com fontes e análise; usa o playbook como padrão e admite adaptações e versões pocket documentadas. Mantém Relatório depreciado e Apresentação depreciada quando solicitados. Use para consolidar registros, apresentação a gestores, devolutiva ou revisão. Não use para facilitar o workshop. No 3E, preserva Test Cards prospectivos; resultados de testes pertencem à experimentacao-inovacao."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.2.3"
---

# Compilar o Relatório 3E

Consolida solução, construção, experimentos e rota; separa plano, execução e reconstrução posterior.

## Escolha da entrega

O padrão é **Relatório oficial 3E** (`three_e_official_report`) ou **Apresentação oficial 3E**
(`three_e_official_presentation`). Leia [a receita oficial](references/entregaveis-oficiais.md) antes de compor.
Ela define conteúdo, JSON, adaptação do método e [tom da autora](references/tom-oficial.md) para os dois oficiais.

Os antigos continuam disponíveis apenas quando pedidos como **Relatório depreciado 3E** (`three_e_report`)
ou **Apresentação depreciada 3E** (`three_e_presentation`). As estruturas anteriores nas referências e no roteiro
integral abaixo orientam análise e os depreciados; não substituem a receita oficial nem obrigam uma aplicação pocket
a cobrir o playbook inteiro. Nos oficiais, prevalecem a receita oficial e o escopo de aplicação documentado.

## Leia primeiro

- [Playbook 3E](references/3e-solution-structuring-playbook.md): estrutura do relatório.
- [Test Card](assets/test-card.md): quatro campos por teste.
- [Análise, rastreabilidade e conclusão](references/analise-e-conclusao-3e.md): do 4D à solução, acabativa e Apresentação 3E.
Para conferir a fonte: [transcrição](<assets/Modelo 3E Estruturacao da Solucao.transcricao.md>), [DOCX](<assets/Modelo 3E Estruturacao da Solucao.docx>), [divergências](references/fonte-3e-e-divergencias.md), [original RC6](assets/3e-solution-structuring-playbook-original-rc6.md). Preserve originais; registre diferença e data.

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

## Passos de análise: aplicação integral de referência

1. **Entrada:** identifique fontes, versões, participantes e decisões de hipótese, problema, 4D, BP1, E1 a E3 e experimentação que existirem. Não exija documentos alheios ao projeto. Em modo assíncrono, indique registros substitutos e deliberações ausentes; etapas previstas no escopo aplicado sem registro exigem parcial. Não atribua aprovação a ausentes nem reescreva decisões anteriores.
2. **Solução/valor:** problema focal, população, hipótese master, escopo, componentes `agora/futuro/fora`, riscos e limites. Expectativa não é resultado observado.
3. **Construção:** recursos, itens a desenvolver, dependências, responsável, apoio e prazo por ação; exponha lacunas antes de declarar MVP pronto.
4. **Experimento:** suposições prioritárias, público elegível, método, intervenção, medida, fonte e critério. Entregue Test Card individual por teste com hipótese, teste, medida e critério, uma frase objetiva por campo (até 280 caracteres); tabela é só índice. Critérios/limiares sem baseline ficam `a fechar antes da coleta`. Preserve originais; cards reconstruídos são retrospectivos. Resultados existentes precisam de fontes/data; Learning Cards somente após execução, nunca achados antes do teste.
5. **Rota:** registre `internal`, `external`, `hybrid` ou `undecided` com fonte e decisão efetiva. Externa/híbrida: o que buscar; interna: o que construir; indefinida: dependências abertas. Rota não valida solução.
6. **Rastreabilidade e conclusão** (obrigatório, conforme [o guia](references/analise-e-conclusao-3e.md)): compare a hipótese do 4D com a refinada no E1; ligue cada componente `precisa ter` à dor ou tema do 4D, com status sustentado, parcial ou sem evidência; confirme que as suposições de "Precisamos validar se" do 4D aparecem no E3 ou estão adiadas com motivo; feche com a conclusão da estruturação (solução, o que construir e testar primeiro, rota, o que segue aberto), condensada também no Resumo. Você compõe essas seções a partir das fontes.
7. Confira relatório/cards/fontes; indique decisões, dados e autorizações necessários ao próximo uso. `experimentacao-inovacao` pode detalhar protocolo/analisar resultados, mas o pacote funciona isoladamente.

## Exemplo

Entrada: “Consolide o 3E do Portal de Solicitações de Dados.”
Saída (trecho):
> Rota híbrida: decisão documentada, capacidades internas/externas distintas.
> TC-01: hipótese, teste, medida e critério prévios.
> Construção planejada não é evidência de eficácia.

## Checagem final

Nos oficiais, confira a receita e as etapas aplicadas conforme [o guia](references/entregaveis-oficiais.md). Os itens metodológicos abaixo se aplicam quando incluídos no escopo, preservando lacunas e exclusões por desenho.

- [ ] Fontes, versão e cronologia preservadas
- [ ] Escopo, construção e lacunas explícitos
- [ ] Cards individuais com quatro campos e status correto
- [ ] Rota sustentada; aprovação não inferida
- [ ] Plano separado de evidências e próximos passos
- [ ] Rastreabilidade do 4D à solução, com status por componente
- [ ] Conclusão com acabativa e Resumo no início

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md), revise com o [guia de escrita](references/guia-de-escrita.md) e siga o [design system](assets/design-system/README.md) e os tipos oficiais acima por padrão; os tipos antigos só
quando o usuário solicitar os depreciados. Faça a análise uma vez e derive relatório e apresentação da mesma base.
Siga [a receita oficial](references/entregaveis-oficiais.md) para montar o JSON de cada oficial e os Test Cards individuais do 3E quando aplicáveis.


Rode `python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o JSON junto dos
derivados. Para oficiais, HTML e PDF fazem parte do perfil; relatório também gera DOCX e apresentação, PPTX.
Use linguagem simples e não use travessão. Corrija falhas de validação; havendo lacuna decisiva, registre versão
parcial ou inconclusiva, sem usar esse estado para esconder conteúdo ausente nem inventar achados.

**Proveniência:** reescrita de fonte metodológica RC6 (`compile-3e-report/`), com separação entre plano, execução e reconstrução posterior, sem restrição por fase.
