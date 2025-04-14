from models.entidade import Magia

# Magias de ataque
bola_de_fogo = Magia(
    nome='Bola de Fogo',
    descricao='Lança uma bola de fogo que causa dano em área.',
    tipo='ATAQUE',
    nivel=1,
    custo_energia=10,
    dano=15,
    sprite_x=0,
    sprite_y=0,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

raio_de_gelo = Magia(
    nome='Raio de Gelo',
    descricao='Lança um raio de gelo que congela o alvo.',
    tipo='ATAQUE',
    nivel=5,
    custo_energia=15,
    dano=20,
    sprite_x=1,
    sprite_y=0,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

relâmpago = Magia(
    nome='Relâmpago',
    descricao='Invoca um relâmpago que causa dano elétrico.',
    tipo='ATAQUE',
    nivel=10,
    custo_energia=20,
    dano=25,
    sprite_x=2,
    sprite_y=0,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

meteorito = Magia(
    nome='Meteorito',
    descricao='Invoca um meteorito que causa dano massivo.',
    tipo='ATAQUE',
    nivel=15,
    custo_energia=30,
    dano=40,
    sprite_x=3,
    sprite_y=0,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

# Magias de cura
cura_leve = Magia(
    nome='Cura Leve',
    descricao='Recupera uma pequena quantidade de vida.',
    tipo='CURA',
    nivel=1,
    custo_energia=10,
    cura=20,
    sprite_x=0,
    sprite_y=1,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

cura_moderada = Magia(
    nome='Cura Moderada',
    descricao='Recupera uma quantidade moderada de vida.',
    tipo='CURA',
    nivel=5,
    custo_energia=15,
    cura=35,
    sprite_x=1,
    sprite_y=1,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

cura_avançada = Magia(
    nome='Cura Avançada',
    descricao='Recupera uma grande quantidade de vida.',
    tipo='CURA',
    nivel=10,
    custo_energia=20,
    cura=50,
    sprite_x=2,
    sprite_y=1,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

cura_completa = Magia(
    nome='Cura Completa',
    descricao='Recupera toda a vida do alvo.',
    tipo='CURA',
    nivel=15,
    custo_energia=30,
    cura=100,
    sprite_x=3,
    sprite_y=1,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

# Magias de suporte
proteção = Magia(
    nome='Proteção',
    descricao='Aumenta a defesa do alvo.',
    tipo='SUPORTE',
    nivel=1,
    custo_energia=10,
    duração=60,
    sprite_x=0,
    sprite_y=2,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

força = Magia(
    nome='Força',
    descricao='Aumenta a força do alvo.',
    tipo='SUPORTE',
    nivel=5,
    custo_energia=15,
    duração=60,
    sprite_x=1,
    sprite_y=2,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

agilidade = Magia(
    nome='Agilidade',
    descricao='Aumenta a agilidade do alvo.',
    tipo='SUPORTE',
    nivel=10,
    custo_energia=20,
    duração=60,
    sprite_x=2,
    sprite_y=2,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

invisibilidade = Magia(
    nome='Invisibilidade',
    descricao='Torna o alvo invisível por um tempo.',
    tipo='SUPORTE',
    nivel=15,
    custo_energia=30,
    duração=30,
    sprite_x=3,
    sprite_y=2,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

# Magias especiais
ressurreição = Magia(
    nome='Ressurreição',
    descricao='Revive um aliado morto.',
    tipo='ESPECIAL',
    nivel=20,
    custo_energia=50,
    sprite_x=0,
    sprite_y=3,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

teleporte = Magia(
    nome='Teleporte',
    descricao='Teleporta o alvo para um local seguro.',
    tipo='ESPECIAL',
    nivel=20,
    custo_energia=40,
    sprite_x=1,
    sprite_y=3,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

invocação = Magia(
    nome='Invocação',
    descricao='Invoca um aliado para ajudar na batalha.',
    tipo='ESPECIAL',
    nivel=20,
    custo_energia=45,
    sprite_x=2,
    sprite_y=3,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)

apocalipse = Magia(
    nome='Apocalipse',
    descricao='Causa dano massivo a todos os inimigos.',
    tipo='ESPECIAL',
    nivel=25,
    custo_energia=100,
    sprite_x=3,
    sprite_y=3,
    sprite_nome='magias.png',
    sprite_largura=32,
    sprite_altura=32
)
