from uuid import uuid4

from models.entidade import OBJETOS_TIPOS, Entidade
from pydantic import Field


class Inimigo(Entidade):
    id_unico: str = Field(default_factory=lambda: str(uuid4()))
    tipo: OBJETOS_TIPOS = 'INIMIGO'
    sprite_particula: str

    @property
    def renascido(self):
        classname = self.__class__
        base_dict = super().renascido.model_dump()
        base_dict['id_unico'] = str(uuid4())
        return classname(**base_dict)
