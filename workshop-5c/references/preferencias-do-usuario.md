# Preferências do usuário

Cada usuário pode ajustar o comportamento desta skill ao próprio jeito de trabalhar. As preferências ficam só na
máquina dele, fora da pasta da skill, e nunca são enviadas para outro lugar. Sem preferências, a skill segue o
comportamento padrão. O script é `scripts/preferencias.py`, ao lado deste arquivo (`../scripts/preferencias.py`).

## No início de cada execução

Rode `python3 scripts/preferencias.py ler <esta-skill> --versao-atual <versão do SKILL.md>`, acrescentando
`--projeto <pasta do projeto>` quando houver uma pasta de projeto. Aplique o que vier, nesta ordem de força:
projeto · esta skill, projeto · todas, usuário · esta skill, usuário · todas. Se duas preferências conflitarem, vale a
mais forte; diga ao usuário qual foi aplicada. Se o script avisar que uma preferência é de versão anterior, aplique-a
e pergunte, uma vez, se ela ainda vale. Se o script não existir ou não houver onde gravar (Claude.ai, ChatGPT e outros
ambientes sem arquivos persistentes), siga sem preferências.

## Quando propor uma preferência

Proponha quando o usuário pedir uma mudança permanente ("sempre", "nunca", "daqui para frente", "pare de") ou
corrigir o mesmo comportamento mais de uma vez. Um pedido só para o documento atual não vira preferência.

Antes de gravar, mostre e peça um "sim":

- o texto da preferência, em uma frase que descreva o comportamento;
- o alcance: só esta skill, ou todas as skills (`--todas`);
- o nível: o usuário em todos os projetos, ou só este projeto (`--projeto`).

Com o "sim", rode `python3 scripts/preferencias.py adicionar <esta-skill> "<texto>" --versao <versão>` com as opções
escolhidas. Sem "sim", não grave.

## O que recusar

As regras do método e do design system valem mais que qualquer preferência. Não grave, e explique por quê, uma
preferência que peça para:

- dispensar critério definido antes da coleta, inventar números, evidências ou decisões, ou tratar hipótese como fato;
- contornar o schema, marcar como completa uma versão sem as seções exigidas ou reduzir a fonte para caber;
- remover licença, fontes ou o crédito de material de terceiros;
- registrar dados pessoais ou conteúdo do projeto. A preferência descreve o comportamento, não o caso.

## Ver, remover e voltar ao padrão de fábrica

- Ver tudo: `python3 scripts/preferencias.py listar` (com `--projeto` para incluir o projeto).
- Remover uma: `python3 scripts/preferencias.py remover <esta-skill> P03` (com `--todas` se estiver no arquivo comum).
- **Padrão de fábrica desta skill:** `python3 scripts/preferencias.py resetar <esta-skill>`.
- **Padrão de fábrica de todas as skills:** `python3 scripts/preferencias.py resetar --todas-as-skills`.

O reset guarda uma cópia `.bak` do arquivo anterior. Os arquivos ficam em `~/.config/eric-skills/` (ou na pasta da
variável `ERIC_SKILLS_CONFIG`) e em `<projeto>/.eric/preferencias/`, e podem ser editados à mão.

Em ambientes sem arquivos persistentes, sugira ao usuário colar a preferência nas instruções do Projeto ou na memória
do app; a skill não consegue gravá-la ali.
