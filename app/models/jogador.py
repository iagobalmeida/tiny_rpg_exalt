import json
import math
from dataclasses import dataclass
from enum import Enum
from logging import getLogger
from typing import Dict, List, Literal, Optional, Tuple, Union

from config import get_config
from models.entidade import Entidade
from models.item import Consumivel, Equipamento
from models.itens import ITEMS
from pydantic import Field

log = getLogger('uvicorn')

CLASSE_TIPOS = Literal['APRENDIZ', 'SELVAGEM', 'BARBARO', 'MAGO', 'FEITICEIRO', 'GUERREIRO', 'TEMPLARIO']


@dataclass
class Classe():
    nome: str
    sprite_x: int
    sprite_y: int
    nivel: int = 1
    proxima_classe: Optional[str] = None
    habilidade_ii_nome: Optional[str] = None
    habilidade_ii_descricao: Optional[str] = None
    habilidade_iii_nome: Optional[str] = None
    habilidade_iii_descricao: Optional[str] = None


class Classes(Enum):
    # Todas as habilidades são afetadas por INT e ATTR principal

    APRENDIZ = Classe(
        nome='APRENDIZ',
        sprite_x=1,
        sprite_y=5
    )

    SELVAGEM = Classe(
        # Aumenta o dano a cada ataque
        nome='SELVAGEM',
        nivel=2,
        sprite_x=0,
        sprite_y=3,
        proxima_classe='BARBARO',
        habilidade_ii_nome='FÚR.',
        habilidade_ii_descricao='Fúria'
    )

    BARBARO = Classe(
        # Aumenta ainda mais o dano a cada ataque
        # Aumenta o dano quanto menos vida tiver
        nome='BÁRBARO',
        nivel=3,
        sprite_x=1,
        sprite_y=3,
        habilidade_ii_nome='FÚR.',
        habilidade_ii_descricao='Fúria',
        habilidade_iii_nome='EXEC.',
        habilidade_iii_descricao='Execução',
    )

    MAGO = Classe(
        # Recupera energia a cada turno
        nome='MAGO',
        nivel=2,
        sprite_x=5,
        sprite_y=2,
        proxima_classe='FEITICEIRO',
        habilidade_ii_nome='BOL. FOG.',
        habilidade_ii_descricao='Bola de Fogo'
    )

    FEITICEIRO = Classe(
        # Recupera mais energia a cada turno
        # Recupera energia conforme leva dano
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
        # Aumenta a resistência conforme leva dano
        nome='GUERREIRO',
        nivel=2,
        sprite_x=0,
        sprite_y=1,
        proxima_classe='TEMPLARIO',
        habilidade_ii_nome='BENÇ.',
        habilidade_ii_descricao='Benção'
    )

    TEMPLARIO = Classe(
        # Aumenta resistência confome leva dano
        # Recupera vida a cada turno
        nome='TEMPLÁRIO',
        nivel=3,
        sprite_x=4,
        sprite_y=1,
        proxima_classe=None,
        habilidade_ii_nome='BENÇ.',
        habilidade_ii_descricao='Benção',
        habilidade_iii_nome='REDN.',
        habilidade_iii_descricao='Redenção',
    )


