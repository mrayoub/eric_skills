---
name: scorecard-inovacao
description: "Avalia a maturidade das evidências de um projeto de inovação com o Innovation Project Scorecard da Strategyzer, oficial ou em adaptação institucional declarada, gerando um retrato datado, sem média geral, com lacunas decisivas e próximos testes. Use quando o usuário perguntar quão validado ou maduro está um projeto, se há evidência suficiente para passar um gate, ou quiser comparar retratos ao longo da esteira. Não use para dar nota a um briefing (use avaliacao-briefing-iqb) nem para priorizar oportunidades novas (use potencial-inovacao)."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Requer Python 3 e os pacotes de assets/design-system/requirements.txt para gerar DOCX, PPTX e PDF."
  author: "GEIN-CCEE"
  version: "1.1.2"
---

# Scorecard de evidências para inovação

Produz retrato datado da maturidade das evidências, não da qualidade de execução da fase nem aprovação automática de gate.

## Leia primeiro

- [Estrutura e adaptação](references/estrutura-e-adaptacao.md) — instrumento oficial Strategyzer e traduções institucionais.
- [Entrevista documental](references/entrevista-e-documentos.md) — leitura, árvore de decisões e conceitos; rotina incorporada, sem instalar outras skills.
- [Extração documental](references/extracao-documental.md) — PDF, Office, HTML, tabelas e imagens.

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md) antes de sintetizar,
pontuar ou planejar, e reaplique-o a cada arquivo ou resposta novos. Em resumo: resolva
nos arquivos tudo que for pesquisável; pergunte só a fronteira de questões decisivas
cujas dependências já estão resolvidas; registre origem e localizador de cada resposta;
entregue versão parcial quando faltar suporte decisivo. Nunca pergunte a nota, o
resultado ou a conclusão desejada — isso não é dado, e contaminaria a avaliação.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Quando usar

A fase do projeto é contexto, não pré-requisito. Se o pedido vier antes do momento
usual, entregue preparação ou versão parcial; se vier depois, use o material posterior
com data e não apresente reconstrução como plano combinado previamente.

## Passos

1. Identifique projeto, pergunta decisória, fase, data de corte, versão, público, escopo e responsáveis pela análise/gate. Preserve retratos anteriores; compare versões sem alterar notas passadas com evidências novas. Se o pedido não deixar claro que o usuário quer o retrato formal do Scorecard, e não apenas uma opinião geral sobre o progresso, confirme isso antes de aplicar as dimensões e gravar o retrato datado.
2. Inventarie fontes de todas as fases disponíveis: `examinada`, `localizada, não examinada`, `indisponível`, `fora do escopo`. Leia escopo/hipótese vigente, depois fontes primárias e versões anteriores; mais recente não significa melhor evidência. Extraia afirmações, definições, decisões, evidências e conflitos com página/slide/seção/célula/tempo; registre falhas e confira tabelas/números no original. Entrevista de descoberta não é observação de uso do MVP.
3. Declare modalidade: oficial como referência para modelo de negócio/proposta de valor, ou adaptação institucional para serviço, eficiência ou conformidade. Explicite tradução de cada dimensão; custo evitado não é receita, uso obrigatório não prova desejabilidade. Não apresente adaptação como formulário oficial nem reproduza seu layout.
4. Aplique a entrevista documental somente às lacunas decisivas: perguntas por fronteira, dependências resolvidas, origem/motivo e recomendação apenas de método/definição/próximo passo. Respostas registram escopo/decisão, não eficácia. Leia fontes apontadas; reabra conflitos. Teste termos ambíguos por cenário, guarde conceitos recorrentes no glossário e decisões duráveis com alternativas/razão; respostas pontuais ficam no registro. Recapitule interpretação decisiva para correção, sem pedir aprovação da conclusão. Com fonte externa ausente ou encerramento do usuário, entregue parcial sem notas dependentes; evite repetir perguntas sem informação nova.
5. Por dimensão aplicável, registre afirmação, fonte/localizador, evidência favorável/contrária, data, população, versão e limites. Distinga `sem evidência`, `evidência contrária`, `não aplicável`, `não avaliado`. Julgue proximidade com comportamento, qualidade da medida, cobertura e replicação. Escala oficial de redução de riscos: 0–5, distinguindo declaração, reação a artefato, ação e mercado real. Nota exige rubrica definida e suporte; adaptação numérica usa rubrica própria declarada. Sem base, `não pontuável`; fase/opinião do sponsor não completam nota.
6. Separe necessidade, usabilidade, implementação, efeito operacional e custo. Relatos não provam adoção/impacto; testes parciais deixam demais dimensões abertas. Não calcule média geral ou sinal verde: uma nota alta não compensa falha crítica. Destaque evidência fraca/contrária, riscos de dano e dependências.
7. Use o [modelo de saída](assets/scorecard-projeto.md): retrato datado, mudanças, lacunas e próximos testes ligados às dimensões/evidências. Registre decisão efetiva só com fonte; recomendação analítica fica separada. Declare pendências que mudariam a leitura.

## Exemplo

Entrada: “Avalie o Portal de Solicitações de Dados; temos só entrevistas.”
Saída (trecho):
> Modalidade: adaptação institucional, traduções declaradas.
> Adoção: sem evidência; intenção de uso não é uso observado.
> Próximo teste: comportamento com MVP; sem média geral.

## Checagem final

- [ ] Modalidade, rubrica e data de corte declaradas
- [ ] Inventário e extração verificáveis, sem fontes presumidas
- [ ] Notas/estados sustentados, com contraevidência e limites
- [ ] Ausência, inaplicabilidade e evidência contrária distinguidas
- [ ] Sem média geral ou aprovação automática
- [ ] Próximos testes ligados às lacunas; decisão documentada

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de
Energia Elétrica). Consulte [a esteira](references/eric-esteira.md) quando precisar
interpretar etapas, pontos de avaliação (BP1/BP2), rotas ou relações entre entregáveis.

## Entrega em arquivo

Use [linguagem simples](references/linguagem-dos-entregaveis.md) no chat e nos arquivos; siga [o design system](assets/design-system/README.md)
com `deliverable_type` `innovation_scorecard`: monte o JSON canônico, rode
`python3 assets/design-system/scripts/render.py entrada.json --out-dir saida` e entregue o
JSON junto dos derivados. Se a validação falhar, corrija o conteúdo ou marque
`metadata.completeness: "partial"` — nunca contorne o schema.

**Proveniência:** instrumento Strategyzer como referência; adaptação institucional e rotina documental incorporadas nos recursos locais, com origens registradas nas referências.
