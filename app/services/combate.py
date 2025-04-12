from typing import List, Tuple
import random
from datetime import datetime

from app.config import get_config
from app.models.entidade import Entidade

class Combate:
    def __init__(self, jogador: Entidade, inimigo: Entidade):
        self.config = get_config()
        self.jogador = jogador
        self.inimigo = inimigo
        self.acao_jogador = None
        self.acao_inimigo = None

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

    async def executar_turno_jogador(self, logs: List[str]) -> Tuple[bool, List[str]]:
        """Executa o turno do jogador."""
        if self.jogador.vida <= 0:
            logs.append(f'{self.hour()} - {self.jogador.nome} morreu')
            return True, logs

        if self.calcular_chance_acerto(self.jogador, self.inimigo):
            dano = self.calcular_dano(self.jogador, self.inimigo)
            self.inimigo.vida -= dano
            logs.append(f'{self.hour()} - {self.jogador.nome} causou {dano} de dano em {self.inimigo.nome}')
        else:
            logs.append(f'{self.hour()} - {self.jogador.nome} errou o ataque')

        if self.inimigo.vida <= 0:
            logs.append(f'{self.hour()} - {self.inimigo.nome} morreu')
            return True, logs

        return False, logs

    async def executar_turno_inimigo(self, logs: List[str]) -> Tuple[bool, List[str]]:
        """Executa o turno do inimigo."""
        if self.inimigo.vida <= 0:
            return True, logs

        if self.calcular_chance_acerto(self.inimigo, self.jogador):
            dano = self.calcular_dano(self.inimigo, self.jogador)
            self.jogador.vida -= dano
            logs.append(f'{self.hour()} - {self.inimigo.nome} causou {dano} de dano em {self.jogador.nome}')
        else:
            logs.append(f'{self.hour()} - {self.inimigo.nome} errou o ataque')

        if self.jogador.vida <= 0:
            logs.append(f'{self.hour()} - {self.jogador.nome} morreu')
            return True, logs

        return False, logs

    async def executar_turno(self) -> Tuple[bool, List[str]]:
        """Executa um turno completo de combate."""
        logs = []
        combate_acabou = False

        # Turno do jogador
        if self.acao_jogador == "ataque":
            combate_acabou, logs = await self.executar_turno_jogador(logs)
            self.acao_jogador = None

        # Turno do inimigo
        if not combate_acabou:
            combate_acabou, logs = await self.executar_turno_inimigo(logs)

        return combate_acabou, logs

    @staticmethod
    def hour() -> str:
        """Retorna a hora atual formatada."""
        return datetime.now().strftime('%H:%M:%S') 