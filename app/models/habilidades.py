from models.entidade import OBJETOS_TIPOS, Entidade, Objeto
from pydantic import Field


class Habilidade(Objeto):
    tipo: OBJETOS_TIPOS = 'HABILIDADE'
    nivel: int = Field(defaul=1)

    def aplicar(self, de: Entidade, para: Entidade):
        pass

    def executar(self, de: Entidade, para: Entidade, atributos_bonus: dict = {}):
        if de.energia >= de.custo_habilidades[self.nivel-1]:
            de.energia -= de.custo_habilidades[self.nivel-1]

            de_com_atributos = de.com_atributos_bonus(atributos_bonus)  # TODO: Só funciona para Jogador por enquanto
            self.aplicar(de_com_atributos, para)

            de.vida = de_com_atributos.vida
            de.energia = de_com_atributos.energia
            de.estados = de_com_atributos.estados
            de.particulas_temporarias = de_com_atributos.particulas_temporarias
