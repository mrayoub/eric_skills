# Melhorias propostas para as skills de inovação

**Data:** 28 de setembro de 2026  
**Escopo:** as 11 skills da pasta `my_skills` e seus 18 tipos de entregável.  
**Estado:** propostas de melhoria; este documento não registra sua implementação.  
**Base:** [Revisão e validação das skills](VALIDACAO_SKILLS_2026-09-28.md), fontes metodológicas locais e requisitos definidos pelo usuário.

## 1. Objetivo

Aumentar a confiabilidade das avaliações e dos arquivos produzidos, mantendo a imparcialidade, a rastreabilidade, o funcionamento do grilling e a consistência visual. A melhoria deve chegar ao comportamento executável: uma instrução no SKILL.md não basta quando o calculador ou o renderizador aceita uma saída que a contradiz.

A revisão anterior confirmou a estrutura das 11 skills, a resolução dos links locais, a sintaxe dos 19 schemas compartilhados, a validação dos 18 inputs de amostra e os cinco testes existentes do renderizador. Também encontrou quatro falhas técnicas e lacunas de confirmação institucional. Esses resultados são o ponto de partida; não equivalem a validação completa de todos os métodos, formatos e provedores de LLM.

## 2. Requisitos que devem ser preservados

- Cada skill funciona com seus recursos locais, sem depender da instalação de outra skill, do aplicativo ERIC ou de uma pasta temporária.
- A fase da esteira fornece contexto; o uso de uma skill pode ocorrer antes, durante ou depois do momento usual.
- ERIC significa **Esteira Robusta de Inovação Colaborativa**. O conhecimento institucional deve continuar disponível em cada skill.
- O grilling atua tanto na leitura crítica dos arquivos quanto na interação. Perguntas dependentes aguardam respostas; silêncio e opções preselecionadas não são respostas.
- A skill pergunta por fatos, definições, restrições e decisões metodológicas. A conclusão analítica é determinada pelas evidências.
- Test Cards e Learning Cards são individuais e têm os quatro campos da Strategyzer. Uma tabela de índice não os substitui.
- Think aloud é uma possibilidade de experimentação. O método deve ser escolhido conforme a hipótese e o tipo de evidência necessário.
- Originais, transcrições integrais e adaptações metodológicas permanecem distinguíveis. Ajustes operacionais não reescrevem o material histórico.
- Todos os derivados de uma entrega usam o mesmo JSON canônico validado, com versões de conteúdo, perfil e sistema visual registradas.
- Cards, fontes, cores, orientação e áreas seguras seguem o design system incluído em cada skill. A paginação deve preservar o conteúdo.

## 3. Prioridades e dependências

| Ordem | Melhoria | Prioridade | Dependência principal | Esforço indicativo |
| --- | --- | --- | --- | --- |
| 1 | Corrigir as quatro falhas técnicas conhecidas | Alta | Reproduzir as falhas com casos mínimos | Pequeno a médio por correção |
| 2 | Validar rastreabilidade e coerência semântica | Alta | Contratos e cálculos corrigidos | Médio |
| 3 | Ampliar os ensaios comportamentais das 11 skills | Alta | Critérios de avaliação e casos de teste | Médio |
| 4 | Versionar fontes e confirmar vigência institucional | Média | Documentos ou confirmação de responsáveis | Pequeno a médio |
| 5 | Conferir conteúdo e estrutura visual entre formatos | Alta para IQB; média para expansão geral | Correções do renderizador e registro semântico | Médio |

Os esforços são estimativas iniciais, sujeitas ao desenho da implementação. A confirmação das fontes pode avançar em paralelo com as correções técnicas. A correção de perda de dados no IQB tem prioridade mesmo antes da expansão geral dos testes visuais.

## 4. Melhoria 1 — corrigir as quatro falhas técnicas

### 4.1 Preservar o detalhamento do IQB nos derivados

**Problema observado:** a função `table_rows` em `_DESIGN_SYSTEM/scripts/render.py` transforma o bloco de dimensões IQB nas 40 respostas. Nesse processo, informações existentes no JSON ficam ausentes dessa representação: contagens, notas brutas e finais, detalhes de vetos, justificativas, auditoria de agrupamento e referências individuais dos critérios.

