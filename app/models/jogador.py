import math
from typing import Literal, Optional
from pydantic import Field

from app.config import get_config
from app.models.entidade import Entidade

CLASSE_TIPOS = Literal['SELVAGEM', 'MAGO', 'GUERREIRO']

SPRITES_X_Y_CLASSES = {
    'SELVAGEM': (0, 0),
    'MAGO': (1, 0),
    'GUERREIRO': (2, 0)
}

class Jogador(Entidade):
    email: str
    senha: str
    classe: CLASSE_TIPOS
    nivel_classe: int = Field(default=1)
    pontos_disponiveis: int = Field(default=0)
    sprite_x: int = Field(default=0)
    sprite_y: int = Field(default=0)
    sprite_nome: str = Field(default='player.png')
    sprite_largura: int = Field(default=32)
    sprite_altura: int = Field(default=32)

    @classmethod
    def primeiro_nivel(cls, nome: str, descricao: str, email: str, senha: str, classe: CLASSE_TIPOS):
        """Cria um novo jogador no primeiro nível."""
        config = get_config()
        return cls(
            nome=nome,
            descricao=descricao,
            email=email,
            senha=senha,
            classe=classe,
            level=1,
            vida=100,
            energia=50,
            experiencia=0,
            forca=10,
            agilidade=10,
            resistencia=10,
            inteligencia=10,
            sprite_x=SPRITES_X_Y_CLASSES[classe][0],
            sprite_y=SPRITES_X_Y_CLASSES[classe][1]
        )

    def atribuir_ponto(self, atributo: str):
        """Atribui um ponto de atributo ao jogador."""
        if self.pontos_disponiveis > 0:
            setattr(self, atributo, getattr(self, atributo) + 1)
            self.pontos_disponiveis -= 1

    def subir_nivel_classe(self, nome_classe: Optional[CLASSE_TIPOS] = None):
        """Sobe o nível da classe do jogador."""
        if nome_classe is None:
            nome_classe = self.classe

        config = get_config()
        
        if self.nivel_classe == 1 and self.level >= 15:
            self.nivel_classe = 2
            self.pontos_disponiveis += config["game"]["pontos_atributo_por_level"]

            self.energia_maxima += math.ceil(self.level/10) * config["game"]["energia_base_por_level"]
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * config["game"]["vida_base_por_level"]
            self.vida = self.vida_maxima
            self.classe = nome_classe
            self.sprite_x = SPRITES_X_Y_CLASSES[nome_classe][0]
            self.sprite_y = SPRITES_X_Y_CLASSES[nome_classe][1]

        elif self.nivel_classe == 2 and self.level >= 30:
            self.nivel_classe = 3
            self.pontos_disponiveis += config["game"]["pontos_atributo_por_level"]

            self.energia_maxima += math.ceil(self.level/10) * config["game"]["energia_base_por_level"]
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * config["game"]["vida_base_por_level"]
            self.vida = self.vida_maxima
            self.classe = nome_classe
            self.sprite_x = SPRITES_X_Y_CLASSES[nome_classe][0]
            self.sprite_y = SPRITES_X_Y_CLASSES[nome_classe][1] 