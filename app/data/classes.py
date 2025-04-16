from enum import Enum

from models.classe import Classe


class Classes(Enum):
    # Todas as habilidades são afetadas por INT e ATTR principal

    APRENDIZ = Classe(
        nome='APRENDIZ',
        sprite_x=1,
        sprite_y=5
    )

    SELVAGEM = Classe(
        nome='SELVAGEM',
        nivel=2,
        sprite_x=0,
        sprite_y=3,
        proxima_classe='BARBARO',
        habilidade_ii_nome='FÚR.',
        habilidade_ii_descricao='Fúria'
    )

    BARBARO = Classe(
        nome='BARBARO',
        nivel=3,
        sprite_x=1,
        sprite_y=3,
        habilidade_ii_nome='FÚR.',
        habilidade_ii_descricao='Fúria',
        habilidade_iii_nome='EXEC.',
        habilidade_iii_descricao='Execução',
    )

    MAGO = Classe(
        nome='MAGO',
        nivel=2,
        sprite_x=5,
        sprite_y=2,
        proxima_classe='FEITICEIRO',
        habilidade_ii_nome='BOL. FOG.',
        habilidade_ii_descricao='Bola de Fogo'
    )

    FEITICEIRO = Classe(
        nome='FEITICEIRO',
        nivel=3,
        sprite_x=6,
        sprite_y=2,
        proxima_classe=None,
        habilidade_ii_nome='BOL. FOG.',
        habilidade_ii_descricao='Bola de Fogo',
        habilidade_iii_nome='CONG.',
        habilidade_iii_descricao='Congelar',
    )

    GUERREIRO = Classe(
        nome='GUERREIRO',
        nivel=2,
        sprite_x=0,
        sprite_y=1,
        proxima_classe='TEMPLARIO',
        habilidade_ii_nome='BENÇ.',
        habilidade_ii_descricao='Benção'
    )

    TEMPLARIO = Classe(
        nome='TEMPLARIO',
        nivel=3,
        sprite_x=4,
        sprite_y=1,
        proxima_classe=None,
        habilidade_ii_nome='BENÇ.',
        habilidade_ii_descricao='Benção',
        habilidade_iii_nome='REDN.',
        habilidade_iii_descricao='Redenção',
    )