**Efeito:** PDF, HTML, Markdown, TXT e DOCX podem oferecer uma matriz de respostas sem os elementos necessários para auditar a nota. A aparência e a validação estrutural podem estar corretas enquanto a equivalência de conteúdo está incompleta.

**Implementação proposta:**

1. Definir uma representação intermediária que conserve todas as informações obrigatórias do relatório IQB.
2. Separar a matriz de critérios do resumo das dimensões, da aplicação dos vetos e da auditoria de agrupamento.
3. Renderizar essas representações em todos os formatos permitidos, mantendo os IDs das fontes e seus localizadores.
4. Manter tabelas e texto editáveis no DOCX; usar a estrutura de cards para sínteses sem esconder a matriz detalhada.
5. Sincronizar a implementação com os bundles locais das 11 skills.

**Arquivos envolvidos:**

- `_DESIGN_SYSTEM/scripts/render.py`.
- `_DESIGN_SYSTEM/tests/test_render.py`.
- `_SAMPLES_ENTREGAVEIS/briefing_validation/input.json` e seus derivados.
- Cópias correspondentes em `<skill>/assets/design-system/`.

**Critérios de aceite:**

- Um relatório completo apresenta os 40 critérios e o resumo das quatro dimensões.
- Notas brutas/finais, contagens, vetos e justificativas presentes no JSON aparecem nos derivados aplicáveis.
- A auditoria de agrupamento aparece quando exigida, com seu resultado registrado.
- Uma referência por critério continua localizável nos formatos entregues.
- O teste compara os dados obrigatórios, além de conferir títulos e orientação.

### 4.2 Validar a consistência matemática do IQB

**Problema observado:** o schema e a validação atual do renderizador aceitam combinações que contradizem a rubrica, como IQB 1 com classificação Excelente, critérios repetidos, notas incompatíveis com veto e referências internas inexistentes. O calculador principal é mais rigoroso, mas sua lógica não é reconciliada com o conteúdo que chega à renderização.

**Implementação proposta:**

1. Acrescentar validação semântica depois da validação do schema e antes da geração dos arquivos.
2. Verificar cobertura e unicidade dos IDs `CLA`, `EVI`, `OUT` e `ACT`, conforme o estado da entrega.
3. Recalcular contagens, notas brutas, tetos de veto, notas finais, média e classificação com a rubrica versionada.
4. Conferir o resultado calculado contra os campos apresentados pelo JSON; informar divergências com localização precisa.
5. Verificar referências aninhadas nos critérios, além das citações nos blocos superiores.
6. Compartilhar as regras entre calculador e validador por recursos incluídos localmente, preservando a independência das skills.

**Critérios de aceite:**

- Relatórios completos inconsistentes são rejeitados antes da geração dos derivados.
- Os casos acima possuem testes de rejeição específicos.
- Um relatório válido com veto ativo é aceito e reproduz o cálculo correto.
- Uma entrega parcial conserva os dados disponíveis e identifica a ausência; não recebe nota final indevidamente.
- O validador não corrige silenciosamente respostas ou notas para fazer a saída passar.

**Risco da mudança:** relatórios antigos inconsistentes poderão deixar de passar. A mensagem deve explicar o problema e permitir corrigir uma nova versão, preservando o histórico.

### 4.3 Separar chave e rótulo de coluna

**Problema observado:** ao receber `columns` com objetos `{key, label}`, a função `table_rows` passa a usar o rótulo visível para buscar o valor na linha. Uma coluna com chave `count`, rótulo `Quantidade` e linha `{"count": 12}` pode produzir uma célula vazia.

**Implementação proposta:**

- Conservar a chave usada para acessar os dados e o rótulo usado para exibição.
- Manter compatibilidade com cabeçalhos simples, linhas como listas e linhas como objetos.
- Definir o tratamento de campos ausentes sem convertê-los em um valor inventado.

**Critérios de aceite:**

- O exemplo acima apresenta `Quantidade` no cabeçalho e `12` na célula.
- A correção vale para todos os formatos que reutilizam a função, inclusive CSV quando permitido.
- Casos com colunas reordenadas continuam associando cada valor à coluna correta.
- Valores vazios, zero e falsos permanecem distinguíveis conforme o contrato do dado.

### 4.4 Exigir avaliação de potencial sustentada

