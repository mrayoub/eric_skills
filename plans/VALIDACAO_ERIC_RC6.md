# Migração das nove skills do ERIC_RC6 para `my_skills`

**Origem:** `/Users/mayoub/Desktop/workspaces/gein_experiences/gein_eric/ERIC_RC6/app/backend/catalog/skills/`  
**Destino:** sete skills portáteis, irmãs de `experimentacao_inovacao` e `scorecard-inovacao`. O projeto de origem não foi alterado.

## Decisão de agrupamento

| Skill de origem | Skill nova | Motivo |
|---|---|---|
| `generate-briefing` | `briefing-inovacao` | Três operações sobre a mesma versão de briefing, selecionáveis por modo. |
| `generate-briefing-one-page` | `briefing-inovacao` | Saída derivada do briefing, com sua versão como entrada obrigatória. |
| `generate-briefing-questions` | `briefing-inovacao` | Perguntas derivadas das lacunas do mesmo briefing; não são avaliação autônoma. |
| `validate-briefing` | `avaliacao-briefing-iqb` | Auditoria com rubrica e cálculo próprios; separada da autoria do briefing. |
| `calculate-innovation-potential` | `potencial-inovacao` | Rubrica de priorização distinta do IQB e do Scorecard da Strategyzer. |
| `facilitate-4d-workshop` | `workshop-4d` | Interação ao vivo e registro de D1–D4. |
| `compile-4d-report` | `relatorio-4d` | Compilação posterior exige fontes e condição de completude diferentes da facilitação. |
| `facilitate-3e-workshop` | `workshop-3e` | Condução de E1–E3 com perguntas e decisões do grupo. |
| `compile-3e-report` | `relatorio-3e` | Relatório e Test Cards prospectivos; entrega separada do workshop. |

## Padrão incorporado

Cada pacote contém `SKILL.md` com fronteira de uso, levantamento documental e grilling por dependências em recurso local, regra de evidência e saída parcial quando faltam dados. Nenhum pacote requer as skills de Matt Pocock instaladas. Referências, schemas, scripts e o PDF de exemplo do 4D necessários à execução foram copiados e ajustados dentro dos pacotes. Grilling pergunta por fatos e decisões metodológicas; nunca por nota ou conclusão desejada.

## Independência da fase

As sete skills são acionadas pela tarefa e pelos insumos, em qualquer ponto da esteira ou fora dela. A fase do RC6 permanece como proveniência do método, não como pré-requisito. A ordem interna D1–D4 ou E1–E3 é uma dependência do método; um BP1, a fase `ideation` e o Scorecard não são autorização nem bloqueio automático de execução. Se o projeto ainda não tiver insumos para a entrega completa, a skill prepara ou entrega versão parcial. Se ela for invocada mais tarde, usa material posterior com data e preserva a distinção entre plano prévio e reconstrução retrospectiva. O Scorecard pode informar lacunas e força das evidências, sem determinar que outra skill só rode após determinada nota.

## Desvios do RC6 corrigidos

1. **4D e BP1:** playbook antigo e trechos de `compile-4d-report` dividiam D1/D2 e D3/D4 em fases e antecipavam o BP1. O ADR-0037, `PIPELINE_SPEC.md`, `AGENTS_SPEC.md` e `SDD_COMPLETION_REVIEW.md` vigentes estabelecem D1–D4 inteiros em aprofundamento e BP1 após o relatório concluído. As duas skills 4D novas seguem essa regra; seus recursos foram atualizados.
2. **3E e Learning Card:** E3 pertencia em referências antigas a `solution_design` e preparava Learning Card. A fase vigente é `ideation`. E3 agora gera Test Cards individuais de quatro campos e apenas planeja o registro futuro; Learning Cards são produzidos depois da execução.
3. **Potencial:** o script original transformava critérios ausentes ou inválidos em zero e ainda classificava a oportunidade. O cálculo novo retorna `incomplete` e nenhuma classificação quando há nota ausente; valor inválido gera erro. Os pesos e cortes originais foram preservados.
4. **IQB:** o cálculo de alto nível agora rejeita matriz incompleta ou resposta sem justificativa. A auditoria de notas agrupadas é marcada como tarefa manual, sem declaração automática de que a evidência já foi reexaminada. Critérios, vetos e faixas originais foram preservados.

