# Menções a RC5 e RC6 nas onze skills

Levantamento solicitado em 29/09/2026, antes da limpeza. Inclui ERIC_RC5, ERIC_RC6, RC5 e RC6, sem distinguir maiúsculas/minúsculas, nos textos e nomes de arquivos. Este registro histórico fica fora das skills.

Resultado: **62 arquivos com referência, 229 menções textuais e quatro nomes de arquivos**. Foram examinados 445 arquivos de texto e 10 documentos DOCX/PDF; os documentos binários não contêm menções detectadas no texto, XML ou metadados.

As cópias compartilhadas estão listadas individualmente para registrar todas as ocorrências. Uma mesma linha pode conter mais de uma menção.

## Comparação antes e depois

O levantamento acima é o estado **antes**, registrado em 29/09/2026. O estado **depois** foi conferido na mesma data, sobre o commit `e5bdf3d`, antes de iniciar os planos 020–023. Não houve limpeza ou edição das referências entre as duas leituras. A varredura atual dos pacotes confirmou os mesmos totais; as alterações não relacionadas já presentes no workspace estão fora das onze skills.

| Medida | Antes | Depois | Variação |
| --- | ---: | ---: | ---: |
| Arquivos com menção no texto ou no nome | 62 | 62 | 0 |
| Menções textuais a `ERIC_RC5`, `ERIC_RC6`, `RC5` ou `RC6` | 229 | 229 | 0 |
| Nomes de arquivo com esses termos | 4 | 4 | 0 |

| Skill | Arquivos antes/depois | Menções antes/depois | Nomes antes/depois |
| --- | ---: | ---: | ---: |
| avaliacao-briefing-iqb | 7 / 7 | 20 / 20 | 0 / 0 |
| briefing-inovacao | 4 / 4 | 17 / 17 | 0 / 0 |
| experimentacao-inovacao | 3 / 3 | 16 / 16 | 0 / 0 |
| potencial-inovacao | 6 / 6 | 19 / 19 | 0 / 0 |
| relatorio-3e | 8 / 8 | 26 / 26 | 1 / 1 |
| relatorio-4d | 8 / 8 | 27 / 27 | 1 / 1 |
| relatorio-5c | 3 / 3 | 16 / 16 | 0 / 0 |
| scorecard-inovacao | 3 / 3 | 16 / 16 | 0 / 0 |
| workshop-3e | 8 / 8 | 26 / 26 | 1 / 1 |
| workshop-4d | 9 / 9 | 30 / 30 | 1 / 1 |
| workshop-5c | 3 / 3 | 16 / 16 | 0 / 0 |

Contagem reproduzível: nas onze pastas com `SKILL.md`, examine cada arquivo legível como texto e conte ocorrências sem distinção de maiúsculas e minúsculas com a expressão `ERIC_RC[56]|RC[56]`; conte separadamente os caminhos que contêm a mesma expressão. Os dez DOCX/PDF foram conferidos no levantamento inicial; nenhum desses binários mudou nesta comparação. Esta comparação registra estabilidade das referências, sem afirmar que foram removidas ou substituídas.

## avaliacao-briefing-iqb/SKILL.md

Linha 67:

```text
**Proveniência:** rubrica, schema e cálculo adaptados de fonte metodológica RC6 (`validate-briefing/`); o cálculo foi endurecido para impedir pontuação com itens ausentes.
```

## avaliacao-briefing-iqb/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## avaliacao-briefing-iqb/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## avaliacao-briefing-iqb/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## avaliacao-briefing-iqb/references/fontes.md

Linha 10:

```text
| Rubrica IQB | rubrica | [references/iqb-rubric.md](<../references/iqb-rubric.md>) | — | desconhecida | 0c2358afc007 | A origem RC6 não comprova norma institucional vigente. |
```

## avaliacao-briefing-iqb/references/iqb-rubric.md

Linha 3:

```text
Preserva os 40 critérios, vetos e faixas do ERIC_RC6 1.0.0. O cálculo portátil exige todos os itens com resposta e justificativa explícitas; a auditoria de agrupamento é tarefa do avaliador, não algo que o script pode declarar como concluído sozinho.
```

## avaliacao-briefing-iqb/scripts/iqb.py

Linha 4:

```text
(adaptada de ``validate-briefing`` do ERIC_RC6).
```

## briefing-inovacao/SKILL.md

Linha 77:

```text
**Proveniência:** adaptação das três skills homônimas das fontes metodológicas do RC6, com a estrutura de briefing do ERIC_RC1 preservada nos recursos locais. Funciona sem infraestrutura da iniciativa de origem.
```