**Problema observado:** `potencial-inovacao/scripts/score.py` aceita booleanos como notas e permite classificar uma avaliação completa sem justificativas. O schema de saída também não exige a representação estruturada das cinco notas, pesos, total e classe.

**Implementação proposta:**

1. Aceitar notas numéricas finitas dentro de 0–100, rejeitando booleanos.
2. Exigir justificativa não vazia para cada critério antes de declarar a avaliação completa.
3. Representar os cinco critérios, suas fontes, pesos, total e classe no contrato de saída.
4. Recalcular total e classificação e conferir sua correspondência com o relatório.
5. Diferenciar nota zero sustentada de ausência de base para pontuar.
6. Manter o estado incompleto quando faltar nota, justificativa ou suporte exigido; registrar a lacuna correspondente.

**Critérios de aceite:**

- Cinco notas sem justificativas não produzem avaliação completa.
- `true` e `false` não são aceitos como notas.
- Ausência de informação não vira zero.
- Uma avaliação completa exige os cinco critérios e o resultado coerente.
- Os limites de classificação e os pesos continuam seguindo a rubrica vigente.

**Arquivos envolvidos:** `potencial-inovacao/scripts/score.py`, schema de potencial, renderizador/validador e amostra de potencial.

## 5. Melhoria 2 — tornar a rastreabilidade verificável

### 5.1 Objetivo

Transformar os requisitos verificáveis de evidência em checagens executáveis, complementando a revisão metodológica feita pela LLM. Checagens estruturais conseguem identificar vínculos ausentes e incoerências de registro; avaliar se uma evidência realmente sustenta uma conclusão também exige interpretação contextual.

### 5.2 Implementação proposta

Definir uma representação consistente para a ligação entre:

`afirmação → fonte/localizador → evidência → teste/medida → aprendizado → recomendação`

Aplicar requisitos proporcionais ao entregável:

- Afirmações decisivas apontam para uma fonte examinada e uma localização verificável, ou recebem estado explícito de lacuna.
- Fontes localizadas, mas não examinadas, continuam identificadas como tal.
- Test Cards preservam ID, versão, hipótese, teste, medida e critério.
- Learning Cards apontam para o Test Card executado e distinguem observação, inferência e ação.
- Medidas registram unidade, elegibilidade/denominador, janela, fórmula, origem e momento de definição quando necessários.
- Critérios retrospectivos permanecem identificados; não aparecem como prévios à coleta.
- Recomendações apontam para os achados que as sustentam e para os limites do método.
- Pendências do grilling permanecem ligadas aos campos ou conclusões que afetam.

Antes de ampliar os schemas, verificar quais campos já existem nos contratos. A implementação deve evitar criar representações concorrentes do mesmo dado.

### 5.3 Critérios de aceite

- Citações inexistentes, inclusive aninhadas, são detectadas.
- Um Learning Card completo sem ligação ou evidência obrigatória é rejeitado.
- Uma análise parcial é permitida com cobertura e lacunas explícitas.
- Um KPI exploratório pós-coleta não é apresentado como critério prospectivo sem uma divergência identificada.
- A revisão metodológica detecta extrapolações, como transformar preferência de workshop em prova de eficácia ou think aloud em demonstração de impacto operacional.
- A validação preserva a finalidade qualitativa: não exige KPI numérico universal para todo experimento exploratório.

## 6. Melhoria 3 — ampliar os testes comportamentais

### 6.1 Situação atual

Dois ensaios independentes exercitaram o grilling: um briefing com lacunas e uma experimentação com resumo contraditório. Eles demonstraram comportamentos úteis, mas não cobrem individualmente as 11 skills.

### 6.2 Matriz mínima de cenários

| Cenário | Comportamento esperado |
| --- | --- |
| Documentos completos | Resolver as questões nos arquivos e entregar sem perguntas artificiais. |
| Informação decisiva ausente | Perguntar pela lacuna e mostrar sua origem e efeito na entrega. |
| Perguntas dependentes | Esperar a resposta necessária antes de abrir o próximo ramo. |
| Fontes contraditórias | Preservar as versões e investigar a divergência. |
| Arquivo ilegível ou incompleto | Declarar limite de leitura; usar extração/OCR disponível e conferir trechos decisivos. |
| Resposta “não sei” | Registrar quem ou o que pode resolver e continuar o trabalho independente. |
| Pedido de versão parcial | Entregar com pendências explícitas, sem forçar conclusão ou prolongar a entrevista. |
| Novo arquivo após uma resposta | Reavaliar a árvore e reabrir questões contrariadas pela nova fonte. |
| Usuário sugere resultado favorável | Examinar a evidência e manter a conclusão proporcional aos registros. |
| Execução anterior sem plano completo | Identificar reconstrução retrospectiva e preservar a lacuna de critérios prévios. |

