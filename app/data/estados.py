from models.entidade import Entidade
from models.estado import Estado
from pydantic import Field


class Sangramento(Estado):
    nome: str = 'Sangramento'
    fator: int = Field(default=1)
    duracao: int = Field(default=5)

    def executar(self, entidade: Entidade) -> bool:
        entidade.aplicar_dano(entidade.vida * 0.01 * self.fator)
        self.duracao = max(0, self.duracao - 1)
        return self.duracao <= 0


class Congelamento(Estado):
    nome: str = 'Congelamento'
    fator: int = Field(default=1)
    duracao: int = Field(default=5)

    def executar(self, entidade: Entidade) -> bool:
        self.duracao = max(0, self.duracao - 1)
        return self.duracao <= 0
