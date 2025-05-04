from enum import Enum

from data import habilidades
from models.classe import Classe


class Classes(Enum):
    FAZENDEIRO = Classe(
        nome='FAZENDEIRO',
        nivel=0,
        sprite_x=0,
        sprite_y=4,
        habilidades=[habilidades.GolpeEspiritual()],
        proximas_classes=[
            'INICIANTE',
            'APRENDIZ',
            'SELVAGEM',
            'VAGABUNDO'
        ]
    )

    # ==============================
    # 🛡 Caminho da Resistência
    # ==============================

    INICIANTE = Classe(
        nome='INICIANTE',
        nivel=1,
        sprite_x=0,
        sprite_y=3,
        proximas_classes=['VIGIA'],
        habilidades=[habilidades.GolpeEspiritual()]
    )

    VIGIA = Classe(
        nome='VIGIA',
        nivel=2,
        sprite_x=1,
        sprite_y=3,
        proximas_classes=['GUARDIAO'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.EscudoTemporal()]
    )

    GUARDIAO = Classe(
        nome='GUARDIAO',
        nivel=3,
        sprite_x=2,
        sprite_y=3,
        proximas_classes=['PALADINO'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.EscudoTemporal(), habilidades.ReflexaoDeDano()]
    )

    PALADINO = Classe(
        nome='PALADINO',
        nivel=4,
        sprite_x=3,
        sprite_y=3,
        habilidades=[habilidades.GolpeEspiritual(), habilidades.EscudoTemporal(), habilidades.ReflexaoDeDano(), habilidades.Regeneracao()]
    )

    # ==============================
    # 🧠 Caminho da Inteligência
    # ==============================

    APRENDIZ = Classe(
        nome='APRENDIZ',
        nivel=1,
        sprite_x=0,
        sprite_y=2,
        proximas_classes=['MAGO'],
        habilidades=[habilidades.GolpeEspiritual()]
    )

    MAGO = Classe(
        nome='MAGO',
        nivel=2,
        sprite_x=1,
        sprite_y=2,
        proximas_classes=['FEITICEIRO'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.BolaDeFogo()]
    )

    FEITICEIRO = Classe(
        nome='FEITICEIRO',
        nivel=3,
        sprite_x=2,
        sprite_y=2,
        proximas_classes=['ARCANO'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.BolaDeFogo(), habilidades.Congelar()]
    )

    ARCANO = Classe(
        nome='ARCANO',
        nivel=4,
        sprite_x=3,
        sprite_y=2,
        habilidades=[habilidades.GolpeEspiritual(), habilidades.BolaDeFogo(), habilidades.Congelar(), habilidades.VortexTemporal()]
    )

    # ==============================
    # 💪 Caminho da Força
    # ==============================

    SELVAGEM = Classe(
        nome='SELVAGEM',
        nivel=1,
        sprite_x=0,
        sprite_y=1,
        proximas_classes=['BARBARO'],
        habilidades=[habilidades.GolpeEspiritual()]
    )

    BARBARO = Classe(
        nome='BARBARO',
        nivel=2,
        sprite_x=1,
        sprite_y=1,
        proximas_classes=['BERSERKER'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.Furia()]
    )

    BERSERKER = Classe(
        nome='BERSERKER',
        nivel=3,
        sprite_x=2,
        sprite_y=1,
        proximas_classes=['CAMPEAO'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.Furia(), habilidades.Execucao()]
    )

    CAMPEAO = Classe(
        nome='CAMPEAO',
        nivel=4,
        sprite_x=3,
        sprite_y=1,
        habilidades=[habilidades.GolpeEspiritual(), habilidades.Furia(), habilidades.Execucao(), habilidades.GolpeDemolidor()]
    )

    # ==============================
    # 🦅 Caminho da Agilidade
    # ==============================

    VAGABUNDO = Classe(
        nome='VAGABUNDO',
        nivel=1,
        sprite_x=0,
        sprite_y=0,
        proximas_classes=['LADINO'],
        habilidades=[habilidades.GolpeEspiritual()]
    )

    LADINO = Classe(
        nome='LADINO',
        nivel=2,
        sprite_x=1,
        sprite_y=0,
        proximas_classes=['ASSASSINO'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.AtaqueRapido()]
    )

    ASSASSINO = Classe(
        nome='ASSASSINO',
        nivel=3,
        sprite_x=2,
        sprite_y=0,
        proximas_classes=['PREDADOR'],
        habilidades=[habilidades.GolpeEspiritual(), habilidades.AtaqueRapido(), habilidades.Esquiva()]
    )

    PREDADOR = Classe(
        nome='PREDADOR',
        nivel=4,
        sprite_x=3,
        sprite_y=0,
        habilidades=[habilidades.GolpeEspiritual(), habilidades.AtaqueRapido(), habilidades.Esquiva(), habilidades.GolpeFurtivo()]
    )
