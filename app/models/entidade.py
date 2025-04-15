from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

OBJETOS_TIPOS = Literal['OBJETO', 'CONSUMIVEL', 'EQUIPAMENTO', 'NPC', 'INIMIGO', 'HUMANO', 'MASMORRA', 'JOGADOR']


class Objeto(BaseModel):
    id_unico: str = Field(default_factory=lambda: str(uuid4()))
    nome: str
    descricao: str
    tipo: OBJETOS_TIPOS = Field(default='OBJETO')


class Entidade(Objeto):
    level: int = Field(default=1)
    vida: int
    energia: int
    experiencia: int
    ouro: int = Field(default=0)
    vida_maxima: int = Field(default=0)
    energia_maxima: int = Field(default=0)
    forca: int
    agilidade: int
    resistencia: int
    inteligencia: int
    sprite_x: int = Field(default=0)
    sprite_y: int = Field(default=0)
    sprite_nome: str = Field(default='rogues.png')
    sprite_largura: int = Field(default=224*3)
    sprite_altura: int = Field(default=224*3)
    estado_nome: Optional[str] = Field(default=None)
    estado_duracao: Optional[int] = Field(default=None)

    def model_post_init(self, __context):
        if self.vida_maxima == 0:
            object.__setattr__(self, 'vida_maxima', self.vida)
        if self.energia_maxima == 0:
            object.__setattr__(self, 'energia_maxima', self.energia)

    @property
    def renascido(self):
        """Retorna uma cópia da entidade com vida e energia máximas."""
        classname = self.__class__
        values = self.model_dump()
        values['vida'] = self.vida_maxima
        values['energia'] = self.energia_maxima
        values['id_unico'] = str(uuid4())
        return classname(**values)
