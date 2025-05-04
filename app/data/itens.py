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


# Recuperação de Vida
pocao_pequena = consumivel_cura(
    identificador='pocao_pequena',
    atributo='vida',
    nivel_cura=0,
    nome='Poção Pequena',
    descricao='Tem menos de um gole.',
    sprite_x=4,
    sprite_y=0
)

pocao_media = consumivel_cura(
    identificador='pocao_media',
    atributo='vida',
    nivel_cura=1,
    nome='Poção Média',
    descricao='Refrescante...',
    sprite_x=5,
    sprite_y=0
)

pocao_grande = consumivel_cura(
    identificador='pocao_grande',
    atributo='vida',
    nivel_cura=3,
    nome='Poção Grande',
    descricao='É o mínimo!',
    sprite_x=6,
    sprite_y=0
)

pocao_dupla = consumivel_cura(
    identificador='pocao_dupla',
    atributo='vida',
    nivel_cura=6,
    nome='Poção Dupla',
    descricao='O dobro de poção',
    sprite_x=7,
    sprite_y=0
)

pocao_de_litro = consumivel_cura(
    identificador='pocao_de_litro',
    atributo='vida',
    nivel_cura=8,
    nome='Poção de Litro',
    descricao='1L de poção!',
    sprite_x=8,
    sprite_y=0
)

pocao_real = consumivel_cura(
    identificador='pocao_real',
    atributo='vida',
    nivel_cura=10,
    nome='Poção Real',
    descricao='Coisa de nobre',
    sprite_x=9,
    sprite_y=0
)


# Recuperação de Energia
elixir_pequeno = consumivel_cura(
    identificador='elixir_pequeno',
    atributo='energia',
    nivel_cura=0,
    nome='Elíxir Pequena',
    descricao='Tem menos de um gole.',
    sprite_x=4,
    sprite_y=1
)

elixir_medio = consumivel_cura(
    identificador='elixir_medio',
    atributo='energia',
    nivel_cura=1,
    nome='Elíxir Média',
    descricao='Refrescante...',
    sprite_x=5,
    sprite_y=1
)

elixir_grande = consumivel_cura(
    identificador='elixir_grande',
    atributo='energia',
    nivel_cura=3,
    nome='Elíxir Grande',
    descricao='É o mínimo!',
    sprite_x=6,
    sprite_y=1
)

elixir_duplo = consumivel_cura(
    identificador='elixir_duplo',
    atributo='energia',
    nivel_cura=6,
    nome='Elíxir Dupla',
    descricao='O dobro de elíxir',
    sprite_x=7,
    sprite_y=1
)

elixir_de_litro = consumivel_cura(
    identificador='elixir_de_litro',
    atributo='energia',
    nivel_cura=8,
    nome='Elíxir de Litro',
    descricao='1L de elíxir!',
    sprite_x=8,
    sprite_y=1
)

elixir_real = consumivel_cura(
    identificador='elixir_real',
    atributo='energia',
    nivel_cura=10,
    nome='Elíxir Real',
    descricao='Coisa de nobre',
    sprite_x=9,
    sprite_y=1
)


EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE = 7
EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE = 5


# Equipamentos - Armaduras Leves
def equipamento_armadura_resistencia_agilidade(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, resistencia: int, agilidade: int = None):
    resistencia = int(resistencia * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE)

    descricao_lista = [
        descricao,
        f'+ {resistencia} ATTR_RESISTENCIA'
    ]

    if agilidade:
        agilidade = int(agilidade * EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE)
        descricao_lista.append(f'+ {agilidade} ATTR_AGILIDADE')

    return Equipamento(
        identificador=identificador,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        nome=nome,
        equipamento_tipo='ARMADURA',
        descricao=descricao_lista,
        resistencia=resistencia,
        agilidade=agilidade
    )


camiseta_comun = equipamento_armadura_resistencia_agilidade(
    identificador='camiseta_comun',
    sprite_x=4,
    sprite_y=2,
    nome='Camiseta Comum',
    descricao='Dá pro gasto.',
    resistencia=2,
    agilidade=1
)

