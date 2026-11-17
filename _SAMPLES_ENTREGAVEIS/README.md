# Amostras dos entregáveis

Todos os dados, participantes, votos, números e resultados são **fictícios**. Estes arquivos servem para avaliar a estrutura, a aparência e a edição de cada tipo de entrega. O playbook 5C original é uma fonte metodológica; suas amostras não registram um workshop real.

Cada pasta contém `input.json`, o JSON canônico validado, um manifesto com hashes e os derivados. Edite uma cópia do JSON e renderize novamente com o script incluído na skill correspondente. Entregas completas passam pelo schema específico de seu tipo; versões parciais devem declarar `metadata.completeness`.

| Tipo e nome apresentado | Skill(s) | Layout | Pasta |
|---|---|---|---|
| `briefing`: Entrevista Inicial de sete campos | briefing-inovacao | `report_portrait` | [briefing](./briefing/) |
| `briefing_one_page`: Briefing | briefing-inovacao | `executive_one_page` | [briefing_one_page](./briefing_one_page/) |
| `briefing_improvement_questionnaire`: Perguntas para fechar lacunas | briefing-inovacao | `report_portrait` | [briefing_improvement_questionnaire](./briefing_improvement_questionnaire/) |
| `briefing_validation` | avaliacao-briefing-iqb | `report_portrait` | [briefing_validation](./briefing_validation/) |
| `innovation_potential_assessment` | potencial-inovacao | `report_portrait` | [innovation_potential_assessment](./innovation_potential_assessment/) |
| `four_d_workshop_record` | workshop-4d | `report_landscape` | [four_d_workshop_record](./four_d_workshop_record/) |
| `four_d_report`: Relatório depreciado 4D | relatorio-4d | `report_landscape` | [four_d_report](./four_d_report/) |
| `four_d_presentation`: Apresentação depreciada 4D | relatorio-4d | `presentation` | [four_d_presentation](./four_d_presentation/) |
| `three_e_workshop_record` | workshop-3e | `report_landscape` | [three_e_workshop_record](./three_e_workshop_record/) |
| `three_e_report`: Relatório depreciado 3E | relatorio-3e | `report_landscape` | [three_e_report](./three_e_report/) |
| `three_e_presentation`: Apresentação depreciada 3E | relatorio-3e | `presentation` | [three_e_presentation](./three_e_presentation/) |
| `innovation_scorecard` | scorecard-inovacao | `report_landscape` | [innovation_scorecard](./innovation_scorecard/) |
| `experiment_plan` | experimentacao-inovacao | `report_portrait` | [experiment_plan](./experiment_plan/) |
| `test_card` | experimentacao-inovacao / workshop-3e / relatorio-3e | `card_portrait` | [test_card](./test_card/) |
| `learning_card` | experimentacao-inovacao | `card_portrait` | [learning_card](./learning_card/) |
| `experiment_report` | experimentacao-inovacao | `report_landscape` | [experiment_report](./experiment_report/) |
| `evidence_recommendation` | experimentacao-inovacao | `report_landscape` | [evidence_recommendation](./evidence_recommendation/) |
| `executive_presentation` | experimentacao-inovacao | `presentation` | [executive_presentation](./executive_presentation/) |
| `five_c_workshop_record` | workshop-5c | `report_landscape` | [five_c_workshop_record](./five_c_workshop_record/) |
| `five_c_report`: Relatório depreciado 5C | relatorio-5c | `report_landscape` | [five_c_report](./five_c_report/) |
| `five_c_presentation`: Apresentação depreciada 5C | relatorio-5c | `presentation` | [five_c_presentation](./five_c_presentation/) |
| `cdt`: Cadastro de Demanda Tecnológica (CDT) | gerador-cdt | `report_portrait` | [cdt](./cdt/) |

Os seis novos tipos oficiais ficam nas pastas de mesmo nome, com `input.json`, JSON canônico, manifesto e
PDF/HTML/DOCX ou PDF/HTML/PPTX. Os casos integrais, adaptados e pocket dos três métodos, mais as sessões combinadas
5C, ficam em [official_variants](./official_variants/). Regenere os JSONs fictícios com
`python3 _TOOLS/build_official_samples.py`; renderize pelo design system.

| Tipo oficial | Skill | Formatos de leitura |
| --- | --- | --- |
| [four_d_official_report](./four_d_official_report/) | relatorio-4d | PDF, HTML, DOCX |
| [four_d_official_presentation](./four_d_official_presentation/) | relatorio-4d | PDF, HTML, PPTX |
| [three_e_official_report](./three_e_official_report/) | relatorio-3e | PDF, HTML, DOCX |
| [three_e_official_presentation](./three_e_official_presentation/) | relatorio-3e | PDF, HTML, PPTX |
| [five_c_official_report](./five_c_official_report/) | relatorio-5c | PDF, HTML, DOCX |
| [five_c_official_presentation](./five_c_official_presentation/) | relatorio-5c | PDF, HTML, PPTX |

Os relatórios agora apresentam seções em cards tabulados; a amostra 4D inclui grades de diagnóstico, jornada, alternativas e priorização inspiradas apenas na estrutura visual do PDF de referência. A orientação continua definida por perfil, e os Test/Learning Cards mantêm seus quatro campos Strategyzer.

Os formatos PDF/HTML mostram a apresentação visual; DOCX/PPTX permitem avaliar a edição. A mesma versão de conteúdo alimenta todos os derivados. Os arquivos CSV existem apenas nas duas tabelas marcadas para exportação.

Os DOCX das 19 amostras foram recompostos com texto, tabelas e cartões editáveis para acompanhar a orientação, a hierarquia e a paginação dos PDFs correspondentes. Para comparar novamente todos os pares após converter DOCX com LibreOffice, execute `python3 _TOOLS/check_docx_pdf_parity.py --out-dir /caminho/para/resultado` no ambiente com as dependências do design system. O `report.json` e as imagens lado a lado registram diferenças visuais que ainda dependem do motor de renderização e das fontes instaladas.
