# Plan 038: Separar o que é da CCEE do que é de terceiros — tirar os PDFs da Strategyzer, restringir o `LICENSE` e gerar `THIRD_PARTY_NOTICES.md`

> **Executor instructions**: Siga este plano passo a passo. Rode cada comando
> de verificação e confirme o resultado esperado antes de avançar. Se algo na
> seção "STOP conditions" ocorrer, pare e reporte — não improvise. Ao
> terminar, atualize a linha de status deste plano em `plans/README.md`
> (a menos que quem te despachou tenha dito que cuida disso).
>
> **Drift check (rode primeiro)**:
> `git diff --stat ab2594d..HEAD -- LICENSE _FONTES _TOOLS experimentacao-inovacao scorecard-inovacao relatorio-final-inovacao`
> Se o Plano 037 já foi mesclado, haverá `build_catalog.py`/`catalog.json`: siga a nota do Step 7.
> Qualquer outra divergência nos arquivos citados em "Current state" é STOP.

## Status

- **Priority**: P1 (bloqueia distribuir as skills fora do grupo atual e tornar o repositório público)
- **Effort**: M
- **Risk**: MED (retira arquivos de duas skills e muda o esquema do manifesto de fontes; não altera scripts de entregáveis)
- **Depends on**: nenhum. Compatível com o 037 em qualquer ordem.
- **Category**: conformidade / licenciamento
- **Planned at**: commit `ab2594d`, 2026-10-07

## Why this matters

O `LICENSE` (Licença de Uso Restrito CCEE) diz que "este repositório e as skills nele contidas,
incluindo […] demais arquivos, são propriedade da CCEE". Uma varredura em 2026-10-07 achou material de
outros titulares sendo **redistribuído** em todos os canais (GitHub, `npx skills`, `.skill`):

