import json
from typing import Dict

from data import inimigos
from models.missoes import Missao

MISSOES: Dict[str, Missao] = {
    'floresta': Missao(
        total=20,
        nome_inimigo=inimigos.rato_guerreiro.nome
    ),
    'mata_fechada': Missao(
        total=30,
        nome_inimigo=inimigos.gnomo_anciao.nome
    ),
    'castelo_abandonado': Missao(
        total=40,
        nome_inimigo=inimigos.entidade_obscura.nome
    ),
    'cemiterio': Missao(
        total=50,
        nome_inimigo=inimigos.morto_vivo.nome
    ),
    'catacumbas': Missao(
        total=60,
        nome_inimigo=inimigos.protetora_das_catacumbas.nome
    ),
    'calabouco': Missao(
        total=70,
        nome_inimigo=inimigos.sacerdote_renegado.nome
    ),
    'laboratorio_secreto': Missao(
        total=80,
        nome_inimigo=inimigos.dragao_anciao.nome
    ),
    'submundo': Missao(
        total=90,
        nome_inimigo=inimigos.experimento_iv.nome
    ),
    'nulo': Missao(
        total=100,
        nome_inimigo=inimigos.barbathos.nome
    )
}


def missoes_dict_to_json(missoes_dict: dict) -> str:
    for nome_regiao in missoes_dict:
        if not isinstance(missoes_dict[nome_regiao], dict):
            missoes_dict[nome_regiao] = missoes_dict[nome_regiao].model_dump()
    return json.dumps(missoes_dict)
