import math
import random
from typing import List, Literal, Optional, Tuple

from models.estado import Estado
from pydantic import BaseModel, Field

OBJETOS_TIPOS = Literal['OBJETO', 'CONSUMIVEL', 'EQUIPAMENTO', 'NPC', 'INIMIGO', 'HUMANO', 'MASMORRA', 'JOGADOR', 'HABILIDADE']

CONFIG_diferenca_agilidade_limite = 8
CONFIG_chance_acerto_base = 50
CONFIG_dano_minimo = 1
CONFIG_fator_aleatorio_max = 1.2
CONFIG_fator_aleatorio_min = 0.8


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
    forca: float
    agilidade: float
    resistencia: float
    inteligencia: float
    sprite_x: int = Field(default=0)
    sprite_y: int = Field(default=0)
    sprite_nome: str = Field(default='sprites_01.png')
    sprite_largura: int = Field(default=320*3)
    sprite_altura: int = Field(default=320*3)
    estados: List[Estado] = Field(default=[])
    particulas_temporarias: Optional[List[Tuple[str, str, str]]] = Field(default_factory=lambda: [])

    def model_post_init(self, __context):
        if self.vida_maxima == 0:
            object.__setattr__(self, 'vida_maxima', self.vida)
        if self.energia_maxima == 0:
            object.__setattr__(self, 'energia_maxima', self.energia)

    @property
    def custo_habilidades(self) -> List[int]:
        custo_habilidade_i = min(self.energia_maxima, max(10, int(math.sqrt(self.inteligencia)*4)))
        custo_habilidade_ii = int(custo_habilidade_i*2)
        custo_habilidade_iii = int(custo_habilidade_ii*3)
        custo_habilidade_iv = int(custo_habilidade_iii*2)
        return [custo_habilidade_i, custo_habilidade_ii, custo_habilidade_iii, custo_habilidade_iv]

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

    @property
    def habilidades_sem_recarga(self):
        return any([e.nome == 'Habilidades Sem Recarga' for e in self.estados])

    @property
    def refletindo_dano(self):
        return any([e.nome == 'Refletindo Dano' for e in self.estados])

    def adicionar_particula_temporaria(self, texto: str, cor: str, sprite: str = None):
        self.particulas_temporarias.append(
            (texto, cor, sprite)
        )

    def aplicar_dano(self, quantidade: int):
        self.vida = int(max(0, self.vida - quantidade))

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

    def calcular_dano_magico(self, alvo: 'Entidade') -> int:
        """Calcula o dano causado por uma entidade em outra."""
        # Base do dano é a força do atacante
        dano_base = self.inteligencia

        # Fator de força: quanto maior a diferença, mais impacto tem
        diferenca_forca = self.inteligencia - alvo.resistencia
        fator_forca = 1 + (diferenca_forca / 20)  # Limita o impacto da diferença

        # Fator de resistência: reduz o dano baseado na resistência do alvo
        fator_resistencia = max(0.5, 1 - (alvo.resistencia / (self.inteligencia + 10)))

        # Adiciona um fator aleatório entre 0.8 e 1.2
        fator_aleatorio = random.uniform(
            CONFIG_fator_aleatorio_min,
            CONFIG_fator_aleatorio_max
        )

        # Cálculo final do dano
        dano = round(dano_base * fator_forca * fator_resistencia * fator_aleatorio)
        return max(CONFIG_dano_minimo, dano)

    def calcular_dano(self, alvo: 'Entidade') -> int:
        """Calcula o dano causado por uma entidade em outra."""
        # Base do dano é a força do atacante
        dano_base = self.forca

        # Fator de força: quanto maior a diferença, mais impacto tem
        diferenca_forca = self.forca - alvo.resistencia
        fator_forca = 1 + (diferenca_forca / 20)  # Limita o impacto da diferença

        # Fator de resistência: reduz o dano baseado na resistência do alvo
        fator_resistencia = max(0.5, 1 - (alvo.resistencia / (self.forca + 10)))

        # Adiciona um fator aleatório entre 0.8 e 1.2
        fator_aleatorio = random.uniform(
            CONFIG_fator_aleatorio_min,
            CONFIG_fator_aleatorio_max
        )

        # Cálculo final do dano
        dano = round(dano_base * fator_forca * fator_resistencia * fator_aleatorio)

        # Garante que o dano mínimo seja 1
        return max(CONFIG_dano_minimo, dano)

    def calcular_chance_acerto(self, alvo: 'Entidade') -> bool:
        """Calcula a chance de acerto de um ataque."""
        # Base de chance de acerto
        chance_base = CONFIG_chance_acerto_base

        if self.agilidade/10 > alvo.agilidade:
            return True

        # Calcula a diferença de agilidade
        diferenca_agilidade = math.floor((self.agilidade - alvo.agilidade)/1.5)

        # Se a diferença for menor que o limite, usa um fator menor
        if abs(diferenca_agilidade) <= CONFIG_diferenca_agilidade_limite:
            fator_agilidade = 1 + (diferenca_agilidade / 20)
        else:
            # Se a diferença for maior que o limite, usa um fator mais impactante
            fator_agilidade = 1 + (diferenca_agilidade / 10)

        # Ajusta a chance base pelo fator de agilidade
        chance_ajustada = chance_base * fator_agilidade

        # Adiciona um pequeno fator aleatório
        chance_final = chance_ajustada + random.uniform(-5, 5)

        # Garante que a chance fique entre 5% e 95%
        chance_final = max(5, min(95, chance_final))

        return random.randint(1, 100) <= chance_final
