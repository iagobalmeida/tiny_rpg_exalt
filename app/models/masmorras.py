from app.models.masmorra import Masmorra
from app.models.inimigos import (
    rato, ratazana, rato_lanceiro, rato_guerreiro,
    lobo, urso, tigre, dragão,
    esqueleto, zumbi, vampiro, lich,
    goblin, orc, troll, ogro,
    slime, slime_venenoso, slime_elétrico, slime_fogo,
    fantasma, espectro, wraith, banshee,
    demônio, diabo, arquidemônio, príncipe_das_trevas
)

# Definição das masmorras
casa = Masmorra(
    nome='Casa',
    descricao='Lar, doce lar.',
    imagem_background='bg_casa.png',
    lista_inimigos=[mae]
)

esgoto = Masmorra(
    nome='Esgoto',
    descricao='Um esgoto meio sujo.',
    imagem_background='bg_esgoto.png',
    lista_inimigos=[
        rato, ratazana, rato_lanceiro, rato_guerreiro
    ]
)

floresta = Masmorra(
    nome='Floresta',
    descricao='Uma floresta densa e misteriosa.',
    imagem_background='bg_floresta.png',
    lista_inimigos=[
        lobo, urso, tigre, dragão
    ]
)

mata_fechada = Masmorra(
    nome='Mata Fechada',
    descricao='Uma mata fechada e perigosa.',
    imagem_background='bg_mata.png',
    lista_inimigos=[
        esqueleto, zumbi, vampiro, lich
    ]
)

castelo_abandonado = Masmorra(
    nome='Castelo Abandonado',
    descricao='Um castelo antigo e abandonado.',
    imagem_background='bg_castelo.png',
    lista_inimigos=[
        goblin, orc, troll, ogro
    ]
)

cemiterio = Masmorra(
    nome='Cemitério',
    descricao='Um cemitério assombrado.',
    imagem_background='bg_cemiterio.png',
    lista_inimigos=[
        slime, slime_venenoso, slime_elétrico, slime_fogo
    ]
)

catacumbas = Masmorra(
    nome='Catacumbas',
    descricao='Catacumbas escuras e úmidas.',
    imagem_background='bg_catacumbas.png',
    lista_inimigos=[
        fantasma, espectro, wraith, banshee
    ]
)

calabouco = Masmorra(
    nome='Calabouço',
    descricao='Um calabouço sombrio e perigoso.',
    imagem_background='bg_calabouco.png',
    lista_inimigos=[
        demônio, diabo, arquidemônio, príncipe_das_trevas
    ]
)

# Dicionário de todas as masmorras
MASMORRAS = {
    'casa': casa,
    'esgoto': esgoto,
    'floresta': floresta,
    'mata_fechada': mata_fechada,
    'castelo_abandonado': castelo_abandonado,
    'cemiterio': cemiterio,
    'catacumbas': catacumbas,
    'calabouco': calabouco
} 