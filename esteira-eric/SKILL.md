---
name: esteira-eric
description: "Porta de entrada da Esteira Robusta de Inovação Colaborativa (ERIC) da CCEE: lê os arquivos e decisões do projeto, identifica em que etapa ele está, mostra o que já existe e o que falta e indica a próxima skill: potencial, briefing, IQB, workshops e relatórios 4D, 3E e 5C, experimentação, scorecard, relatório final ou Cadastro de Demanda Tecnológica (CDT) para a Tecnologia. Use quando o usuário pedir orientação geral sobre a esteira ou o projeto: por onde começar, qual o próximo passo, o que falta, em que etapa estamos, que skill usar. Não use quando o pedido já indicar o entregável ou a skill (por exemplo, \"faça o relatório 4D\" ou \"avalie o IQB\"): nesse caso, use diretamente a skill específica."
license: "Licença de Uso Restrito CCEE. Termos completos em LICENSE."
metadata:
  requirements: "Não gera entregáveis; Python opcional, só para preferências locais e aviso de atualização."
  author: "GEIN-CCEE"
  version: "1.2.4"
---

# Esteira ERIC

Orienta o projeto de inovação pela esteira e encaminha para a skill certa. Esta skill **não produz entregáveis**:
quem escreve briefing, relatório, cards ou apresentação é a skill específica. Qualquer skill pode ser usada a
qualquer momento; a etapa é contexto, nunca pré-requisito.

## Grilling

Leia [o protocolo de grilling](references/grilling-operacional.md). Resolva nos arquivos tudo que for pesquisável e
pergunte só o que decide o encaminhamento. Nunca pergunte o resultado ou a nota desejada.

## Preferências do usuário

No início, leia as preferências locais do usuário conforme [o guia](references/preferencias-do-usuario.md) e aplique-as
abaixo das regras do método. Quando o usuário pedir uma mudança permanente de comportamento, proponha gravá-la (só esta
skill ou todas; usuário ou projeto) e só grave com confirmação. "Resetar" volta ao padrão de fábrica.

## Passos

1. **Inventário:** liste os arquivos e registros do projeto e classifique cada um pelo entregável que representa
   (oportunidade, briefing, IQB, potencial, registros D1 a D4 e relatório 4D, 5C, 3E e Test Cards, modelo de
   experimentação e Learning Cards, scorecard, relatório final, CDT). Registre data, versão e se foi examinado.
   Sem arquivos, pergunte em uma frase o que o projeto já tem.
2. **Etapa provável:** use [o mapa](references/mapa-das-skills.md) e [a esteira](references/eric-esteira.md) para
   situar o projeto pela entrega real mais recente, não pelo nome dos arquivos. Se as fontes se contradisserem
   (por exemplo, relatório 4D sem briefing), diga isso em vez de escolher uma versão.
3. **Diagnóstico:** o que já existe, o que falta para a próxima decisão (BP1, BP2 ou implementação) e lacunas ou
   contradições que afetam o próximo passo. Não reabra decisões já tomadas nem trate hipótese como fato.
4. **Encaminhamento:** indique **uma** próxima skill (no máximo duas alternativas), com o motivo e o que levar
   para ela. Com o aceite do usuário, siga essa skill por completo, lendo o `SKILL.md` dela; não reproduza aqui o
   trabalho dela.
5. **Pedido direto:** se o usuário pedir um entregável ou uma skill específica, vá direto a ela, mesmo que a etapa
   pareça outra; apenas registre lacunas relevantes.

## Resposta

Curta, em linguagem simples e sem travessão ([guia](references/linguagem-dos-entregaveis.md)), revisada com o
[guia de escrita](references/guia-de-escrita.md):

- **Onde o projeto está**: etapa provável e a evidência que a indica.
- **O que já existe**: entregáveis encontrados, com data ou versão.
- **O que falta**: só o que pesa na próxima decisão.
- **Próximo passo**: a skill indicada, por quê e o que levar.

## Exemplo

Entrada: “Tenho o briefing v2 e o relatório 4D do portal; e agora?”
Saída (trecho):
> Etapa: aprofundamento concluído (relatório 4D de 12/09); falta o parecer do BP1.
> Próximo passo: `workshop-3e`, para tornar testável a alternativa priorizada no D4. Leve o relatório 4D e a decisão do BP1.

## Checagem final

- [ ] Etapa sustentada por arquivos ou respostas, com contradições explícitas
- [ ] Uma skill indicada, com motivo e insumos
- [ ] Nenhum entregável produzido aqui; nenhuma decisão reaberta

## Contexto ERIC

ERIC = Esteira Robusta de Inovação Colaborativa da CCEE (Câmara de Comercialização de Energia Elétrica).

**Proveniência:** skill própria desta pasta, construída sobre a síntese metodológica em `references/eric-esteira.md`.
