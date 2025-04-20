import math

from models.inimigo import Inimigo

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
        'vida_maxima': int(BASE_VIDA + ((FATOR_VIDA + atributos_principais.get('vida', 0))*level ^ 3)),
        'energia': int(BASE_VIDA + ((FATOR_VIDA + atributos_principais.get('energia', 0))*level ^ 3)),
        'energia_maxima': int(BASE_VIDA + ((FATOR_VIDA + atributos_principais.get('energia', 0))*level ^ 3)),
        'experiencia': int(BASE_EXP + ((FATOR_EXP + atributos_principais.get('experiencia', 0))*level ^ 2)),
        'ouro': int(BASE_OURO + ((FATOR_OURO + atributos_principais.get('ouro', 0))*level)),
        'level': math.ceil(level),
    }


def gerar_inimigo(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int, atributos_principais: dict = {}, sprite_particula: str = 'particulas/ataque_arranhao.webp'):
    return Inimigo(
        nome=nome,
        descricao=descricao,
        sprite_nome="monsters.webp",
        sprite_altura=416*3,
        sprite_largura=384*3,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        sprite_particula=sprite_particula,
        **inimigo_attrs(level, atributos_principais)
    )


def gerar_inimigo_rapido(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int, sprite_particula: str = None):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'agilidade': math.ceil(level/20)
    }, sprite_particula=sprite_particula)


def gerar_inimigo_bruto(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int, sprite_particula: str = None):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'forca':  math.ceil(level/20)
    }, sprite_particula=sprite_particula)


def gerar_inimigo_resistente(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int, sprite_particula: str = None):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'resistencia':  math.ceil(level/20)
    }, sprite_particula=sprite_particula)


def gerar_inimigo_mago(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int, sprite_particula: str = None):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'inteligencia':  math.ceil(level/20)
    }, sprite_particula=sprite_particula)


def gerar_inimigo_chefe(nome: str, descricao: str, sprite_x: int, sprite_y: int, level: int, sprite_particula: str = None):
    return gerar_inimigo(nome, descricao, sprite_x, sprite_y, level, {
        'forca':  math.ceil(level/20),
        'resistencia':  math.ceil(level/20),
        'vida':  math.ceil(level/20) * 2
    }, sprite_particula=sprite_particula)


# Esgoto
rato = gerar_inimigo_rapido('Rato', '"Skweek skweek"', 11, 6, 0, sprite_particula='particulas/ataque_arranhao.webp')
ratazana = gerar_inimigo('Ratazana', '"Skeeek"', 10, 6, 1, sprite_particula='particulas/ataque_arranhao.webp')
rato_lanceiro = gerar_inimigo('Rato Lanceiro', '"Você não é bem-vindo!"', 0, 9, 2, sprite_particula='particulas/ataque_pontudo.webp')
rato_guerreiro = gerar_inimigo_resistente('Rato Guerreiro', '"Daqui você não passa"', 1, 9, 2, sprite_particula='particulas/ataque_pontudo.webp')

# Floresta
gnomo = gerar_inimigo_rapido('Gnomo', '"Humano fedorento!"', 2, 0, 4, sprite_particula='particulas/ataque_pontudo.webp')
gnomo_guerreiro = gerar_inimigo('Gnomo Guerreiro', '"Ossos grandes, humano!"', 5, 0, 5, sprite_particula='particulas/ataque_pontudo.webp')
gnomo_mago = gerar_inimigo_mago('Gnomo Mago', '"Sinta o gosto do fogo!"', 6, 0, 6, sprite_particula='particulas/ataque_pontudo.webp')
gnomo_espadachim = gerar_inimigo_bruto('Gnomo Espadachim', '"Sua cabeça será minha!"', 3, 0, 6, sprite_particula='particulas/ataque_lamina.webp')
gnomo_bruto = gerar_inimigo_bruto('Gnomo Bruto', '"Mim matar humano!"', 0, 0, 6, sprite_particula='particulas/ataque_pesado.webp')
gnomo_anciao = gerar_inimigo_chefe('Gnomo Ancião', '"Humano fedorento!"', 1, 0, 8, sprite_particula='particulas/ataque_magico.webp')

# Mata Fechada
golem_de_pedra = gerar_inimigo_resistente('Golem de Pedra', '"..."', 2, 7, 10, sprite_particula='particulas/ataque_pesado.webp')
entedidade_florestal = gerar_inimigo('Entidade Florestal', '"Sua energia é estranha..."', 0, 7, 11, sprite_particula='particulas/ataque_magico.webp')
entidade_animal = gerar_inimigo('Entidade Animal', '"Você não faz parte do meu reino!"', 1, 7, 11, sprite_particula='particulas/ataque_magico.webp')
entidade_obscura = gerar_inimigo_chefe('Entidade Obscura', '"A escuridão..."', 5, 7, 11, sprite_particula='particulas/ataque_magico.webp')

