import math
from logging import getLogger
from typing import Dict, Literal, Optional, Tuple

from config import get_config
from data.classes import Classes
from models.classe import Classe
from models.entidade import Entidade
from pydantic import Field

log = getLogger('uvicorn')


class Jogador(Entidade):
    id: int
    email: str
    classe: Classe
    pontos_disponiveis: int = Field(default=0)
    bonus_atributos_classe: Dict[str, int] = Field(default_factory=lambda: {
        'forca': 0,
        'resistencia': 0,
        'agilidade': 0,
        'inteligencia': 0
    })

    @property
    def custo_habilidades(self) -> Tuple[int, int, int]:
        custo_habilidade_i = min(self.energia_maxima, max(10, int(math.sqrt(self.inteligencia)*4)))
        custo_habilidade_ii = int(custo_habilidade_i*2)
        custo_habilidade_iii = int(custo_habilidade_ii*3)
        return custo_habilidade_i, custo_habilidade_ii, custo_habilidade_iii

    @classmethod
    def a_partir_de_usuario(cls, usuario):
        """Cria um novo jogador no primeiro nível."""
        # config = get_config()
        classe = Classes[usuario.classe]

        return cls(
            id=usuario.id,
            nome=usuario.nome,
            descricao=usuario.descricao,
            email=usuario.email,
            ouro=usuario.ouro,
            classe=classe.value,
            level=usuario.level,
            experiencia=usuario.experiencia,
            vida=usuario.vida,
            energia=usuario.energia,
            forca=usuario.forca,
            agilidade=usuario.agilidade,
            resistencia=usuario.resistencia,
            inteligencia=usuario.inteligencia,
            pontos_disponiveis=usuario.pontos_disponiveis,
            tamanho_inventario=usuario.tamanho_inventario,
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
        custo_habilidade_i, custo_habilidade_ii, custo_habilidade_iii = self.custo_habilidades
        base_dict['custo_habilidade_i'] = custo_habilidade_i
        base_dict['custo_habilidade_ii'] = custo_habilidade_ii
        base_dict['custo_habilidade_iii'] = custo_habilidade_iii
        return base_dict

    def subir_nivel(self):
        self.experiencia -= self.experiencia_proximo_nivel
        self.level += 1
        self.pontos_disponiveis += self.classe.nivel+1

        self.energia_maxima += math.ceil(self.level/150) * (2 * (self.classe.nivel+1))
        self.vida_maxima += math.ceil(self.level/50) * (2 * (self.classe.nivel+1))
        self.energia = self.energia_maxima
        self.vida = self.vida_maxima

    def atribuir_ponto(self, atributo: str):
        """Atribui um ponto de atributo ao jogador."""
        if self.pontos_disponiveis > 0:
            setattr(self, atributo, getattr(self, atributo) + 1)
            self.pontos_disponiveis -= 1

    def subir_nivel_classe(self, nome_classe: Optional[Literal['APRENDIZ', 'SELVAGEM', 'BARBARO', 'MAGO', 'FEITICEIRO', 'GUERREIRO', 'TEMPLARIO']] = None):
        """Sobe o nível da classe do jogador."""
        config = get_config()

        if self.classe.nivel == 1 and self.level >= 15 and self.ouro >= 1500:
            self.ouro -= 1500
            self.pontos_disponiveis += config["game"]["pontos_atributo_por_level"]

            self.energia_maxima += math.ceil(self.level/10) * config["game"]["energia_base_por_level"]
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * config["game"]["vida_base_por_level"]
            self.vida = self.vida_maxima
            self.classe = Classes[nome_classe].value
            self.sprite_x = self.classe.sprite_x
            self.sprite_y = self.classe.sprite_y

        elif self.classe.nivel == 2 and self.level >= 30 and self.ouro >= 100000:
            self.ouro -= 100000
            self.pontos_disponiveis += config["game"]["pontos_atributo_por_level"]

            self.energia_maxima += math.ceil(self.level/10) * config["game"]["energia_base_por_level"]
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * config["game"]["vida_base_por_level"]
            self.vida = self.vida_maxima
            self.classe = Classes[self.classe.proxima_classe].value
            self.sprite_x = self.classe.sprite_x
            self.sprite_y = self.classe.sprite_y
