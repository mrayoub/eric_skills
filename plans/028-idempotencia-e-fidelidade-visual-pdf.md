# Plan 028: Idempotência verificável do PDF (Fase 1 autônoma) e fidelidade visual contra referência aprovada (Fase 2, requer aprovação humana)

> **Executor instructions**: Siga o plano passo a passo. Rode cada comando de
> verificação e confirme o resultado esperado antes de avançar. Se ocorrer algo
> da seção "STOP conditions", pare e reporte — não improvise. Ao terminar,
> atualize a linha deste plano em `plans/README.md`.
>
> **Aviso de verificação**: este plano foi escrito num ambiente **sem a
> biblioteca nativa `pango`** instalada (confirmado: `python3 -c "import
> weasyprint"` falha com `OSError: cannot load library 'pango-1.0-0'` nesta
> máquina de autoria). Por isso, a Fase 1 (idempotência via `pypdf`) foi
> especificada mas **não pôde ser executada ponta a ponta nesta sessão** — o
> código segue a API documentada do `pypdf` (já é dependência do projeto,
> `requirements.txt`), mas rode o Step 0 primeiro para confirmar que seu
> ambiente consegue gerar PDF antes de seguir.
>
> **Drift check (rode primeiro)**:
> `git diff --stat 857d0b7..HEAD -- _DESIGN_SYSTEM/scripts/render.py _DESIGN_SYSTEM/requirements.txt`

## Status

- **Priority**: P3
- **Effort**: Fase 1: S | Fase 2: L (e requer decisão do operador antes de começar)
- **Risk**: LOW (Fase 1) | MED (Fase 2 — nova dependência + curadoria manual)
- **Depends on**: nenhum dos planos 026/027 (independente, mas pode rodar depois deles)
- **Category**: tests
- **Planned at**: commit `857d0b7`, 2026-10-02

## Por que isto importa

