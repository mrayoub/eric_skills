#!/usr/bin/env python3
"""Mantém exemplos fictícios dos oficiais e variantes, sem registrar execução real."""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_SAMPLES_ENTREGAVEIS"

SCENARIOS = {
    "four_d": {
        "title": "O acompanhamento dos pedidos depende de registros dispersos",
        "summary": "Exemplo fictício. O aprofundamento relacionou a falta de previsão ao registro disperso. O grupo priorizou uma visão compartilhada do fluxo; o efeito sobre prazos ainda precisa ser testado.",
        "context": "O briefing apontava demora nas respostas aos pedidos internos. Atendimento e operação retomaram episódios do fluxo antes de desenhar alternativas. O 4D aprofundou o diagnóstico para orientar a estruturação de uma hipótese no 3E.",
        "setup": "A sessão coletiva reuniu quatro profissionais de atendimento e operação, selecionados por atuar na abertura e no tratamento dos pedidos. Jornada e barco da inovação ajudaram a examinar passagens entre áreas; brainwriting e créditos apoiaram a comparação das alternativas.",
        "stages": [
            ("A ausência de previsão aparece antes da discussão de soluções", "Os quatro participantes relataram episódios de pedidos sem retorno. A condução apresentou o briefing e registrou a expectativa de acompanhar o fluxo.", "A conversa delimitou o acompanhamento como questão do diagnóstico. O relato de demora ainda não identifica sua causa nem mede o prazo real."),
            ("O pedido perde continuidade quando muda de área", "A jornada mostrou que o protocolo, a previsão e o responsável ficam em registros diferentes. No barco, os participantes relacionaram o retrabalho à passagem entre atendimento e operação.", "O registro disperso apareceu nas duas dinâmicas. A leitura sugere examinar a passagem entre áreas, além do tempo de resposta percebido; não houve medição de retrabalho."),
            ("As alternativas combinam registro compartilhado e revisão da passagem", "O brainwriting gerou três alternativas: visão compartilhada, aviso de mudança e revisão do repasse. O grupo associou cada uma às dificuldades registradas na jornada.", "A visão compartilhada reuniu mecanismo e público numa hipótese. Acreditamos que ela pode tornar o fluxo previsível, porque o diagnóstico mostrou registros dispersos; precisamos validar se as áreas atualizam e usam a informação."),
            ("O grupo priorizou a visão compartilhada sem aprovar sua construção", "Cada participante recebeu três créditos. A visão compartilhada recebeu oito dos doze créditos; o aviso recebeu três e a revisão do repasse, um. A ata conservou a objeção sobre atualização dos dados.", "A preferência orienta o que aprofundar no 3E. Não houve aprovação de construção; responsabilidade pela atualização e esforço de manutenção continuam abertos."),
        ],
        "conclusion": "O 4D aprofundou o problema de demora ao relacioná-lo à continuidade do registro entre áreas. A hipótese de uma visão compartilhada segue ao 3E com preferência do grupo, sem evidência de redução de prazo. A atualização da informação é a principal condição a examinar.",
        "next": "A equipe do projeto deve estruturar escopo e responsabilidade pela atualização no 3E; prazo a definir. A aprovação de construção permanece pendente de escopo e esforço. A preferência registrada não substitui essa aprovação.",
        "decision": "Solicita-se ao sponsor deliberar sobre a abertura do 3E para estruturar a hipótese. A construção da solução ainda não está submetida à aprovação; a decisão deve considerar a disponibilidade das duas áreas.",
        "cta": "Sponsor e representantes das duas áreas: indiquem quem participará do 3E e registrem a decisão sobre sua abertura. Prazo a definir com a equipe do projeto.",
    },
    "three_e": {
        "title": "A visão compartilhada depende de atualização antes de automação",
        "summary": "Exemplo fictício. O 3E delimitou uma visão compartilhada dos pedidos e um teste de atualização entre áreas. A construção permanece planejada; uso e melhoria de previsibilidade ainda não foram medidos.",
        "context": "O 4D apontou registros dispersos na passagem de pedidos entre atendimento e operação. O 3E retomou essa hipótese e a objeção sobre atualização para definir escopo, construção e testes antes de solicitar implementação.",
        "setup": "A sessão reuniu responsáveis pelo fluxo, atendimento e apoio técnico, escolhidos por conhecer o repasse e a manutenção dos dados. O quadro de escopo separou o que precisa existir do que pode evoluir; os Test Cards organizaram testes prospectivos.",
        "stages": [
            ("O primeiro recorte acompanha o pedido sem substituir os sistemas", "O grupo refinou a hipótese do 4D: tornar visíveis responsável, estado e previsão do pedido. Integração automática e substituição dos sistemas ficaram fora do primeiro recorte.", "Os três componentes respondem à dificuldade de continuidade registrada no 4D. A hipótese permanece parcial quanto ao esforço de atualização, que precisa ser avaliado antes da coleta."),
            ("A responsabilidade pela atualização condiciona o primeiro protótipo", "O plano prevê um protótipo com campos de responsável, estado e previsão. Atendimento abrirá o registro; operação atualizará a passagem. O apoio técnico verificará acesso, enquanto prazos e esforço de manutenção seguem a definir.", "A construção está planejada, não concluída. A rota permanece indefinida até a avaliação técnica; a dependência central é manter o registro atualizado sem duplicar trabalho."),
            ("O teste observará atualização antes de avaliar ganho de prazo", "TC-01: acreditamos que as duas áreas conseguirão manter o pedido atualizado. O teste acompanhará uma rodada simulada; medirá atualizações feitas e tempo de registro. O limiar será fechado antes da coleta, com responsáveis pelo fluxo.", "O Test Card é prospectivo e ainda precisa do critério aprovado antes da coleta. Não há resultado de uso ou eficácia. O plano separa observar atualização de medir eventual melhoria da previsibilidade."),
        ],
        "conclusion": "O 3E transformou a hipótese do 4D em escopo e construção planejados, com teste voltado à atualização. A rota e o esforço técnico seguem abertos. O próximo avanço depende de fechar responsabilidades e critério antes de executar o teste.",
        "next": "Responsáveis pelo fluxo devem fechar o critério do TC-01 antes da coleta; prazo a definir. Apoio técnico deve avaliar esforço e alternativas de rota. A aprovação para construir depende dessa avaliação, sem presumir autorização já concedida.",
        "decision": "Solicita-se aos responsáveis pelo fluxo deliberar sobre a disponibilidade para a simulação. A aprovação do critério do teste permanece pendente; este material não solicita escala da solução.",
        "cta": "Responsáveis pelo fluxo e apoio técnico: registrem critério, responsáveis e data da simulação antes da coleta. Prazo para fechar o plano a definir com a equipe do projeto.",
    },
    "five_c": {
        "title": "Os clientes relacionam previsibilidade a estado e responsabilidade",
        "summary": "Exemplo fictício. A escuta relacionou a falta de previsão à informação sobre estado e responsável. Os grupos cocriaram duas propostas; a preferência registrada ainda não demonstra uso nem redução de prazo.",
        "context": "O diagnóstico de pedidos apontava dúvidas sobre andamento. A equipe apresentou essa leitura e ouviu organizações externas antes de discutir propostas. O 5C examinou o que os clientes precisam saber para acompanhar um pedido e orientar testes posteriores.",
        "setup": "A sessão coletiva reuniu seis representantes de três organizações externas, escolhidas por utilizar o fluxo com frequências diferentes. A jornada orientou a escuta, o quadro de experiência desejada apoiou a confirmação e os canvases organizaram a cocriação. A contagem de créditos foi por pessoa presente.",
        "stages": [
            ("A escuta começou pela dúvida sobre o andamento do pedido", "A equipe apresentou o diagnóstico e perguntou quais dúvidas permaneciam na prática. Os seis presentes conheceram a agenda e os combinados de registro; propostas ficaram para depois da escuta.", "Os participantes reconheceram a questão do acompanhamento e pediram atenção à passagem entre áreas. Esse enquadramento define o recorte, sem representar todo o público do serviço."),
            ("O cliente procura uma previsão quando o pedido muda de área", "Quatro dos seis presentes relataram procurar atendimento quando não viam uma previsão. Os episódios apontaram mudanças de responsável sem atualização visível. Dois participantes também citaram utilidade no protocolo de abertura.", "A escuta aprofundou a relação entre estado, responsável e previsão. As quatro menções indicam experiências dos presentes, não prevalência no mercado nem votos de priorização."),
            ("A experiência desejada exige saber quem responde pelo próximo movimento", "A confirmação reuniu três necessidades: ver o estado, entender a previsão e identificar o responsável. Os participantes descreveram situações em que a previsão muda e pediram que o motivo da mudança fosse visível.", "Os critérios desejados foram registrados como sinais observáveis de acompanhamento. Não houve aprovação de meta de prazo nem medição de satisfação."),
            ("Os grupos propuseram consulta de andamento e avisos de mudança", "Dois grupos produziram canvases. Um propôs uma consulta com estado, previsão e responsável; outro, avisos quando esses dados mudam. As duas propostas responderam às necessidades confirmadas.", "As propostas são hipóteses cocriadas. Menos contatos de acompanhamento é benefício esperado, ainda sem medição; atualização dos dados e acesso às informações são dependências a avaliar."),
            ("A consulta de andamento recebeu mais créditos entre os presentes", "Cada um dos seis presentes recebeu dez créditos. A consulta recebeu quarenta dos sessenta créditos; os avisos, vinte. A ata registrou a objeção sobre a possibilidade de mostrar uma previsão desatualizada.", "A consulta ficou como preferência para investigação. A distribuição não aprova implementação nem demonstra eficácia; a qualidade da atualização segue como condição para testar a proposta."),
        ],
        "conclusion": "O 5C aprofundou a necessidade de previsibilidade e a ligou à informação sobre estado e responsabilidade. A consulta de andamento recebeu mais créditos, com uma condição explícita: a informação precisa ser atualizada. As propostas seguem como hipóteses para avaliação e teste.",
        "next": "A equipe do projeto deve avaliar atualização e acesso com operação e apoio técnico; prazo a definir. A devolutiva às organizações deve registrar dependências e plano de teste. A aprovação de implementação continua pendente dessa avaliação.",
        "decision": "Solicita-se ao sponsor deliberar sobre a avaliação de dependências da consulta de andamento. O pedido não inclui aprovação de implementação; o plano de teste deverá voltar com responsáveis e critérios antes da coleta.",
        "cta": "Equipe do projeto e sponsor: registrem responsáveis pela avaliação e combinem a data da devolutiva com as organizações. Prazo a definir, antes de iniciar o teste da proposta.",
    },
}


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compose(method: str, form: str, sessions: list, variant_note: str = "") -> dict:
    scenario = SCENARIOS[method]
    kind = f"{method}_official_{form}"
    item = {"schema_version": "1.0.0", "deliverable_type": kind, "locale": "pt-BR", "title": scenario["title"], "summary": scenario["summary"], "blocks": [],
            "citations": [{"id": "F01", "source_id": "roteiro-ficticio", "locator": "Método e escopo planejado da sessão; exemplo fictício."}, {"id": "F02", "source_id": "registro-ficticio", "locator": "Mural, ata e encaminhamentos do exemplo fictício; não é evidência de execução real."}],
            "metadata": {"artifact_id": f"sample-{kind.replace('_', '-')}", "content_version": "1.0.0", "completeness": "complete", "method_application": {"sessions": sessions}}}
    reduced = all(s["variant"] == "pocket" for s in sessions)
    adapted = any(s["variant"] == "adapted" for s in sessions)
    if reduced:
        item["summary"] = "Exemplo fictício. A sessão pocket aprofundou o recorte inicial. As etapas seguintes ficaram fora do escopo por desenho; os achados orientam a decisão sobre uma próxima rodada."
    elif adapted:
        item["summary"] = "Exemplo fictício. A aplicação adaptada confrontou condições de uma oferta existente na rodada final. Os registros orientam novas perguntas; não houve votação nessa rodada nem aprovação de implementação."
    if len(sessions) > 1:
        item["summary"] = "Exemplo fictício. O remoto confirmou temas; no presencial, os grupos cocriaram propostas e priorizaram a consulta. A preferência depende de informação atualizada e ainda não demonstra eficácia."
    if form == "presentation":
        item["metadata"]["decision_required"] = True

    def section(key: str, title: str, text: str, citation: str = "F02") -> None:
        item["blocks"].extend([{"id": f"h_{key}", "type": "heading", "data": {"section_key": key, "text": title, "level": 2}}, {"id": f"p_{key}", "type": "paragraph", "data": {"section_key": key, "text": text}, "citation_ids": [citation]}])

    if form == "report":
        section("purpose", "O registro permite retomar a análise e seus encaminhamentos", "Este relatório registra como a aplicação foi estruturada, o que ocorreu nas etapas e o que os achados permitem encaminhar. Serve à equipe do projeto e a quem retoma ou decide sobre o trabalho.", "F01")
        section("introduction", "O ponto de partida orientou a pergunta do encontro", scenario["context"])
    else:
        section("challenge_context", "O ponto de partida orientou a pergunta do encontro", scenario["context"])
    setup = scenario["setup"]
    if reduced:
        setup = {
            "four_d": "A sessão curta reuniu atendimento e operação para explicitar percepções e diagnosticar o fluxo com jornada e barco. D3 e D4 ficaram fora do escopo por desenho; não houve desenho de alternativas nem priorização nesta rodada.",
            "three_e": "A sessão curta reuniu responsáveis pelo fluxo e apoio técnico para esclarecer o escopo e estruturar a construção. E3 ficou fora do escopo por desenho; Test Cards e planejamento de experimentos não fizeram parte desta rodada.",
            "five_c": "A sessão remota curta reuniu representantes de organizações externas para contextualizar, compreender e confirmar temas por post-its. A confirmação não construiu experiência desejada nem critérios; C4 e C5 ficaram fora do escopo. Não houve cocriação ou votação de propostas.",
        }[method]
    elif adapted:
        setup = {
            "four_d": "Atendimento e operação usaram jornada, barco e brainwriting para aprofundar o fluxo e desenhar alternativas. A rodada final foi adaptada para confrontar condições de uma oferta existente, sem distribuição de créditos.",
            "three_e": "Responsáveis pelo fluxo e apoio técnico esclareceram o escopo e estruturaram a construção. A rodada final confrontou condições de uma oferta existente em vez de planejar experimentos; não foram produzidos Test Cards nessa rodada.",
            "five_c": "Representantes de organizações externas contextualizaram o desafio, relataram experiências, confirmaram necessidades e cocriaram propostas em grupos. A rodada final confrontou condições de uma oferta existente, sem créditos ou ranking.",
        }[method]
    if len(sessions) > 1:
        setup = "Duas sessões ouviram organizações externas que usam o fluxo em frequências diferentes. No remoto, a escuta e os post-its confirmaram temas. No presencial, seis representantes trabalharam experiência desejada, canvases e créditos por pessoa presente. A confirmação remota não incluiu critérios de experiência."
    rationale = {
        "four_d": "O 4D aprofunda um desafio por percepções, diagnóstico, alternativas e priorização. Foi escolhido para investigar a demora percebida antes de assumir uma solução.",
        "three_e": "O 3E estrutura uma hipótese de solução em escopo, construção e experimentos. Foi escolhido para detalhar a hipótese do 4D e expor as condições ainda abertas antes de construir.",
        "five_c": "O 5C organiza a escuta e a cocriação com clientes, do contexto aos encaminhamentos. Foi escolhido para entender o que os clientes precisam saber sobre um pedido antes de testar propostas de acompanhamento.",
    }
    setup = rationale[method] + " " + setup
    titles = {"four_d": "A jornada e o barco orientaram o aprofundamento do fluxo", "three_e": "A estruturação reuniu operação e apoio técnico para delimitar a construção", "five_c": "O formato delimitou a escuta e a contribuição de cada sessão"}
    section("structuring", titles[method], setup + (" " + variant_note if variant_note else ""), "F01")
    for session in sessions:
        for index, stage in enumerate(session["stages"]):
            # Fixtures de adaptação têm seu próprio conteúdo, não apenas outro rótulo.
            if session["variant"] == "adapted" and index == len(session["stages"]) - 1:
                title = "A rodada adaptada confrontou condições antes de escolher propostas"
                execution = "O grupo examinou uma oferta já descrita e registrou condições de adoção. A rodada substituiu a dinâmica prevista; não houve distribuição de créditos nem ranking."
                outcome = "As condições registradas orientam perguntas para o próximo teste. A adaptação não fornece preferência comparável ao método integral nem decisão de implementação."
            else:
                original = next((i for i, s in enumerate(METHODS[method]["stages"]) if s["id"] in stage["official_stage_ids"]), index)
                title, execution, outcome = scenario["stages"][original]
                if session["variant"] == "pocket" and method == "five_c" and original == 2:
                    title = "A confirmação curta registrou os temas que ainda precisam de aprofundamento"
                    execution = "Na sessão remota, os participantes confirmaram os temas por post-its. O formato curto não incluiu experiência desejada, critérios, cocriação ou priorização de propostas."
                    outcome = "A confirmação indica os temas a aprofundar. Os critérios de experiência ficaram fora do escopo por desenho; não são lacuna de registro desta sessão."
            prefix = f"{session['id']}: " if len(sessions) > 1 else ""
            if form == "report":
                section(stage["id"] + "_description", stage["label"] + ": descrição da etapa", prefix + stage["meaning"], "F01")
                section(stage["id"] + "_execution", stage["label"] + ": execução realizada", prefix + execution)
                section(stage["id"] + "_outcome", stage["label"] + ": desfecho", prefix + outcome)
            else:
                section("execution_" + stage["id"], title, prefix + execution + " " + outcome)
    reduced = all(s["variant"] == "pocket" for s in sessions)
    adapted = any(s["variant"] == "adapted" for s in sessions)
    if reduced or adapted:
        scoped_conclusions = {
            ("four_d", True): "A sessão pocket relacionou a demora percebida à passagem de pedidos entre registros dispersos. D1 e D2 aprofundaram a questão, sem desenhar alternativas ou registrar preferência. O próximo recorte deve decidir se essa leitura sustenta uma rodada de desenho; não há hipótese priorizada nesta sessão.",
            ("three_e", True): "A sessão pocket delimitou responsável, estado e previsão no primeiro recorte e explicitou a dependência de atualização entre áreas. E1 e E2 produziram escopo e construção planejados; E3 ficou fora do escopo. O plano de teste ainda precisa ser elaborado, e a construção não foi executada.",
            ("five_c", True): "A escuta curta relacionou a dúvida sobre andamento à falta de informação atualizada. A confirmação por post-its delimitou temas para aprofundar, sem experiência desejada, critérios, propostas ou ranking. O próximo passo é avaliar quais temas exigem nova escuta antes de discutir soluções.",
            ("four_d", False): "O diagnóstico relacionou a demora a registros dispersos e o desenho gerou alternativas para a passagem entre áreas. A rodada final confrontou condições de uma oferta, sem priorização por créditos. Os achados sustentam examinar atualização e manutenção, mas não escolher uma alternativa vencedora.",
            ("three_e", False): "O escopo de acompanhamento e a construção planejada dependem da atualização entre áreas. A rodada final confrontou condições de adoção da oferta em vez de planejar experimentos. Não houve Test Card nessa rodada; a avaliação técnica e o plano de teste continuam abertos antes de construir.",
            ("five_c", False): "A escuta ligou previsibilidade a estado e responsabilidade; os grupos cocriaram consulta e avisos de mudança. A rodada final confrontou condições da oferta, sem créditos ou ranking. Atualização e acesso seguem como dependências para testar, sem preferência formal entre as propostas.",
        }
        conclusion = scoped_conclusions[(method, reduced)]
        next_step = "A equipe do projeto deve avaliar se os achados exigem nova rodada e definir seu escopo; responsável e prazo a definir. Nenhuma decisão das etapas excluídas é presumida a partir desta aplicação."
        decision = "Solicita-se ao sponsor deliberar se haverá nova rodada de aprofundamento. O pedido se limita a esse encaminhamento, sem aprovação de construção ou escala."
        cta = "Equipe do projeto e sponsor: registrem a decisão sobre a próxima rodada e seu escopo. Responsável pela organização e prazo a definir."
    else:
        conclusion, next_step, decision, cta = (scenario[k] for k in ("conclusion", "next", "decision", "cta"))
    section("conclusion", "O desfecho orienta o próximo passo dentro do escopo realizado", conclusion)
    section("recommendations", "As dependências precisam de responsáveis antes do próximo avanço", next_step)
    if form == "presentation":
        section("decision", "A decisão solicitada delimita o próximo avanço do projeto", decision)
        section("call_to_action", "Os responsáveis devem registrar o encaminhamento antes da próxima rodada", cta)
    return item


