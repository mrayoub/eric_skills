# EXEMPLO FICTÍCIO: Entrada guiada para solicitações completas

ID sample-cdt · versão 1.0.0 · Completo

Amostra de validação visual e estrutural. Dados, pessoas e resultados são fictícios.

## Estado da CDT

Pronta para envio. Todos os campos da área têm fonte e os seis itens do comunicado estão atendidos. Principal ponto fraco: a meta de devoluções é uma proposta da área, ainda sem estudo de viabilidade.

Fontes: FIC-01

## Título da demanda

Pedidos de dados com formulário guiado e protocolo único

Fontes: FIC-01

## Descrição: objetivo da demanda

Fazer com que os pedidos de dados cheguem completos na primeira tentativa, reduzindo devoluções e o tempo até a resposta.

Fontes: FIC-01

## Descrição: problema e contexto

Pedidos de dados chegam por e-mail e planilha sem as informações mínimas. No exemplo, cerca de 4 em cada 10 voltam ao solicitante para complemento, o que atrasa a resposta e gera retrabalho na equipe de atendimento.

Fontes: FIC-01

## Descrição: públicos impactados

- Agentes de mercado que pedem dados (organizações, não pessoas)
- Analistas da equipe de atendimento, que recebem e respondem
- Gestores da área, que acompanham prazos

Fontes: FIC-01

## Descrição: como funciona hoje

O agente envia e-mail ou planilha. O analista confere manualmente, pede complementos por e-mail quando falta informação e registra o andamento em planilha própria. Não há campo obrigatório nem status visível ao agente.

Fontes: FIC-02

## Descrição: resultados esperados e indicadores

- Devoluções por informação ausente: de 40% para até 15% dos pedidos em 3 meses (meta proposta pela área, sem estudo de viabilidade)
- Já medido no teste: 7 de 8 analistas simulados preencheram o formulário guiado sem ajuda
- Fonte de apuração: registro de pedidos da equipe

Fontes: FIC-02

## Descrição: entregas essenciais

- Formulário guiado com campos obrigatórios por tipo de pedido
- Registro único dos pedidos com número de protocolo

Fontes: FIC-02

## Descrição: entregas importantes, que podem vir depois

- Status do pedido visível ao agente
- Painel de prazos para a gestão

Fontes: FIC-02

## Descrição: fora do escopo

- Integração automática com outros sistemas internos (depende de outra área)
- Resposta automática dos pedidos

Fontes: FIC-02

## Descrição: prioridades

Primeiro o formulário guiado, porque ataca a principal causa das devoluções; depois o registro único.

Fontes: FIC-02

## Descrição: regras, restrições e dependências

- Campos obrigatórios variam por tipo de pedido (regra a detalhar com a área)
- Pedidos trazem dados de contato de pessoas: tratar como dados pessoais
- Acesso externo de agentes depende das regras de autenticação da Tecnologia

Fontes: FIC-02

## Descrição: responsáveis

- Dúvidas de negócio: coordenação da equipe de atendimento (exemplo)
- Validação das entregas: coordenação da equipe de atendimento (exemplo)
- Decisão sobre mudanças de escopo: patrocinador da área (exemplo)

Fontes: FIC-01

## Descrição: evidências

Teste com protótipo do formulário guiado: 7 de 8 analistas simulados preencheram sem ajuda (critério prévio: 6 de 8). Devoluções em produção ainda não foram medidas.

Fontes: FIC-02

## Informações Gerais: tema(s)

Aprimoramento Tecnológico (sugestão: a demanda melhora um processo existente com apoio de sistema).

Fontes: FIC-01

## Informações Gerais: é uma demanda regulatória?

Não. Nenhuma norma exige a mudança neste exemplo.

Fontes: FIC-01

## Informações Gerais: há riscos associados à não implementação?

Sim. Justificativa: as devoluções continuam consumindo a capacidade da equipe e atrasando respostas aos agentes.

Fontes: FIC-01

## Informações Gerais: benefícios

- Menos devoluções por informação ausente
- Resposta mais rápida aos agentes
- Rastreabilidade de cada pedido por protocolo