roupa_de_escoteiro = equipamento_armadura_resistencia_agilidade(
    identificador='roupa_de_escoteiro',
    sprite_x=4,
    sprite_y=3,
    nome='Roupa de Escoteiro',
    descricao='Pra ajudar idosas a atravessar a rua.',
    resistencia=4,
    agilidade=3
)

traje_de_cacador = equipamento_armadura_resistencia_agilidade(
    identificador='traje_de_cacador',
    sprite_x=4,
    sprite_y=4,
    nome='Traje de Caçador',
    descricao='Tem tudo que eu preciso!',
    resistencia=6,
    agilidade=6
)

armadura_de_samurai = equipamento_armadura_resistencia_agilidade(
    identificador='armadura_de_samurai',
    sprite_x=4,
    sprite_y=5,
    nome='Armadura de Samurai',
    descricao='Uchinaru heiwa...',
    resistencia=8,
    agilidade=12
)


# Equipamentos - Armaduras Pesadas
def equipamento_armadura_resistencia_inteligencia(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, resistencia: int, inteligencia: int = None):
    resistencia = int(resistencia * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE)

    descricao_lista = [
        descricao,
        f'+ {resistencia} ATTR_RESISTENCIA'
    ]

    if inteligencia:
        inteligencia = int(inteligencia * EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE)
        descricao_lista.append(f'+ {inteligencia} ATTR_INTELIGENCIA')

    return Equipamento(
        identificador=identificador,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        nome=nome,
        equipamento_tipo='ARMADURA',
        descricao=descricao_lista,
        resistencia=resistencia,
        inteligencia=inteligencia
    )


malha_de_ferro = equipamento_armadura_resistencia_inteligencia(
    identificador='malha_de_ferro',
    sprite_x=5,
    sprite_y=2,
    nome='Malha de Ferro',
    descricao='Pesada, mas eficiente.',
    resistencia=3,
    inteligencia=1
)


roupa_de_soldado = equipamento_armadura_resistencia_inteligencia(
    identificador='roupa_de_soldado',
    sprite_x=5,
    sprite_y=3,
    nome='Roupa de Soldado',
    descricao='SIM, SENHOR!',
    resistencia=6,
    inteligencia=2
)


peito_de_aco = equipamento_armadura_resistencia_inteligencia(
    identificador='peito_de_aco',
    sprite_x=5,
    sprite_y=4,
    nome='Peito de Aço',
    descricao='Inabalável!',
    resistencia=9,
    inteligencia=3
)


protecao_divina = equipamento_armadura_resistencia_inteligencia(
    identificador='protecao_divina',
    sprite_x=5,
    sprite_y=5,
    nome='Proteção Divina',
    descricao='Uma armadura abençoada',
    resistencia=12,
    inteligencia=4
)


# Equipamentos - Mantos
def equipamento_armadura_inteligencia_resistencia(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, inteligencia: int, resistencia: int = None):
    inteligencia = int(inteligencia * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE)

    descricao_lista = [
        descricao,
        f'+ {inteligencia} ATTR_INTELIGENCIA'
    ]

    if resistencia:
        resistencia = int(resistencia * EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE)
        descricao_lista.append(f'+ {resistencia} ATTR_RESISTENCIA')

    return Equipamento(
        identificador=identificador,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        nome=nome,
        equipamento_tipo='ARMADURA',
        descricao=descricao_lista,
        inteligencia=inteligencia,
        resistencia=resistencia
    )


manto_de_aprendiz = equipamento_armadura_inteligencia_resistencia(
    identificador='manto_de_aprendiz',
    sprite_x=6,
    sprite_y=2,
    nome='Manto de Aprendiz',
    descricao='Estudar, é o que há!',
    inteligencia=3,
    resistencia=1
)


