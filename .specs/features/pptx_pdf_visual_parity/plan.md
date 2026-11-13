# Paridade visual das apresentações PPTX e PDF

**Approved**: 2026-11-13 - user: "entao se estiver validado de acordo com o /tlc-spec-lean execute commit, push, PR e merge!"

## Problem

O usuário constatou que as apresentações 4D e 3E em PPTX estavam visualmente aquém dos PDFs: "preciso que vc alinhe os estilos de forma que o pptx tenha o mesmo design system e a mesma aparencia do pdf". A implementação anterior ficou preparada na branch `fix/pptx-design-system`, sem commit. Esta retomada valida esse escopo já solicitado, sem tratar o relato anterior de 283 testes como prova atual.

Ao publicar, as quatro apresentações do renderizador compartilhado seguem o desenho do PDF e continuam editáveis. A autorização acima abrange a validação e a publicação dessa implementação existente; não é uma aprovação inventada de um plano novo.

## Shape

Reutiliza a sequência de slides, as medidas e os estilos do PDF. As regras são exercitadas nos testes Python do renderizador.

1. JSON da apresentação -> `_DESIGN_SYSTEM/scripts/render.py` (exists): valida o conteúdo e carrega tokens e layout.
2. `render.py` -> `_DESIGN_SYSTEM/scripts/pdf_reportlab.py` (exists): obtém sequência de slides e medidas compartilhadas.
3. `render.py` (exists): grava texto, formas e tabelas nativas no PPTX.
4. `_TOOLS/sync_shared.py` e `_TOOLS/build_dist.py` (exists): distribuem o mesmo renderizador nas skills e nos pacotes.

```mermaid
flowchart LR
    A[1. JSON] --> B[1. render.py]
    B --> C[2. pdf_reportlab.py]
    C --> B
    B --> D[3. PPTX editável]
    B --> E[4. sync_shared.py]
    E --> F[4. build_dist.py]
```

**Changes underneath**

| Front | What changes |
| --- | --- |
| domain | A composição de apresentações passa a usar os mesmos estilos e planejamento de slides do PDF |
| stored data | Amostras PPTX e manifestos regenerados; versões e pacotes atualizados; nenhum contrato JSON alterado |
| readers | PowerPoint e LibreOffice abrem PPTX com textos, formas e tabelas editáveis; os quatro tipos estão no AC 1 |

Data: none - arquivos de saída derivados de JSON versionado; sem banco ou migração.

## Surface

None - assinatura do CLI e contratos de conteúdo permanecem existentes, sem nova API.

## Landing

None - usa as dependências e os formatos já adotados; sem mudança de contrato persistido ou nova dependência de produção.

## Criteria

### S1: Apresentações editáveis com o desenho do PDF (P1)

**Acceptance Criteria**

1. WHEN cada amostra `executive_presentation`, `five_c_presentation`, `four_d_presentation` e `three_e_presentation` é renderizada THEN o PPTX SHALL preservar a contagem, ordem e texto dos slides do PDF, sem omitir blocos ou fontes.
2. WHEN uma apresentação contém texto, cards, callout ou tabela THEN o PPTX SHALL manter esses elementos nativos e editáveis, sem imagem de página inteira.
3. WHEN a apresentação é renderizada THEN o PPTX SHALL usar os tamanhos, famílias e cores dos tokens do PDF, a barra da capa e os cards com preenchimento e faixa de tom; título 24 pt e corpo 17 pt nos tokens atuais.
4. WHEN os slides são enumerados THEN cada rodapé SHALL conter identidade e `n / N` corretos, e as citações SHALL permanecer sobrescritas nos blocos aplicáveis.
5. IF um parágrafo excede a área útil THEN o PPTX SHALL continuar em outros slides sem perder, repetir ou partir palavras; exemplo forte: 220 palavras numeradas.
6. WHEN uma tabela com 20 linhas é renderizada THEN o PPTX SHALL preservar as 20 linhas na ordem, em tabelas nativas com cabeçalho repetido e dentro da área útil; células longas também devem caber.
7. WHEN as quatro apresentações são abertas pelo LibreOffice com as fontes do repositório THEN os slides SHALL corresponder às referências PDF em `captures/`, com dimensão e conteúdo preservados, sem sobreposição ou corte. Cada captura do PPTX é renderizada na mesma escala do PDF, sem redimensionamento posterior.
8. WHEN a distribuição é conferida THEN as 13 skills que recebem o renderer SHALL estar sincronizadas, e fontes, versões, pacotes e os 14 canais do catálogo SHALL passar nas verificações existentes.

