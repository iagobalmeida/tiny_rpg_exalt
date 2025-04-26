from enum import Enum

from data import habilidades
from models.classe import Classe


class Classes(Enum):
    # Todas as habilidades são afetadas por INT e ATTR principal

    APRENDIZ = Classe(
        nome='APRENDIZ',
        nivel=1,
        sprite_x=1,
        sprite_y=5,
        habilidades=[habilidades.GolpeEspiritual()]
    )

    SELVAGEM = Classe(
        nome='SELVAGEM',
        nivel=2,
        sprite_x=0,
        sprite_y=3,
        proxima_classe='BARBARO',
        habilidades=[habilidades.GolpeEspiritual(), habilidades.Furia()]
    )

    BARBARO = Classe(
        nome='BARBARO',
        nivel=3,
        sprite_x=1,
        sprite_y=3,
        habilidades=[habilidades.GolpeEspiritual(), habilidades.Furia(), habilidades.Execucao()]
    )

    MAGO = Classe(
        nome='MAGO',
        nivel=2,
        sprite_x=5,
        sprite_y=2,
        proxima_classe='FEITICEIRO',
        habilidades=[habilidades.GolpeEspiritual(), habilidades.BolaDeFogo()]
    )

    FEITICEIRO = Classe(
        nome='FEITICEIRO',
        nivel=3,
        sprite_x=6,
        sprite_y=2,
        proxima_classe=None,
        habilidades=[habilidades.GolpeEspiritual(), habilidades.BolaDeFogo(), habilidades.Congelar()]
    )

    GUERREIRO = Classe(
        nome='GUERREIRO',
        nivel=2,
        sprite_x=0,
        sprite_y=1,
        proxima_classe='TEMPLARIO',
        habilidades=[habilidades.GolpeEspiritual(), habilidades.Bencao()]
    )

    TEMPLARIO = Classe(
        nome='TEMPLARIO',
        nivel=3,
        sprite_x=4,
        sprite_y=1,
        proxima_classe=None,
        habilidades=[habilidades.GolpeEspiritual(), habilidades.Bencao(), habilidades.Redencao()]
    )
