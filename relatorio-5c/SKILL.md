---
name: relatorio-5c
description: "Compila ou revisa o Relatório oficial 5C e a Apresentação oficial 5C a partir dos registros da execução, com fontes e análise; usa o playbook como padrão e admite adaptações e versões pocket documentadas. Mantém Relatório depreciado e Apresentação depreciada quando solicitados. Use para consolidar registros, apresentação a gestores, devolutiva ou revisão. Não use para facilitar o workshop."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.4.4"
---

# Compilar o Relatório 5C

Consolida cocriação; playbook sozinho não fornece achados, votos ou consenso, nem valida eficácia ou autoriza escala.

## Escolha da entrega

O padrão é **Relatório oficial 5C** (`five_c_official_report`) ou **Apresentação oficial 5C**
(`five_c_official_presentation`). Leia [a receita oficial](references/entregaveis-oficiais.md) antes de compor.
Ela define conteúdo, JSON, adaptação do método e [tom da autora](references/tom-oficial.md) para os dois oficiais.

Os antigos continuam disponíveis apenas quando pedidos como **Relatório depreciado 5C** (`five_c_report`)
ou **Apresentação depreciada 5C** (`five_c_presentation`). As estruturas anteriores nas referências e no roteiro
integral abaixo orientam análise e os depreciados; não substituem a receita oficial nem obrigam uma aplicação pocket
a cobrir o playbook inteiro. Nos oficiais, prevalecem a receita oficial e o escopo de aplicação documentado.

## Leia primeiro

- [Método 5C](references/metodo-5c.md): estrutura metodológica.
- [Relatório e apresentação do 5C](references/entregas-5c.md): as duas entregas, a base comum da análise, a triangulação com o diagnóstico e a estrutura dos slides.
- [Escrita e organização do Relatório 5C](references/escrita-relatorio-5c.md): eixo da análise, ordem das seções, de onde vem cada seção e jeito de escrever.
- [Exemplos](references/exemplos/README.md): o exemplo de referência, feito pela autora do playbook, prevalece sobre os demais; imite estrutura e escrita, nunca o conteúdo.
Para conferir a fonte: [transcrição](assets/Playbook_Modelo_5C_Centralidade_Cliente.transcricao.md) e [DOCX](assets/Playbook_Modelo_5C_Centralidade_Cliente.docx).

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

1. **Entrada/contexto:** inventarie briefing, diagnóstico, convites/presença, materiais exibidos, mural/notas, gravações, formulários, votos, canvases, ata e decisões. Registre identificador/data/versão/localizador; distinga fala de cliente, relato interno, dado, proposta, inferência e decisão. Documente desafio original/revisão, convidados/presentes, perfis cobertos/ausentes, objetivo, duração/adaptações e regras. Presença não representa toda população; pergunte só por fontes/definições/decisões decisivas. O playbook é o 5C oficial; se a execução adaptou etapas, formato ou regras, declare a adaptação (etapa oficial, etapa aplicada, o que mudou e motivo) e a unidade de contagem, usando a organização participante como eixo da análise.
2. **C1 Contextualizar:** enquadramento apresentado, evidências, dúvidas e mudanças.
3. **C2 Compreender:** temas, experiências positivas, dificuldades, episódios, contradições e oportunidades; votos com regra efetiva, elegibilidade e denominador. Menções não são prevalência sem desenho adequado.
4. **C3 Confirmar:** dores escolhidas, experiência desejada, situações a evitar, necessidades e critérios observáveis. Separe critério proposto, meta aprovada e resultado medido.
5. **C4 Cocriar:** ideias/propostas, composição real dos grupos, origem das ideias, dor, funcionamento, benefícios alegados, dependências, riscos e alternativas descartadas.
6. **C5 Conduzir:** pitches, créditos, votos/ranking reproduzível, razões, objeções e aprendizados; separe preferência, recomendação e decisão efetiva. Sem votação confiável, registre lacuna, não ranking fabricado.
7. **Síntese/próximos passos:** Resumo no topo, divergências entre organizações e hipóteses a testar (não são decisões), com achados citados, limites, responsáveis e devolutiva acordada. Você compõe essas seções a partir das fontes e do grilling; não peça ao usuário que as escreva (veja "De onde vem cada seção" no guia de escrita). Eficácia, adesão e viabilidade exigem experimento adequado, sem antecipar resultado.

Reconcilie totais entre narrativa/quadros; preserve conflitos e não atribua fala/aprovação sem fonte. Nos depreciados integrais, relatório completo exige síntese/fonte em C1 a C5. Nos oficiais, completude considera as etapas do escopo aplicado: exclusão por desenho não é lacuna. Fontes posteriores atualizam com data; revisões preservam a versão original.

## Exemplo

Entrada: “Relate o 5C do Portal de Solicitações de Dados.”
Saída (trecho):
> Ata: B aprovada; planilha: A recebeu mais créditos.
> Conflito preservado; pedir fonte da decisão formal.
> Votos não validam efeito da solução.

## Checagem final

Nos oficiais, confira a receita e as etapas aplicadas conforme [o guia](references/entregaveis-oficiais.md). Os itens metodológicos abaixo se aplicam quando incluídos no escopo, preservando lacunas e exclusões por desenho.

- [ ] C1 a C5 e versões separadas, com síntese/fonte
- [ ] Adaptação do 5C oficial declarada, quando houver, e eixo da análise adequado ao formato (tema ou organização)
- [ ] Relatório e apresentação, quando houver os dois, consistentes entre si e com a mesma base
- [ ] Denominadores, regras e totais conferidos
- [ ] Falas, conflitos e alternativas preservados
- [ ] Preferência, meta, decisão e efeito distinguidos
- [ ] Recomendação proporcional e pendências explícitas

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md), revise com o [guia de escrita](references/guia-de-escrita.md) e siga o [design system](assets/design-system/README.md) e os tipos oficiais acima por padrão; os tipos antigos só
quando o usuário solicitar os depreciados. Faça a análise uma vez e derive relatório e apresentação da mesma base.
Siga [a receita oficial](references/entregaveis-oficiais.md) para montar o JSON de cada oficial.


Rode `python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o JSON junto dos
derivados. Para oficiais, HTML e PDF fazem parte do perfil; relatório também gera DOCX e apresentação, PPTX.
Use linguagem simples e não use travessão. Corrija falhas de validação; havendo lacuna decisiva, registre versão
parcial ou inconclusiva, sem usar esse estado para esconder conteúdo ausente nem inventar achados.

**Proveniência:** adaptação do playbook 5C fornecido pelo usuário, preservado integralmente em `assets/`. A análise de uma execução depende de fontes adicionais daquela execução.
