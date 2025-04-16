from typing import List, Literal, Union

from models.entidade import Objeto
from pydantic import Field

EQUIPAMENTO_TIPOS = Literal['ARMA', 'ARMADURA', 'ACESSORIO']


class Item(Objeto):
    descricao: List[str]
    quantidade: int = Field(default=1)
    sprite_x: int = Field(default=0)
    sprite_y: int = Field(default=0)

    def usar(self, jogador):
        pass


class Consumivel(Item):
    tipo: str = 'CONSUMIVEL'


class ConsumivelCura(Consumivel):
    atributo: str = Field('vida')
    fator: int = Field(5)

    def usar(self, jogador):
        setattr(jogador, self.atributo, getattr(jogador, self.atributo) + self.fator)


class Equipamento(Item):
    tipo: str = 'EQUIPAMENTO'
    descricao: List[str]
    equipamento_tipo: EQUIPAMENTO_TIPOS
    em_uso: bool = Field(default=False)
    forca: int = Field(default=0)
    agilidade: int = Field(default=0)
    resistencia: int = Field(default=0)
    inteligencia: int = Field(default=0)


UNION_ITEM = Union[Consumivel, ConsumivelCura, Equipamento]
