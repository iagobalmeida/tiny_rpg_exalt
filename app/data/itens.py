from models.item import ConsumivelCura, Equipamento

CURA_BASE = 5
CRECIMENTO_CURA = 3


def consumivel_cura(identificador: str, atributo: str, nome: str, descricao: str, sprite_x: int, sprite_y: int, nivel_cura: int = 0):
    fator = CURA_BASE + CURA_BASE*CRECIMENTO_CURA*nivel_cura*nivel_cura
    descricao_dicional = f'+{fator} ATTR_{atributo.upper()}'
    return ConsumivelCura(
        identificador=identificador,
        atributo=atributo,
        fator=fator,
        nome=nome,
        descricao=[
            descricao,
            descricao_dicional
        ],
        sprite_x=sprite_x,
        sprite_y=sprite_y
    )


queijo = consumivel_cura(
    identificador='queijo',
    atributo='vida',
    nivel_cura=0,
    nome='Queijo',
    descricao='Não parece tão estragado...',
    sprite_x=0,
    sprite_y=25
)

maca = consumivel_cura(
    identificador='maca',
    atributo='vida',
    nivel_cura=1,
    nome='Maçã',
    descricao='Como que isso caiu da árvore?',
    sprite_x=2,
    sprite_y=25
)

pao = consumivel_cura(
    identificador='pao',
    atributo='vida',
    nivel_cura=2,
    nome='Pão',
    descricao='Cacetinho, pão frânces, sei lá.',
    sprite_x=1,
    sprite_y=25
)

pocao_pequena = consumivel_cura(
    identificador='pocao_pequena',
    atributo='vida',
    nivel_cura=3,
    nome='Poção Pequena',
    descricao='Tem um gosto duvidoso.',
    sprite_x=2,
    sprite_y=20
)

pocao_media = consumivel_cura(
    identificador='pocao_media',
    atributo='vida',
    nivel_cura=4,
    sprite_x=1,
    sprite_y=19,
    nome='Poção Média',
    descricao='Parece bom.'
)

pocao_grande = consumivel_cura(
    identificador='pocao_grande',
    atributo='vida',
    nivel_cura=5,
    sprite_x=3,
    sprite_y=19,
    nome='Poção Grande',
    descricao='Um litro de puro sabor!'
)

pocao_suprema = consumivel_cura(
    identificador='pocao_suprema',
    atributo='vida',
    nivel_cura=6,
    sprite_x=4,
    sprite_y=20,
    nome='Poção Suprema',
    descricao='É forte, mas é bom!'
)

# Recuperação de Energia

vinho = consumivel_cura(
    identificador='vinho',
    atributo='energia',
    nivel_cura=0,
    nome='Vinho',
    descricao='Um vinho colonial, de boa qualidade.',
    sprite_x=3,
    sprite_y=25
)

rum = consumivel_cura(
    identificador='rum',
    atributo='energia',
    nivel_cura=1,
    nome='Rum',
    descricao='ARRr!',
    sprite_x=2,
    sprite_y=19
)

absinto = consumivel_cura(
    identificador='absinto',
    atributo='energia',
    nivel_cura=2,
    nome='Absynto',
    descricao='Isso é consumível?',
    sprite_x=4,
    sprite_y=19
)

elixir_impuro = consumivel_cura(
    identificador='elixir_impuro',
    atributo='energia',
    nivel_cura=3,
    nome='Elixir Ímpuro',
    descricao='É sobre o custo-benefício.',
    sprite_x=0,
    sprite_y=20
)

elixir_semipuro = consumivel_cura(
    identificador='elixir_semipuro',
    atributo='energia',
    nivel_cura=4,
    nome='Elixir 60%',
    descricao='Como fazem isso?',
    sprite_x=1,
    sprite_y=20
)

elixir_puro = consumivel_cura(
    identificador='elixir_puro',
    atributo='energia',
    nivel_cura=5,
    nome='Elixir Puro',
    descricao='É caro, mas vale a pena.',
    sprite_x=4,
    sprite_y=25
)

elixir_concentrado = consumivel_cura(
    identificador='elixir_concentrado',
    atributo='energia',
    nivel_cura=6,
    sprite_x=3,
    sprite_y=20,
    nome='Elixir Concentrado',
    descricao='É forte, mas é bom!'
)


EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE = 3
EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE = 1.5
# Equipamentos - Espadas


def equipamento_forca_agilidade(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, forca: int, agilidade: int = None):
    forca = int(forca * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE)

    descricao_lista = [
        descricao,
        f'+ {forca} ATTR_FORCA'
    ]

    if agilidade:
        agilidade = int(agilidade * EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE)
        descricao_lista.append(f'+ {agilidade} ATTR_AGILIDADE')

    return Equipamento(
        identificador=identificador,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        nome=nome,
        equipamento_tipo='ARMA',
        descricao=descricao_lista,
        forca=forca,
        agilidade=agilidade
    )


