# Skills de inovação da GEIN-CCEE

Catorze skills no padrão aberto [Agent Skills](https://agentskills.io/specification) para a Esteira
Robusta de Inovação Colaborativa (ERIC) da CCEE: briefing, avaliação IQB, potencial, workshops e
relatórios 4D, 3E e 5C, experimentação, scorecard, relatório final e o Cadastro de Demanda Tecnológica (CDT) para a Tecnologia, mais a `esteira-eric`, porta de entrada
que diagnostica a etapa do projeto e indica a próxima skill. Pedidos diretos (por exemplo, "faça o relatório 4D")
continuam indo direto para a skill específica. Funcionam no Claude (app e
Claude Code), no ChatGPT/Codex e em outras ferramentas compatíveis.

Na `briefing-inovacao`, as entregas são **Entrevista Inicial de sete campos**,
**Briefing** de uma página e **Perguntas para fechar lacunas**. A skill
`avaliacao-briefing-iqb` identifica qual desses documentos está avaliando.

Cada skill tem versão própria (`metadata.version` no `SKILL.md`) e é atualizada de forma independente.
O [`catalog.json`](catalog.json) registra a versão publicada de cada uma.

## 1. Instalar com `npx skills` (Claude Code, Codex, Cursor, Copilot e outras)

```bash
npx skills add mrayoub/eric_skills --all                 # as 14 skills em todas as ferramentas detectadas
npx skills add mrayoub/eric_skills --skill relatorio-4d  # só uma skill
npx skills add mrayoub/eric_skills --all -g              # instalação global (todos os projetos)
npx skills add mrayoub/eric_skills --skill relatorio-4d -a claude-code codex  # ferramentas específicas
npx skills update                                        # atualiza só as skills que mudaram
```

Enquanto o repositório for privado, é preciso ter acesso a ele no GitHub, com credencial configurada no `git`.

## 2. Instalar pelo arquivo `.skill`

<!-- Fontes: https://support.claude.com/en/articles/12512180-use-skills-in-claude (consultado em 2026-10-09);
     https://learn.chatgpt.com/docs/build-skills (pasta $HOME/.agents/skills do Codex). -->

Baixe na Release [`pacotes`](https://github.com/mrayoub/eric_skills/releases/tag/pacotes), que sempre tem a versão
mais recente das 14 skills (mais `catalog.json` e `SHA256SUMS`); cada versão também tem sua própria Release
(`<skill>-v<versão>`). Localmente, `python3 _TOOLS/build_dist.py` gera os mesmos pacotes em `_DIST/`. Cada `.skill`
é um ZIP com a pasta da skill na raiz.

- **Claude.ai ou app do Claude:** Customize → Skills → *Upload a skill*. Se a interface não aceitar a
  extensão `.skill`, renomeie uma cópia para `.zip`.
- **ChatGPT:** envie o mesmo arquivo pelo fluxo de instalação de skills.
- **Claude Code (manual):** descompacte em `~/.claude/skills/`.
- **Codex (manual):** descompacte em `~/.agents/skills/`.

## 3. Clonar o repositório (mantenedores)

Clone o repositório e crie links simbólicos de cada pasta de skill em `~/.claude/skills/` e
`~/.agents/skills/`. Um `git pull` atualiza todas as instalações.

## 4. Verificar atualizações

```bash
python3 <pasta-da-skill>/scripts/check_updates.py
```

Lista cada skill como `atualizada`, `instalada X; disponível Y` ou `alterada localmente`. Não altera
nenhum arquivo. Com o repositório privado, defina `GITHUB_TOKEN` para ler o catálogo.

## 5. Publicar uma nova versão (mantenedores)

1. Edite a skill ou a fonte compartilhada (`_DESIGN_SYSTEM/`, `_SHARED/`, `_ERIC_CONTEXT/`).
2. `python3 _TOOLS/sync_shared.py` e `python3 _TOOLS/build_sources.py`.
3. `python3 _TOOLS/build_catalog.py --bump` sobe a versão das skills cujo conteúdo mudou (`--bump minor` ou `major` quando couber).
4. Rode os testes e abra um pull request. A CI recusa conteúdo de skill alterado sem `--bump` e confere os três
   canais (`python3 _TOOLS/check_channels.py`). Depois do merge, a CI publica as Releases das versões novas.

Uma mudança no design system altera o pacote das 13 skills e, portanto, a versão de todas.

## Preferências do usuário

Cada skill aceita ajustes de comportamento do próprio usuário, guardados só na máquina dele e nunca enviados para
outro lugar. Quando você pede uma mudança permanente ("sempre", "nunca", "daqui para frente"), a skill propõe gravá-la,
mostra o texto e o alcance (só ela ou todas as skills; você em todos os projetos ou só o projeto atual) e grava com o
seu "sim". As regras do método continuam valendo acima de qualquer preferência.
Preferências vindas da pasta do projeto aparecem como não confirmadas até você aprovar o conjunto; qualquer mudança
nesses arquivos exige nova confirmação.

- Arquivos: `~/.config/eric-skills/<skill>.md` e `todas.md`; no projeto, `.eric/preferencias/`.
- Ver: `python3 <skill>/scripts/preferencias.py listar`.
- Padrão de fábrica: `python3 <skill>/scripts/preferencias.py resetar <skill>` ou `resetar --todas-as-skills`
  (guarda uma cópia `.bak`).

Funciona no Claude Code e no Codex locais. No Claude.ai e no ChatGPT, que não guardam arquivos entre conversas,
cole a preferência nas instruções do Projeto ou na memória do app.

## Licença

Conteúdo da CCEE sob a Licença de Uso Restrito CCEE ([`LICENSE`](LICENSE)). Material de terceiros está
listado em [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md), com titulares e licenças próprios.
