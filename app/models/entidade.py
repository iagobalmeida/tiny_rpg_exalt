from typing import Literal, Optional
from pydantic import BaseModel, Field

OBJETOS_TIPOS = Literal['OBJETO', 'EQUIPAMENTO', 'NPC', 'INIMIGO', 'HUMANO', 'MASMORRA', 'JOGADOR']
EQUIPAMENTO_TIPOS = Literal['CAPACETE', 'ARMADURA', 'ARMA', 'ACESSÓRIO']

class Objeto(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    nome: str
    descricao: str
    tipo: OBJETOS_TIPOS = Field(default='OBJETO')
    equipamento_tipo: Optional[EQUIPAMENTO_TIPOS] = Field(default=None)

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
        return classname(**values) 