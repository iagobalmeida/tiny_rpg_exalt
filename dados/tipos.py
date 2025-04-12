import math
import random
from datetime import datetime
from typing import List, Literal, Optional, Tuple, Union
from uuid import uuid4

from pydantic import BaseModel, Field

OBJETOS_TIPOS = Literal['OBJETO', 'EQUIPAMENTO', 'NPC', 'INIMIGO', 'HUMANO', 'MASMORRA', 'JOGADOR']
EQUIPAMENTO_TIPOS = Literal['CAPACETE', 'ARMADURA', 'ARMA', 'ACESSÓRIO']


def hour():
    now = datetime.now()
    return now.strftime('%H:%M:%S')


class Abstrato(BaseModel):
    tipo: OBJETOS_TIPOS
    nome: str
    descricao: str
    sprite_nome: Optional[str] = 'monsters.png'
    sprite_largura: Optional[int] = 384
    sprite_altura: Optional[int] = 416
    sprite_x: Optional[int] = None
    sprite_y: Optional[int] = None
    id_unico: str = Field(default_factory=lambda: str(uuid4()))


class Objeto(Abstrato):
    forca: int
    agilidade: int
    resistencia: int
    inteligencia: int


class Equipamento(Objeto):
    tipo: Literal['EQUIPAMENTO'] = Field(default='EQUIPAMENTO')
    equipamento_tipo: EQUIPAMENTO_TIPOS


class Entidade(Objeto):
    level: int = Field(default=1)
    vida: int
    energia: int
    experiencia: int
    ouro: int = Field(default=0)
    level: int
    vida_maxima: int = Field(default=0)
    energia_maxima: int = Field(default=0)

    def model_post_init(self, __context):
        if self.vida_maxima == 0:
            object.__setattr__(self, 'vida_maxima', self.vida)
        if self.energia_maxima == 0:
            object.__setattr__(self, 'energia_maxima', self.energia)

    @property
    def renascido(self):
        classname = self.__class__
        values = self.model_dump()
        values['vida'] = self.vida_maxima
        values['energia'] = self.energia_maxima
        del values['id_unico']
        return classname(**values)


class Inimigo(Entidade):
    tipo: Literal['INIMIGO'] = Field(default='INIMIGO')


class Humano(Entidade):
    tipo: Literal['HUMANO'] = Field(default='HUMANO')
    sprite_nome: str = 'rogues.png'
    sprite_largura: int = 224
    sprite_altura: int = 224


SPRITES_X_Y_CLASSES = {
    'APRENDIZ': (1, 5),
    'SELVAGEM': (0, 3, 'BÁRBARO'),
    'BÁRBARO': (1, 3),
    'MAGO': (5, 2, 'SACERDOTE'),
    'SACERDOTE': (6, 2),
    'GUERREIRO': (0, 1, 'PALADINO'),
    'PALADINO': (4, 1),
}


class Jogador(Humano):
    tipo: Literal['JOGADOR'] = Field(default='JOGADOR')
    email: str
    senha: str
    nivel_classe: int = Field(default=1)
    classe: Literal[
        'APRENDIZ',
        'SELVAGEM', 'BÁRBARO',
        'MAGO', 'SACERDOTE',
        'GUERREIRO', 'PALADINO',
    ]
    pontos_disponiveis: int = Field(default=0)

    @property
    def deve_subir_nivel(self):
        return self.experiencia >= 15 + self.level * 15

    @classmethod
    def primeiro_nivel(cls, nome: str, descricao: str, email: str, senha: str, classe: Literal['APRENDIZ', 'LADRÃO', 'ASSASSINO', 'MAGO', 'SACERDOTE']):
        return cls(
            nome=nome,
            descricao=descricao,
            email=email,
            senha=senha,
            classe=classe,
            level=1,
            experiencia=0,
            energia=25,
            energia_maxima=25,
            vida=25,
            vida_maxima=25,
            forca=1,
            nivel_classe=1,
            agilidade=1,
            resistencia=1,
            inteligencia=1,
            pontos_disponiveis=0,
            sprite_x=SPRITES_X_Y_CLASSES[classe][0],
            sprite_y=SPRITES_X_Y_CLASSES[classe][1]
        )

    @property
    def classe_proxima(self):
        return SPRITES_X_Y_CLASSES[self.classe][2]

    def atribuir_ponto(self, atributo: Literal['forca', 'agilidade', 'resistencia', 'inteligencia']):
        if self.pontos_disponiveis > 0:
            self.pontos_disponiveis -= 1
            setattr(self, atributo, getattr(self, atributo) + 1)

    def subir_nivel(self):
        self.experiencia -= 15 + self.level * 15
        self.level += 1
        self.pontos_disponiveis += 3

        self.energia_maxima += math.ceil(self.level/10) * 8
        self.vida_maxima += math.ceil(self.level/10) * 5
        self.energia = self.energia_maxima
        self.vida = self.vida_maxima

    def subir_nivel_classe(self, nome_classe: Union[Literal['SELVAGEM', 'MAGO', 'GUERREIRO'], None] = None):
        if nome_classe is None:
            nome_classe = self.classe_proxima

        if self.nivel_classe == 1 and self.level >= 15:
            self.nivel_classe = 2
            self.pontos_disponiveis += 3

            self.energia_maxima += math.ceil(self.level/10) * 8
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * 5
            self.vida = self.vida_maxima
            self.classe = nome_classe
            self.sprite_x = SPRITES_X_Y_CLASSES[nome_classe][0]
            self.sprite_y = SPRITES_X_Y_CLASSES[nome_classe][1]

        elif self.nivel_classe == 2 and self.level >= 30:
            self.nivel_classe = 3
            self.pontos_disponiveis += 3

            self.energia_maxima += math.ceil(self.level/10) * 8
            self.energia = self.energia_maxima
            self.vida_maxima += math.ceil(self.level/10) * 5
            self.vida = self.vida_maxima
            self.classe = nome_classe
            self.sprite_x = SPRITES_X_Y_CLASSES[nome_classe][0]
            self.sprite_y = SPRITES_X_Y_CLASSES[nome_classe][1]


