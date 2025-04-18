from pydantic import BaseModel, Field


class Missao(BaseModel):
    total: int
    nome_inimigo: str
    completa: bool = Field(False)
    contagem: int = Field(0)