## Out of scope

| Excluded | Why |
| --- | --- |
| Conteúdo oficial e exemplos externos do GEIN-44 | Esta publicação trata o repositório eric_skills e seus exemplos sintéticos |
| Alterar `SUGESTOES-4D-3E.md` ou publicá-lo | Orientação anterior exige mantê-lo local e ignorado |
| Dependabot #26 e #27 | Atualizações independentes da correção visual |
| Embutir fontes no PPTX | Não fazia parte da implementação; conversão usa as fontes distribuídas no repositório |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Escopo desta retomada | Validar e publicar a correção existente | Pedido atual condicionado à validação | y |
| Meio de captura | Renderização do PDF e do PPTX convertido pelo LibreOffice na mesma escala | São documentos estáticos, sem tela de aplicativo ou navegação a capturar | n |

**Open questions:** none.

## Differences from the source

None - a composição deve corresponder ao PDF; antialiasing do conversor é medido e não autoriza omissão de elementos ou conteúdo.

## Sources

- Pedido original de 11/11/2026, recuperado da sessão Claude `867830ea-63d9-4db1-919b-fff22f99e060` - binding - aparência do PDF e edição preservada.
- Autorização de 13/11/2026 citada no início - publicação condicionada à validação.
- `_SAMPLES_ENTREGAVEIS/{executive_presentation,five_c_presentation,four_d_presentation,three_e_presentation}/*.pdf` - binding - todas as páginas desses PDFs são exportadas sem alteração para `captures/`; a lista fica em `captures/index.json`.

### Binding page captures

- ![executive_presentation-01](captures/executive_presentation-01.png) - binding - PDF, escala 1 ponto por pixel.
- ![executive_presentation-02](captures/executive_presentation-02.png) - binding - PDF, escala 1 ponto por pixel.
- ![executive_presentation-03](captures/executive_presentation-03.png) - binding - PDF, escala 1 ponto por pixel.
- ![executive_presentation-04](captures/executive_presentation-04.png) - binding - PDF, escala 1 ponto por pixel.
- ![executive_presentation-05](captures/executive_presentation-05.png) - binding - PDF, escala 1 ponto por pixel.
- ![executive_presentation-06](captures/executive_presentation-06.png) - binding - PDF, escala 1 ponto por pixel.
- ![executive_presentation-07](captures/executive_presentation-07.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-01](captures/five_c_presentation-01.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-02](captures/five_c_presentation-02.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-03](captures/five_c_presentation-03.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-04](captures/five_c_presentation-04.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-05](captures/five_c_presentation-05.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-06](captures/five_c_presentation-06.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-07](captures/five_c_presentation-07.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-08](captures/five_c_presentation-08.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-09](captures/five_c_presentation-09.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-10](captures/five_c_presentation-10.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-11](captures/five_c_presentation-11.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-12](captures/five_c_presentation-12.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-13](captures/five_c_presentation-13.png) - binding - PDF, escala 1 ponto por pixel.
- ![five_c_presentation-14](captures/five_c_presentation-14.png) - binding - PDF, escala 1 ponto por pixel.
- ![four_d_presentation-01](captures/four_d_presentation-01.png) - binding - PDF, escala 1 ponto por pixel.
- ![four_d_presentation-02](captures/four_d_presentation-02.png) - binding - PDF, escala 1 ponto por pixel.
- ![four_d_presentation-03](captures/four_d_presentation-03.png) - binding - PDF, escala 1 ponto por pixel.
- ![four_d_presentation-04](captures/four_d_presentation-04.png) - binding - PDF, escala 1 ponto por pixel.
- ![four_d_presentation-05](captures/four_d_presentation-05.png) - binding - PDF, escala 1 ponto por pixel.
- ![four_d_presentation-06](captures/four_d_presentation-06.png) - binding - PDF, escala 1 ponto por pixel.
- ![four_d_presentation-07](captures/four_d_presentation-07.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-01](captures/three_e_presentation-01.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-02](captures/three_e_presentation-02.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-03](captures/three_e_presentation-03.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-04](captures/three_e_presentation-04.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-05](captures/three_e_presentation-05.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-06](captures/three_e_presentation-06.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-07](captures/three_e_presentation-07.png) - binding - PDF, escala 1 ponto por pixel.
- ![three_e_presentation-08](captures/three_e_presentation-08.png) - binding - PDF, escala 1 ponto por pixel.
