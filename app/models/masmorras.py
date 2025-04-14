from models import inimigos, itens
from models.masmorra import Masmorra
from models.npcs import mae

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
        inimigos.rato,
        inimigos.ratazana,
        inimigos.rato_lanceiro,
        inimigos.rato_guerreiro,
    ],
    lista_itens=[
        (0.99, itens.queijo),
        (0.5, itens.pocao_pequena)
    ]
)

floresta = Masmorra(
    nome='Floresta',
    descricao='Uma floresta aberta.',
    imagem_background='bg_floresta.png',
    lista_inimigos=[
        inimigos.gnomo,
        inimigos.gnomo_guerreiro,
        inimigos.gnomo_mago,
        inimigos.gnomo_espadachim,
        inimigos.gnomo_bruto,
        inimigos.gnomo_anciao
    ]
)

mata_fechada = Masmorra(
    nome='Mata Fechada',
    descricao='Uma mata fechada com muitas árvores.',
    imagem_background='bg_mata_fechada.png',
    lista_inimigos=[
        inimigos.golem_de_pedra,
        inimigos.entedidade_florestal,
        inimigos.entidade_animal,
        inimigos.entidade_obscura,
    ]
)

castelo_abandonado = Masmorra(
    nome='Castelo Abandonado',
    descricao='Já foi uma grande civilização.',
    imagem_background='bg_castelo_abandonado.png',
    lista_inimigos=[
        inimigos.esqueleto,
        inimigos.esqueleto_arqueiro,
        inimigos.esqueleto_mago,
        inimigos.armadura_fantasma,
        inimigos.zumbi,
        inimigos.morto_vivo,
    ]
)

cemiterio = Masmorra(
    nome='Cemitério',
    descricao='Uma conexão com outro plano.',
    imagem_background='bg_cemiterio.png',
    lista_inimigos=[
        inimigos.alma_penada,
        inimigos.sentenca_final,
        inimigos.mensageiro_indesejado,
        inimigos.guia_dos_mortos,
        inimigos.protetora_das_catacumbas,
    ]
)

catacumbas = Masmorra(
    nome='Catacumbas',
    descricao='Um lugar com energia negativa.',
    imagem_background='bg_catacumbas.png',
    lista_inimigos=[
        inimigos.alma_penada,
        inimigos.sentenca_final,
        inimigos.bispo_corrompido,
        inimigos.sacerdote_renegado,
    ]
)

calabouco = Masmorra(
    nome='Calabouco dos Dragões',
    descricao='Parece ter um tesouro escondido.',
    imagem_background='bg_calabouco.png',
    lista_inimigos=[
        inimigos.filhote_de_dragao,
        inimigos.dragao_jovem,
        inimigos.dragao_violento,
        inimigos.dragao_adulto,
        inimigos.dragao_anciao,
    ]
)

laboratorio_secreto = Masmorra(
    nome='Laboratório Secreto',
    descricao='Que tipo de coisa faziam aqui?',
    imagem_background='bg_laboratorio_secreto.jpg',
    lista_inimigos=[
        inimigos.experimento_i,
        inimigos.experimento_ii,
        inimigos.experimento_iv,
    ]
)

submundo = Masmorra(
    nome='Submundo',
    descricao='Eu não deveria estar aqui.',
    imagem_background='bg_submundo.png',
    lista_inimigos=[
        inimigos.serpente_infecciosa,
        inimigos.peste_sangrenta,
        inimigos.peste_sangrenta_gigante,
        inimigos.amon,
        inimigos.astaroth,
        inimigos.barbathos,
    ]
)

nulo = Masmorra(
    nome='Nulo',
    descricao='O começo de tudo.',
    imagem_background='bg_nulo.png',
    lista_inimigos=[
        inimigos.nulo
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
    'calabouco': calabouco,
    'laboratorio_secreto': laboratorio_secreto,
    'submundo': submundo,
    'nulo': nulo
}
