from typing import List, Literal

from models.estado import Estado
from pydantic import BaseModel, Field

OBJETOS_TIPOS = Literal['OBJETO', 'CONSUMIVEL', 'EQUIPAMENTO', 'NPC', 'INIMIGO', 'HUMANO', 'MASMORRA', 'JOGADOR']


class Objeto(BaseModel):
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
    sprite_nome: str = Field(default='rogues.webp')
    sprite_largura: int = Field(default=224*3)
    sprite_altura: int = Field(default=224*3)
    estados: List[Estado] = Field(default=[])

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
        values['estados'] = []
        return classname(**values)

    @property
    def congelado(self):
        return any([e.nome == 'Congelamento' for e in self.estados])

    def aplicar_dano(self, quantidade: int):
        self.vida = max(0, self.vida - quantidade)

    def adicionar_estado(self, estado):
        for estado_atual in self.estados:
            if estado_atual.nome == estado.nome:
                estado_atual.duracao += estado.duracao
                return
        self.estados.append(estado)

    def executar_estados(self) -> bool:
        index_estados_finalizados = []

        for indice, estado in enumerate(self.estados):
            if estado.executar(self):
                index_estados_finalizados.append(indice)

        for indice in index_estados_finalizados:
            self.estados.pop(indice)
        return True

    def get_websocket_data(self):
        base_dict = self.model_dump()
        if self.estados:
            base_dict['estado'] = [estado.model_dump() for estado in self.estados]
        return base_dict
