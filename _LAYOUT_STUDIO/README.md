# Layout Studio

Ferramenta local, de uso pessoal, para desenhar visualmente a estrutura/posicionamento
dos "slots" (zonas de conteúdo) de cada tipo de entregável das 11 skills — sem precisar
editar `render.py` ou mexer em coordenadas no código.

**Não é uma skill.** Fica numa pasta com `_` (como `_TOOLS`, `_SHARED`, `_DESIGN_SYSTEM`),
que o `_TOOLS/sync_shared.py` já ignora por convenção (só sincroniza pastas sem `_` na
frente). Não é distribuída com nenhuma skill nem usada por elas em tempo de execução —
é só um instrumento de autoria.

## Como usar

1. Abra `index.html` direto no navegador (duplo clique no arquivo — não precisa de
   servidor nem instalação). Funciona em qualquer navegador; o passo 2 abaixo (pasta
   conectada) só funciona em **Chrome/Edge**.
2. Clique **"📁 Selecionar pasta de layouts…"** e escolha
   `my_skills/_DESIGN_SYSTEM/layouts/`. A partir daí:
   - "Carregar layout existente…" lista os `*.layout.json` que já estão nessa pasta.
   - "Exportar JSON" passa a **salvar direto nela**, em vez de baixar e você ter que
     mover o arquivo manualmente.
   - Se seu navegador não suportar isso, o botão fica desabilitado e tudo continua
     funcionando do jeito antigo: "Importar JSON (de outro lugar)" (seletor de arquivo
     comum) e "Exportar JSON" baixa o arquivo normalmente.
3. Escolha o **"Tipo de entregável"** na lista (os 18 valores reais de
   `_DESIGN_SYSTEM/contracts/*.schema.json`, não é mais texto livre). Se a pasta estiver
   conectada (passo 2) e já existir um `<tipo>.layout.json` salvo para esse tipo, a
   estrutura já existente é **carregada automaticamente na tela** — se houver slots
   não salvos na tela, ele pergunta antes de substituir.
4. Escolha o tamanho do canvas no dropdown, organizado em grupos: ISO A6-A0 (retrato e
   paisagem — A2/A1/A0 para o board estilo Mural), US/ANSI (Letter, Legal, Tabloid/Ledger)
   e Apresentação (slide 16:9 e 4:3) — ou "Personalizado" para outra medida em mm.
5. Clique **"+ Novo slot"**, depois clique-e-arraste dentro do canvas para desenhar uma
   zona. Repita para cada zona (ex: `hero`, `card_1`, `card_2`, `card_3`, `pergunta_01`...).
6. Clique num slot para selecioná-lo: arraste o corpo para mover, o círculo no canto
   inferior direito para redimensionar, ou edite os valores exatos de x/y/largura/altura
   na lista à direita (mais preciso que arrastar). Em **"Fonte de dados"**, escolha o
   `section_key` real do schema do tipo selecionado (a lista muda conforme o tipo). Em
   **"Como exibir"**, escolha como esse conteúdo deve aparecer dentro do slot: título e
   conteúdo, somente conteúdo, ou listagem tabular.
7. (Opcional) **"Carregar tokens.json"** aplica as cores e fontes do design system de
   verdade no desenho (bordas, preenchimento, tipografia dos rótulos) — não é só
   decoração ao lado, afeta o canvas.
8. **"Visualizar JSON"** mostra exatamente o que será salvo antes de confirmar.
9. **"Exportar JSON"** salva direto na pasta conectada (passo 2), ou baixa o arquivo se
   nenhuma pasta estiver conectada.
10. Para editar um layout já existente depois, use o dropdown "Carregar layout
    existente…" (se a pasta estiver conectada) ou "Importar JSON (de outro lugar)".

Atalhos: com um slot selecionado, `Delete`/`Backspace` remove ele (quando o foco não
está num campo de texto); `Esc` fecha o preview do JSON.

## Formato exportado (`<deliverable_type>.layout.json`)

```json
{
  "schema_version": "1.2.0",
  "deliverable_type": "executive_presentation",
  "canvas": { "unit": "mm", "width": 338.67, "height": 190.5 },
  "grid_mm": 5,
  "slots": [
    { "id": "s1", "name": "hero", "x": 0, "y": 0, "width": 338.67, "height": 95, "z": 1, "section_key": "context", "display_mode": "title_and_content" },
    { "id": "s2", "name": "card_1", "x": 10, "y": 105, "width": 100, "height": 75, "z": 1, "section_key": "findings", "display_mode": "tabular_list" }
  ]
}
```

- `canvas`: sempre em milímetros, igual à convenção de `tokens.json` (`tokens["page"]`),
  para ficar direto compatível quando `render.py` for adaptado a ler isso.
- `slots[].section_key`: a **fonte de dados real** daquele slot — o mesmo valor de
  `data.section_key` usado no JSON canônico dos entregáveis para aquele
  `deliverable_type` (extraído diretamente dos schemas em `contracts/`), ou uma das
  opções estruturais (`titulo_documento`, `identificacao_versao`, `rodape`, `logo`,
  `outro`) para zonas que não vêm de uma seção de conteúdo específica. Arquivos
  exportados pela versão anterior desta ferramenta usavam o campo `content_hint` com uma
  lista genérica — ainda são lidos ao importar (viram `section_key` automaticamente),
  mas o valor pode não corresponder a um `section_key` real; revise ao reabrir.
- `slots[].display_mode`: como o conteúdo daquela fonte de dados é exibido dentro do
  slot — `title_and_content` (título e conteúdo), `content_only` (somente conteúdo),
  `tabular_list` (listagem tabular), ou vazio (não definido). Independente de *qual*
  dado é (`section_key`); é só sobre *como* ele aparece.
- `slots[].z`: ordem de empilhamento, caso dois slots se sobreponham.

**Atenção**: a lista de `section_key` por tipo está hardcoded no `index.html`
(`SECTION_KEYS_BY_TYPE`), extraída dos schemas em 02/10/2026. Se um schema em
`_DESIGN_SYSTEM/contracts/` ganhar/perder seções, essa lista precisa ser atualizada à
mão — a ferramenta não lê os schemas automaticamente (eles não mudam com frequência,
mas não há verificação cruzada automática ainda).

## O que esta ferramenta NÃO faz (ainda)

Ela só desenha e exporta a estrutura (posições/tamanhos/nomes/fonte de dados). Ela **não**:
- Lê nem escreve o `render.py` — a integração para `render.py` de fato posicionar o
  conteúdo real segundo esse layout é trabalho futuro, separado.
- Valida se os slots cobrem todas as seções obrigatórias de `response-sections.json` ou
  dos schemas em `contracts/` (só oferece as opções corretas no dropdown; não avisa se
  faltou alguma).
- Renderiza o conteúdo real (texto/tabelas) dentro dos slots — mostra só o nome e o
  `section_key` como retângulo de referência, estilizado com as cores/fontes do
  `tokens.json` carregado.

Essas coisas ficam para quando a integração com `render.py` for desenhada (ver
`~/skills-research/relatorio/analise-fidelidade-visual-objetividade.md` e a conversa que
originou esta ferramenta).