`_DESIGN_SYSTEM/README.md` já define idempotência em prosa ("os mesmos JSON,
perfil, tokens, fontes e versão do renderer produzem o mesmo conteúdo,
geometria e aparência"), mas nenhum teste verifica isso (`grep -n
"idempot\|geometry\|pixel\|screenshot\|visual" tests/test_render.py
tests/test_validators.py`: zero ocorrências). O `manifest.json` que `render.py`
já grava (`content_sha256`/`profile_sha256`/`tokens_sha256`/hash por arquivo,
`render.py:908-922`) **não serve** para provar isso: o próprio README avisa que
bytes de PDF variam por metadado interno do WeasyPrint entre execuções, então
um teste de hash de arquivo teria falso-negativo constante — não tente
reaproveitar o manifesto para esta verificação.

Este plano é deliberadamente dividido em duas fases de risco e custo muito
diferentes:

- **Fase 1 (autônoma, sem dependência nova)**: prova de idempotência por
  **conteúdo textual extraído**, não por imagem — renderiza o mesmo JSON duas
  vezes e compara o texto extraído de cada PDF com `pypdf` (já é dependência
  do projeto). Pega bugs reais de não-determinismo (ordem de iteração
  instável, timestamp vazando para o conteúdo visível, etc.) sem precisar de
  imagem, biblioteca nova ou aprovação humana.
- **Fase 2 (requer decisão do operador antes de começar, não execute sem
  autorização explícita)**: comparação visual real contra uma imagem de
  referência aprovada, usando um limiar de similaridade (nunca pixel-exato —
  fontes/Pango variam entre máquinas/SO, igual ao que o `plans/README.md` já
  decidiu para hash binário de PDF/DOCX: "a equivalência é checada por
  conteúdo", não por igualdade de bytes). Isto precisa de bibliotecas que
  **não estão em `requirements.txt` hoje** (`pdf2image`, `Pillow`,
  `scikit-image` — confirmado ausentes por `grep` no arquivo) e de alguém
  olhando e aprovando manualmente a primeira imagem de referência por tipo —
  não é algo que um executor sozinho deveria decidir que "está certo".

## Current state

`_DESIGN_SYSTEM/requirements.txt` (arquivo inteiro):
```
jsonschema==4.26.0
referencing==0.36.2
weasyprint==61.2
pydyf==0.10.0
python-docx==1.1.2
python-pptx==1.0.2
pypdf==5.9.0
```
`pypdf` já está disponível — a Fase 1 não precisa de nenhuma dependência nova.
`pdf2image`/`Pillow`/`scikit-image` **não estão na lista** — a Fase 2 exigiria
adicioná-las.

Padrão de skip já estabelecido pelo Plano 007 para ambientes sem `pango`
(`plans/007-fallback-pdf-sem-pango.md:60-61`): testes de PDF devem pular
(`skipTest`), nunca falhar, quando `python3 -c "import weasyprint"` retorna
código diferente de 0. Siga o mesmo padrão aqui.

## Commands you will need

```
PLAN_PYTHON=python3
"$PLAN_PYTHON" -c "import weasyprint" ; echo "pango: $?"
"$PLAN_PYTHON" -c "import pypdf; print('pypdf ok')"
```

| Purpose | Command | Expected on success |
|---|---|---|
| Checar pango (gate da Fase 1 e 2) | `"$PLAN_PYTHON" -c "import weasyprint"; echo $?` | `0` com pango instalado; se ≠0, os testes deste plano devem pular (`skipTest`), não falhar — igual ao Plano 007 |
| Suíte de render | `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest tests.test_render -v` | Nenhuma falha nova; novo teste da Fase 1 aparece (passando ou pulado, nunca falhando) |

## Scope

**Fase 1 — in scope**:
- `_DESIGN_SYSTEM/tests/test_render.py` (novo teste de idempotência textual)

**Fase 2 — fora de escopo deste plano enquanto não houver autorização**: não
crie `requirements.txt` novo, não adicione `pdf2image`/`Pillow`/
`scikit-image`, não gere nem aprove nenhuma imagem golden sem o operador ter
visto e confirmado explicitamente. A seção "Fase 2 — especificação para quando
houver autorização" abaixo existe para ser executada **depois**, como um plano
separado ou uma continuação explicitamente pedida — não como parte automática
deste plano.

**Out of scope** (não toque, mesmo que pareça relacionado):
- `_DESIGN_SYSTEM/scripts/render.py` — este plano não muda o renderizador, só
  adiciona teste.
- `manifest.json`/lógica de hash em `render.py:908-922` — não tente reutilizar
  para idempotência, pelos motivos já explicados.
- Planos 026/027 — independentes, não precisam estar prontos antes deste.

## Git workflow

- Branch: `advisor/028-idempotencia-pdf-fase1`
- Um commit (só Fase 1).
- Não dar push nem abrir PR.
- Não crie branch/commit para a Fase 2 neste plano — ela é um documento de
  especificação, não trabalho autorizado a executar agora.

## Steps (Fase 1 — autônoma)

### Step 0: Confirmar que o ambiente consegue gerar PDF

```
cd _DESIGN_SYSTEM
"$PLAN_PYTHON" -c "import weasyprint"; echo "pango: $?"
```

Se o código for diferente de `0`: o teste do Step 1 deve existir mas pular
(`self.skipTest("pango indisponível")`), exatamente como os testes de PDF do
Plano 007 já fazem. Não trate isso como falha nem tente instalar `pango`
sozinho (fora de escopo, exige `brew`/`apt-get` com privilégios que o executor
não deveria assumir ter).

### Step 1: Teste de idempotência textual

Em `_DESIGN_SYSTEM/tests/test_render.py`, siga o padrão de
`tests/test_validators.py:31-45` para invocar `render.py` duas vezes via
`subprocess` a partir do **mesmo** JSON de entrada, em dois diretórios
temporários separados, e comparar o texto extraído com `pypdf`:

```python
class PdfIdempotencyTests(unittest.TestCase):
    def test_same_json_produces_same_pdf_text(self):
        try:
            import weasyprint  # noqa: F401
        except OSError:
            self.skipTest("pango indisponível neste ambiente")
        from pypdf import PdfReader
        path = ROOT.parent / "_SAMPLES_ENTREGAVEIS/briefing_validation/input.json"
        if not path.exists():
            self.skipTest("Amostra ausente")
        texts = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as temp:
                out = Path(temp)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path),
                                         "--out-dir", str(out), "--formats", "pdf"],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                pdf_file = next(out.glob("*.pdf"))
                reader = PdfReader(str(pdf_file))
                texts.append("\n".join(page.extract_text() or "" for page in reader.pages))
                page_count = len(reader.pages)
        self.assertEqual(texts[0], texts[1], "Mesmo JSON produziu texto diferente entre duas execuções")
