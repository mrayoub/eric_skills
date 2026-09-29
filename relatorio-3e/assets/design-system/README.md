# Sistema visual dos entregáveis de `my_skills`

Esta pasta é o contrato compartilhado das onze skills. O `content_json` validado por schema é a fonte canônica; HTML, PDF, DOCX, PPTX e Markdown são derivados. O conteúdo e as fontes não mudam quando se troca o formato.

**Regra obrigatória:** nenhum arquivo é uma entrega final apenas por ter a aparência correta. Antes de renderizar, valide a resposta contra `contracts/deliverable-content.schema.json`, o perfil do seu `deliverable_type` e o schema específico quando existir. Falha de validação exige correção do conteúdo ou uma entrega parcial marcada como tal; não ignore o erro nem altere silenciosamente o schema para acomodar a resposta. Todos os formatos de uma mesma versão devem derivar do mesmo JSON validado. Esta regra preserva campos, ordem lógica, rastreabilidade e identidade visual entre skills.

## Arquivos normativos

- `tokens.json`: cores, tipografia, medidas e componentes versionados da baseline ERIC_RC6.
- `profiles.json`: tipo de entrega, variante, orientação, formatos e seções esperadas. A orientação é determinada pelo perfil; só muda por variante explicitamente aceita.
- `contracts/deliverable-content.schema.json`: envelope de conteúdo comum do ERIC_RC6.
- `contracts/*.schema.json`: contrato específico para **cada um dos 18 tipos** de entregável. Os schemas de briefing e 4D preservam os contratos adaptados do RC6; os demais exigem as seções decisivas do respectivo método.
- `response-sections.json`: nomes canônicos de `data.section_key` exigidos nas versões completas dos tipos que usam contratos por seção.
- `contracts/five-c-workshop-record.schema.json` e `contracts/five-c-report.schema.json`: exigem síntese rastreável de C1 a C5 em versões completas.
- `contracts/test-card.schema.json` e `contracts/learning-card.schema.json`: exigem os quatro campos individuais, em ordem. O Learning Card completo exige citação nas observações.
- `scripts/render.py`: valida conteúdo e gera arquivos derivados de modo determinístico a partir de um JSON.
- `assets/logo_ccee.png`: timbre incorporado à saída visual; proveniente do ERIC_RC6.
- `assets/fonts/`: arquivos variáveis Montserrat e Roboto da biblioteca oficial Google Fonts, incorporados ao HTML/PDF; licenças OFL incluídas.

## Uso pelas skills

Antes de montar o conteúdo, leia `references/linguagem-dos-entregaveis.md` na pasta
da skill (fonte: `_SHARED/linguagem-dos-entregaveis.md`).
Títulos, explicações e células de tabelas devem ser compreensíveis sem conhecimento
do método. Preserve os nomes de campos exigidos nos schemas; escreva seus valores
textuais para o leitor, explicando medidas e termos necessários.

1. Produza primeiro um JSON canônico com `schema_version`, `deliverable_type`, `locale`, `title`, `blocks`, `citations` e `metadata`. Preserve IDs estáveis de blocos e citações. Não use o layout para esconder dado ausente ou trocar a conclusão.
2. Escolha o `deliverable_type` do perfil correspondente à entrega. Quando um método produzir vários arquivos, cada um recebe seu tipo e sua própria versão de conteúdo. Leia o schema desse tipo e, quando aplicável, `response-sections.json` antes de compor blocos. Uma entrega completa só pode usar `metadata.completeness = complete` se todas as seções obrigatórias e as fontes exigidas estiverem presentes. Use a orientação padrão do perfil, salvo variante explicitamente aceita pelo perfil e pedida pelo usuário.
   Nos cards completos, use `data.section_key` e `data.text` em quatro blocos: Test Card = `hypothesis`, `test`, `measure`, `criteria`; Learning Card = `hypothesis`, `observations`, `learning`, `action`. Se faltar informação decisiva, identifique `metadata.completeness` como `partial` ou `inconclusive`; a validação comum continua obrigatória.
   O Learning Card completo exige `metadata.test_card_id` e `metadata.test_card_version`, iguais ao `artifact_id` e `content_version` do Test Card executado.
