# Fontes metodológicas

Página gerada de `_FONTES/manifest.json` por `_TOOLS/build_sources.py`. Não edite manualmente.

A vigência indica o que está confirmado sobre a fonte. Publicação oficial não equivale a adoção institucional; confira as notas.

| Fonte | Tipo | Arquivo | Deriva de | Vigência | Titular | Licença | SHA-256 (12 caracteres) | Notas |
|---|---|---|---|---|---|---|---|---|
| Campos do formulário da CDT no Jira e padrão de escrita | adaptacao | [references/campos-jira.md](<../references/campos-jira.md>) | Publicação interna sobre definição de escopo para a Tecnologia (cdt-publicacao) | desconhecida | CCEE | Licença de Uso Restrito CCEE | 6dfef4529311 | Regras confirmadas pelo usuário em 23/10/2026. Listas de processos, famílias e serviços transcritas como no Jira; siglas de áreas, nome de fornecedor, nomes de pessoas e números de ticket ficaram de fora. O padrão de escrita vem de uma CDT real, descrita sem identificação. |
| Publicação interna sobre definição de escopo para a Tecnologia | transcricao | [references/publicacao-escopo-tecnologia.md](<../references/publicacao-escopo-tecnologia.md>) | não se aplica | desconhecida | CCEE | Licença de Uso Restrito CCEE | d1ef2262cc23 | Transcrição anonimizada: nome de pessoa e marca de campanha retirados. Orienta a qualidade esperada; não é norma formal do formulário do Jira. |
| Qualidade e veracidade da CDT | adaptacao | [references/qualidade-e-veracidade.md](<../references/qualidade-e-veracidade.md>) | Publicação interna sobre definição de escopo para a Tecnologia (cdt-publicacao) | desconhecida | CCEE | Licença de Uso Restrito CCEE | 669380a36498 | Regras estruturais conferidas por scripts/checar_cdt.py e pelo validador do tipo cdt. |
| Checagem da CDT | script | [scripts/checar_cdt.py](<../scripts/checar_cdt.py>) | Qualidade e veracidade da CDT (cdt-qualidade) | desconhecida | CCEE | Licença de Uso Restrito CCEE | 19e7cf2b4d7d | Confere estrutura e pendências; não julga a qualidade do conteúdo. |
| Contexto da esteira ERIC | adaptacao | [references/eric-esteira.md](<../references/eric-esteira.md>) | não se aplica | desconhecida | CCEE | Licença de Uso Restrito CCEE | 15fb2918475f | Há trechos de origem em draft; decisões institucionais posteriores podem prevalecer. A cópia é sincronizada por sync_shared.py. |

## Vigência a confirmar

- Campos do formulário da CDT no Jira e padrão de escrita (cdt-campos-jira).
- Publicação interna sobre definição de escopo para a Tecnologia (cdt-publicacao).
- Qualidade e veracidade da CDT (cdt-qualidade).
- Checagem da CDT (cdt-script).
- Contexto da esteira ERIC (eric-esteira).
