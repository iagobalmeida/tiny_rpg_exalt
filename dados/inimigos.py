import math

from dados.tipos import Inimigo

BASE_EXP = 5
FATOR_EXP = 6

BASE_VIDA = 10
FATOR_VIDA = 22

BASE_ATTR = 1
FATOR_ATTR = 3

BASE_OURO = 1
FATOR_OURO = 4


def inimigo_attrs(level: int, atributos_principais: dict):
    return {
        'forca': int(BASE_ATTR + ((FATOR_ATTR + atributos_principais.get('forca', 0))*level)),
        'agilidade': int(BASE_ATTR + ((FATOR_ATTR + atributos_principais.get('agilidade', 0))*level)),
        'resistencia': int(BASE_ATTR + ((FATOR_ATTR + atributos_principais.get('resistencia', 0))*level)),
        'inteligencia': int(BASE_ATTR + ((FATOR_ATTR + atributos_principais.get('inteligencia', 0))*level)),
        'vida': int(BASE_VIDA + ((FATOR_VIDA + atributos_principais.get('vida', 0))*level ^ 3)),
        'energia': int(BASE_VIDA + ((FATOR_VIDA + atributos_principais.get('energia', 0))*level ^ 3)),
        'experiencia': int(BASE_EXP + ((FATOR_EXP + atributos_principais.get('experiencia', 0))*level ^ 2)),
        'ouro': int(BASE_OURO + ((FATOR_OURO + atributos_principais.get('ouro', 0))*level)),
        'level': math.ceil(level),
    }


def gerar_inimigo(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int, atributos_principais: dict = {}):
    return Inimigo(
        nome=nome,
        descricao=descricao,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        **inimigo_attrs(level, atributos_principais)
    )

def gerar_inimigo_rapido(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'agilidade': math.ceil(level/20)
    })

def gerar_inimigo_bruto(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'forca':  math.ceil(level/20)
    })

def gerar_inimigo_resistente(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'resistencia':  math.ceil(level/20)
    })

def gerar_inimigo_mago(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'inteligencia':  math.ceil(level/20)
    })

def gerar_inimigo_chefe(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'forca':  math.ceil(level/20),
        'resistencia':  math.ceil(level/20),
        'vida':  math.ceil(level/20) * 2
    })

# Esgoto
rato = gerar_inimigo_rapido('Rato', '"Skweek skweek"', 11, 6, 0)
ratazana = gerar_inimigo('Ratazana', '"Skeeek"', 10, 6, 1)
rato_lanceiro = gerar_inimigo('Rato Lanceiro', '"Você não é bem-vindo!"', 0, 9, 2)
rato_guerreiro = gerar_inimigo_resistente('Rato Guerreiro', '"Daqui você não passa"', 1, 9, 2)

# Floresta
gnomo = gerar_inimigo_rapido('Gnomo', '"Humano fedorento!"', 2, 0, 4)
gnomo_guerreiro = gerar_inimigo('Gnomo Guerreiro', '"Ossos grandes, humano!"', 5, 0, 5)
gnomo_mago = gerar_inimigo_mago('Gnomo Mago', '"Sinta o gosto do fogo!"', 6, 0, 6)
gnomo_espadachim = gerar_inimigo_bruto('Gnomo Espadachim', '"Sua cabeça será minha!"', 3, 0, 6)
gnomo_bruto = gerar_inimigo_bruto('Gnomo Bruto', '"Mim matar humano!"', 0, 0, 6)
gnomo_anciao = gerar_inimigo_chefe('Gnomo Ancião', '"Humano fedorento!"', 1, 0, 8)

# Mata Fechada
golem_de_pedra = gerar_inimigo_resistente('Golem de Pedra', '"..."', 2, 7, 10)
entedidade_florestal = gerar_inimigo('Entidade Florestal', '"Sua energia é estranha..."', 0, 7, 11)
entidade_animal = gerar_inimigo('Entidade Animal', '"Você não faz parte do meu reino!"', 1, 7, 11)
entidade_obscura = gerar_inimigo_chefe('Entidade Obscura', '"A escuridão..."', 5, 7, 11)

# Castelo Abandonado
esqueleto = gerar_inimigo('Esqueleto', '"..."', 0, 4, 12)
esqueleto_arqueiro = gerar_inimigo_rapido('Esqueleto Arqueiro', '"..."', 1, 4, 12)
esqueleto_mago = gerar_inimigo_mago('Esqueleto Mago', '"..."', 2, 4, 12)
armadura_fantasma = gerar_inimigo_resistente('Armadura Fantasma', '"..."', 3, 4, 13)
zumbi = gerar_inimigo('Zumbi', '"..."', 4, 4, 13)
morto_vivo = gerar_inimigo_chefe('Morto Vivo', '"..."', 5, 4, 15)

# Cemitério
alma_penada = gerar_inimigo('Alma Penada', '"..."', 0, 5, 16)
sentenca_final = gerar_inimigo_rapido('Sentença Final', '"..."', 1, 5, 16)
mensageiro_indesejado = gerar_inimigo_mago('Mensageiro Indesejado', '"..."', 2, 5, 17)
guia_dos_mortos = gerar_inimigo_mago('Guia dos Mortos', '"..."', 3, 5, 17)
protetora_das_catacumbas = gerar_inimigo_chefe('Protetora das Catacumbas', '"..."', 4, 5, 19)

# Catacumbas
bispo_corrompido = gerar_inimigo_mago('Bispo Corrompido', '"..."', 0, 3, 21)
sacerdote_renegado = gerar_inimigo_chefe('Sacerdote Renegado', '"..."', 1, 3, 21)

# Calabouco
filhote_de_dragao = gerar_inimigo_rapido('Filhote de Dragão', '"..."', 3, 8, 22)
dragao_jovem = gerar_inimigo('Dragão Jovem', '"..."', 4, 8, 22)
dragao_violento = gerar_inimigo_bruto('Dragão Violento', '"..."', 0, 8, 23)
dragao_adulto = gerar_inimigo_resistente('Dragão Adulto', '"..."', 1, 8, 23)
dragao_anciao = gerar_inimigo_chefe('Dragão Ancião', '"..."', 2, 8, 25)

# Laboratório Secreto
experimento_inicial = gerar_inimigo('Experimento Inicial', '"..."', 0, 12, 27)
experimento_intermediario = gerar_inimigo_resistente('Experimento Intermediário', '"..."', 1, 12, 27)
experimento_final = gerar_inimigo_chefe('Experimento Final', '"..."', 2, 12, 27)

# Submundo
serpente_infecciosa = gerar_inimigo_rapido('Serpente Infecciosa', '"..."', 0, 6, 29)
peste_sangrenta = gerar_inimigo('Peste Sangrenta', '"..."', 1, 6, 29)
peste_sangrenta_gigante = gerar_inimigo_resistente('Peste Sangrenta Gigante', '"..."', 2, 6, 31)
cerberus = gerar_inimigo('Cerberus', '"..."', 3, 6, 31)
cao_do_inferno = gerar_inimigo_rapido('Cão do Inferno', '"..."', 4, 6, 33)
o_inominavel = gerar_inimigo_chefe('O Inominável', '"..."', 1, 11, 35)

# Nulo
nulo = gerar_inimigo_chefe('Nulo', '"..."', 0, 11, 50)
