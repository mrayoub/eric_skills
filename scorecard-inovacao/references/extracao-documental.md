# Protocolo de extração documental

## Fontes e escopo desta incorporação

- A [skill PDF da Anthropic](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md) descreve extração de texto e tabelas por página e OCR de PDF digitalizado; sua [referência avançada](https://github.com/anthropics/skills/blob/main/skills/pdf/reference.md) mostra renderização de páginas para conferir conteúdo visual. A skill da Anthropic declara licença proprietária: esta referência **parafraseia o método**, sem copiar suas instruções ou código.
- A [skill MarkItDown da comunidade](https://github.com/coroboros/agent-skills/blob/main/skills/markitdown/SKILL.md) ensina a converter diversos formatos para Markdown, verificar os conversores disponíveis, reter o resultado sem imprimir documentos enormes e conferir permissões de transferência de dados em OCR/áudio e serviços externos. A [ferramenta Microsoft MarkItDown](https://github.com/microsoft/markitdown) preserva parte da estrutura, como títulos, listas e tabelas, mas sua saída é intermediária para análise, não cópia fiel do documento original.

As ferramentas citadas são **opções de implementação**, não dependências da skill. Use leitor nativo do ambiente quando ele permitir inspeção e citação confiáveis. A ausência de um conversor específico não autoriza declarar que um arquivo foi lido. Qualquer serviço externo para OCR, transcrição ou conversão depende de autorização para enviar o conteúdo; prefira processamento local quando disponível.

## 1. Inventário e estratégia por arquivo

Liste todos os arquivos dentro do escopo antes de resumir o projeto. Para cada um, guarde ID, caminho, formato, tamanho ou páginas quando relevante, data/versão, fase de origem, estado de leitura e motivo de exclusão. Detecte duplicatas ou versões e indique qual foi usada. Não diga “todos os documentos analisados” quando alguns foram apenas localizados. Identifique arquivos protegidos, corrompidos ou inacessíveis como lacunas.

Escolha a rota de leitura conforme o conteúdo:

| Fonte | Primeira leitura | Checagem que evita perda relevante | Localizador mínimo |
|---|---|---|---|
| Markdown, texto, HTML | Leia a estrutura e o texto; preserve títulos, tabelas e links. | Confira conteúdo carregado por scripts, anexos e tabelas que a extração omitiu. | Arquivo + seção/linha ou âncora. |
| PDF com texto | Extraia por página, mantendo a ordem e as quebras; extraia tabelas separadamente quando necessário. | Compare páginas decisivas renderizadas com o texto; verifique colunas, notas, gráficos e números. | Arquivo + página; tabela/trecho. |
| PDF digitalizado ou visual | Renderize páginas e aplique OCR por página; confira o resultado na imagem. | Marque páginas vazias, sem texto legível ou com OCR incerto; não invente páginas ausentes pelo rodapé. | Arquivo + página da imagem; confiança/limite. |
| DOCX e PPTX | Extraia parágrafos, tabelas, notas e texto de slides com ferramenta local ou conversão para Markdown. | Inspecione imagens, diagramas, comentários ou notas que possam conter afirmações decisivas. | Arquivo + seção/tabela ou slide. |
| XLSX e CSV | Leia abas, cabeçalhos, tipos, fórmulas e linhas relevantes; preserve unidades e filtros. | Confira se os valores são dados brutos, fórmulas, amostra ou resumo; recalcule medidas decisivas se possível. | Arquivo + aba/célula ou intervalo/linha. |
| Imagem, áudio e vídeo | Use OCR ou transcrição quando houver capacidade autorizada. | Confira trechos críticos visualmente ou por tempo; transcrição não equivale a revisão do vídeo. | Arquivo + região/página ou timestamp. |

Conversão em lote pode acelerar a leitura inicial. Salve o texto extraído em área autorizada, com vínculo ao arquivo original e versão. Para arquivos grandes, leia por partes e retenha um índice; não despeje todo o conteúdo em uma resposta. Não trate texto convertido como fonte independente nem conte versões duplicadas como várias evidências.

## 2. Extração de afirmações para o Scorecard

Depois de ler a fonte, separe **conteúdo do documento** de **inferência do avaliador**. Registre apenas afirmações que influenciem alinhamento, oportunidade ou algum risco. Use este registro mínimo:

| Campo | Conteúdo esperado |
|---|---|
| Afirmação | O que a fonte diz ou mostra, sem ampliar seu alcance. |
| Localização | ID da fonte e página/seção/slide/aba/tempo verificáveis. |
| Contexto | Autor/data, fase, população, versão da solução e método. |
| Natureza | Hipótese, intenção, decisão, relato, observação, medida ou resultado. |
| Qualidade | Cobertura, denominador, fonte independente, erro de OCR/conversão e limitação. |
| Papel | Dimensão do Scorecard que pode informar; evidência favorável ou contrária. |

Mantenha uma matriz `dimensão → afirmações → fontes`. Se duas fontes divergirem, cite ambas e investigue diferença de data, versão, população e definição. Se um documento afirma um resultado mas não fornece dados que o sustentem, registre a afirmação como **relato de resultado** e peça a fonte primária quando ela for decisiva. Não eleve a pontuação por repetição da mesma afirmação em apresentações derivadas.

## 3. Controle de qualidade antes da entrevista

1. Reconcilie a contagem de páginas/slides/abas com o que foi efetivamente extraído. Verifique páginas sem texto e trechos onde a ordem de leitura parece incorreta.
2. Confira no original os números, tabelas, negações, condições e frases que mudariam uma nota ou recomendação. Para OCR, registre correção e incerteza sem sobrescrever o bruto.
3. Marque as fontes `examinada`, `examinada parcialmente`, `localizada não examinada`, `indisponível` ou `fora do escopo`; documente cobertura e motivo. Reduza a força de conclusão onde faltou leitura.
4. Passe à entrevista somente as definições, decisões e fontes ainda ausentes após a leitura. Perguntas que podem ser resolvidas inspecionando arquivos continuam sendo responsabilidade do agente.
