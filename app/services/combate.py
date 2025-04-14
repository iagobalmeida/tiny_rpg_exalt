import random
from datetime import datetime
from typing import List, Tuple, Union

from config import get_config
from models.entidade import Entidade
from models.jogador import Jogador


class Combate:

    def __init__(self, jogador: Jogador, inimigo: Entidade):
        self.config = get_config()
        self.jogador = jogador
        self.inimigo = inimigo
        self.acao_jogador = None
        self.acao_inimigo = None

    def calcular_dano_magico(self, de: Entidade, para: Entidade) -> int:
        """Calcula o dano causado por uma entidade em outra."""
        # Base do dano é a força do atacante
        dano_base = de.inteligencia

        # Fator de força: quanto maior a diferença, mais impacto tem
        diferenca_forca = de.inteligencia - para.resistencia
        fator_forca = 1 + (diferenca_forca / 20)  # Limita o impacto da diferença

        # Fator de resistência: reduz o dano baseado na resistência do alvo
        fator_resistencia = max(0.5, 1 - (para.resistencia / (de.inteligencia + 10)))

        # Adiciona um fator aleatório entre 0.8 e 1.2
        fator_aleatorio = random.uniform(
            self.config["game"]["fator_aleatorio_min"],
            self.config["game"]["fator_aleatorio_max"]
        )

        # Cálculo final do dano
        dano = round(dano_base * fator_forca * fator_resistencia * fator_aleatorio)
        return max(self.config["game"]["dano_minimo"], dano)

    def calcular_dano(self, de: Entidade, para: Entidade) -> int:
        """Calcula o dano causado por uma entidade em outra."""
        # Base do dano é a força do atacante
        dano_base = de.forca

        # Fator de força: quanto maior a diferença, mais impacto tem
        diferenca_forca = de.forca - para.resistencia
        fator_forca = 1 + (diferenca_forca / 20)  # Limita o impacto da diferença

        # Fator de resistência: reduz o dano baseado na resistência do alvo
        fator_resistencia = max(0.5, 1 - (para.resistencia / (de.forca + 10)))

        # Adiciona um fator aleatório entre 0.8 e 1.2
        fator_aleatorio = random.uniform(
            self.config["game"]["fator_aleatorio_min"],
            self.config["game"]["fator_aleatorio_max"]
        )

        # Cálculo final do dano
        dano = round(dano_base * fator_forca * fator_resistencia * fator_aleatorio)

        # Garante que o dano mínimo seja 1
        return max(self.config["game"]["dano_minimo"], dano)

    def calcular_chance_acerto(self, de: Entidade, para: Entidade) -> bool:
        """Calcula a chance de acerto de um ataque."""
        # Base de chance de acerto
        chance_base = self.config["game"]["chance_acerto_base"]

        # Calcula a diferença de agilidade
        diferenca_agilidade = de.agilidade - para.agilidade

        # Se a diferença for menor que o limite, usa um fator menor
        if abs(diferenca_agilidade) <= self.config["game"]["diferenca_agilidade_limite"]:
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

    async def executar_turno_jogador(self) -> Tuple[bool, List[str]]:
        if self.jogador.vida <= 0:
            return True

        if self.calcular_chance_acerto(self.jogador, self.inimigo):
            dano = self.calcular_dano(self.jogador, self.inimigo)
            self.inimigo.vida = max(0, self.inimigo.vida - dano)

        return False

    async def executar_turno_inimigo(self) -> Tuple[bool, List[str]]:
        if self.inimigo.vida <= 0:
            return True

        if self.calcular_chance_acerto(self.inimigo, self.jogador):
            dano = self.calcular_dano(self.inimigo, self.jogador)
            self.jogador.vida = max(0, self.jogador.vida - dano)

        return False

    async def executar_acao_jogador(self) -> Tuple[bool, List[str]]:
        if self.acao_jogador is None:
            return False

        if self.acao_jogador == 'golpe_espiritual' and self.jogador.energia >= 10:
            self.jogador.energia -= 10
            dano = self.calcular_dano_magico(self.jogador, self.inimigo) * 2
            self.inimigo.vida = max(0, self.inimigo.vida - dano)


        self.acao_jogador = None

        return True

    async def executar_turno(self) -> Union[bool, str]:

        jogador_morreu = await self.executar_turno_jogador()
        if jogador_morreu:
            return 'inimigo'

        await self.executar_acao_jogador()

        inimigo_morreu = await self.executar_turno_inimigo()
        if inimigo_morreu:
            return 'jogador'

        return False

    @staticmethod
    def hour() -> str:
        """Retorna a hora atual formatada."""
        return datetime.now().strftime('%H:%M:%S')
