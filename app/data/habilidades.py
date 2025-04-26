from enum import Enum

from data.estados import Congelamento
from models.entidade import Entidade
from models.habilidades import Habilidade


class GolpeEspiritual(Habilidade):
    nome: str = 'GLP. SP.'
    descricao: str = 'Golpe Espiritual'
    nivel: int = 1

    def aplicar(self, de: Entidade, para: Entidade):
        para.particula_temporaria = 'ataque_nulo.png'
        dano = de.calcular_dano_magico(para) * 2
        para.vida = max(0, para.vida - dano)


# Selvagem & Bárbaro
class Furia(Habilidade):
    nome: str = 'FR.'
    descricao: str = 'Fúria'
    nivel: int = 2

    def aplicar(self, de: Entidade, _):
        de.particula_temporaria = 'habilidade_furia.png'
        if getattr(de, 'bonus_atributos_classe', None):
            de.bonus_atributos_classe['agilidade'] += int(max(3, de.inteligencia/5))


class Execucao(Habilidade):
    nome: str = 'EXCC.'
    descricao: str = 'Execução'
    nivel: int = 3

    def aplicar(self, de: Entidade, para: Entidade):
        para.particula_temporaria = 'habilidade_execucao.png'
        if para.vida <= para.vida/2:
            para.vida = 0
        else:
            para.vida = int(max(0, para.vida - para.vida_maxima/3))


# Mago & Feiticeiro
class BolaDeFogo(Habilidade):
    nome: str = 'BL. FG.'
    descricao: str = 'Bola de Fogo'
    nivel: int = 2

    def aplicar(self, de: Entidade, para: Entidade):
        para.particula_temporaria = 'habilidade_bola_de_fogo.png'
        dano = de.calcular_dano_magico(para) * 4
        para.vida = max(0, para.vida - dano)


class Congelar(Habilidade):
    nome: str = 'CNGLR.'
    descricao: str = 'Congelar'
    nivel: int = 3

    def aplicar(self, de: Entidade, para: Entidade):
        para.particula_temporaria = 'habilidade_congelar.png'
        dano = de.calcular_dano_magico(para) * 8
        para.vida = max(0, para.vida - dano)
        para.adicionar_estado(Congelamento())


# Guerreiro & Templário
class Bencao(Habilidade):
    nome: str = 'BNC.'
    descricao: str = 'Benção'
    nivel: int = 2

    def aplicar(self, de: Entidade, _):
        de.particula_temporaria = 'habilidade_cura.png'
        de.vida += max(10, int(de.inteligencia/1.5))


class Redencao(Habilidade):
    nome: str = 'RDNC.'
    descricao: str = 'Redenção'
    nivel: int = 3

    def aplicar(self, de: Entidade, _):
        de.vida = de.vida_maxima
        de.particula_temporaria = 'habilidade_cura.png'
        if getattr(de, 'bonus_atributos_classe', None):
            de.bonus_atributos_classe['resistencia'] += int(max(3, de.inteligencia/5))