### 6.3 Foco por família de skill

- **Briefing:** sete campos, versionamento, metas propostas versus aprovadas, perguntas resolvidas documentalmente e ausência de sponsor.
- **IQB:** 40 critérios, vetos, cálculo e distinção entre evidência ausente e fonte inacessível.
- **Potencial:** justificativas, falta de base para pontuar, impacto esperado versus medido e sensibilidade da classificação.
- **Workshops 4D/3E/5C:** preparação versus registro de execução, regras de voto, participantes, dissensos e ausência de decisão formal.
- **Relatórios 4D/3E/5C:** fidelidade aos registros, ausência de ranking comprovável e distinção entre playbook e resultados.
- **Experimentação:** escolha do método, definição prévia de critérios, ajuda do moderador, denominadores e cards individuais.
- **Scorecard:** força das evidências, dimensões não aplicáveis, adaptação institucional e ausência de nota sustentada.

### 6.4 Critérios de aceite

Cada skill possui ao menos um caso com suporte suficiente e outro com lacuna ou contradição relevante. Os casos usados para verificar interação incluem respostas em múltiplas rodadas. O avaliador recebe o pedido, a skill e os arquivos, sem receber a conclusão esperada.

A avaliação usa comportamentos observáveis, fontes e estados da entrega; não exige correspondência literal com uma resposta-modelo. Quando uma falha for encontrada, a correção deve ser verificada no caso que a revelou. Novos testes em outros provedores podem ampliar a evidência de portabilidade, com modelo e versão registrados.

## 7. Melhoria 4 — versionar fontes e confirmar vigência

### 7.1 Registro de proveniência

Criar um manifesto local de fontes em cada skill, ou aproveitar um registro já existente, com:

- ID, título e tipo da fonte.
- Arquivo local e URL/origem quando aplicável.
- Autor ou instituição, quando conhecidos.
- Versão declarada, data de publicação e data de consulta/importação.
- Hash do original.
- Estado de vigência: confirmado, histórico ou desconhecido.
- Relação entre original, transcrição e adaptação.
- Diferenças metodológicas introduzidas e razão de cada uma.

Metadados desconhecidos devem continuar desconhecidos. Uma cópia do RC6 ou uma fonte fornecida pelo usuário não comprova, por si só, aprovação institucional.

### 7.2 Pendências conhecidas

| Material | Situação atual | Informação útil para resolver |
| --- | --- | --- |
| Perguntas/modelo do briefing | Modelo Markdown e DOCX histórico localizados | Confirmar a versão vigente e fornecer roteiro oficial adicional, se existir. |
| IQB | Rubrica e calculador derivados do RC6 | Norma institucional aprovada, versão e responsável. |
| Potencial de inovação | Cinco critérios, pesos e faixas derivados do RC6 | Confirmar regra vigente e obter âncoras de pontuação, se houver. |
| Esteira ERIC | Contexto local baseado em RC5/RC6, com partes da origem em draft | Documento institucional vigente ou registro de aprovação. |
| 4D e 3E | Originais DOCX e transcrições importados | Autoria, revisão ou aprovação, caso existam fora do texto. |
| 5C | Original de um encontro de Centralidade no Cliente e transcrição integral | Versão institucional genérica mais recente, caso exista. |

### 7.3 Critérios de aceite

- Cada adaptação relevante pode ser relacionada a uma fonte identificada.
- Originais continuam preservados sem reescrita.
- Transcrições mantêm o conteúdo e a ordem, com limites de conversão documentados.
- Uma fonte nova gera comparação e versão atualizada, preservando a anterior.
- As cópias necessárias permanecem dentro de cada skill.
- A confirmação institucional não bloqueia correções técnicas que já tenham evidência suficiente.

## 8. Melhoria 5 — conferir conteúdo e estrutura visual entre formatos

### 8.1 Objetivo

