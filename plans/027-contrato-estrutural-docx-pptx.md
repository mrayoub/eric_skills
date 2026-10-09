# Plan 027: Contrato estrutural de fonte/cor para DOCX e PPTX (teste de manutenção)

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Drift check (rode primeiro)**:
> `git diff --stat 857d0b7..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/tokens.json`
> Se algum desses arquivos mudou desde que este plano foi escrito, compare os
> trechos de "Current state" abaixo com o código atual antes de prosseguir; em
> caso de divergência, trate como condição de STOP.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt
- **Planned at**: commit `857d0b7`, 2026-10-02

## Por que isto importa

DOCX e PPTX, neste projeto, não são rasterizados — são montados
programaticamente (`render_docx`, `render.py:623-739`; `render_pptx`,
`render.py:740-...`), por exigência do próprio `_DESIGN_SYSTEM/README.md`
("DOCX/PPTX... devem usar texto e tabelas editáveis, sem converter páginas
inteiras em imagem"). Comparação visual por pixel não faz sentido aqui; o
equivalente correto de "fidelidade ao design system" é um **contrato
estrutural**: abrir o arquivo gerado de volta e confirmar que fonte, cor e
tamanho batem com `tokens.json` — e isso não existe hoje (confirmado por
`grep -n "idempot\|geometry\|pixel\|visual" tests/test_render.py
tests/test_validators.py`: zero ocorrências).

**Achado concreto já confirmado nesta investigação** (não é hipotético — foi
reproduzido renderizando uma amostra real e inspecionando o `.pptx` resultante
com `python-pptx`): em `render_pptx`, a função interna `slide()`
(`render.py`, dentro do bloco que começa em `def slide(title: str, body: str)`)
define a fonte do título e do corpo com **strings literais** `"Montserrat"` e
`"Roboto"`, em vez de ler `tokens["typography"]["font_brand"]`/`font_body`
como `render_docx` já faz corretamente. Hoje os dois valores coincidem (os
literais e os tokens são iguais), então nenhum teste atual pega a diferença —
mas se `tokens.json` mudar a fonte da marca no futuro, `render_docx`
acompanharia automaticamente e `render_pptx` **não acompanharia** no título
nem no corpo (só o rodapé lê `tokens["typography"]["font_body"]`
dinamicamente, confirmado em `render.py` no textbox de rodapé). Este plano cria
o teste que detectaria esse drift assim que ele acontecesse, e corrige a causa
agora, enquanto o custo é baixo.

## Current state

Trechos confirmados por inspeção direta (renderizando
`_SAMPLES_ENTREGAVEIS/briefing_validation/input.json` com `--formats docx` e
`_SAMPLES_ENTREGAVEIS/executive_presentation/input.json` com `--formats pptx`
e lendo o resultado com `python-docx`/`python-pptx`):

`render_docx` (`render.py:647-650`, já correto, serve de exemplar):
```python
    style = doc.styles["Normal"]
    style.font.name = tokens["typography"]["font_body"]
    style.font.size = Pt(tokens["typography"]["styles"]["body"]["size"])
    for key in ("Title", "Heading 1", "Heading 2"):
        doc.styles[key].font.name = tokens["typography"]["font_brand"]
        doc.styles[key].font.color.rgb = RGBColor.from_string(tokens["color"]["document_primary"].lstrip("#"))
```
Confirmado por leitura do `.docx` gerado: `doc.styles["Normal"].font.name ==
"Roboto"`; `doc.styles["Title"].font.name == "Montserrat"`;
`doc.styles["Title"].font.color.rgb == RGBColor.from_string("193C8E")`
(= `tokens["color"]["document_primary"]` sem `#`).

`render_pptx`, função `slide()` (dentro de `render.py:740-...`, dentro da
função `render_pptx`), trechos **hardcoded**:
```python
        run.text, run.font.name, run.font.size, run.font.color.rgb = title, "Montserrat", Pt(28), primary
        ...
            para.font.name, para.font.size = "Roboto", Pt(17)
```
Contraste com o rodapé, que já lê o token corretamente (mesma função):
```python
        paragraph.font.name = tokens["typography"]["font_body"]
```

Confirmado por leitura do `.pptx` gerado: no slide 0, `shapes[1]` é a caixa de
título (`run.font.name == "Montserrat"`, `run.font.color.rgb ==
RGBColor.from_string("193C8E")`); `shapes[2]` é a caixa de corpo (parágrafos
usam `paragraph.font.name`, não `run.font.name` — confirmado por teste direto:
`run.font.name` retorna `None` no corpo porque o código seta a fonte no nível
do parágrafo, `para.font.name`, não no run; **o teste deste plano precisa ler
`paragraph.font.name`, nunca `run.font.name`, para os parágrafos de corpo**);
`shapes[3]` é o rodapé (`paragraph.font.name == tokens["typography"]["font_body"]`,
já correto). Ordem dos shapes é estável porque `slide()` sempre adiciona
logo → título → corpo → rodapé, nessa ordem, por chamada.

Tokens relevantes (`_DESIGN_SYSTEM/tokens.json`):
```json
"typography": {"font_brand": "Montserrat", "font_body": "Roboto",
  "styles": {"body": {"size": 9.5}, "footer": {"size": 7.5}}},
"color": {"document_primary": "#193C8E"}
```

## Commands you will need

```
PLAN_PYTHON=python3
"$PLAN_PYTHON" -c 'import docx, pptx; print("ok")'
```

| Purpose | Command | Expected on success |
|---|---|---|
| Suíte de render | `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest tests.test_render -v` | Nenhuma falha nova; novos testes do Step 2 aparecem |
| Checar só os testes novos | `cd _DESIGN_SYSTEM && "$PLAN_PYTHON" -m unittest tests.test_render.VisualTokenContractTests -v` | Todos passam |

## Scope

**In scope**:
- `_DESIGN_SYSTEM/scripts/render.py` — só a função interna `slide()` dentro de
  `render_pptx` (trocar os 2 literais hardcoded por leitura de `tokens`)
- `_DESIGN_SYSTEM/tests/test_render.py` (novos casos de teste)

**Out of scope** (não toque, mesmo que pareça relacionado):
- `render_docx` — já está correto, não precisa de mudança, só serve de
  referência/exemplar nos testes.
- Tamanhos de fonte do `render_pptx` (`Pt(28)`, `Pt(17)`) — esses números não
  têm uma entrada correspondente em `tokens["typography"]["styles"]` para
  apresentação (o schema de `styles` tem `body`/`footer`/`cover_title`/etc.,
  pensado para documento, não slide 16:9). Trocar esses tamanhos exigiria
  decidir se vale criar uma entrada nova em `tokens.json` — fora do escopo
  deste plano, que trata só de fonte/cor onde a correspondência com o token
  já existe sem ambiguidade. Ver "Maintenance notes".
- Qualquer schema em `contracts/`, `profiles.json`, `response-sections.json`.
- As 11 skills e `_SHARED/`.

## Git workflow

- Branch: `advisor/027-contrato-docx-pptx`
- Dois commits: (1) corrigir `render_pptx` para ler tokens; (2) adicionar os
  testes. Mensagens no estilo de `git log` deste repositório.
- Não dar push nem abrir PR.

## Steps

### Step 1: Corrigir `render_pptx` para ler os tokens em vez de literais

Dentro da função `slide()` em `render_pptx` (`render.py`), troque:

```python
        run.text, run.font.name, run.font.size, run.font.color.rgb = title, "Montserrat", Pt(28), primary
```
por:
```python
        run.text, run.font.name, run.font.size, run.font.color.rgb = title, tokens["typography"]["font_brand"], Pt(28), primary
```

E troque:
```python
            para.font.name, para.font.size = "Roboto", Pt(17)
```
por:
```python
            para.font.name, para.font.size = tokens["typography"]["font_body"], Pt(17)
```

(`tokens` já é parâmetro de `render_pptx`, não precisa importar nada novo.)

**Verify**: renderize a amostra executive_presentation para um diretório
temporário e confirme que o resultado é textualmente idêntico ao de antes da
mudança (já que os valores de token e os literais coincidem hoje):
```
cd _DESIGN_SYSTEM
TMP=$(mktemp -d)
"$PLAN_PYTHON" scripts/render.py ../_SAMPLES_ENTREGAVEIS/executive_presentation/input.json --out-dir "$TMP" --formats pptx
"$PLAN_PYTHON" -c "
from pptx import Presentation
import os
f = [x for x in os.listdir('$TMP') if x.endswith('.pptx')][0]
p = Presentation('$TMP/' + f)
s = p.slides[0]
print(s.shapes[1].text_frame.paragraphs[0].runs[0].font.name)
print(s.shapes[2].text_frame.paragraphs[0].font.name)
"
rm -rf "$TMP"
```
→ imprime `Montserrat` e depois `Roboto` (sem mudança visível de comportamento,
só deixou de ser hardcoded).

### Step 2: Testes de contrato estrutural

Em `_DESIGN_SYSTEM/tests/test_render.py`, siga o padrão já usado no arquivo
para testes que invocam o render real (veja a classe equivalente em
`tests/test_validators.py:31-45` para o padrão de `setUp`/`subprocess`/
`tempfile`, adaptado aqui para abrir o arquivo gerado em vez de só rodar o
processo). Adicione:

```python
class VisualTokenContractTests(unittest.TestCase):
    """Garante que DOCX/PPTX herdam fonte/cor de tokens.json, não de literais soltos."""

    def setUp(self):
        self.tokens = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))

    def test_docx_normal_and_title_follow_tokens(self):
        from docx import Document
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json"
        if not path.exists():
            self.skipTest("Amostra ausente")
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            subprocess.run([sys.executable, str(SCRIPT), str(path), "--out-dir", str(out), "--formats", "docx"],
                           check=True, capture_output=True, text=True)
            docx_file = next(out.glob("*.docx"))
            doc = Document(str(docx_file))
            self.assertEqual(doc.styles["Normal"].font.name, self.tokens["typography"]["font_body"])
            self.assertEqual(doc.styles["Title"].font.name, self.tokens["typography"]["font_brand"])
            expected_rgb = self.tokens["color"]["document_primary"].lstrip("#").upper()
            self.assertEqual(str(doc.styles["Title"].font.color.rgb), expected_rgb)

    def test_pptx_title_and_body_follow_tokens(self):
        from pptx import Presentation
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/executive_presentation/input.json"
        if not path.exists():
            self.skipTest("Amostra ausente")
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            subprocess.run([sys.executable, str(SCRIPT), str(path), "--out-dir", str(out), "--formats", "pptx"],
                           check=True, capture_output=True, text=True)
            pptx_file = next(out.glob("*.pptx"))
            prs = Presentation(str(pptx_file))
            slide = prs.slides[0]
            title_run = slide.shapes[1].text_frame.paragraphs[0].runs[0]
            self.assertEqual(title_run.font.name, self.tokens["typography"]["font_brand"])
            body_paragraph = slide.shapes[2].text_frame.paragraphs[0]
            self.assertEqual(body_paragraph.font.name, self.tokens["typography"]["font_body"])
            footer_paragraph = slide.shapes[3].text_frame.paragraphs[0]
            self.assertEqual(footer_paragraph.font.name, self.tokens["typography"]["font_body"])
```

**Verify**: `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest tests.test_render.VisualTokenContractTests -v` →
2 testes, ambos passam.

## Test plan

- `test_docx_normal_and_title_follow_tokens`: renderiza a amostra de
  `briefing_validation` e confirma fonte do corpo (`Normal`) e do título
  (`Title`) e cor do título contra `tokens.json`.
- `test_pptx_title_and_body_follow_tokens`: renderiza a amostra de
  `executive_presentation` e confirma fonte do título (nível `run`), do corpo
  e do rodapé (nível `paragraph`) contra `tokens.json` — este é o teste que
  teria pego o hardcoding corrigido no Step 1, se existisse antes.
- Rodar a suíte completa (`tests.test_render`) para confirmar que a correção
  do Step 1 não quebra nenhum teste existente (não deveria, já que os valores
  não mudam, só deixam de ser literais).

## Done criteria

- [ ] `render_pptx`/`slide()` lê `tokens["typography"]["font_brand"]` e
      `tokens["typography"]["font_body"]` em vez de `"Montserrat"`/`"Roboto"` literais
- [ ] `grep -n '"Montserrat"\|"Roboto"' _DESIGN_SYSTEM/scripts/render.py` não retorna
      nenhuma ocorrência dentro da função `render_pptx` (pode haver ocorrências
      em comentários/docstrings fora dela — confira manualmente se o grep pegar algo)
- [ ] Os 2 testes novos em `VisualTokenContractTests` passam
- [ ] `tests.test_render` completo continua passando, sem regressão
- [ ] `git status` não mostra nenhum arquivo fora da lista em "Scope"
- [ ] `plans/README.md` com a linha deste plano atualizada

## STOP conditions

Pare e reporte (não improvise) se:
- Os trechos citados em "Current state" não baterem com o `render.py` atual
  (deriva desde que este plano foi escrito).
- `tokens["typography"]["font_brand"]` ou `font_body` não forem mais
  `"Montserrat"`/`"Roboto"` no `tokens.json` atual — isso não quebra o plano,
  mas significa que o teste vai detectar uma mudança de marca já em andamento;
  confirme com o operador antes de "corrigir" `render_pptx` para o valor novo.
- `slide.shapes[1]`/`[2]`/`[3]` não corresponderem a título/corpo/rodapé na
  amostra usada (ex. se `executive_presentation/input.json` for alterado para
  ter mais ou menos conteúdo e isso mudar a ordem dos shapes) — nesse caso,
  ajuste o teste para localizar os shapes por conteúdo/posição em vez de
  índice fixo, e documente por quê.

## Maintenance notes

- Os tamanhos de fonte do PPTX (`Pt(28)` título, `Pt(17)` corpo) continuam
  hardcoded de propósito, fora do escopo — se um dia vocês quiserem
  tokenizá-los, isso exige primeiro decidir uma convenção de tamanhos para
  apresentação em `tokens.json` (hoje só existe para documento A4), o que é
  uma decisão de design, não um bug a corrigir silenciosamente.
- Esta é a mesma categoria de proteção que o Plano 026 dá para o conteúdo
  (JSON de entrada); este plano protege a etapa de renderização (como o JSON
  vira arquivo). Os dois são independentes e não têm ordem de dependência
  entre si.
- Se no futuro o PDF (via WeasyPrint/HTML) ganhar um teste de fidelidade
  visual (ver análise em `~/skills-research/relatorio/analise-fidelidade-visual-objetividade.md`,
  item 2a — possível Plano 028), ele cobre um mecanismo de renderização
  diferente (raster, não shapes/XML) e não deve ser fundido com este teste.