3. Valide o JSON e renderize com `python scripts/render.py input.json --out-dir pasta --formats html,pdf,md` a partir desta pasta. O renderizador executa os schemas antes de criar arquivos. `--formats` é opcional e usa os formatos padrão do perfil. Para DOCX/PPTX, passe o formato explicitamente quando permitido e instale as bibliotecas indicadas em `requirements.txt`. Se o PDF não puder ser gerado por falta de bibliotecas nativas (WeasyPrint/pango), o renderizador gera os demais formatos e registra `unavailable.pdf` no manifesto. Informe isso ao usuário e ofereça DOCX; não declare que o PDF foi entregue.
   No potencial de inovação, o total e a classificação usam as notas publicadas com uma casa decimal; o total é arredondado uma vez após a aplicação dos pesos.
4. Guarde o JSON junto dos derivados. O renderizador grava um manifesto com hashes do conteúdo, dos tokens, do perfil e dos arquivos. Reexecutar o mesmo JSON e as mesmas versões sobrescreve somente os derivados daquele ID; alterações de conteúdo exigem novo `content_version`.

5. Para `briefing_validation` e `innovation_potential_assessment` completos, o renderizador recalcula notas, vetos, totais e classes e rejeita o JSON se algum número divergir. Corrija o conteúdo com o resultado do script da skill (`iqb.py` ou `score.py`); não edite números à mão.

## Regras visuais

- Relatórios analíticos e matrizes: A4 paisagem (`report_landscape`). Briefings, avaliações e documentos narrativos: A4 retrato (`report_portrait`). Síntese executiva: A4 paisagem em uma página (`executive_one_page`), com erro se o conteúdo não couber. Apresentação: 16:9 (`presentation`). Test Cards e Learning Cards: A4 retrato, um card por página.
- PDF/HTML usam Montserrat nos títulos, Roboto no corpo, cores e escala do `tokens.json`. O renderer não reduz corpo abaixo de 8 pt nem texto abaixo de 7,5 pt; pagina conteúdo extenso. Em tela, `wide` é uma prévia responsiva do A4 paisagem ou slide 16:9, e `portrait` é a do A4 retrato. Para impressão, a medida física do perfil prevalece sobre pixels de tela.
- Logo no cabeçalho, título e identificação no topo, corpo dentro da área segura, referências e metadados no fim. Relatórios usam seções em cards tabulados; `card_grid` cria grades de 1 a 4 colunas para métricas, jornadas, ideias e comparações. Use `table` para dados que exigem cabeçalho e linhas. Não invente preenchimento de cards para completar uma grade. Cores distinguem níveis visuais; estados como “pendente” e “inconclusivo” também aparecem por texto.
- MD mantém toda a semântica e as citações. DOCX/PPTX, quando solicitados, devem usar texto e tabelas editáveis, sem converter páginas inteiras em imagem.
- A equivalência exigida entre formatos é semântica. Idempotência significa que os mesmos JSON, perfil, tokens, fontes e versão do renderer produzem o mesmo conteúdo, geometria e aparência; bytes de PDF/DOCX/PPTX podem variar por metadados internos das bibliotecas e não são usados como critério de equivalência visual.

## Proveniência e limites

Baseline de tokens e decisões: `ERIC_RC6/sdd/specs/DELIVERABLE_DESIGN_SPEC.md`, ADR-008 e ADR-0027, versão consultada em 25 set 2026. A referência 4D rasterizada orienta qualidade e hierarquia; seu conteúdo e o corte no rodapé não devem ser copiados. HTML/PDF incorporam as fontes fornecidas. Para aparência equivalente em DOCX/PPTX editáveis, instale essas mesmas fontes no programa que abre os arquivos. Se uma biblioteca, fonte ou logo não estiver disponível, o renderizador informa o limite; não declara fidelidade visual idêntica silenciosamente.
