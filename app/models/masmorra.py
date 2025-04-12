from typing import List, Dict, Type
import random
from pydantic import Field

from app.models.entidade import Entidade
from app.services.combate import Combate

class Masmorra(Entidade):
    lista_inimigos: List[Entidade] = Field(default_factory=list)
    passos: int = Field(default=0)
    total_passos: int = Field(default=100)
    pausado: bool = Field(default=False)
    imagem_background: str = Field(default='default_bg.png')

    def iniciar_combate(self, jogador: Entidade):
        """Inicia um novo combate na masmorra."""
        inimigo = random.choice(self.lista_inimigos).renascido
        self.combate = Combate(jogador, inimigo)

    @classmethod
    def casa(cls):
        """Retorna uma instância da masmorra Casa."""
        from app.models.masmorras import casa
        return casa.clone()

    @classmethod
    def por_nome(cls, nome: str):
        """Retorna uma instância da masmorra pelo nome."""
        from app.models.masmorras import MASMORRAS
        return MASMORRAS[nome].clone()

    def clone(self):
        """Retorna uma cópia da masmorra."""
        return self.__class__(**self.model_dump()) 