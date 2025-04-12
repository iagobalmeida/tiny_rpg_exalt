from app.models.entidade import Entidade

# Inimigos do Esgoto
rato = Entidade(
    nome='Rato',
    descricao='Um rato comum.',
    tipo='INIMIGO',
    level=1,
    vida=20,
    energia=10,
    experiencia=5,
    ouro=2,
    forca=5,
    agilidade=8,
    resistencia=3,
    inteligencia=2,
    sprite_x=0,
    sprite_y=0,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

ratazana = Entidade(
    nome='Ratazana',
    descricao='Uma ratazana grande e agressiva.',
    tipo='INIMIGO',
    level=3,
    vida=40,
    energia=15,
    experiencia=10,
    ouro=5,
    forca=8,
    agilidade=10,
    resistencia=5,
    inteligencia=3,
    sprite_x=1,
    sprite_y=0,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

rato_lanceiro = Entidade(
    nome='Rato Lanceiro',
    descricao='Um rato armado com uma lança.',
    tipo='INIMIGO',
    level=5,
    vida=60,
    energia=20,
    experiencia=15,
    ouro=8,
    forca=10,
    agilidade=12,
    resistencia=7,
    inteligencia=5,
    sprite_x=2,
    sprite_y=0,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

rato_guerreiro = Entidade(
    nome='Rato Guerreiro',
    descricao='Um rato treinado em combate.',
    tipo='INIMIGO',
    level=7,
    vida=80,
    energia=25,
    experiencia=20,
    ouro=12,
    forca=12,
    agilidade=15,
    resistencia=10,
    inteligencia=7,
    sprite_x=3,
    sprite_y=0,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

# Inimigos da Floresta
lobo = Entidade(
    nome='Lobo',
    descricao='Um lobo selvagem.',
    tipo='INIMIGO',
    level=10,
    vida=100,
    energia=30,
    experiencia=25,
    ouro=15,
    forca=15,
    agilidade=18,
    resistencia=12,
    inteligencia=8,
    sprite_x=0,
    sprite_y=1,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

urso = Entidade(
    nome='Urso',
    descricao='Um urso poderoso.',
    tipo='INIMIGO',
    level=15,
    vida=150,
    energia=40,
    experiencia=35,
    ouro=25,
    forca=20,
    agilidade=15,
    resistencia=18,
    inteligencia=10,
    sprite_x=1,
    sprite_y=1,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

tigre = Entidade(
    nome='Tigre',
    descricao='Um tigre feroz.',
    tipo='INIMIGO',
    level=20,
    vida=200,
    energia=50,
    experiencia=45,
    ouro=35,
    forca=25,
    agilidade=20,
    resistencia=15,
    inteligencia=12,
    sprite_x=2,
    sprite_y=1,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

dragão = Entidade(
    nome='Dragão',
    descricao='Um dragão lendário.',
    tipo='INIMIGO',
    level=25,
    vida=300,
    energia=70,
    experiencia=60,
    ouro=50,
    forca=30,
    agilidade=25,
    resistencia=25,
    inteligencia=20,
    sprite_x=3,
    sprite_y=1,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

# Inimigos da Mata Fechada
esqueleto = Entidade(
    nome='Esqueleto',
    descricao='Um esqueleto reanimado.',
    tipo='INIMIGO',
    level=30,
    vida=250,
    energia=60,
    experiencia=70,
    ouro=40,
    forca=22,
    agilidade=15,
    resistencia=20,
    inteligencia=10,
    sprite_x=0,
    sprite_y=2,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

zumbi = Entidade(
    nome='Zumbi',
    descricao='Um zumbi lento mas resistente.',
    tipo='INIMIGO',
    level=35,
    vida=350,
    energia=80,
    experiencia=85,
    ouro=55,
    forca=25,
    agilidade=10,
    resistencia=28,
    inteligencia=5,
    sprite_x=1,
    sprite_y=2,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

vampiro = Entidade(
    nome='Vampiro',
    descricao='Um vampiro sedento por sangue.',
    tipo='INIMIGO',
    level=40,
    vida=400,
    energia=100,
    experiencia=100,
    ouro=70,
    forca=28,
    agilidade=25,
    resistencia=22,
    inteligencia=30,
    sprite_x=2,
    sprite_y=2,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

lich = Entidade(
    nome='Lich',
    descricao='Um lich poderoso.',
    tipo='INIMIGO',
    level=45,
    vida=450,
    energia=120,
    experiencia=120,
    ouro=90,
    forca=20,
    agilidade=15,
    resistencia=25,
    inteligencia=40,
    sprite_x=3,
    sprite_y=2,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

# Inimigos do Castelo Abandonado
goblin = Entidade(
    nome='Goblin',
    descricao='Um goblin pequeno e ágil.',
    tipo='INIMIGO',
    level=50,
    vida=300,
    energia=90,
    experiencia=140,
    ouro=80,
    forca=18,
    agilidade=30,
    resistencia=15,
    inteligencia=12,
    sprite_x=0,
    sprite_y=3,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

orc = Entidade(
    nome='Orc',
    descricao='Um orc forte e brutal.',
    tipo='INIMIGO',
    level=55,
    vida=500,
    energia=110,
    experiencia=160,
    ouro=100,
    forca=35,
    agilidade=20,
    resistencia=30,
    inteligencia=15,
    sprite_x=1,
    sprite_y=3,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

troll = Entidade(
    nome='Troll',
    descricao='Um troll gigante e regenerativo.',
    tipo='INIMIGO',
    level=60,
    vida=600,
    energia=130,
    experiencia=180,
    ouro=120,
    forca=40,
    agilidade=15,
    resistencia=35,
    inteligencia=10,
    sprite_x=2,
    sprite_y=3,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

ogro = Entidade(
    nome='Ogro',
    descricao='Um ogro enorme e poderoso.',
    tipo='INIMIGO',
    level=65,
    vida=700,
    energia=150,
    experiencia=200,
    ouro=150,
    forca=45,
    agilidade=10,
    resistencia=40,
    inteligencia=8,
    sprite_x=3,
    sprite_y=3,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

# Inimigos do Cemitério
slime = Entidade(
    nome='Slime',
    descricao='Um slime básico.',
    tipo='INIMIGO',
    level=70,
    vida=400,
    energia=100,
    experiencia=220,
    ouro=100,
    forca=20,
    agilidade=5,
    resistencia=25,
    inteligencia=5,
    sprite_x=0,
    sprite_y=4,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

slime_venenoso = Entidade(
    nome='Slime Venenoso',
    descricao='Um slime que exala veneno.',
    tipo='INIMIGO',
    level=75,
    vida=450,
    energia=120,
    experiencia=240,
    ouro=120,
    forca=25,
    agilidade=5,
    resistencia=30,
    inteligencia=15,
    sprite_x=1,
    sprite_y=4,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

slime_elétrico = Entidade(
    nome='Slime Elétrico',
    descricao='Um slime que emite eletricidade.',
    tipo='INIMIGO',
    level=80,
    vida=500,
    energia=140,
    experiencia=260,
    ouro=140,
    forca=30,
    agilidade=10,
    resistencia=35,
    inteligencia=25,
    sprite_x=2,
    sprite_y=4,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

slime_fogo = Entidade(
    nome='Slime de Fogo',
    descricao='Um slime que queima tudo ao redor.',
    tipo='INIMIGO',
    level=85,
    vida=550,
    energia=160,
    experiencia=280,
    ouro=160,
    forca=35,
    agilidade=15,
    resistencia=40,
    inteligencia=35,
    sprite_x=3,
    sprite_y=4,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

# Inimigos das Catacumbas
fantasma = Entidade(
    nome='Fantasma',
    descricao='Um fantasma assombrador.',
    tipo='INIMIGO',
    level=90,
    vida=600,
    energia=180,
    experiencia=300,
    ouro=180,
    forca=25,
    agilidade=30,
    resistencia=20,
    inteligencia=40,
    sprite_x=0,
    sprite_y=5,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

espectro = Entidade(
    nome='Espectro',
    descricao='Um espectro mais poderoso.',
    tipo='INIMIGO',
    level=95,
    vida=650,
    energia=200,
    experiencia=320,
    ouro=200,
    forca=30,
    agilidade=35,
    resistencia=25,
    inteligencia=45,
    sprite_x=1,
    sprite_y=5,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

wraith = Entidade(
    nome='Wraith',
    descricao='Um wraith sombrio.',
    tipo='INIMIGO',
    level=100,
    vida=700,
    energia=220,
    experiencia=340,
    ouro=220,
    forca=35,
    agilidade=40,
    resistencia=30,
    inteligencia=50,
    sprite_x=2,
    sprite_y=5,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

banshee = Entidade(
    nome='Banshee',
    descricao='Uma banshee aterrorizante.',
    tipo='INIMIGO',
    level=105,
    vida=750,
    energia=240,
    experiencia=360,
    ouro=240,
    forca=40,
    agilidade=45,
    resistencia=35,
    inteligencia=55,
    sprite_x=3,
    sprite_y=5,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

# Inimigos do Calabouço
demônio = Entidade(
    nome='Demônio',
    descricao='Um demônio menor.',
    tipo='INIMIGO',
    level=110,
    vida=800,
    energia=260,
    experiencia=380,
    ouro=260,
    forca=45,
    agilidade=35,
    resistencia=40,
    inteligencia=45,
    sprite_x=0,
    sprite_y=6,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

diabo = Entidade(
    nome='Diabo',
    descricao='Um diabo poderoso.',
    tipo='INIMIGO',
    level=115,
    vida=850,
    energia=280,
    experiencia=400,
    ouro=280,
    forca=50,
    agilidade=40,
    resistencia=45,
    inteligencia=50,
    sprite_x=1,
    sprite_y=6,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

arquidemônio = Entidade(
    nome='Arquidemônio',
    descricao='Um arquidemônio temível.',
    tipo='INIMIGO',
    level=120,
    vida=900,
    energia=300,
    experiencia=420,
    ouro=300,
    forca=55,
    agilidade=45,
    resistencia=50,
    inteligencia=55,
    sprite_x=2,
    sprite_y=6,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

príncipe_das_trevas = Entidade(
    nome='Príncipe das Trevas',
    descricao='O príncipe das trevas, o inimigo final.',
    tipo='INIMIGO',
    level=125,
    vida=1000,
    energia=350,
    experiencia=500,
    ouro=500,
    forca=60,
    agilidade=50,
    resistencia=55,
    inteligencia=60,
    sprite_x=3,
    sprite_y=6,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
)

# NPCs
mae = Entidade(
    nome='Mãe',
    descricao='Sua mãe amorosa.',
    tipo='NPC',
    level=1,
    vida=100,
    energia=50,
    experiencia=0,
    ouro=0,
    forca=5,
    agilidade=5,
    resistencia=5,
    inteligencia=5,
    sprite_x=0,
    sprite_y=7,
    sprite_nome='inimigos.png',
    sprite_largura=32,
    sprite_altura=32
) 