```

**Verify**: `cd _DESIGN_SYSTEM && PYTHONDONTWRITEBYTECODE=1 "$PLAN_PYTHON" -m unittest tests.test_render.PdfIdempotencyTests -v` →
passa (com `pango`) ou pula com motivo explícito (sem `pango`) — nunca falha
silenciosamente nem trava.

## Test plan (Fase 1)

- 1 teste novo (`test_same_json_produces_same_pdf_text`), cobrindo o caso
  central: mesma entrada, duas execuções, mesmo texto extraído.
- Rodar a suíte completa (`tests.test_render`) para confirmar que nada mais
  quebrou.

## Done criteria (Fase 1)

- [ ] `PdfIdempotencyTests` existe em `tests/test_render.py`
- [ ] O teste passa quando `pango` está disponível, e pula (não falha) quando
      não está
- [ ] `tests.test_render` completo continua passando
- [ ] `git status` não mostra nenhum arquivo fora de `tests/test_render.py`
- [ ] `plans/README.md` com a linha deste plano atualizada, status da Fase 1
      separado do status da Fase 2 (que deve ficar `TODO` / "aguardando
      autorização", não `DONE`)

## STOP conditions (Fase 1)

- O texto extraído divergir entre as duas execuções por um motivo que pareça
  **intencional** (ex. timestamp de geração embutido no rodapé) — não decida
  sozinho se isso é um bug ou um comportamento aceito; reporte o diff exato
  encontrado.
- `pypdf.PdfReader(...).pages[i].extract_text()` retornar string vazia para
  todas as páginas mesmo com `pango` disponível — isso indicaria um problema
  de extração de texto do PDF (ex. texto renderizado como curva/imagem em vez
  de texto selecionável), que é um achado por si só, fora do escopo deste
  plano corrigir.

## Fase 2 — especificação para quando houver autorização (NÃO execute sem confirmação)

Isto é uma especificação detalhada para um plano futuro, não trabalho a
executar agora. Inclua-a aqui para não perder o desenho feito nesta análise,
mas trate como TODO condicionado à decisão do operador sobre a dependência
nova e à disponibilidade de alguém para aprovar a primeira imagem de cada
tipo.

**Decisões que precisam do operador antes de começar**:
1. Adicionar `pdf2image`, `Pillow`, `scikit-image` a `requirements.txt` (ou
   usar `pdftoppm` via `subprocess` para evitar a dependência Python de
   `pdf2image`, mas isso ainda exige o binário `poppler` instalado no sistema
   — nenhuma das duas opções evita uma dependência de sistema nova).
2. Quantos tipos de `deliverable_type` precisam de golden (18 no total; talvez
   baste 1 por orientação — retrato/paisagem/16:9/página única de card — em
   vez de 1 por tipo, dado que o layout varia por orientação, não por tipo
   específico, segundo `_DESIGN_SYSTEM/README.md` "Regras visuais").
3. Quem aprova visualmente a primeira imagem golden de cada orientação antes
   de ser commitada.

**Mecanismo proposto** (para quando as decisões acima estiverem tomadas):
- `_DESIGN_SYSTEM/tests/goldens/<orientação>.png` — referência aprovada.
- Novo script `_DESIGN_SYSTEM/scripts/verify_visual.py`: renderiza uma amostra
  fixa, converte a primeira página para PNG, calcula similaridade estrutural
  (`skimage.metrics.structural_similarity`, não comparação de pixel exata) contra
  o golden, e devolve um veredito fechado: `match` (acima do limiar), `drift`
  (abaixo do limiar mas estrutura básica presente — log, não bloqueia),
  `broken` (página vazia, overflow, ou orientação errada — bloqueia a entrega,
  mesma disciplina de "nunca entregue com erro" que já existe para IQB/
  potencial).
- O limiar exato de similaridade precisa ser calibrado empiricamente (rodar o
  mesmo golden contra si mesmo em duas máquinas diferentes, se possível, para
  medir o ruído natural de anti-aliasing antes de fixar o número) — não adivinhe
  um valor sem medir.

## Maintenance notes

- A Fase 1 é barata e já entrega valor real (pega não-determinismo) sem
  esperar a Fase 2. Não trate a ausência da Fase 2 como bloqueio para fechar
  este plano.
- Se a Fase 2 for autorizada depois, ela deve virar um plano próprio (ex. 029),
  não uma reabertura deste — mantenha a numeração monotônica do índice.
- Este plano não cobre DOCX/PPTX — isso é o Plano 027 (contrato estrutural,
  mecanismo completamente diferente, já que esses formatos não são
  rasterizados).
