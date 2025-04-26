from dataclasses import dataclass
from logging import getLogger
from typing import List, Optional

from models.habilidades import Habilidade
from pydantic import Field

log = getLogger('uvicorn')


@dataclass
class Classe:
    nome: str
    sprite_x: int
    sprite_y: int
    nivel: int
    proxima_classe: Optional[str] = None
    habilidades: List[Habilidade] = Field(default_factory=lambda: [])

    def get_websocket_data(self):
        base_dict = self.__dict__.copy()
        base_dict['habilidades'] = [
            habilidade.model_dump() for habilidade in self.habilidades
        ]
        return base_dict
