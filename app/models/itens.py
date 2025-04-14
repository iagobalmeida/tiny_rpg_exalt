from models.item import ConsumivelCura, Equipamento

queijo = ConsumivelCura(
    fator=5,
    nome='Queijo',
    descricao=[
        'Não parece tão estragado...',
        '+5 ATTR_VIDA'
    ],
    sprite_x=0,
    sprite_y=25
)

pocao_pequena = ConsumivelCura(
    fator=15,
    nome='Poção Pequena',
    descricao=[
        'Tem um gosto duvidoso.',
        '+15 ATTR_VIDA'
    ],
    sprite_x=0,
    sprite_y=19
)


pocao_media = ConsumivelCura(
    fator=45,
    sprite_x=1,
    sprite_y=19,
    nome='Poção Média',
    descricao=[
        'Parece bom.',
        '+45 ATTR_VIDA'
    ]
)

pocao_grande = ConsumivelCura(
    fator=125,
    sprite_x=3,
    sprite_y=19,
    nome='Poção Grande',
    descricao=[
        'Um litro de puro sabor!',
        '+125 ATTR_VIDA'
    ]
)

pocao_suprema = ConsumivelCura(
    fator=500,
    sprite_x=4,
    sprite_y=20,
    nome='Poção Suprema',
    descricao=[
        'É forte, mas é bom!',
        '+500 ATTR_VIDA'
    ]
)

faca_de_cozinha = Equipamento(
    sprite_x=0,
    sprite_y=0,
    nome='Faca de Cozinha',
    equipamento_tipo='ARMA',
    descricao=[
        'Essa era a melhor faca...',
        '+ 1 ATTR_FORCA',
        '+ 1 ATTR_AGILIDADE'
    ],
    forca=1,
    agilidade=1
)

gorro_de_la = Equipamento(
    sprite_x=0,
    sprite_y=15,
    nome='Gorro de lã',
    equipamento_tipo='ARMADURA',
    descricao=[
        'Não tá frio, mas vai saber.',
        '+ 1 ATTR_RESISTENCIA'
    ],
    resistencia=1
)

ITEMS = {
    'queijo': queijo,
    'pocao_pequena': pocao_pequena,
    'pocao_media': pocao_media,
    'pocao_grande': pocao_grande,
    'pocao_suprema': pocao_suprema,
    'faca_de_cozinha': faca_de_cozinha,
    'gorro_de_la': gorro_de_la
}