METHODS = json.loads((ROOT / "_DESIGN_SYSTEM/official-methods.json").read_text())


def main() -> None:
    for method, definition in METHODS.items():
        base = {"id": "sessao", "variant": "standard", "stages": [{**s, "official_stage_ids": [s["id"]]} for s in definition["stages"]], "out_of_scope_stages": [], "adaptation_reason": ""}
        for form in ("report", "presentation"):
            kind = f"{method}_official_{form}"
            write(OUT / kind / "input.json", compose(method, form, [copy.deepcopy(base)]))
            for variant in ("adapted", "pocket"):
                session = copy.deepcopy(base)
                session["variant"] = variant
                if variant == "pocket":
                    count = 3 if method == "five_c" else 2
                    removed = session["stages"][count:]
                    session["stages"] = session["stages"][:count]
                    session["out_of_scope_stages"] = [{"official_stage_id": s["id"], "reason": "Fora do escopo por desenho da sessão curta."} for s in removed]
                    session["adaptation_reason"] = "A rodada curta aprofundou a escuta sem realizar as etapas seguintes."
                    if method == "five_c":
                        session["stages"][-1]["meaning"] = "Confirmar temas por post-its, sem construir experiência desejada e critérios nesta sessão curta."
                else:
                    session["adaptation_reason"] = "O grupo precisava confrontar uma oferta existente antes de decidir novos testes."
                    session["stages"][-1]["label"] = "Confrontar condições"
                    session["stages"][-1]["meaning"] = "Examinar condições de adoção da oferta apresentada, sem votar propostas."
                note = session["adaptation_reason"] + " Etapas fora do escopo: " + (", ".join(s["official_stage_id"].upper() for s in session["out_of_scope_stages"]) or "nenhuma") + "."
                write(OUT / "official_variants" / f"{kind}.{variant}.json", compose(method, form, [session], note))
            if method == "five_c":
                remote = json.loads((OUT / "official_variants" / f"{kind}.pocket.json").read_text())["metadata"]["method_application"]["sessions"][0]
                remote["id"] = "remoto"
                onsite = copy.deepcopy(base)
                onsite["id"] = "presencial"
                for session in (remote, onsite):
                    for stage in session["stages"]:
                        stage["id"] = session["id"] + "_" + stage["id"]
                note = "A sessão remota cobriu C1 a C3 por desenho, com confirmação curta; C4 e C5 ocorreram apenas no presencial."
                write(OUT / "official_variants" / f"{kind}.mixed.json", compose(method, form, [remote, onsite], note))


if __name__ == "__main__":
    main()
