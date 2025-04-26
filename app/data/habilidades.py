from enum import Enum

from data.estados import Congelamento
from models.entidade import Entidade
from models.habilidades import Habilidade


class GolpeEspiritual(Habilidade):
    nome: str = 'GLP. SP.'
    descricao: str = 'Golpe Espiritual'
    nivel: int = 1

    def aplicar(self, de: Entidade, para: Entidade):
        dano = de.calcular_dano_magico(para) * 2
        para.adicionar_particula_temporaria(str(dano), '#ff0000', 'ataque_nulo.png')
        para.vida = max(0, para.vida - dano)


# Selvagem & Bárbaro
class Furia(Habilidade):
    nome: str = 'FR.'
    descricao: str = 'Fúria'
    nivel: int = 2

    def aplicar(self, de: Entidade, _):
        de.adicionar_particula_temporaria('Fúria!', '#ffffff', 'habilidade_furia.png')
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
        para.adicionar_particula_temporaria(str(dano), '#ff0000', 'habilidade_execucao.png')
        para.vida = int(max(0, para.vida - dano))


# Mago & Feiticeiro
class BolaDeFogo(Habilidade):
    nome: str = 'BL. FG.'
    descricao: str = 'Bola de Fogo'
    nivel: int = 2

    def aplicar(self, de: Entidade, para: Entidade):
        dano = de.calcular_dano_magico(para) * 4
        para.adicionar_particula_temporaria(str(dano), '#ff0000', 'habilidade_bola_de_fogo.png')
        para.vida = max(0, para.vida - dano)


class Congelar(Habilidade):
    nome: str = 'CNGLR.'
    descricao: str = 'Congelar'
    nivel: int = 3

    def aplicar(self, de: Entidade, para: Entidade):
        para.vida = max(0, para.vida - dano)
        para.adicionar_particula_temporaria(str(dano), '#00aaff', 'habilidade_congelar.png')
        dano = de.calcular_dano_magico(para) * 8
        para.adicionar_estado(Congelamento())


# Guerreiro & Templário
class Bencao(Habilidade):
    nome: str = 'BNC.'
    descricao: str = 'Benção'
    nivel: int = 2

    def aplicar(self, de: Entidade, _):
        cura = int(de.inteligencia/1.5)
        de.vida += max(10, cura)
        de.adicionar_particula_temporaria(str(cura), '#00ff00', 'habilidade_cura.png')


class Redencao(Habilidade):
    nome: str = 'RDNC.'
    descricao: str = 'Redenção'
    nivel: int = 3

    def aplicar(self, de: Entidade, _):
        de.vida = de.vida_maxima
        cura = de.vida_maxima - de.vida
        de.adicionar_particula_temporaria(str(cura), '#00ff00', 'habilidade_cura.png')
        if getattr(de, 'bonus_atributos_classe', None):
            de.bonus_atributos_classe['resistencia'] += int(max(3, de.inteligencia/5))
