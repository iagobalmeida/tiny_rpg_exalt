import math

from data.colors import (colorDamage, colorEnergy, colorHeal, colorIce,
                         colorMiss)
from data.estados import Congelamento, HabilidadesSemRecarga, RefletindoDano
from models.entidade import Entidade
from models.habilidades import Habilidade


class GolpeEspiritual(Habilidade):
    nome: str = 'GLP. SP.'
    descricao: str = 'Golpe Espiritual'
    nivel: int = 1

    def aplicar(self, de: Entidade, para: Entidade):
        dano = int((de.forca + de.agilidade + de.resistencia + de.inteligencia)/2)
        para.adicionar_particula_temporaria(str(dano), colorDamage, 'ataque_nulo.png')
        para.vida = max(0, para.vida - dano)


# ==============================
# 🛡 Caminho da Resistência
# ==============================
class EscudoTemporal(Habilidade):
    nome: str = "ESCD. TMP."
    descricao: str = "Escudo Temporal"
    nivel: int = 2

    def aplicar(self, de: Entidade, _):
        if getattr(de, 'bonus_atributos_classe', None):
            de.adicionar_particula_temporaria('+RES', colorEnergy, 'aumento_atributo.png')
            de.bonus_atributos_classe['resistencia'] += int(max(3, de.inteligencia/5))


class ReflexaoDeDano(Habilidade):
    nome: str = "RFLX. DANO"
    descricao: str = "Reflexão de Dano"
    nivel: int = 3

    def aplicar(self, de: Entidade, _):
        # TODO: Melhorar
        de.adicionar_particula_temporaria('Reflexão de Dano!', colorEnergy, 'aumento_atributo.png')
        de.adicionar_estado(RefletindoDano())


class Regeneracao(Habilidade):
    nome: str = "RNG."
    descricao: str = "Regeneração"
    nivel: int = 4

    def aplicar(self, de: Entidade, _):
        cura = int(((de.resistencia*4 + de.inteligencia)/5)/2)
        cura = int(max(10, cura))
        de.adicionar_particula_temporaria(str(cura), colorHeal, 'recuperacao_vida.png')
        de.vida = max(0, de.vida + cura)


# ==============================
# 🧠 Caminho da Inteligência
# ==============================
class BolaDeFogo(Habilidade):
    nome: str = 'BL. FG.'
    descricao: str = 'Bola de Fogo'
    nivel: int = 2

    def aplicar(self, de: Entidade, para: Entidade):
        dano = de.calcular_dano_magico(para) * 4
        para.adicionar_particula_temporaria(str(dano), colorDamage, 'habilidade_bola_de_fogo.png')
        para.vida = max(0, para.vida - dano)


class Congelar(Habilidade):
    nome: str = 'CNGLR.'
    descricao: str = 'Congelar'
    nivel: int = 3

    def aplicar(self, de: Entidade, para: Entidade):
        dano = de.calcular_dano_magico(para) * 8
        para.vida = max(0, para.vida - dano)
        para.adicionar_particula_temporaria(str(dano), colorIce, 'habilidade_congelar.png')
        para.adicionar_estado(Congelamento())


class VortexTemporal(Habilidade):
    nome: str = "VRTX. TMP."
    descricao: str = "Vortex Temporal"
    nivel: int = 4

    def aplicar(self, de: Entidade, para: Entidade):
        de.adicionar_particula_temporaria('Vortex Temporal!', colorEnergy, 'habilidade_vortex_temporal.png')
        para.adicionar_particula_temporaria('Vortex Temporal!', colorEnergy, 'habilidade_vortex_temporal.png')
        de.adicionar_estado(HabilidadesSemRecarga())


# ==============================
# 💪 Caminho da Força
# ==============================
class Furia(Habilidade):
    nome: str = 'FR.'
    descricao: str = 'Fúria'
    nivel: int = 2

    def aplicar(self, de: Entidade, _):
        de.adicionar_particula_temporaria('Fúria!', colorMiss, 'habilidade_furia.png')
        if getattr(de, 'bonus_atributos_classe', None):
            de.bonus_atributos_classe['agilidade'] += int(max(3, de.inteligencia/5))


class Execucao(Habilidade):
    nome: str = 'EXCC.'
    descricao: str = 'Execução'
    nivel: int = 3

    def aplicar(self, de: Entidade, para: Entidade):
        if para.vida <= para.vida/2:
            dano = para.vida
        else:
            dano = int(para.vida_maxima/3)
        para.adicionar_particula_temporaria(str(dano), colorDamage, 'habilidade_execucao.png')
        para.vida = int(max(0, para.vida - dano))


class GolpeDemolidor(Habilidade):
    nome: str = "GLP. DML."
    descricao: str = "Golpe Demolidor"
    nivel: int = 4

    def aplicar(self, de: Entidade, para: Entidade):
        # TODO: Melhorar
        dano = ((de.vida_maxima - de.vida) * de.forca)
        para.adicionar_particula_temporaria(str(dano), colorDamage, 'habilidade_execucao.png')
        para.vida = int(max(0, para.vida - dano))


# ==============================
# 🦅 Caminho da Agilidade
# ==============================o
class AtaqueRapido(Habilidade):
    nome: str = "ATK. RPD."
    descricao: str = "Ataque Rápido"
    nivel: int = 2

    def aplicar(self, de: Entidade, para: Entidade):
        quantidade_ataques = math.ceil((de.agilidade * 4) - (para.agilidade/4))
        for ataque in quantidade_ataques:
            dano = de.calcular_dano(para)
            para.adicionar_particula_temporaria(str(dano), colorDamage, 'ataque_lamina.png')
            para.vida = int(max(0, para.vida - dano))


class Esquiva(Habilidade):
    nome: str = "ESQ."
    descricao: str = "Esquiva"
    nivel: int = 3

    def aplicar(self, de: Entidade, _):
        if getattr(de, 'bonus_atributos_classe', None):
            de.adicionar_particula_temporaria('+AGI', colorEnergy, 'aumento_atributo.png')
            de.bonus_atributos_classe['agilidade'] += max(3, int((de.agilidade*4 + de.inteligencia)/10))


class GolpeFurtivo(Habilidade):
    nome: str = "GLP. FURT."
    descricao: str = "Golpe Furtivo"
    nivel: int = 4

    def aplicar(self, de: Entidade, para: Entidade):
        para_sem_resistencia = para.model_copy()
        para_sem_resistencia.resistencia = 0

        quantidade_ataques = math.ceil((de.agilidade * 6) - (para.agilidade/4))
        for ataque in quantidade_ataques:
            dano = de.calcular_dano(para_sem_resistencia)
            para.adicionar_particula_temporaria(str(dano), colorDamage, 'ataque_lamina.png')
            para.vida = int(max(0, para.vida - dano))
