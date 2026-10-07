---
name: relatorio-5c
description: "Compila ou revisa o Relatório 5C de um encontro de cocriação com clientes, ligando C1 a C5 a falas, votos com denominador, critérios de experiência, propostas, dissensos e próximos passos. Use quando houver registros de um workshop 5C (notas, mural, gravação, votos, ata) e o usuário quiser o relatório, a síntese ou a devolutiva aos participantes. Não use para preparar ou facilitar o encontro (use workshop-5c)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.0.0"
---

# Compilar o Relatório 5C

Consolida cocriação; playbook sozinho não fornece achados, votos ou consenso, nem valida eficácia ou autoriza escala.

## Leia primeiro

- [Método 5C](references/metodo-5c.md) — estrutura metodológica.
Para conferir a fonte: [transcrição](assets/Playbook_Modelo_5C_Centralidade_Cliente.transcricao.md) e [DOCX](assets/Playbook_Modelo_5C_Centralidade_Cliente.docx).

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md) antes de sintetizar,
pontuar ou planejar, e reaplique-o a cada arquivo ou resposta novos. Em resumo: resolva
nos arquivos tudo que for pesquisável; pergunte só a fronteira de questões decisivas
cujas dependências já estão resolvidas; registre origem e localizador de cada resposta;
entregue versão parcial quando faltar suporte decisivo. Nunca pergunte a nota, o
resultado ou a conclusão desejada — isso não é dado, e contaminaria a avaliação.

## Quando usar

A fase do projeto é contexto, não pré-requisito. Se o pedido vier antes do momento
usual, entregue preparação ou versão parcial; se vier depois, use o material posterior
com data e não apresente reconstrução como plano combinado previamente.

## Passos

1. **Entrada/contexto:** inventarie briefing, diagnóstico, convites/presença, materiais exibidos, mural/notas, gravações, formulários, votos, canvases, ata e decisões. Registre identificador/data/versão/localizador; distinga fala de cliente, relato interno, dado, proposta, inferência e decisão. Documente desafio original/revisão, convidados/presentes, perfis cobertos/ausentes, objetivo, duração/adaptações e regras. Presença não representa toda população; pergunte só por fontes/definições/decisões decisivas.
2. **C1 — Contextualizar:** enquadramento apresentado, evidências, dúvidas e mudanças.
3. **C2 — Compreender:** temas, experiências positivas, dificuldades, episódios, contradições e oportunidades; votos com regra efetiva, elegibilidade e denominador. Menções não são prevalência sem desenho adequado.
4. **C3 — Confirmar:** dores escolhidas, experiência desejada, situações a evitar, necessidades e critérios observáveis. Separe critério proposto, meta aprovada e resultado medido.
5. **C4 — Cocriar:** ideias/propostas, composição real dos grupos, origem das ideias, dor, funcionamento, benefícios alegados, dependências, riscos e alternativas descartadas.
6. **C5 — Conduzir:** pitches, créditos, votos/ranking reproduzível, razões, objeções e aprendizados; separe preferência, recomendação e decisão efetiva. Sem votação confiável, registre lacuna, não ranking fabricado.
7. **Síntese/próximos passos:** achados citados, limites, suposições a testar, responsáveis e devolutiva acordada. Eficácia, adesão e viabilidade exigem experimento adequado, sem antecipar resultado.

Reconcilie totais entre narrativa/quadros; preserve conflitos e não atribua fala/aprovação sem fonte. Relatório completo exige síntese/fonte em C1–C5; etapas ausentes mantêm parcial. Fontes posteriores atualizam com data; revisões preservam a versão original.

## Exemplo

Entrada: “Relate o 5C do Portal de Solicitações de Dados.”
Saída (trecho):
> Ata: B aprovada; planilha: A recebeu mais créditos.
> Conflito preservado; pedir fonte da decisão formal.
> Votos não validam efeito da solução.

## Checagem final

- [ ] C1–C5 e versões separadas, com síntese/fonte
- [ ] Denominadores, regras e totais conferidos
- [ ] Falas, conflitos e alternativas preservados
- [ ] Preferência, meta, decisão e efeito distinguidos
- [ ] Recomendação proporcional e pendências explícitas

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `five_c_report`: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** adaptação do playbook 5C fornecido pelo usuário, preservado integralmente em `assets/`. A análise de uma execução depende de fontes adicionais daquela execução.
