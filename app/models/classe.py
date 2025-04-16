from dataclasses import dataclass
from logging import getLogger
from typing import Optional

log = getLogger('uvicorn')


@dataclass
class Classe():
    nome: str
    sprite_x: int
    sprite_y: int
    nivel: int = 1
    proxima_classe: Optional[str] = None
    habilidade_ii_nome: Optional[str] = None
    habilidade_ii_descricao: Optional[str] = None
    habilidade_iii_nome: Optional[str] = None
    habilidade_iii_descricao: Optional[str] = None