# Castelo Abandonado
esqueleto = gerar_inimigo('Esqueleto', '"cLiCk"', 0, 4, 12, sprite_particula='particulas/ataque_pontudo.webp')
esqueleto_arqueiro = gerar_inimigo_rapido('Esqueleto Arqueiro', '"cLaCk cLiCk"', 1, 4, 12, sprite_particula='particulas/ataque_lamina.webp')
esqueleto_mago = gerar_inimigo_mago('Esqueleto Mago', '"cLiCk cLaCk BoOm"', 2, 4, 12, sprite_particula='particulas/ataque_magico.webp')
armadura_fantasma = gerar_inimigo_resistente('Armadura Fantasma', '"..."', 3, 4, 13, sprite_particula='particulas/ataque_magico.webp')
zumbi = gerar_inimigo('Zumbi', '"Ghurr..."', 4, 4, 13, sprite_particula='particulas/ataque_arranhao.webp')
morto_vivo = gerar_inimigo_chefe('Morto Vivo', '"GHAAA!"', 5, 4, 15, sprite_particula='particulas/ataque_arranhao.webp')

# Cemitério
# TODO - Mais particulas!
alma_penada = gerar_inimigo('Alma Penada', '"Eu...não lembro..."', 0, 5, 16, sprite_particula='particulas/ataque_magico.webp')
sentenca_final = gerar_inimigo_rapido('Sentença Final', '"Sua hora chegou!"', 1, 5, 16, sprite_particula='particulas/ataque_magico.webp')
mensageiro_indesejado = gerar_inimigo_mago('Mensageiro Indesejado', '"Venha comigo..."', 2, 5, 17, sprite_particula='particulas/ataque_magico.webp')
guia_dos_mortos = gerar_inimigo_mago('Guia dos Mortos', '"A luz, a luz!"', 3, 5, 17, sprite_particula='particulas/ataque_magico.webp')
protetora_das_catacumbas = gerar_inimigo_chefe('Protetora das Catacumbas', '"Você desequilibrou tudo!"', 4, 5, 19, sprite_particula='particulas/ataque_magico.webp')

# Catacumbas
bispo_corrompido = gerar_inimigo_mago('Bispo Corrompido', '"Vou te guiar até o submundo."', 0, 3, 21, sprite_particula='particulas/ataque_magico.webp')
sacerdote_renegado = gerar_inimigo_chefe('Sacerdote Renegado', '"A verdade é sangrenta..."', 1, 3, 21, sprite_particula='particulas/ataque_magico.webp')

# Calabouco
filhote_de_dragao = gerar_inimigo_rapido('Filhote de Dragão', '"Vou contar pra minha mãe!"', 3, 8, 22, sprite_particula='particulas/ataque_fogo.webp')
dragao_jovem = gerar_inimigo('Dragão Jovem', '"Carne humana, finalmente..."', 4, 8, 22, sprite_particula='particulas/ataque_fogo.webp')
dragao_violento = gerar_inimigo_bruto('Dragão Violento', '"Me passa tudo!"', 0, 8, 23, sprite_particula='particulas/ataque_pontudo.webp')
dragao_adulto = gerar_inimigo_resistente('Dragão Adulto', '"Esse tesouro não te percente!"', 1, 8, 23, sprite_particula='particulas/ataque_fogo.webp')
dragao_anciao = gerar_inimigo_chefe('Dragão Ancião', '"Um oponente digno, talvez?"', 2, 8, 25, sprite_particula='particulas/ataque_fogo.webp')

# Laboratório Secreto
experimento_i = gerar_inimigo('Experimento I', '"Una-se a nós..."', 0, 12, 27, sprite_particula='particulas/ataque_magico.webp')
experimento_ii = gerar_inimigo_resistente('Experimento II', '"Una-se a mim..."', 1, 12, 27, sprite_particula='particulas/ataque_magico.webp')
experimento_iv = gerar_inimigo_chefe('Experimento IV', '"Humano, deixe-me te ajudar!"', 2, 12, 27, sprite_particula='particulas/ataque_magico.webp')

# Submundo
serpente_infecciosa = gerar_inimigo_rapido('Serpente Infecciosa', '"Skssss!"', 0, 6, 29, sprite_particula='particulas/ataque_arranhao.webp')
peste_sangrenta = gerar_inimigo('Peste Sangrenta', '"..."', 1, 6, 29, sprite_particula='particulas/ataque_arranhao.webp')
peste_sangrenta_gigante = gerar_inimigo_resistente('Peste Sangrenta Gigante', '"..."', 2, 6, 31, sprite_particula='particulas/ataque_arranhao.webp')
amon = gerar_inimigo('Amon', '"Tão inocente..."', 3, 6, 31, sprite_particula='particulas/ataque_fogo.webp')
astaroth = gerar_inimigo_rapido('Astaroth', '"O sofrimento te chama!"', 4, 6, 33, sprite_particula='particulas/ataque_fogo.webp')
barbathos = gerar_inimigo_chefe('Barbathos', '"Sua dor, meu prazer!"', 1, 11, 35, sprite_particula='particulas/ataque_fogo.webp')

# Nulo
nulo = gerar_inimigo_chefe('Nulo', '"Volte..."', 0, 11, 50, sprite_particula='particulas/ataque_nulo.webp')