faca_de_cozinha = equipamento_forca_agilidade(
    identificador='faca_de_cozinha',
    sprite_x=0,
    sprite_y=0,
    nome='Faca de Cozinha',
    descricao='Essa era a melhor faca...',
    forca=1,
    agilidade=1
)

espada_de_treino = equipamento_forca_agilidade(
    identificador='espada_de_treino',
    sprite_x=1,
    sprite_y=0,
    nome='Espada de Treino',
    descricao='É um bom começo.',
    forca=5,
    agilidade=2
)

espada_longa = equipamento_forca_agilidade(
    identificador='espada_longa',
    sprite_x=1,
    sprite_y=0,
    nome='Espada Longa',
    descricao='Não é tão veloz.',
    forca=15,
    agilidade=5
)

espada_pesada = equipamento_forca_agilidade(
    identificador='espada_pesada',
    sprite_x=0,
    sprite_y=1,
    nome='Espada Pesada',
    descricao='É mais pesada do que parece.',
    forca=20,
    agilidade=1
)

matadora_de_dragoes = equipamento_forca_agilidade(
    identificador='matadora_de_dragoes',
    sprite_x=5,
    sprite_y=0,
    nome='Matadora de Dragões',
    descricao='Tem uma história.',
    forca=35,
    agilidade=5
)

lamina_fantasma = equipamento_forca_agilidade(
    identificador='lamina_fantasma',
    sprite_x=10,
    sprite_y=0,
    nome='Lâmina Fantasma',
    descricao='Não tem peso algum.',
    forca=25,
    agilidade=25
)

brasa_eterna = equipamento_forca_agilidade(
    identificador='brasa_eterna',
    sprite_x=9,
    sprite_y=0,
    nome='Brasa Eterna',
    descricao='Se segurar direito não queima.',
    forca=50,
    agilidade=35
)

ruptura = equipamento_forca_agilidade(
    identificador='ruptura',
    sprite_x=8,
    sprite_y=0,
    nome='Ruptura',
    descricao='Corta até o tecido do tempo.',
    forca=100,
    agilidade=50
)

# Equipamentos - Cajados


def equipamento_inteligencia_resistencia(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, inteligencia: int, resistencia: int = None):
    inteligencia = inteligencia * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE

    descricao_lista = [
        descricao,
        f'+ {inteligencia} ATTR_INTELIGENCIA'
    ]

    if resistencia:
        resistencia = resistencia * EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE
        descricao_lista.append(f'+ {resistencia} ATTR_RESISTENCIA')

    return Equipamento(
        identificador=identificador,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        nome=nome,
        equipamento_tipo='ARMA',
        descricao=descricao_lista,
        inteligencia=inteligencia,
        resistencia=resistencia
    )


bengala = equipamento_inteligencia_resistencia(
    identificador='bengala',
    sprite_x=9,
    sprite_y=10,
    nome='Bengala',
    descricao='Pelo menos concentra energia.',
    inteligencia=5,
    resistencia=2
)

cajado_improvisado = equipamento_inteligencia_resistencia(
    identificador='cajado_improvisado',
    sprite_x=7,
    sprite_y=10,
    nome='Cajado Improvisado',
    descricao='Um graveto e um cristal.',
    inteligencia=15,
    resistencia=8
)

cajado_de_aprendiz = equipamento_inteligencia_resistencia(
    identificador='cajado_de_aprendiz',
    sprite_x=0,
    sprite_y=10,
    nome='Cajado de Aprendiz',
    descricao='Usar com responsabilidade.',
    inteligencia=35,
    resistencia=16
)

tronco_de_salgueiro = equipamento_inteligencia_resistencia(
    identificador='tronco_de_salgueiro',
    sprite_x=2,
    sprite_y=10,
    nome='Tronco de Salgueiro',
    descricao='Como deve ser.',
    inteligencia=75,
    resistencia=32
)

linha_da_verdade = equipamento_inteligencia_resistencia(
    identificador='linha_da_verdade',
    sprite_x=3,
    sprite_y=10,
    nome='Linha da Verdade',
    descricao='Ou existe, ou não.',
    inteligencia=125,
    resistencia=16
)

setenca_final = equipamento_inteligencia_resistencia(
    identificador='setenca_final',
    sprite_x=8,
    sprite_y=10,
    nome='Sentença Final',
    descricao='Poder inimaginável',
    inteligencia=180,
    resistencia=64
)
