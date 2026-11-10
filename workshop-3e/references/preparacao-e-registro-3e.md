# Preparar e registrar o 3E a partir do 4D

O 3E e o 4D são sequenciais. O objetivo do 3E é transformar a hipótese priorizada no 4D numa solução mais concreta, e
o E1 abre apresentando essa hipótese. Desde a orientação da autora do playbook 4D (10/11/2026), o `relatorio-4d`
termina numa **hipótese de solução** em três partes ("Acreditamos que... / Porque o diagnóstico mostrou... /
Precisamos validar se...") e numa **conclusão** que diz o que o 3E precisa resolver. Prepare o 3E a partir delas, e
registre o encontro para que o `relatorio-3e` consiga mostrar a ligação entre os dois.

## 1. Ponto de partida (antes do E1)

Extraia do relatório 4D, sem reescrever:

- **A hipótese de solução**, com as três partes. Se o 4D não tiver hipótese formulada, monte uma versão provisória a
  partir das conclusões e do ranking, rotulada como provisória, e confirme no E1.
- **O que o 3E precisa resolver** e o que seguiu aberto.
- **Os temas e dores que sustentam a hipótese**, com os IDs do 4D quando houver.
- **As suposições** de "Precisamos validar se", que alimentam o E3.

Sem relatório 4D (o 3E pode partir de outra origem), registre de onde veio a solução candidata e trate a ligação com o
diagnóstico como lacuna a fechar.

## 2. Formato, presença e regras

- **Convidados e presentes, separados**, com área e papel. Registre quem pode assumir ações e dependências.
- **Adaptações** do playbook registradas antes, com motivo.

## 3. O que registrar em cada E

| Etapa | Registre no dia | Por que o relatório precisa |
|---|---|---|
| E1 | A hipótese apresentada; as frases "é / não é / resolve a dor de / gera valor para"; mudanças que o grupo fez na hipótese e o motivo | Hipótese refinada e o que mudou desde o 4D |
| E2 | Componentes com ID (C01...), classificados em precisa ter, pode evoluir e fora do recorte; para cada um, a dor ou tema do 4D que o justifica; ação, responsável, apoio, dependência e prazo aceitos | Rastreabilidade 4D e 3E; plano de construção |
| E3 | Suposições com ID (S01...), ligadas aos componentes e priorizadas por risco; um Test Card por teste, com critério fechado ou marcado como rascunho | Plano de experimento e Test Cards |
| Convergência | As três respostas da rodada final (abaixo) | Acabativa do relatório |

**Componente sem dor que o justifique** é sinal de escopo crescendo: registre e pergunte ao grupo se fica em "pode
evoluir" ou "fora do recorte".

## 4. Rodada de convergência (5 a 10 minutos, ao fim do E3)

Pergunte ao grupo e registre as respostas:

1. **O que vamos construir ou testar primeiro**, e por quê?
2. **Qual rota parece mais provável** (interna, externa, híbrida, indefinida) e do que ela depende?
3. **O que segue aberto** e quem responde?

Antes de encerrar, confira: responsáveis e prazos aceitos, Test Cards com critério ou status de rascunho, respostas da
convergência anotadas. O que faltar vira lacuna anotada no dia, com o motivo.

## 5. Registro do encontro como base do relatório

O registro (`three_e_workshop_record`) segue a base que o `relatorio-3e` usa:

| `section_key` | Conteúdo |
|---|---|
| `starting_point` | Hipótese do 4D (ou origem da solução candidata), o que o 3E precisa resolver, temas e suposições herdados |
| `e1` a `e3` | O que aconteceu em cada etapa, com os registros da tabela acima e fonte por item |
| `convergence` | Respostas da rodada de convergência, ou a indicação de que ela não ocorreu |
| `record_gaps` | O que não foi registrado, em que etapa, por quê e como obter; "nenhuma lacuna" quando for o caso |
