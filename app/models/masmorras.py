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
        (0.09, itens.queijo),
        (0.09, itens.vinho),
        (0.04, itens.faca_de_cozinha),
        (0.04, itens.bengala)
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
    ],
    lista_itens=[
        (0.09, itens.maca),
        (0.09, itens.rum),
        (0.04, itens.espada_de_treino),
        (0.04, itens.cajado_improvisado)
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
    ],
    lista_itens=[
        (0.09, itens.pocao_pequena),
        (0.09, itens.absinto),
        (0.04, itens.espada_longa),
        (0.04, itens.cajado_de_aprendiz),
        (0.02, itens.tronco_de_salgueiro)
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
    ],
    lista_itens=[
        (0.09, itens.pocao_media),
        (0.09, itens.elixir_impuro),
        (0.04, itens.espada_pesada),
        (0.04, itens.cajado_de_aprendiz)
        # TODO: Criar item especial
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
    ],
    lista_itens=[
        (0.09, itens.pocao_media),
        (0.09, itens.elixir_impuro),
        (0.04, itens.espada_pesada),
        (0.04, itens.cajado_de_aprendiz),
        (0.02, itens.lamina_fantasma)
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
    ],
    lista_itens=[
        (0.09, itens.pocao_media),
        (0.09, itens.elixir_semipuro),
        (0.04, itens.espada_pesada),
        (0.04, itens.cajado_de_aprendiz),
        (0.02, itens.lamina_fantasma)
        # TODO: Criar item especial
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
    ],
    lista_itens=[
        (0.09, itens.pocao_grande),
        (0.09, itens.elixir_semipuro),
        (0.04, itens.espada_pesada),
        (0.04, itens.cajado_de_aprendiz),
        (0.02, itens.matadora_de_dragoes)
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
    ],
    lista_itens=[
        (0.09, itens.pocao_grande),
        (0.09, itens.elixir_puro),
        (0.04, itens.espada_pesada),
        (0.04, itens.cajado_de_aprendiz),
        (0.02, itens.linha_da_verdade)
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
    ],
    lista_itens=[
        (0.09, itens.pocao_suprema),
        (0.09, itens.elixir_concentrado),
        (0.04, itens.espada_pesada),
        (0.04, itens.cajado_de_aprendiz),
        (0.02, itens.brasa_eterna)
    ]
)

nulo = Masmorra(
    nome='Nulo',
    descricao='O começo de tudo.',
    imagem_background='bg_nulo.png',
    lista_inimigos=[
        inimigos.nulo
    ],
    lista_itens=[
        (0.09, itens.pocao_suprema),
        (0.09, itens.elixir_concentrado),
        (0.02, itens.ruptura),
        (0.02, itens.setenca_final)
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