| Material | Titular / condição | Problema |
|---|---|---|
| `experimentacao-inovacao/assets/strategyzer-test-card-2023.pdf`, `…/strategyzer-learning-card-2023.pdf`, `scorecard-inovacao/assets/strategyzer-innovation-project-scorecard-2023.pdf` | "Copyright Strategyzer AG" no rodapé. Termos de uso (https://www.strategyzer.com/legal/terms-of-service): *"Any unauthorized reproduction, publication, further distribution or public exhibition of the materials […] is strictly prohibited."* | Redistribuição sem autorização. **Tem de sair.** |
| Modelos adaptados (`assets/test-card.md`, `assets/learning-card.md`) e menções em ~23 arquivos | Metodologia e nomes da Strategyzer | Pode ficar com crédito explícito; a CCEE não pode reivindicar autoria. |
| `relatorio-final-inovacao/assets/ThePitchCanvas.pdf` | Best 3 Minutes (David Beckett); ilustrações Birgit Smit; **CC BY-SA 4.0** declarada no PDF | Redistribuição permitida com atribuição e aviso de licença; *ShareAlike* pode alcançar `references/pitch-canvas-executivo.md` se for considerado adaptação (decisão do jurídico). |
| `_DESIGN_SYSTEM/assets/fonts/` (Montserrat, Roboto, variáveis e `static/`), copiadas para as 12 skills | **SIL OFL 1.1** (arquivos `*-OFL.txt` já presentes) | Uso correto, mas o `LICENSE` da CCEE não pode abrangê-las. |
| DOCX 4D, 3E e 5C (`dc:creator` = "Michele Barros") | Titularidade **a confirmar pelo operador** (produção interna CCEE ou consultoria contratada) | Registrar como "a confirmar" até haver resposta. |

O `LICENSE` precisa valer só para o que é da CCEE e apontar para um inventário de terceiros, gerado
do manifesto para não depender de manutenção manual.

## Current state (em `ab2594d`; confira)

- `LICENSE` na raiz; `_TOOLS/sync_shared.py` copia para `<skill>/LICENSE` (bloco "A licença acompanha cada skill…").
- Cada `SKILL.md`: `license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."`.
- `_FONTES/manifest.json`: lista de entradas com **exatamente** os campos
  `id, titulo, tipo, arquivo, skills, origem, autor, versao_declarada, data_importacao, deriva_de, vigencia, notas`
  (`_TOOLS/build_sources.py`, constante `FIELDS`). `validate_sources()` exige que `<skill>/<arquivo>` exista.
  Entradas da Strategyzer: `strategyzer-test`, `strategyzer-learning`, `strategyzer-scorecard` (`tipo: original`);
  Pitch Canvas: `pitch-canvas-company`.
- `build_sources.py` gera `<skill>/references/fontes.md`, que hoje linkam os PDFs da Strategyzer
  (`experimentacao-inovacao/references/fontes.md`, `scorecard-inovacao/references/fontes.md`).
- Textos que dizem que os PDFs estão no pacote:
  - `experimentacao-inovacao/SKILL.md:86` — "cards seguem os modelos oficiais Strategyzer 2023 em `assets/`."
  - Confira com `git grep -n -iE "strategyzer.*(pdf|assets/)|pdf.*strategyzer|ThePitchCanvas" -- '*.md'` (ignore `plans/`).
- Links oficiais já usados nas referências: `https://www.strategyzer.com/library/innovation-project-scorecard`,
  `https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card`,
  `https://www.strategyzer.com/library/capture-customer-insights-and-action…` (veja `experimentacao-inovacao/references/entregaveis.md:37`).
- `_DESIGN_SYSTEM/tests/test_render.py` referencia `build_sources`/manifesto — rode a suíte inteira.
- **Pendência alheia**: `executive_presentation.layout.json` (fonte e 12 cópias) modificado e não commitado no
  diretório do operador; quebra 2 testes. Não commite nem reverta.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Fontes | `python3 _TOOLS/build_sources.py && python3 _TOOLS/build_sources.py --check` | exit 0 |
| Sync | `python3 _TOOLS/sync_shared.py && python3 _TOOLS/sync_shared.py --check` | exit 0 |
| Testes | `python3 -m pytest -q -p no:cacheprovider _DESIGN_SYSTEM/tests _TESTS` | `0 failed` (com o layout do `HEAD`) |
| Varredura | `git ls-files \| grep -iE 'strategyzer.*\.pdf$'` | vazio |

## Scope

**In scope**: `_FONTES/manifest.json`, `_TOOLS/build_sources.py`, `_TOOLS/sync_shared.py`, `_TOOLS/README.md`,
`LICENSE`, `THIRD_PARTY_NOTICES.md` (novo, gerado) e cópias nas skills, remoção dos 3 PDFs da Strategyzer,
`references/fontes.md` regeneradas, `experimentacao-inovacao/SKILL.md` (só a linha de proveniência),
`experimentacao-inovacao/assets/{test-card,learning-card}.md`, `scorecard-inovacao/references/estrutura-e-adaptacao.md`,
`relatorio-final-inovacao/references/pitch-canvas-executivo.md` (só o cabeçalho de fonte/licença),
`_TESTS/test_licencas.py` (novo), `plans/README.md`.

**Out of scope**: reescrever o histórico do git (veja Maintenance notes — exige autorização expressa);
conteúdo metodológico das skills; scripts de entregáveis; decisão jurídica sobre *ShareAlike*; tornar o repositório público.

## Git workflow

Branch `advisor/038-licenca-terceiros`; um commit por passo; português no imperativo; sem push/merge.

## Steps

### Step 1: Manifesto com titular, licença e distribuição

Em `_TOOLS/build_sources.py`, acrescente três campos obrigatórios a `FIELDS` e valide:

- `titular`: texto não vazio ou `null` (= titularidade a confirmar).
- `licenca`: texto não vazio (ex.: `"Licença de Uso Restrito CCEE"`, `"CC BY-SA 4.0"`,
  `"Todos os direitos reservados — Strategyzer AG"`, `"A confirmar"`).
- `distribuido`: booleano. `true` → `<skill>/<arquivo>` **tem** de existir (regra atual). `false` → `arquivo` é
  uma URL `https://` e **nenhum** arquivo com o nome da URL pode existir na skill; o hash vira `"—"` na página.

Preencha todas as entradas de `_FONTES/manifest.json`:

| Entradas | `titular` | `licenca` | `distribuido` |
|---|---|---|---|
| rubricas, scripts, adaptações locais, `eric-esteira`, `4d-rc6`, `3e-rc6`, `4d-pdf` | `"CCEE"` | `"Licença de Uso Restrito CCEE"` | `true` |
| `4d-docx`, `3e-docx`, `5c-docx` e transcrições | `null` | `"A confirmar"` | `true` |
| `strategyzer-test`, `strategyzer-learning`, `strategyzer-scorecard` | `"Strategyzer AG"` | `"Todos os direitos reservados — Strategyzer AG"` | `false`, `arquivo` = URL oficial |
| adaptações dos cards (`3e-test-card`, `experimento-test-template`, `experimento-learning-template`, `scorecard-adaptacao`) | `"CCEE (adaptação de método da Strategyzer AG)"` | `"Licença de Uso Restrito CCEE"` | `true` |
| `pitch-canvas-company` | `"Best 3 Minutes (David Beckett); ilustrações de Birgit Smit"` | `"CC BY-SA 4.0"` | `true` |
| `pitch-canvas-adaptacao` | `"CCEE (usa a estrutura do The Pitch Canvas)"` | `"A confirmar (CC BY-SA 4.0 se for adaptação)"` | `true` |

Se o operador já tiver respondido sobre os DOCX (veja STOP conditions), use a resposta em vez de `null`.
Mantenha `PINNED` dos DOCX. Inclua as colunas Titular e Licença na tabela de `page()`.

**Verify**: `python3 _TOOLS/build_sources.py --check` falha (PDFs ainda presentes com `distribuido: false`) —
esperado até o Step 2.

### Step 2: Retirar os PDFs da Strategyzer

- `git rm` dos três PDFs.
- URLs oficiais nas entradas: confirme cada uma abrindo a página (a da Learning Card está truncada em
  `entregaveis.md:37`; copie a completa). Se uma URL não carregar ou redirecionar para página sem o
  instrumento, use a página da biblioteca mais próxima e registre em `notas`.
- `experimentacao-inovacao/SKILL.md:86`: troque por "cards seguem os modelos Test Card e Learning Card da
  Strategyzer AG (links em `references/fontes.md`); os modelos em `assets/` são adaptações locais."
- `experimentacao-inovacao/assets/test-card.md` e `learning-card.md`: acrescente no topo uma linha de crédito
  — "Adaptação do Test Card/Learning Card © Strategyzer AG (strategyzer.com). Os nomes e o modelo original
  pertencem à Strategyzer; esta adaptação não é endossada por ela."
- `scorecard-inovacao/references/estrutura-e-adaptacao.md`: mesma linha de crédito para o Innovation Project Scorecard.
- Rode `build_sources.py` (regenera `fontes.md`).

**Verify**: `git ls-files | grep -iE 'strategyzer.*\.pdf$'` → vazio; `build_sources.py --check` → exit 0;
`git grep -n -iE "strategyzer-[a-z-]+-2023\.pdf" -- ':(exclude)plans'` → vazio.

### Step 3: Pitch Canvas — atribuição completa

No topo de `relatorio-final-inovacao/references/pitch-canvas-executivo.md`, mantenha a linha de fonte existente
e acrescente: "*The Pitch Canvas©* é licenciado sob CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/);
referência obrigatória a Best3minutes.com. Se esta orientação for considerada adaptação do canvas, ela também
fica sob CC BY-SA 4.0 — veja `THIRD_PARTY_NOTICES.md`." **Não** mude a licença declarada no `SKILL.md` da skill.

**Verify**: a linha aparece; o PDF continua no lugar com hash igual ao do manifesto.

### Step 4: `THIRD_PARTY_NOTICES.md` gerado

Acrescente a `build_sources.py` a geração de `THIRD_PARTY_NOTICES.md` na raiz (e `--check` compara):

1. Cabeçalho: "Gerado de `_FONTES/manifest.json` por `_TOOLS/build_sources.py`. Não edite manualmente."
2. **Material de terceiros** — entradas cujo `titular` não é `"CCEE"` nem `null`: título, titular, licença,
   skills, se é distribuído (arquivo) ou só referenciado (URL), notas.
3. **Fontes tipográficas** — lista fixa no script (`FONT_NOTICES`): Montserrat e Roboto, "SIL Open Font
   License 1.1", caminho `assets/design-system/assets/fonts/` e o arquivo `*-OFL.txt`. O script falha se os
   `*-OFL.txt` não existirem em `_DESIGN_SYSTEM/assets/fonts/`.
4. **Titularidade a confirmar** — entradas com `titular: null` ou `licenca` começando por "A confirmar".

**Verify**: `build_sources.py --check` → exit 0; o arquivo lista Strategyzer (3, não distribuídos),
Pitch Canvas, as duas fontes e os DOCX a confirmar.

### Step 5: `LICENSE` restrito ao que é da CCEE

Substitua o segundo e o terceiro parágrafos do `LICENSE` por:

```
Esta licença se aplica ao conteúdo de autoria da CCEE neste repositório e nas
skills dele derivadas. É proibido usar, copiar, modificar, distribuir ou
sublicenciar esse conteúdo, no todo ou em parte, sem autorização prévia e por
escrito da CCEE.

Esta licença NÃO se aplica aos materiais de terceiros listados em
THIRD_PARTY_NOTICES.md (por exemplo, métodos e nomes da Strategyzer AG,
The Pitch Canvas e as fontes tipográficas Montserrat e Roboto), que permanecem
sob a titularidade e as licenças indicadas naquele arquivo. Itens marcados
como "a confirmar" ali não são reivindicados por esta licença até que sua
titularidade seja confirmada.
```

Mantenha título, copyright, isenção de garantia e a linha de contato (`[PREENCHER: e-mail da GEIN]`).

Em `_TOOLS/sync_shared.py`, copie também `THIRD_PARTY_NOTICES.md` para `<skill>/THIRD_PARTY_NOTICES.md`
(mesmo padrão do `LICENSE`; adicione à lista `required`). Rode o sync.

**Verify**: `sync_shared.py --check` → exit 0; `ls */THIRD_PARTY_NOTICES.md | wc -l` → 12.

### Step 6: `_TESTS/test_licencas.py`

Use cópias em `tmp_path`; nunca altere o repositório real.

- Manifesto sem `titular`/`licenca`/`distribuido` → `build_sources` falha.
- Entrada `distribuido: false` com o arquivo presente na skill → falha; com URL não-`https` → falha.
- Nenhum arquivo versionado casa `strategyzer.*\.pdf`.
- `THIRD_PARTY_NOTICES.md` contém "Strategyzer AG", "CC BY-SA 4.0", "SIL Open Font License 1.1".
- `LICENSE` contém "NÃO se aplica" e "THIRD_PARTY_NOTICES.md"; cada skill tem `LICENSE` e
  `THIRD_PARTY_NOTICES.md` idênticos aos da raiz.
- Todo arquivo de fonte em `_DESIGN_SYSTEM/assets/fonts/` tem um `*-OFL.txt` da mesma família.

**Verify**: suíte inteira `0 failed`.

### Step 7: Documentação e versão

- `_TOOLS/README.md`: novos campos do manifesto, `THIRD_PARTY_NOTICES.md` e a regra "material de terceiros
  sem licença que permita redistribuição entra como `distribuido: false` com URL — nunca como arquivo".
- **Se o Plano 037 já estiver mesclado**: rode `python3 _TOOLS/build_catalog.py --bump` (sobe
  `experimentacao-inovacao`, `scorecard-inovacao`, `relatorio-final-inovacao` e, pelas cópias de
  `LICENSE`/`THIRD_PARTY_NOTICES.md`, as 12) e `--check`.

**Verify**: todos os comandos da tabela "Commands" passam.

## Test plan

`_TESTS/test_licencas.py` (Step 6) cobre esquema do manifesto, ausência dos PDFs, conteúdo dos avisos e
cópias nas skills; `build_sources --check` e `sync_shared --check` garantem que nada foi editado à mão.

## Done criteria

- [ ] Nenhum PDF da Strategyzer versionado; links oficiais nas `fontes.md`
- [ ] Manifesto com `titular`, `licenca` e `distribuido` em todas as entradas; `build_sources --check` → 0
- [ ] `THIRD_PARTY_NOTICES.md` gerado, na raiz e nas 12 skills
- [ ] `LICENSE` restrito ao conteúdo da CCEE, com exceção explícita para terceiros
- [ ] Créditos à Strategyzer nos modelos adaptados e CC BY-SA no guia do Pitch Canvas
- [ ] Suíte `0 failed`; sync → 0; status em `plans/README.md`

## STOP conditions

- O operador ainda não respondeu sobre a titularidade dos DOCX 4D/3E/5C: **não pare** — use `null`/"A confirmar"
  e registre no status. Pare só se a resposta disser que são de terceiro **sem** cessão de direitos à CCEE:
  aí o tratamento passa a ser o mesmo da Strategyzer e precisa de decisão do operador.
- Alguma skill depende do conteúdo dos PDFs da Strategyzer para funcionar (um script lê o PDF, um eval o anexa).
- Encontrar outro material de terceiros distribuído que não esteja nesta lista (registre e pergunte antes de remover).
- Algum passo exigiria reescrever o histórico do git.

## Maintenance notes

- **Histórico do git**: os PDFs da Strategyzer continuam nos commits antigos. Enquanto o repositório for
  privado, retirá-los do `HEAD` resolve a distribuição atual. **Antes de torná-lo público**, é preciso
  reescrever o histórico (`git filter-repo --path <pdf> --invert-paths`) e forçar o push — operação destrutiva
  que exige autorização expressa do operador e aviso a quem tem clones. Não faz parte deste plano.
- A decisão sobre *ShareAlike* no guia do Pitch Canvas e o texto final do `LICENSE` são do jurídico da CCEE;
  o `THIRD_PARTY_NOTICES.md` é o material para essa consulta.
- Pacotes `.skill` antigos em `_DIST/` e releases já publicadas ainda contêm os PDFs: regenere (Plano 037) e
  apague releases antigas que os contenham.
