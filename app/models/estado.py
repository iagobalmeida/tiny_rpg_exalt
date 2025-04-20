from pydantic import BaseModel


class Estado(BaseModel):
    fator: int
    nome: str
    duracao: int

    def executar(self, entidade) -> bool:
        return True
