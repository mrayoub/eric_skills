"""Regras da Apresentação 3E: devolutiva curta para gerência e diretoria.

Segue o desenho da Apresentação 4D (orientação da autora do playbook 4D, 10/11/2026): cerca de cinco slides, cada um
com título que diz a conclusão, derivados da mesma análise do Relatório 3E. Mostra a solução, por que ela responde ao
diagnóstico do 4D, o que será construído e testado primeiro, a rota e os próximos passos.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

_spec = importlib.util.spec_from_file_location("validators_four_d_presentation_rules",
                                               Path(__file__).resolve().parent / "four_d_presentation.py")
_rules = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rules)

GENERIC_TITLES = {
    "contexto", "solucao", "a solucao", "rastreabilidade", "construcao", "testes", "experimentos", "rota",
    "proximos passos", "conclusao", "resumo", "fontes", "conteudo", "e1", "e2", "e3",
}


def validate(content: dict[str, Any]) -> list[str]:
    return _rules.check_slides(content, GENERIC_TITLES)
