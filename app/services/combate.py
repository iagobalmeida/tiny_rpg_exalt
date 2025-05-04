import math
import random
from typing import Union

from config import get_config
from data import estados, inimigos
from data.colors import colorDamage, colorEnergy, colorHeal, colorMiss
from models.inimigo import Inimigo
from models.jogador import Jogador

UNION_INIMIGO_JOGADOR = Union[Inimigo, Jogador]


class Combate:

    def __init__(self, jogador: Jogador, inimigo: Inimigo):
        self.config = get_config()
        self.jogador = jogador
        self.inimigo = inimigo
        self.acao_jogador = None
        self.acao_inimigo = None
        self.contagem_turno = 0

    async def executar_turno_jogador(self, atributos_equipamentos: dict = {}):
        jogador_equipado = self.jogador.com_atributos_bonus(atributos_equipamentos)
        if jogador_equipado.calcular_chance_acerto(self.inimigo):
            dano = jogador_equipado.calcular_dano(self.inimigo)
            self.inimigo.vida = max(0, self.inimigo.vida - dano)
            self.inimigo.adicionar_particula_temporaria(
                str(-dano) if dano >= 0 else 'Erro',
                colorDamage if dano >= 0 else colorMiss,
                'ataque_basico.png' if dano >= 0 else 'ataque_erro.png'
            )
        else:
            self.inimigo.adicionar_particula_temporaria('Errou!', '#333')

    async def executar_turno_inimigo(self, atributos_equipamentos: dict = {}):
        jogador_equipado = self.jogador.com_atributos_bonus(atributos_equipamentos)
        if self.inimigo.calcular_chance_acerto(jogador_equipado):
            dano = self.inimigo.calcular_dano(jogador_equipado)

            if self.jogador.refletindo_dano:
                self.inimigo.vida = max(0, self.inimigo.vida - dano)
                self.inimigo.adicionar_particula_temporaria(
                    str(-dano) if dano >= 0 else 'Erro',
                    colorDamage if dano >= 0 else colorMiss,
                    self.inimigo.sprite_particula if dano >= 0 else 'ataque_erro.png'
                )
            else:
                self.jogador.vida = max(0, self.jogador.vida - dano)
                self.jogador.adicionar_particula_temporaria(
                    str(-dano) if dano >= 0 else 'Erro',
                    colorDamage if dano >= 0 else colorMiss,
                    self.inimigo.sprite_particula if dano >= 0 else 'ataque_erro.png'
                )
        else:
            self.jogador.adicionar_particula_temporaria('Errou!', '#333')

    async def executar_acao_jogador(self, atributos_equipamentos) -> bool:
        self.jogador.recarga_habilidades = max(0, self.jogador.recarga_habilidades-1)
        if self.jogador.habilidades_sem_recarga:
            self.jogador.recarga_habilidades = 0

        if self.acao_jogador is None or self.jogador.recarga_habilidades > 0:
            return False

        for habilidade in self.jogador.classe.habilidades:
            if habilidade.descricao == self.acao_jogador:
                habilidade.executar(self.jogador, self.inimigo, atributos_equipamentos)
                if not self.jogador.habilidades_sem_recarga:
                    self.jogador.recarga_habilidades = 6

        print(f'{self.jogador.habilidades_sem_recarga} - {self.jogador.recarga_habilidades}')
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
        atributo_bonus = math.floor(random.random() * self.jogador.classe.nivel*1.5)

        if self.jogador.classe.nome in ['VAGABUNDO', 'LADINO', 'ASSASSINO', 'PREDADOR']:
            atributo_maximo = int(self.jogador.agilidade + self.jogador.level/8)
            self.jogador.bonus_atributos_classe['agilidade'] = min(atributo_maximo, self.jogador.bonus_atributos_classe['agilidade'] + atributo_bonus)

        elif self.jogador.classe.nome in ['SELVAGEM', 'BARBARO', 'BERSERKER', 'CAMPEAO']:
            atributo_maximo = int(self.jogador.forca + self.jogador.level/8)
            self.jogador.bonus_atributos_classe['forca'] = min(atributo_maximo, self.jogador.bonus_atributos_classe['forca'] + atributo_bonus)

        elif self.jogador.classe.nome in ['APRENDIZ', 'MAGO', 'FEITICEIRO', 'ARCANO']:
            atributo_maximo = int(self.jogador.inteligencia + self.jogador.level/8)
            self.jogador.bonus_atributos_classe['inteligencia'] = min(atributo_maximo, self.jogador.bonus_atributos_classe['inteligencia'] + atributo_bonus)

            energia = atributo_bonus * 2
            if energia > 0:
                self.jogador.adicionar_particula_temporaria(str(energia), colorEnergy, 'recuperacao_energia.png')
            self.jogador.energia = min(self.jogador.energia_maxima, self.jogador.energia + energia)

        elif self.jogador.classe.nome in ['INICIANTE', 'VIGIA', 'GUARDIAO', 'PALADINO']:
            atributo_maximo = int(self.jogador.resistencia + self.jogador.level/8)
            self.jogador.bonus_atributos_classe['resistencia'] = min(atributo_maximo, self.jogador.bonus_atributos_classe['resistencia'] + atributo_bonus)

            cura = atributo_bonus * 2
            if cura > 0:
                self.jogador.adicionar_particula_temporaria(str(cura), colorHeal, 'recuperacao_vida.png')
            self.jogador.vida = min(self.jogador.vida_maxima, self.jogador.vida + cura)

    async def executar_turno(self, atributos_equipamentos_jogador: dict = {}) -> Union[bool, str]:
        self.contagem_turno += 1

        self.jogador.executar_estados()
        self.inimigo.executar_estados()

        if self.inimigo.vida <= 0:
            return 'jogador'
        elif self.jogador.vida <= 0:
            return 'inimigo'

        await self.executar_acao_jogador(atributos_equipamentos_jogador)  # Jogador tem preferência mesmo congelado

        if self.inimigo.vida <= 0:
            return 'jogador'
        elif self.jogador.vida <= 0:
            return 'inimigo'

        await self.executar_passiva_jogador_classe()
        if not self.jogador.congelado:
            await self.executar_turno_jogador(atributos_equipamentos_jogador)

        if self.inimigo.vida <= 0:
            return 'jogador'
        elif self.jogador.vida <= 0:
            return 'inimigo'

        if not self.inimigo.congelado:
            await self.executar_turno_inimigo(atributos_equipamentos_jogador)
            await self.executar_acao_inimigo(atributos_equipamentos_jogador)

        if self.inimigo.vida <= 0:
            return 'jogador'
        elif self.jogador.vida <= 0:
            return 'inimigo'
        return False