## briefing-inovacao/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## briefing-inovacao/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## briefing-inovacao/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## experimentacao-inovacao/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## experimentacao-inovacao/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## experimentacao-inovacao/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## potencial-inovacao/SKILL.md

Linha 73:

```text
**Proveniência:** rubrica e algoritmo adaptados do RC6 (`calculate-innovation-potential/`), revistos para preservar incompletude em vez de classificar faltas como zero.
```

## potencial-inovacao/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## potencial-inovacao/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## potencial-inovacao/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## potencial-inovacao/references/fontes.md

Linha 10:

```text
| Rubrica de potencial de inovação | rubrica | [references/innovation-potential-rubric.md](<../references/innovation-potential-rubric.md>) | — | desconhecida | 25d8812909b7 | A origem RC6 não comprova norma institucional vigente. |
```

## potencial-inovacao/references/innovation-potential-rubric.md

Linha 3:

```text
Preserva critérios, pesos e faixas do ERIC_RC6 1.0.0. A regra de ausência foi corrigida: nota faltante ou inválida não é zero; sem os cinco critérios sustentados o resultado permanece incompleto e sem classificação. Zero continua possível quando há avaliação explícita e justificada.
```

## relatorio-3e/SKILL.md

Linha 14:

```text
Para conferir a fonte: [transcrição](<assets/Modelo 3E Estruturação da Solução.transcricao.md>), [DOCX](<assets/Modelo 3E Estruturação da Solução.docx>), [divergências](references/fonte-3e-e-divergencias.md), [original RC6](assets/3e-solution-structuring-playbook-original-rc6.md). Preserve originais; registre diferença e data.
```

Linha 70:

```text
**Proveniência:** reescrita de fonte metodológica RC6 (`compile-3e-report/`), com separação entre plano, execução e reconstrução posterior, sem restrição por fase.
```

## relatorio-3e/assets/3e-solution-structuring-playbook-original-rc6.md

- O nome/caminho do arquivo contém `rc6`.

## relatorio-3e/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## relatorio-3e/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## relatorio-3e/references/3e-solution-structuring-playbook.md

Linha 5:

```text
> Adaptação da referência textual do ERIC_RC6. A ordem E1–E3 pertence ao método; a fase da esteira é contexto, não condição de uso.
```

Linha 13:

```text
- Aplique E1–E3 quando houver uma solução candidata, inclusive antes da ideação formal ou após testes para revisar o plano. No RC6, os registros costumam ficar em `ideation`.
```

## relatorio-3e/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## relatorio-3e/references/fonte-3e-e-divergencias.md

Linha 1:

```text
# Fonte 3E fornecida e comparação com o RC6
```

## relatorio-3e/references/fontes.md

Linha 9:

```text
| Método operacional 3E | adaptacao | [references/3e-solution-structuring-playbook.md](<../references/3e-solution-structuring-playbook.md>) | Fonte fornecida 3E (3e-docx) | desconhecida | 509207c6b969 | Também utiliza contexto histórico RC6; regras operacionais adicionais não são exigências literais do DOCX. |
```

Linha 12:

```text
| Playbook histórico 3E do RC6 | historico | [assets/3e-solution-structuring-playbook-original-rc6.md](<../assets/3e-solution-structuring-playbook-original-rc6.md>) | — | historica | 484d1d4aebe1 | Contexto histórico; não substitui automaticamente o DOCX fornecido. |
```

## relatorio-4d/SKILL.md

Linha 14:

```text
Para conferir a fonte: [transcrição](<assets/Modelo 4D de Aprofundamento.transcricao.md>), [DOCX](<assets/Modelo 4D de Aprofundamento.docx>), [divergências](references/fonte-4d-e-divergencias.md), [original RC6](assets/4d-workshop-playbook-original-rc6.md), [PDF de referência](assets/official-four-d-report.pdf). Preserve originais; registre diferenças e datas; não copie conteúdo de outro projeto.
```

Linha 70:

```text
**Proveniência:** reescrita de fonte metodológica RC6 (`compile-4d-report/`); a ordem interna D1–D4 foi preservada, sem transformar a fase de origem em condição de uso.
```

## relatorio-4d/assets/4d-workshop-playbook-original-rc6.md

- O nome/caminho do arquivo contém `rc6`.

## relatorio-4d/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## relatorio-4d/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## relatorio-4d/references/4d-workshop-playbook.md

Linha 5:

```text
> Adaptação da referência textual do ERIC_RC6. A ordem D1–D4 é do método; a fase citada na origem é contexto, não condição de uso.
```

Linha 14:

```text
- No RC6, a rodada é registrada em `problem_deepening` e o relatório pode alimentar o BP1; esses campos não bloqueiam o método fora dessa posição.
```

## relatorio-4d/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## relatorio-4d/references/fonte-4d-e-divergencias.md

Linha 1:

```text
# Fonte 4D fornecida e comparação com o RC6
```

Linha 9:

```text
A referência adaptada do RC6 reproduz esses elementos. Seus trechos de integração com a esteira e suas regras de evidência são adaptações posteriores; não constam como exigências na fonte DOCX.
```

## relatorio-4d/references/fontes.md

Linha 9:

```text
| Método operacional 4D | adaptacao | [references/4d-workshop-playbook.md](<../references/4d-workshop-playbook.md>) | Fonte fornecida 4D (4d-docx) | desconhecida | 27ae817e7c94 | Também utiliza contexto histórico RC6; regras operacionais adicionais não são exigências literais do DOCX. |
```

Linha 13:

```text
| Playbook histórico 4D do RC6 | historico | [assets/4d-workshop-playbook-original-rc6.md](<../assets/4d-workshop-playbook-original-rc6.md>) | — | historica | 76dc8d5335b0 | Contexto histórico; não substitui automaticamente o DOCX fornecido. |
```

## relatorio-5c/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## relatorio-5c/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## relatorio-5c/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## scorecard-inovacao/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## scorecard-inovacao/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## scorecard-inovacao/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## workshop-3e/SKILL.md

Linha 14:

```text
Para conferir a fonte: [transcrição](<assets/Modelo 3E Estruturação da Solução.transcricao.md>), [DOCX](<assets/Modelo 3E Estruturação da Solução.docx>), [divergências](references/fonte-3e-e-divergencias.md), [original RC6](assets/3e-solution-structuring-playbook-original-rc6.md). Preserve originais e registre diferenças/data.
```

Linha 72:

```text
**Proveniência:** reescrita de fonte metodológica RC6 (`facilitate-3e-workshop/`). A ordem interna E1–E3 e a separação entre plano e evidência foram preservadas sem restringir a fase de uso.
```

## workshop-3e/assets/3e-solution-structuring-playbook-original-rc6.md

- O nome/caminho do arquivo contém `rc6`.

## workshop-3e/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## workshop-3e/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## workshop-3e/references/3e-solution-structuring-playbook.md

Linha 5:

```text
> Adaptação da referência textual do ERIC_RC6. A ordem E1–E3 pertence ao método; a fase da esteira é contexto, não condição de uso.
```

Linha 13:

```text
- Aplique E1–E3 quando houver uma solução candidata, inclusive antes da ideação formal ou após testes para revisar o plano. No RC6, os registros costumam ficar em `ideation`.
```

## workshop-3e/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## workshop-3e/references/fonte-3e-e-divergencias.md

Linha 1:

```text
# Fonte 3E fornecida e comparação com o RC6
```

## workshop-3e/references/fontes.md

Linha 9:

```text
| Método operacional 3E | adaptacao | [references/3e-solution-structuring-playbook.md](<../references/3e-solution-structuring-playbook.md>) | Fonte fornecida 3E (3e-docx) | desconhecida | 509207c6b969 | Também utiliza contexto histórico RC6; regras operacionais adicionais não são exigências literais do DOCX. |
```

Linha 12:

```text
| Playbook histórico 3E do RC6 | historico | [assets/3e-solution-structuring-playbook-original-rc6.md](<../assets/3e-solution-structuring-playbook-original-rc6.md>) | — | historica | 484d1d4aebe1 | Contexto histórico; não substitui automaticamente o DOCX fornecido. |
```

## workshop-4d/SKILL.md

Linha 13:

```text
Para conferir a fonte: [transcrição](<assets/Modelo 4D de Aprofundamento.transcricao.md>), [DOCX](<assets/Modelo 4D de Aprofundamento.docx>), [divergências](references/fonte-4d-e-divergencias.md), [original RC6](assets/4d-workshop-playbook-original-rc6.md). Preserve originais; registre diferenças e datas.
```

Linha 71:

```text
**Proveniência:** reescrita de fonte metodológica RC6 (`facilitate-4d-workshop/`). A sequência interna D1–D4 foi preservada; o vínculo do RC6 com fase e BP1 é apenas contexto histórico da fonte.
```

## workshop-4d/assets/4d-workshop-playbook-original-rc6.md

- O nome/caminho do arquivo contém `rc6`.

## workshop-4d/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## workshop-4d/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## workshop-4d/references/4d-workshop-playbook.md

Linha 5:

```text
> Adaptação da referência textual do ERIC_RC6. A ordem D1–D4 é do método; a fase citada na origem é contexto, não condição de uso.
```