class Combate:
    def __init__(self, jogador: Jogador, inimigo: Inimigo):
        self.jogador = jogador
        self.acao_jogador = None
        self.inimigo = inimigo
        self.acao_inimigo = None

    def calcular_dano(self, de: Entidade, para: Entidade) -> int:
        # Base do dano é a força do atacante
        dano_base = de.forca

        # Fator de força: quanto maior a diferença, mais impacto tem
        diferenca_forca = de.forca - para.resistencia
        fator_forca = 1 + (diferenca_forca / 20)  # Limita o impacto da diferença

        # Fator de resistência: reduz o dano baseado na resistência do alvo
        fator_resistencia = max(0.5, 1 - (para.resistencia / (de.forca + 10)))

        # Adiciona um fator aleatório entre 0.8 e 1.2
        fator_aleatorio = random.uniform(0.8, 1.2)

        # Cálculo final do dano
        dano = round(dano_base * fator_forca * fator_resistencia * fator_aleatorio)

        # Garante que o dano mínimo seja 1
        return max(1, dano)

    def calcular_chance_acerto(self, de: Entidade, para: Entidade) -> bool:
        # Base de chance de acerto é 50%
        chance_base = 50

        # Calcula a diferença de agilidade
        diferenca_agilidade = de.agilidade - para.agilidade

        # Se a diferença for menor que 8, usa um fator menor
        if abs(diferenca_agilidade) <= 8:
            fator_agilidade = 1 + (diferenca_agilidade / 20)
        else:
            # Se a diferença for maior que 8, usa um fator mais impactante
            fator_agilidade = 1 + (diferenca_agilidade / 10)

        # Ajusta a chance base pelo fator de agilidade
        chance_ajustada = chance_base * fator_agilidade

        # Adiciona um pequeno fator aleatório
        chance_final = chance_ajustada + random.uniform(-5, 5)

        # Garante que a chance fique entre 5% e 95%
        chance_final = max(5, min(95, chance_final))

        # Rola um número aleatório e verifica se acertou
        return random.randint(1, 100) <= chance_final

    async def executar_turno_jogador(self, logs: List[str]) -> Tuple[bool, List[str]]:
        if self.jogador.vida <= 0:
            logs.append(f'{hour()} - {self.jogador.nome} morreu')
            return True, logs

        if self.calcular_chance_acerto(self.jogador, self.inimigo):
            dano = self.calcular_dano(self.jogador, self.inimigo)
            logs.append(f'{hour()} - {self.jogador.nome} causou {dano} de dano em {self.inimigo.nome}')
            self.inimigo.vida = max(0, self.inimigo.vida - dano)
        else:
            logs.append(f'{hour()} - {self.jogador.nome} errou o ataque')
        return False, logs

    async def executar_turno_inimigo(self, logs: List[str]) -> Tuple[bool, List[str]]:
        if self.inimigo.vida <= 0:
            logs.append(f'{hour()} - {self.inimigo.nome} morreu')
            return True, logs

        if self.calcular_chance_acerto(self.inimigo, self.jogador):
            dano = self.calcular_dano(self.inimigo, self.jogador)
            logs.append(f'{hour()} - {self.inimigo.nome} causou {dano} de dano em {self.jogador.nome}')
            self.jogador.vida = max(0, self.jogador.vida - dano)
        else:
            logs.append(f'{hour()} - {self.inimigo.nome} errou o ataque')
        return False, logs

    async def executar_acao_jogador(self, logs: List[str]) -> Tuple[bool, List[str]]:
        if self.acao_jogador is None:
            return False, logs

        if self.acao_jogador == 'ataque_especial' and self.jogador.energia >= 10:
            self.jogador.energia -= 10
            dano = self.calcular_dano(self.jogador, self.inimigo)
            self.inimigo.vida = max(0, self.inimigo.vida - dano*2)

        self.acao_jogador = None

        return True, logs

    async def executar_turno(self) -> Tuple[bool, List[str]]:
        logs = []

        jogador_morreu, logs = await self.executar_turno_jogador(logs)
        if jogador_morreu:
            return 'inimigo', logs

        _, logs = await self.executar_acao_jogador(logs)

        inimigo_morreu, logs = await self.executar_turno_inimigo(logs)
        if inimigo_morreu:
            return 'jogador', logs

        return False, logs


