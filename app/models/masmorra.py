import math
import random
from typing import List, Literal, Tuple, Union

from models.entidade import Entidade, Objeto
from models.inimigos import Inimigo
from models.item import UNION_ITEM
from pydantic import Field


class Masmorra(Objeto):
    tipo: Literal['MASMORRA'] = 'MASMORRA'
    lista_inimigos: List[Union[Entidade, Inimigo]] = Field(default_factory=list)
    lista_itens: List[Tuple[float, UNION_ITEM]] = Field(default_factory=list)  # chance, item
    passos: int = Field(default=0)
    pausado: bool = Field(default=False)
    imagem_background: str = Field(default='default_bg.png')

    @property
    def total_passos(self) -> int:
        return math.ceil(len(self.lista_inimigos)/1.5) * len(self.lista_inimigos)

    @classmethod
    def casa(cls):
        """Retorna uma instância da masmorra Casa."""
        from models.masmorras import casa
        return casa.clone()

    @classmethod
    def por_nome(cls, nome: str):
        """Retorna uma instância da masmorra pelo nome."""
        from models.masmorras import MASMORRAS
        return MASMORRAS[nome].clone()

    def clone(self):
        """Retorna uma cópia da masmorra."""
        return self.__class__(**self.model_dump())

    def get_websocket_data(self):
        base_dict = self.model_dump()
        base_dict['total_passos'] = self.total_passos
        return base_dict

    def inimigo_aleatorio(self) -> Inimigo:
        tamanho_intervalo = math.ceil(len(self.lista_inimigos)/1.5)
        indice_maximo = self.passos // tamanho_intervalo
        indice_minimo = max(0, indice_maximo - 1)

        # Garante que os índices não ultrapassem o tamanho da lista
        indice_maximo = min(indice_maximo, len(self.lista_inimigos) - 1)
        indice_minimo = min(indice_minimo, len(self.lista_inimigos) - 1)

        # Escolhe aleatoriamente um inimigo entre o índice mínimo e máximo
        indice_escolhido = random.randint(indice_minimo, indice_maximo)
        inimigo = self.lista_inimigos[indice_escolhido]

        ret = inimigo.renascido
        return ret

    def item_aleatorio(self) -> UNION_ITEM:
        if not self.lista_itens:
            return None
        tamanho_intervalo = math.ceil(len(self.lista_itens)/1.5)
        indice_maximo = self.passos // tamanho_intervalo
        indice_minimo = max(0, indice_maximo - 1)

        # Garante que os índices não ultrapassem o tamanho da lista
        indice_maximo = min(indice_maximo, len(self.lista_itens) - 1)
        indice_minimo = min(indice_minimo, len(self.lista_itens) - 1)

        # Escolhe aleatoriamente um item entre o índice mínimo e máximo
        indice_escolhido = random.randint(indice_minimo, indice_maximo)
        chance, item = self.lista_itens[indice_escolhido]

        chance = max(0, 1 - chance)

        if random.random() >= chance:
            return item.model_copy()