Linha 14:

```text
- No RC6, a rodada é registrada em `problem_deepening` e o relatório pode alimentar o BP1; esses campos não bloqueiam o método fora dessa posição.
```

## workshop-4d/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```

## workshop-4d/references/fonte-4d-e-divergencias.md

Linha 1:

```text
# Fonte 4D fornecida e comparação com o RC6
```

Linha 9:

```text
A referência adaptada do RC6 reproduz esses elementos. Seus trechos de integração com a esteira e suas regras de evidência são adaptações posteriores; não constam como exigências na fonte DOCX.
```

## workshop-4d/references/fontes.md

Linha 9:

```text
| Método operacional 4D | adaptacao | [references/4d-workshop-playbook.md](<../references/4d-workshop-playbook.md>) | Fonte fornecida 4D (4d-docx) | desconhecida | 27ae817e7c94 | Também utiliza contexto histórico RC6; regras operacionais adicionais não são exigências literais do DOCX. |
```

Linha 12:

```text
| Playbook histórico 4D do RC6 | historico | [assets/4d-workshop-playbook-original-rc6.md](<../assets/4d-workshop-playbook-original-rc6.md>) | — | historica | 76dc8d5335b0 | Contexto histórico; não substitui automaticamente o DOCX fornecido. |
```

## workshop-4d/references/mural-board-4d-template.md

Linha 7:

```text
Use o board para D1–D4 em qualquer fase. Se a rodada for retomada, registre versão e data de cada contribuição; no RC6, o relatório completo pode alimentar o BP1.
```

Linha 194:

```text
Alinhado ao DOCX `assets/Modelo 4D de Aprofundamento.docx` fornecido em 28 set 2026: Ventos / Âncoras / Icebergs / Porto e 10 créditos por participante. O histórico RC6 permanece preservado nos assets. Outra regra só deve ser usada como adaptação explícita, combinada antes da votação e registrada na execução.
```

## workshop-5c/assets/design-system/README.md

Linha 9:

```text
- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
```

Linha 11:

```text
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
```

Linha 12:

```text
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
```

Linha 17:

```text
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
```

Linha 50:

```text
Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
```

## workshop-5c/assets/design-system/scripts/render.py

Linha 2:

```text
"""Render canonical my_skills deliverables using the ERIC_RC6 visual baseline."""
```

## workshop-5c/references/eric-esteira.md

Linha 13:

```text
As etapas abaixo são o arranjo metodológico de referência do RC6. O RC5 usa rótulos abreviados (`garimpar`, `confirmar`, `aprofundar`, `ideias`, `desenhar`, `externas`, `experimentar`, `implementar`) e descrições mais gerais. Para interpretar materiais com nomenclaturas diferentes, use objetivo, data e entrega real da etapa, não só seu nome.
```

Linha 23:

```text
| 6 | **Buscar soluções externas** | Há alternativa externa aderente e viável? | Quando a rota justificar, comparar ferramentas, startups, fornecedores e parceiros com critérios de integração, custo, risco e adequação. | Comparação de alternativas e recomendação; etapa condicional na referência RC6. |
```

Linha 49:

```text
- **Briefing → 4D:** o desafio fornece ponto de partida; o 4D pode corrigi-lo. D1–D4 são etapas internas do método. No arranjo RC6, os quatro D ocorrem no aprofundamento e BP1 examina o relatório completo; essa alocação não limita quando a skill 4D pode ser chamada.
```

Linha 50:

```text
- **4D → 3E:** alternativas priorizadas pelo grupo são candidatas, não soluções validadas. E1–E3 tornam uma delas testável. No arranjo RC6, os três E ocorrem na geração de ideias; a skill também pode ser aplicada antes ou depois, com origem e data explícitas.
```

Linha 51:

```text
- **3E → experimentação:** E3 produz Test Cards e plano. **Learning Card exige teste executado e evidência**. Uma menção a Learning Card em E3 no texto de referência do RC6 é tratada aqui como planejamento do registro futuro, nunca como achado antecipado.
```

Linha 75:

```text
Síntese metodológica da **Especificação da Esteira de Inovação**, §§2 e 5 (RC6), e da decisão **4D/3E em fase única** (RC6, aceita em 21 ago 2026); nomes e descrições comparados com a esteira documentada no RC5. As especificações do RC6 ainda têm partes em **draft**; quando um projeto trouxer decisão institucional mais recente, registre a divergência e use a fonte vigente para ele. ERIC designa, nesta referência, exclusivamente a **Esteira Robusta de Inovação Colaborativa**.
```