Verificar que o conteúdo validado chega inteiro aos formatos permitidos, com a estrutura de cards e tabelas acordada. A equivalência deve considerar semântica e geometria; hashes binários de PDF/DOCX/PPTX podem variar por metadados internos.

### 8.2 Implementação proposta

1. Selecionar dados obrigatórios de cada tipo de entregável e compará-los com os derivados.
2. Conferir títulos, campos, ordem, valores, notas, estados, IDs e referências.
3. Incluir casos com texto longo, tabelas extensas, múltiplas páginas, grades de cards e fontes numerosas.
4. Verificar página/orientação, áreas seguras, fonte mínima, cortes e sobreposição no PDF.
5. Inspecionar o DOCX e o PPTX quanto à presença de texto e componentes editáveis; conferir a aparência no software-alvo quando possível.
6. Testar renderização repetida do mesmo JSON com as mesmas versões de perfil, tokens, fontes e renderizador.
7. Validar apenas formatos permitidos pelo perfil: PPTX para apresentação e CSV para tabelas exportáveis.
8. Regenerar as amostras afetadas depois da correção e guardar manifestos atualizados.

### 8.3 Critérios de aceite

- Dados obrigatórios presentes no JSON aparecem nos derivados aplicáveis.
- Uma tabela não perde valores por mudança de chave/rótulo.
- Test Cards e Learning Cards mantêm seus quatro campos individuais.
- O resumo de uma página respeita esse limite; excesso de conteúdo gera indicação clara, sem corte ou redução abaixo da fonte mínima.
- Relatórios extensos paginam conservando a leitura dos cards e tabelas.
- A orientação definida no perfil é respeitada.
- Reexecutar o mesmo conteúdo mantém a aparência e a estrutura, dentro dos limites conhecidos das bibliotecas e aplicações.

## 9. Organização da implementação

A manutenção do design system deve partir de `_DESIGN_SYSTEM`, seguida de sincronização e conferência dos bundles em cada skill. As skills distribuídas continuam contendo todos os recursos necessários.

Para cada melhoria:

1. Registrar o problema e um caso que reproduza seu efeito.
2. Definir arquivos e contratos afetados.
3. Implementar a alteração e verificar o caso concreto.
4. Rodar os testes existentes pertinentes e os testes novos necessários.
5. Sincronizar recursos locais e conferir diferenças entre bundles.
6. Regenerar somente as amostras afetadas e revisar os derivados.
7. Registrar resultado, limitações e pendências.

Quando uma alteração de contrato invalidar conteúdos antigos, versionar a mudança e definir como reconhecer ou converter versões anteriores. Nenhum resultado histórico deve ser recalculado e substituído silenciosamente.

## 10. Verificações de referência

O validador estrutural pode ser executado para cada pasta de skill:

```bash
python /Users/mayoub/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/mayoub/Desktop/workspaces/my_skills/<skill>
```

Os testes existentes do renderizador podem ser executados a partir da raiz, em ambiente com as dependências e bibliotecas nativas de PDF disponíveis:

```bash
python -m pytest -q _DESIGN_SYSTEM/tests/test_render.py
```

A validação e renderização de uma amostra usam o script incluído no bundle correspondente:

```bash
python <skill>/assets/design-system/scripts/render.py input.json --out-dir pasta-de-validacao --formats html,pdf,docx,md,txt
```

A lista de formatos deve ser ajustada ao perfil da entrega. Esses comandos documentam a verificação atual; os novos critérios exigem novos casos e checagens. Uma execução bem-sucedida dos testes existentes não resolve automaticamente as falhas registradas na auditoria.

## 11. Condição de conclusão das melhorias

O conjunto estará concluído quando:

- As quatro falhas técnicas tiverem correção demonstrada por casos de regressão.
- A validação estrutural e semântica rejeitar inconsistências relevantes sem fabricar informação.
- Cada skill tiver evidência de funcionamento do grilling em leitura e interação, conforme sua finalidade.
- Fontes e adaptações estiverem versionadas, com vigência desconhecida explicitamente registrada quando necessário.
- Os derivados preservarem dados obrigatórios e a estrutura visual dos perfis.
- As 11 skills continuarem independentes, portáveis e utilizáveis em diferentes momentos do processo de inovação.

A conclusão deve ser sustentada pelas verificações registradas, mantendo visíveis os limites de cobertura por formato, aplicação e provedor de LLM.