Fontes: FIC-02

## Simplificação do Processo

Simplificação do processo: média (sugestão: elimina a troca de e-mails de complemento, mas mantém a conferência pelo analista).
Há processo atual e/ou futuro desenhado? Sim: jornada atual anexada (exemplo).

Fontes: FIC-02

## Dados do Solicitante

Diretoria, gerência e gerência executiva da área solicitante, perfil e gestor de quem abre a CDT (preencher com os dados reais no Jira).

Fontes: FIC-01

## Histórico: faz uso de dados pessoais ou sensíveis (LGPD)?

Sim. Nome e telefone de contatos dos agentes informados nos pedidos.

Fontes: FIC-02

## Solução: protótipo

Protótipo navegável do formulário guiado, usado no teste com analistas (exemplo).

Fontes: FIC-02

## Anexos

- Jornada atual do processo
- Relatório da experimentação

Fontes: FIC-02

## Checklist do comunicado de escopo

- Problema e objetivo: atendido. Problema com frequência estimada e objetivo verificável.
- Públicos impactados: atendido. Agentes, analistas e gestores separados.
- Entregas essenciais: atendido. Duas entregas ligadas ao objetivo e testadas com protótipo.
- Prioridades e resultados esperados: atendido. Ordem justificada; indicador com linha de base e meta proposta.
- Regras, restrições e dependências: atendido. Regra de campos, dados pessoais e autenticação registrados.
- Responsáveis: atendido. Dúvidas, validação e mudanças de escopo com papel definido.
Perguntas do comunicado: o problema, o público, o processo atual, o resultado e a prioridade estão nos campos de mesmo nome da Descrição.

Fontes: FIC-01, FIC-02

## Avaliação crítica: pontos fortes e fracos

Pontos fortes:
- Escopo em três grupos, com o essencial testado com protótipo (Descrição: entregas essenciais).
- Restrição de dados pessoais identificada e coerente com o campo LGPD.
Pontos fracos:
- A meta de 15% é proposta, sem estudo: a Tecnologia pode questionar o indicador. Fortalecer com a linha de base medida e o prazo de apuração.
- O teste usou 8 analistas simulados e protótipo: não mostra o efeito em produção.
- Sistemas impactados não foram levantados pela área.
Perguntas que a Tecnologia deve fazer:
- Quais tipos de pedido existem e quais campos cada um exige? Falta a regra detalhada.
- Quem homologa as entregas? Respondido em Descrição: responsáveis.

Fontes: FIC-01, FIC-02

## Dados a obter antes do envio

Nenhum dado pendente que impeça o envio. Vale obter antes da análise da Tecnologia a regra de campos por tipo de pedido.

Fontes: FIC-02

| Dado a obter | Campo da CDT | Por que a Tecnologia precisa | Onde ou com quem obter | Pergunta pronta | Impede o envio? |
| --- | --- | --- | --- | --- | --- |
| Campos obrigatórios por tipo de pedido | Descrição: regras, restrições e dependências | Define o formulário e o esforço | Coordenação da equipe de atendimento | Quais campos cada tipo de pedido exige? | Não: pode ser detalhado na análise |

## Origem e natureza dos dados

19 campos da área com fonte: 12 documentados, 3 medidos, 2 decididos e 2 propostas. Fontes: Entrevista Inicial e relatório 3E simulados; nenhuma fonte real.

Fontes: FIC-01, FIC-02

| Campo | Fonte e localizador | Natureza | Limite |
| --- | --- | --- | --- |
| Descrição: problema e contexto | FIC-01, exemplo fictício | medido | estimativa do exemplo |
| Descrição: resultados esperados | FIC-02, exemplo fictício | proposta | meta sem estudo |
| Descrição: entregas essenciais | FIC-02, exemplo fictício | decidido | teste só com protótipo |

## Fontes

- FIC-01: entrevista-inicial-simulada exemplo fictício, sem dados reais
- FIC-02: relatorio-3e-simulado exemplo fictício, sem coleta real