manto_autoral = equipamento_armadura_inteligencia_resistencia(
    identificador='manto_autoral',
    sprite_x=6,
    sprite_y=3,
    nome='Manto Autoral',
    descricao='É único, eu juro!',
    inteligencia=6,
    resistencia=2
)


ombros_de_turmalina = equipamento_armadura_inteligencia_resistencia(
    identificador='ombros_de_turmalina',
    sprite_x=6,
    sprite_y=4,
    nome='Ombros de Turmalina',
    descricao='Consigo sentir a energia...',
    inteligencia=10,
    resistencia=3
)


robe_mistico = equipamento_armadura_inteligencia_resistencia(
    identificador='robe_mistico',
    sprite_x=6,
    sprite_y=5,
    nome='Robe Místico',
    descricao='Cheio de firulas, poderosas firulas!',
    inteligencia=14,
    resistencia=4
)


# Equipamentos - Couraças
def equipamento_armadura_forca_resistencia(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, forca: int, resistencia: int = None):
    forca = int(forca * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE)

    descricao_lista = [
        descricao,
        f'+ {forca} ATTR_FORCA'
    ]

    if resistencia:
        resistencia = int(resistencia * EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE)
        descricao_lista.append(f'+ {resistencia} ATTR_RESISTENCIA')

    return Equipamento(
        identificador=identificador,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        nome=nome,
        equipamento_tipo='ARMADURA',
        descricao=descricao_lista,
        forca=forca,
        resistencia=resistencia
    )


couraca_simples = equipamento_armadura_forca_resistencia(
    identificador='couraca_simples',
    sprite_x=7,
    sprite_y=2,
    nome='Couraça Simples',
    descricao='Só o necessário.',
    forca=3,
    resistencia=1
)


couraca_de_javali = equipamento_armadura_forca_resistencia(
    identificador='couraca_de_javali',
    sprite_x=7,
    sprite_y=3,
    nome='Couraça de Javali',
    descricao='Foi difícil de fazer.',
    forca=6,
    resistencia=4
)


couraca_de_tigre_dente_de_sabre = equipamento_armadura_forca_resistencia(
    identificador='couraca_de_tigre_dente_de_sabre',
    sprite_x=7,
    sprite_y=4,
    nome='Couraça de Tigre Dente-de-Sabre',
    descricao='A caçada, me fortalece!',
    forca=9,
    resistencia=7
)


couraca_de_mamute = equipamento_armadura_forca_resistencia(
    identificador='couraca_de_mamute',
    sprite_x=7,
    sprite_y=5,
    nome='Couraça de Mamute',
    descricao='Caçar, para sempre!',
    forca=15,
    resistencia=8
)


# Equipamentos - Arcos
def equipamento_arma_forca_agilidade(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, forca: int, agilidade: int = None):
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


arco_curto = equipamento_arma_forca_agilidade(
    identificador='arco_curto',
    sprite_x=5,
    sprite_y=7,
    nome='Arco Curto',
    descricao='É um bom começo!',
    forca=2,
    agilidade=2
)

arco_militar = equipamento_arma_forca_agilidade(
    identificador='arco_militar',
    sprite_x=6,
    sprite_y=7,
    nome='Arco Militar',
    descricao='Uma boa arma.',
    forca=6,
    agilidade=4
)

arco_composto = equipamento_arma_forca_agilidade(
    identificador='arco_composto',
    sprite_x=7,
    sprite_y=7,
    nome='Arco Composto',
    descricao='Feito sob medida, perfeito para combate.',
    forca=8,
    agilidade=6
)

besta = equipamento_arma_forca_agilidade(
    identificador='besta',
    sprite_x=8,
    sprite_y=7,
    nome='Besta',
    descricao='Agora ninguém me pega!',
    forca=14,
    agilidade=16
)

besta_celestial = equipamento_arma_forca_agilidade(
    identificador='besta_celestial',
    sprite_x=9,
    sprite_y=7,
    nome='Besta Celestial',
    descricao='Um monstro...',
    forca=20,
    agilidade=15
)


