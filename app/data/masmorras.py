from data import inimigos, itens
from models.masmorra import Masmorra
from models.npcs import mae

CHANCE_CONSUMIVEIS = 0.1
CHANCE_EQUIPAMENTOS_ARMAS = 0.05

# Definição das masmorras
casa = Masmorra(
    nome='Casa',
    descricao='Lar, doce lar.',
    imagem_background='backgrounds/casa.webp',
    lista_inimigos=[mae]
)

esgoto = Masmorra(
    nome='Esgoto',
    descricao='Um esgoto meio sujo.',
    imagem_background='backgrounds/esgoto.webp',
    lista_inimigos=[
        inimigos.rato,
        inimigos.ratazana,
        inimigos.rato_lanceiro,
        inimigos.rato_guerreiro,
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.arco_curto),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.espada_curta),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.tronco_magico),
        (CHANCE_CONSUMIVEIS, itens.pocao_pequena),
        (CHANCE_CONSUMIVEIS, itens.elixir_pequeno),
    ]
)

floresta = Masmorra(
    nome='Floresta',
    descricao='Uma floresta aberta.',
    imagem_background='backgrounds/floresta.webp',
    lista_inimigos=[
        inimigos.gnomo,
        inimigos.gnomo_guerreiro,
        inimigos.gnomo_mago,
        inimigos.gnomo_espadachim,
        inimigos.gnomo_bruto,
        inimigos.gnomo_anciao
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.camiseta_comun),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.malha_de_ferro),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.manto_de_aprendiz),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.couraca_simples),
        (CHANCE_CONSUMIVEIS, itens.pocao_pequena),
        (CHANCE_CONSUMIVEIS, itens.elixir_pequeno),
    ]
)

mata_fechada = Masmorra(
    nome='Mata Fechada',
    descricao='Uma mata fechada com muitas árvores.',
    imagem_background='backgrounds/mata_fechada.webp',
    lista_inimigos=[
        inimigos.golem_de_pedra,
        inimigos.entedidade_florestal,
        inimigos.entidade_animal,
        inimigos.entidade_obscura,
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.arco_militar),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.serpentina),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.cajado_de_aprendiz),
        (CHANCE_CONSUMIVEIS, itens.pocao_media),
        (CHANCE_CONSUMIVEIS, itens.elixir_medio),
    ]
)

castelo_abandonado = Masmorra(
    nome='Castelo Abandonado',
    descricao='Já foi uma grande civilização.',
    imagem_background='backgrounds/castelo_abandonado.webp',
    lista_inimigos=[
        inimigos.esqueleto,
        inimigos.esqueleto_arqueiro,
        inimigos.esqueleto_mago,
        inimigos.armadura_fantasma,
        inimigos.zumbi,
        inimigos.morto_vivo,
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.roupa_de_escoteiro),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.roupa_de_soldado),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.manto_autoral),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.couraca_de_javali),
        (CHANCE_CONSUMIVEIS, itens.pocao_media),
        (CHANCE_CONSUMIVEIS, itens.elixir_medio),
    ]
)

cemiterio = Masmorra(
    nome='Cemitério',
    descricao='Uma conexão com outro plano.',
    imagem_background='backgrounds/cemiterio.webp',
    lista_inimigos=[
        inimigos.alma_penada,
        inimigos.sentenca_final,
        inimigos.mensageiro_indesejado,
        inimigos.guia_dos_mortos,
        inimigos.protetora_das_catacumbas,
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.arco_composto),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.aniquiladora),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.cajado_de_conducao),
        (CHANCE_CONSUMIVEIS, itens.pocao_grande),
        (CHANCE_CONSUMIVEIS, itens.elixir_grande),
    ]
)

catacumbas = Masmorra(
    nome='Catacumbas',
    descricao='Um lugar com energia negativa.',
    imagem_background='backgrounds/catacumbas.webp',
    lista_inimigos=[
        inimigos.alma_penada,
        inimigos.sentenca_final,
        inimigos.bispo_corrompido,
        inimigos.sacerdote_renegado,
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.traje_de_cacador),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.peito_de_aco),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.ombros_de_turmalina),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.couraca_de_tigre_dente_de_sabre),
        (CHANCE_CONSUMIVEIS, itens.pocao_dupla),
        (CHANCE_CONSUMIVEIS, itens.elixir_duplo),
    ]
)

calabouco = Masmorra(
    nome='Calabouco dos Dragões',
    descricao='Parece ter um tesouro escondido.',
    imagem_background='backgrounds/calabouco.webp',
    lista_inimigos=[
        inimigos.filhote_de_dragao,
        inimigos.dragao_jovem,
        inimigos.dragao_violento,
        inimigos.dragao_adulto,
        inimigos.dragao_anciao,
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.besta),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.ultima_fantasia),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.cajado_de_grao_mestre),
        (CHANCE_CONSUMIVEIS, itens.pocao_de_litro),
        (CHANCE_CONSUMIVEIS, itens.elixir_de_litro),
    ]
)

laboratorio_secreto = Masmorra(
    nome='Laboratório Secreto',
    descricao='Que tipo de coisa faziam aqui?',
    imagem_background='backgrounds/laboratorio_secreto.webp',
    lista_inimigos=[
        inimigos.experimento_i,
        inimigos.experimento_ii,
        inimigos.experimento_iv,
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.armadura_de_samurai),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.protecao_divina),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.robe_mistico),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.couraca_de_mamute),
        (CHANCE_CONSUMIVEIS, itens.pocao_de_litro),
        (CHANCE_CONSUMIVEIS, itens.elixir_de_litro),
    ]
)

submundo = Masmorra(
    nome='Submundo',
    descricao='Eu não deveria estar aqui.',
    imagem_background='backgrounds/submundo.webp',
    lista_inimigos=[
        inimigos.serpente_infecciosa,
        inimigos.peste_sangrenta,
        inimigos.peste_sangrenta_gigante,
        inimigos.amon,
        inimigos.astaroth,
        inimigos.barbathos
    ],
    lista_itens=[
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.besta_celestial),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.atravesssa_planos),
        (CHANCE_EQUIPAMENTOS_ARMAS, itens.centro_do_universo),
        (CHANCE_CONSUMIVEIS, itens.pocao_real),
        (CHANCE_CONSUMIVEIS, itens.elixir_real),
    ]
)

nulo = Masmorra(
    nome='Nulo',
    descricao='O começo de tudo.',
    imagem_background='backgrounds/nulo.webp',
    lista_inimigos=[
        inimigos.nulo
    ],
    lista_itens=[
        (CHANCE_CONSUMIVEIS, itens.pocao_real),
        (CHANCE_CONSUMIVEIS, itens.elixir_real),
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
