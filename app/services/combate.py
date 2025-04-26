import math
import random
from typing import Union

from config import get_config
from data import estados, inimigos
from models.inimigo import Inimigo
from models.jogador import Classes, Jogador

UNION_INIMIGO_JOGADOR = Union[Inimigo, Jogador]


class Combate:

    def __init__(self, jogador: Jogador, inimigo: Inimigo):
        self.config = get_config()
        self.jogador = jogador
        self.inimigo = inimigo
        self.acao_jogador = None
        self.acao_inimigo = None
        self.contagem_turno = 0

    async def executar_turno_jogador(self, atributos_equipamentos: dict = {}) -> Union[bool, int]:
        jogador_equipado = self.jogador.com_atributos_bonus(atributos_equipamentos)
        if jogador_equipado.calcular_chance_acerto(self.inimigo):
            dano = jogador_equipado.calcular_dano(self.inimigo)
            self.inimigo.vida = max(0, self.inimigo.vida - dano)
            return dano
        return False

    async def executar_turno_inimigo(self, atributos_equipamentos: dict = {}) -> Union[bool, int]:
        jogador_equipado = self.jogador.com_atributos_bonus(atributos_equipamentos)
        if self.inimigo.calcular_chance_acerto(jogador_equipado):
            dano = self.inimigo.calcular_dano(jogador_equipado)
            self.jogador.vida = max(0, self.jogador.vida - dano)
            return dano
        return False

    async def executar_acao_jogador(self, atributos_equipamentos) -> bool:
        # TODO: Achar uma forma de lidar sempre com `float` com até 1 casa decimal, no jogo todo
        if self.acao_jogador is None:
            return False

        for habilidade in self.jogador.classe.habilidades:
            if habilidade.descricao == self.acao_jogador:
                habilidade.executar(self.jogador, self.inimigo, atributos_equipamentos)

        self.acao_jogador = None

    async def executar_acao_inimigo(self, atributos_equipamentos) -> bool:
        inimigos_causam_sangramento = [
            inimigos.rato_lanceiro.nome,
            inimigos.gnomo_espadachim.nome,
            inimigos.esqueleto_arqueiro.nome,
            inimigos.armadura_fantasma.nome,
            inimigos.sentenca_final.nome,
            inimigos.mensageiro_indesejado.nome,
            inimigos.dragao_violento.nome,
            inimigos.experimento_iv.nome,
            inimigos.serpente_infecciosa.nome,
            inimigos.peste_sangrenta.nome,
            inimigos.peste_sangrenta_gigante.nome,
            inimigos.nulo.nome
        ]

        if self.inimigo.nome in inimigos_causam_sangramento:
            jogador_equipado = self.jogador.com_atributos_bonus(atributos_equipamentos)

            chance_adicional = random.random() > 0.5
            if self.inimigo.calcular_chance_acerto(jogador_equipado) and chance_adicional:
                self.jogador.adicionar_estado(estados.Sangramento())

    async def executar_passiva_jogador_classe(self):
        if self.jogador.classe == Classes.SELVAGEM.value:
            self.jogador.bonus_atributos_classe['forca'] = int(self.contagem_turno * math.ceil(self.jogador.level/64))
        elif self.jogador.classe == Classes.BARBARO.value:
            self.jogador.bonus_atributos_classe['forca'] = int(self.contagem_turno * math.ceil(self.contagem_turno/24))
        elif self.jogador.classe == Classes.MAGO.value:
            self.jogador.energia = int(min(self.jogador.energia_maxima, self.jogador.energia + math.ceil(self.jogador.level*self.jogador.inteligencia/144)))
        elif self.jogador.classe == Classes.FEITICEIRO.value:
            self.jogador.energia = int(min(self.jogador.energia_maxima, self.jogador.energia + math.ceil(self.jogador.level*self.jogador.inteligencia/36)))
        elif self.jogador.classe == Classes.GUERREIRO.value:
            self.jogador.vida = int(min(self.jogador.vida_maxima, self.jogador.vida + math.ceil(self.jogador.level/24)))
        elif self.jogador.classe == Classes.TEMPLARIO.value:
            self.jogador.vida = int(min(self.jogador.vida_maxima, self.jogador.vida + math.ceil(self.jogador.level/4)))

    async def executar_turno(self, atributos_equipamentos_jogador: dict = {}) -> Union[bool, str]:
        self.contagem_turno += 1
        self.jogador.particula_temporaria = ''
        self.inimigo.particula_temporaria = ''
        jogador_dano_causado = None
        inimigo_dano_causado = False

        await self.executar_passiva_jogador_classe()
        if not self.jogador.congelado:
            jogador_dano_causado = await self.executar_turno_jogador(atributos_equipamentos_jogador)
        await self.executar_acao_jogador(atributos_equipamentos_jogador)  # Jogador tem preferência mesmo congelado
        self.jogador.executar_estados()

        if not self.inimigo.congelado:
            inimigo_dano_causado = await self.executar_turno_inimigo(atributos_equipamentos_jogador)
            await self.executar_acao_inimigo(atributos_equipamentos_jogador)
        self.inimigo.executar_estados()

        if self.jogador.particula_temporaria == '' and inimigo_dano_causado == 0:
            self.jogador.particula_temporaria = 'ataque_erro.png'

        if self.inimigo.particula_temporaria == '' and jogador_dano_causado == 0:
            self.inimigo.particula_temporaria = 'ataque_erro.png'

        if self.inimigo.vida <= 0:
            return 'jogador'
        elif self.jogador.vida <= 0:
            return 'inimigo'
        return False