# Equipamentos - Espadas
def equipamento_arma_forca_resistencia(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, forca: int, resistencia: int = None):
    forca = int(forca * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE)

    descricao_lista = [
        descricao,
        f'+ {forca} ATTR_FORCA'
    ]

    if resistencia:
        resistencia = int(resistencia * EQUIPAMENTOS_ATRIBUTO_SECUNDARIO_BASE)
        descricao_lista.append(f'+ {resistencia} ATTR_RESISTENCIA')

    return Equipamento(
        identificador=identificador,
        sprite_x=sprite_x,
        sprite_y=sprite_y,
        nome=nome,
        equipamento_tipo='ARMA',
        descricao=descricao_lista,
        forca=forca,
        resistencia=resistencia
    )


espada_curta = equipamento_arma_forca_resistencia(
    identificador='espada_curta',
    sprite_x=5,
    sprite_y=8,
    nome='Espada Curta',
    descricao='É um bom começo!',
    forca=2,
    resistencia=1
)

serpentina = equipamento_arma_forca_resistencia(
    identificador='serpentina',
    sprite_x=6,
    sprite_y=8,
    nome='Serpentina',
    descricao='Seu corte é imprevisível',
    forca=6,
    resistencia=5
)

aniquiladora = equipamento_arma_forca_resistencia(
    identificador='aniquiladora',
    sprite_x=7,
    sprite_y=8,
    nome='Aniquiladora',
    descricao='Tem uma energia pesada...',
    forca=8,
    resistencia=0
)

ultima_fantasia = equipamento_arma_forca_resistencia(
    identificador='ultima_fantasia',
    sprite_x=8,
    sprite_y=8,
    nome='Última Fantasia',
    descricao='Eu me lembro dessa espada!',
    forca=14,
    resistencia=6
)

atravesssa_planos = equipamento_arma_forca_resistencia(
    identificador='atravesssa_planos',
    sprite_x=9,
    sprite_y=8,
    nome='Atravessa Planos',
    descricao='Isso não deveria existir...',
    forca=20,
    resistencia=10
)


# Equipamentos - Cajados
def equipamento_arma_inteligencia_agilidade(identificador: str, sprite_x: int, sprite_y: int, nome: str, descricao: str, inteligencia: int, agilidade: int = None):
    inteligencia = inteligencia * EQUIPAMENTOS_ATRIBUTO_PRIMARIO_BASE

    descricao_lista = [
        descricao,
        f'+ {inteligencia} ATTR_INTELIGENCIA'
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
        inteligencia=inteligencia,
        agilidade=agilidade
    )


tronco_magico = equipamento_arma_inteligencia_agilidade(
    identificador='tronco_magico',
    sprite_x=5,
    sprite_y=9,
    nome='Tronco Mágico',
    descricao='O poder, da natureza!',
    inteligencia=1,
    agilidade=1
)


cajado_de_aprendiz = equipamento_arma_inteligencia_agilidade(
    identificador='cajado_de_aprendiz',
    sprite_x=6,
    sprite_y=9,
    nome='Cajado de Aprendiz',
    descricao='"Use com responsabilidade"',
    inteligencia=3,
    agilidade=2
)


cajado_de_conducao = equipamento_arma_inteligencia_agilidade(
    identificador='cajado_de_conducao',
    sprite_x=7,
    sprite_y=9,
    nome='Cajado de Condução',
    descricao='Parece canalizar minha energia',
    inteligencia=7,
    agilidade=3
)


cajado_de_grao_mestre = equipamento_arma_inteligencia_agilidade(
    identificador='cajado_de_grao_mestre',
    sprite_x=8,
    sprite_y=9,
    nome='Cajado de Grão Mestre',
    descricao='O equilíbrio...',
    inteligencia=14,
    agilidade=6
)


centro_do_universo = equipamento_arma_inteligencia_agilidade(
    identificador='centro_do_universo',
    sprite_x=9,
    sprite_y=9,
    nome='Centro do Universo',
    descricao='Tanto...PODER!',
    inteligencia=20,
    agilidade=12
)