## Validação por pacote

| Pacote | Estrutura `quick_validate.py` | Recursos internos | Verificação específica |
|---|---|---|---|
| `briefing-inovacao` | Válida | Links e três schemas JSON válidos | Modos de briefing, one-page e perguntas mantêm linhagem e fronteiras distintas. |
| `avaliacao-briefing-iqb` | Válida | Link, schema e script presentes | 40 respostas `no` → IQB 1; 40 `yes` → IQB 5; item ausente gera erro; agrupamento solicita reauditoria. |
| `potencial-inovacao` | Válida | Link e script presentes | Critério ausente → sem classificação; cinco zeros explícitos → `arquivar`; cinco notas 80 → `priorizar`. |
| `workshop-4d` | Válida | Links presentes | D1–D4 precedem BP1; blueprint corrigido. |
| `relatorio-4d` | Válida | Links e PDF presentes | Relatório final requer D1–D4 e separa snapshot D2. |
| `workshop-3e` | Válida | Links e modelo presentes | E3 gera Test Cards individuais e não gera Learning Card prematuro. |
| `relatorio-3e` | Válida | Links e modelo presentes | Relatório distingue plano, execução futura e decisão de rota. |

Os checks estruturais e os testes determinísticos foram executados na área de preparação. Após a revisão de independência de fase, `quick_validate.py` passou novamente nos sete pacotes. Não houve execução real de workshop, cálculo de IQB sobre briefing de projeto nem integração com Mural; essas validações dependem de um cenário e fontes escolhidos para cada skill.

### Cenários de uso fora da fase usual

Os cenários abaixo foram conferidos contra os arquivos originais do `SAMPLE/GEIN-123`; são testes de contrato e de disponibilidade de insumos, não simulações de decisões ou sessões que não ocorreram.

| Skill | Chamada antecipada | Chamada tardia |
|---|---|---|
| `briefing-inovacao` | Reconstruir briefing provisório da entrevista antiga, com campos pendentes. | Atualizar o briefing original à luz dos relatórios 4D/3E, mantendo versão anterior e data das evidências. |
| `avaliacao-briefing-iqb` | Avaliar apenas a transcrição como reconstrução identificada, sem declarar briefing aprovado. | Avaliar o DOCX original ou versão atualizada independentemente de 4D/3E já realizados; cada versão recebe matriz própria de 40 itens. |
| `potencial-inovacao` | Preparar matriz parcial com critérios não pontuáveis. | Reavaliar a oportunidade usando os relatórios 4D/3E, sem converter ausência de custo, baseline ou viabilidade em zero. |
| `workshop-4d` | Preparar D1–D4 com briefing e entrevista, sem simular respostas do grupo. | Retomar diagnóstico após o 3E como nova rodada datada, sem atribuir contribuições novas à sessão antiga. |
| `relatorio-4d` | Compilar D1/D2 como parcial se só esses registros existirem. | Revisar o relatório com o PDF 4D e fontes 3E posteriores, mantendo achados originais e atualizações separados. |
| `workshop-3e` | Preparar E1–E3 a partir de uma hipótese candidata antes de BP1, com riscos explícitos. | Revisar E1–E3 após resultados de teste, se houver, distinguindo Test Cards prévios de reconstruídos. |
| `relatorio-3e` | Entregar estrutura parcial e Test Cards em rascunho se faltarem escopo, baseline ou critério. | Compilar o HTML 3E existente, incorporar resultados posteriores quando disponíveis e nunca chamar um critério retrospectivo de prévio. |

No `SAMPLE`, há briefing, relatório 4D e relatório 3E; não há comprovação de execução de um experimento nem seus resultados. Portanto os dois últimos cenários tardios descrevem o comportamento exigido quando resultados forem fornecidos, sem afirmar que já ocorreram. O corpus permite conferir a independência da fase e a rastreabilidade, mas não valida facilitação ao vivo.
