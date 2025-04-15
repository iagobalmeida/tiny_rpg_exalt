import math
import random
from datetime import datetime
from typing import Union

from config import get_config
from models.entidade import Entidade
from models.jogador import Classes, Jogador


class Combate:

    def __init__(self, jogador: Jogador, inimigo: Entidade):
        self.config = get_config()
        self.jogador = jogador
        self.inimigo = inimigo
        self.acao_jogador = None
        self.acao_inimigo = None
        self.contagem_turno = 0

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

    def jogador_com_atributos_bonus(self, atributos_equipamentos: dict = {}) -> Jogador:
        jogador = self.jogador.model_copy()
        jogador.forca += atributos_equipamentos.get('forca', 0)
        jogador.agilidade += atributos_equipamentos.get('agilidade', 0)
        jogador.resistencia += atributos_equipamentos.get('resistencia', 0)
        jogador.inteligencia += atributos_equipamentos.get('inteligencia', 0)

        jogador.forca += self.jogador.bonus_atributos_classe['forca']
        jogador.agilidade += self.jogador.bonus_atributos_classe['agilidade']
        jogador.resistencia += self.jogador.bonus_atributos_classe['resistencia']
        jogador.inteligencia += self.jogador.bonus_atributos_classe['inteligencia']
        return jogador

    async def executar_turno_jogador(self, atributos_equipamentos: dict = {}) -> bool:
        if self.jogador.vida <= 0:
            return True

        jogador_equipado = self.jogador_com_atributos_bonus(atributos_equipamentos)

        if self.calcular_chance_acerto(jogador_equipado, self.inimigo):
            dano = self.calcular_dano(jogador_equipado, self.inimigo)
            self.inimigo.vida = max(0, self.inimigo.vida - dano)

        return False

    async def executar_turno_inimigo(self, atributos_equipamentos: dict = {}) -> bool:
        if self.inimigo.vida <= 0:
            return True

        jogador_equipado = self.jogador_com_atributos_bonus(atributos_equipamentos)

        if self.calcular_chance_acerto(self.inimigo, jogador_equipado):
            dano = self.calcular_dano(self.inimigo, jogador_equipado)
            self.jogador.vida = max(0, self.jogador.vida - dano)

        return False

    async def executar_acao_jogador(self, atributos_equipamentos) -> bool:
        if self.acao_jogador is None:
            return False

        jogador_equipado = self.jogador_com_atributos_bonus(atributos_equipamentos)
        custo_habilidade_i = max(10, self.jogador.inteligencia*2)
        custo_habilidade_ii = int(custo_habilidade_i*1.5)
        custo_habilidade_iii = int(custo_habilidade_ii*3)

        if self.acao_jogador == 'golpe_espiritual' and self.jogador.energia >= 10:
            self.jogador.energia -= custo_habilidade_i
            dano = self.calcular_dano_magico(jogador_equipado, self.inimigo) * 2
            self.inimigo.vida = max(0, self.inimigo.vida - dano)

        # SELVAGEM & BÁRBARO
        if self.acao_jogador == 'Fúria' and self.jogador.classe in [Classes.SELVAGEM.value, Classes.BARBARO.value] and self.jogador.energia >= custo_habilidade_ii:
            self.jogador.energia -= custo_habilidade_ii
            self.jogador.bonus_atributos_classe['agilidade'] += max(3, self.jogador.inteligencia/20)

        if self.acao_jogador == 'Execução' and self.jogador.classe == Classes.BARBARO.value and self.jogador.energia >= custo_habilidade_iii:
            self.jogador.energia -= custo_habilidade_iii
            if self.inimigo.vida <= self.inimigo.vida_maxima/2:
                self.inimigo.vida = 0
            else:
                self.inimigo.vida = max(0, self.inimigo.vida - math.ceil(self.jogador.forca*10/self.inimigo.vida_maxima))

        # MAGO & FEITICEIRO
        if self.acao_jogador == 'Bola de Fogo' and self.jogador.classe in [Classes.MAGO.value, Classes.FEITICEIRO.value] and self.jogador.energia >= custo_habilidade_ii:
            self.jogador.energia -= custo_habilidade_ii
            dano = self.calcular_dano_magico(jogador_equipado, self.inimigo) * 3
            self.inimigo.vida = max(0, self.inimigo.vida - dano)

        if self.acao_jogador == 'Congelar' and self.jogador.classe == Classes.FEITICEIRO.value and self.jogador.energia >= custo_habilidade_iii:
            self.jogador.energia -= custo_habilidade_iii
            # TODO: Implementar status "congelado"

        # GUERREIRO & PALADINO
        if self.acao_jogador == 'Benção' and self.jogador.classe in [Classes.GUERREIRO.value, Classes.TEMPLARIO.value] and self.jogador.energia >= custo_habilidade_ii:
            self.jogador.energia -= custo_habilidade_ii
            self.jogador.vida += max(10, int(self.jogador.inteligencia/1.5))

        if self.acao_jogador == 'Redenção' and self.jogador.classe == Classes.TEMPLARIO.value and self.jogador.energia >= custo_habilidade_iii:
            self.jogador.energia = 0
            self.jogador.vida = self.jogador.vida_maxima
            self.jogador.bonus_atributos_classe['resistencia'] += max(3, int(self.jogador.nivel/3))

        self.acao_jogador = None

    async def executar_passiva_jogador_classe(self):
        if self.jogador.classe == Classes.SELVAGEM.value:
            self.jogador.bonus_atributos_classe['forca'] = self.contagem_turno * math.ceil(self.jogador.level/60)
        elif self.jogador.classe == Classes.BARBARO.value:
            self.jogador.bonus_atributos_classe['forca'] = self.contagem_turno * math.ceil(self.contagem_turno/30)
        elif self.jogador.classe == Classes.MAGO.value:
            self.jogador.energia += math.ceil(self.jogador.level/30)
        elif self.jogador.classe == Classes.FEITICEIRO.value:
            self.jogador.energia += math.ceil(self.jogador.level/15)
        elif self.jogador.classe == Classes.GUERREIRO.value:
            self.jogador.vida += math.ceil(self.jogador.level/15)
        elif self.jogador.classe == Classes.TEMPLARIO.value:
            self.jogador.vida += math.ceil(self.jogador.level/3)

    async def executar_turno(self, atributos_equipamentos_jogador: dict = {}) -> Union[bool, str]:
        self.contagem_turno += 1

        jogador_morreu = await self.executar_turno_jogador(atributos_equipamentos_jogador)
        if jogador_morreu:
            return 'inimigo'

        await self.executar_acao_jogador(atributos_equipamentos_jogador)
        await self.executar_passiva_jogador_classe()

        inimigo_morreu = await self.executar_turno_inimigo(atributos_equipamentos_jogador)
        if inimigo_morreu:
            return 'jogador'

        return False

    @staticmethod
    def hour() -> str:
        """Retorna a hora atual formatada."""
        return datetime.now().strftime('%H:%M:%S')