class Masmorra:
    tipo: Literal['MASMORRA'] = Field(default='MASMORRA')
    nome: str
    descricao: str
    imagem_background: str
    lista_inimigos: List[Inimigo]
    passos: Optional[int] = 0
    humano: Optional[Humano] = None
    combate: Optional[Combate] = None
    combate_acabou: bool = Field(default=False)
    pausado: Optional[bool] = False

    def __init__(self, nome: str, descricao: str, lista_inimigos: List[Inimigo], imagem_background: str):
        self.nome = nome
        self.descricao = descricao
        self.lista_inimigos = lista_inimigos
        self.imagem_background = imagem_background

    def clone(self):
        return self.__class__(self.nome, self.descricao, self.lista_inimigos, self.imagem_background)

    @property
    def total_passos(self):
        return math.ceil(len(self.lista_inimigos)/1.5) * len(self.lista_inimigos)

    def inimigo_aleatorio(self) -> Inimigo:
        '''Pega um inimigo aleatório baseado no número de passos atual.
        A cada 10 passos, novos inimigos são desbloqueados.'''
        tamanho_intervalo = math.ceil(len(self.lista_inimigos)/1.5)
        indice_maximo = self.passos // tamanho_intervalo
        indice_minimo = max(0, indice_maximo - 1)

        # Garante que os índices não ultrapassem o tamanho da lista
        indice_maximo = min(indice_maximo, len(self.lista_inimigos) - 1)
        indice_minimo = min(indice_minimo, len(self.lista_inimigos) - 1)

        # Escolhe aleatoriamente um inimigo entre o índice mínimo e máximo
        indice_escolhido = random.randint(indice_minimo, indice_maximo)
        inimigo = self.lista_inimigos[indice_escolhido]

        return inimigo.renascido

    def iniciar_combate(self, jogador: Jogador):
        self.jogador = jogador
        self.combate = Combate(self.jogador, self.inimigo_aleatorio())
        self.combate_acabou = False

    async def executar_turno(self) -> List[str]:
        resultado_turno, logs = await self.combate.executar_turno()
        if not resultado_turno:
            return logs

        if resultado_turno == 'inimigo':
            self.jogador = self.jogador.renascido
            logs.append(f'{hour()} - {self.jogador.nome} morreu')
            experiencia_perdida = int(self.combate.inimigo.experiencia * 1.5)
            self.jogador.experiencia = max(0, self.jogador.experiencia - experiencia_perdida)
            self.jogador.ouro = max(0, int(self.jogador.ouro - self.combate.inimigo.ouro/2))
            logs.append(f'{hour()} - {self.jogador.nome} perdeu {experiencia_perdida} de experiência e {self.combate.inimigo.ouro} de ouro')
            self.passos = 0

        elif resultado_turno == 'jogador':
            experiencia_ganha = self.combate.inimigo.experiencia
            self.jogador.experiencia += experiencia_ganha
            self.jogador.ouro = max(0, self.jogador.ouro + self.combate.inimigo.ouro)
            logs.append(f'{hour()} - {self.jogador.nome} ganhou {experiencia_ganha} de experiência e {self.combate.inimigo.ouro} de ouro')
            self.passos += 1
            if self.jogador.deve_subir_nivel:
                self.jogador.subir_nivel()
                logs.append(f'{hour()} - {self.jogador.nome} subiu de nível')

        self.combate_acabou = True
        return logs

    @property
    def websocket_data(self):
        return {
            "masmorra": {
                "nome": self.nome,
                "descricao": self.descricao,
                "pausado": self.pausado,
                "passos": self.passos,
                "total_passos": self.total_passos,
                "imagem_background": self.imagem_background
            },
            "inimigo": self.combate.inimigo.model_dump(),
            "jogador": self.combate.jogador.model_dump()
        }


class Casa(Masmorra):
    async def executar_turno(self) -> List[str]:
        cura = math.ceil(self.jogador.vida * 0.2)
        cura_energia = math.ceil(self.jogador.energia * 0.2)
        logs = [f'{hour()} - {self.jogador.nome} descansou e recuperou {cura} de vida e {cura_energia} de energia']
        self.jogador.vida = min(max(1, self.jogador.vida + cura), self.jogador.vida_maxima)
        self.jogador.energia = min(max(1, self.jogador.energia + cura_energia), self.jogador.energia_maxima)
        return logs