class Jogador(Entidade):
    email: str
    senha: str
    classe: Classe
    pontos_disponiveis: int = Field(default=0)
    missoes: Dict[str, Tuple[int, int, str, bool]] = Field(default_factory=lambda: {
        'floresta': (0, 25, 'Rato Guerreiro', True),
        'mata_fechada': (0, 30, 'Gnomo Ancião', False),
        'castelo_abandonado': (0, 35, 'Entidade Obscura', False),
        'cemiterio': (0, 40, 'Esqueleto', False),
        'catacumbas': (0, 40, 'Protetor das Catacumbas', False),
        'calabouco': (0, 50, 'Bispo Corrompido', False),
        'laboratorio_secreto': (0, 100, 'Dragão Jovem', False),
        'submundo': (0, 200, 'Experimento IV', False),
        'nulo': (0, 250, 'Amon', False)
    })

    @classmethod
    def primeiro_nivel(cls, nome: str, descricao: str, email: str, senha: str, classe: Classes):
        """Cria um novo jogador no primeiro nível."""
        config = get_config()

        return cls(
            nome=nome,
            descricao=descricao,
            email=email,
            senha=senha,
            classe=classe.value,
            level=1,
            vida=250,
            energia=250,
            experiencia=0,
            forca=10,
            agilidade=10,
            resistencia=10,
            inteligencia=10,
            sprite_x=classe.value.sprite_x,
            sprite_y=classe.value.sprite_y
        )

    @property
    def experiencia_proximo_nivel(self):
        return 10 + ((self.level - 1) * 15)

    @property
    def deve_subir_nivel(self):
        return self.experiencia >= self.experiencia_proximo_nivel

    def get_websocket_data(self):
        base_dict = self.model_dump()
        base_dict['classe'] = self.classe.__dict__
        base_dict['experiencia_proximo_nivel'] = self.experiencia_proximo_nivel
        base_dict['missoes'] = self.missoes
        return base_dict

    def subir_nivel(self):
        self.experiencia -= self.experiencia_proximo_nivel
        self.level += 1
        self.pontos_disponiveis += math.ceil(1.5 * (self.classe.nivel+1))

        self.energia_maxima += math.ceil(self.level/100) * (2 * (self.classe.nivel+1))
        self.vida_maxima += math.ceil(self.level/10) * (2 * (self.classe.nivel+1))
        self.energia = self.energia_maxima
        self.vida = self.vida_maxima

    def atribuir_ponto(self, atributo: str):
        """Atribui um ponto de atributo ao jogador."""
        if self.pontos_disponiveis > 0:
            setattr(self, atributo, getattr(self, atributo) + 1)
            self.pontos_disponiveis -= 1

    def subir_nivel_classe(self, nome_classe: Optional[CLASSE_TIPOS] = None):
        """Sobe o nível da classe do jogador."""
        config = get_config()

        if self.classe.nivel == 1 and self.level >= 15 and self.ouro >= 1500:
            self.ouro -= 1500
            self.pontos_disponiveis += config["game"]["pontos_atributo_por_level"]

            self.energia_maxima += math.ceil(self.level/10) * config["game"]["energia_base_por_level"]
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * config["game"]["vida_base_por_level"]
            self.vida = self.vida_maxima
            self.classe = Classes[nome_classe]
            self.sprite_x = self.classe.sprite_x
            self.sprite_y = self.classe.sprite_y

        elif self.classe.nivel == 2 and self.level >= 30 and self.ouro >= 100000:
            self.ouro -= 100000
            self.pontos_disponiveis += config["game"]["pontos_atributo_por_level"]

            self.energia_maxima += math.ceil(self.level/10) * config["game"]["energia_base_por_level"]
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * config["game"]["vida_base_por_level"]
            self.vida = self.vida_maxima
            self.classe = Classes[self.classe.proxima_classe]
            self.sprite_x = self.classe.sprite_x
            self.sprite_y = self.classe.sprite_y

    def progredir_missao(self, nome_inimigo: str):
        try:
            for nome_masmorra in self.missoes:
                if self.missoes[nome_masmorra][2] == nome_inimigo:
                    self.missoes[nome_masmorra] = (
                        self.missoes[nome_masmorra][0] + 1,
                        self.missoes[nome_masmorra][1],
                        self.missoes[nome_masmorra][2],
                        self.missoes[nome_masmorra][3],
                    )

                if self.missoes[nome_masmorra][0] >= self.missoes[nome_masmorra][1]:
                    self.missoes[nome_masmorra] = (
                        self.missoes[nome_masmorra][0],
                        self.missoes[nome_masmorra][1],
                        self.missoes[nome_masmorra][2],
                        True
                    )
        except Exception as ex:
            log.exception(ex)
            pass
