import json
import math
from datetime import datetime
from logging import getLogger
from typing import Any, Dict, List

from config import get_config
from models.item import UNION_ITEM
from models.itens import ITEMS
from models.jogador import Classes, Jogador
from models.masmorra import Masmorra
from services.combate import Combate

log = getLogger('uvicorn')
class GameState:
    def __init__(self, timeout_turno: float):
        self.config = get_config()
        self.jogador: Jogador = None
        self.inventario: List[UNION_ITEM] = []
        self.masmorra: Masmorra = None
        self.combate: Combate = None
        self.combate_acabou: bool = False
        self.pausado: bool = False
        self.logs: List[str] = []
        self.ultima_execucao: datetime = None
        self.timeout_turno = timeout_turno

    @property
    def deve_executar(self):
        if not self.ultima_execucao: return True
        return (datetime.now() - self.ultima_execucao).total_seconds() > self.timeout_turno

    def get_websocket_data(self) -> Dict[str, Any]:
        """Retorna os dados necessários para o frontend."""
        ret = {
            "jogador": self.jogador.get_websocket_data() if self.jogador else None,
            "inimigo": self.combate.inimigo.model_dump() if self.combate else None,
            "masmorra": self.masmorra.get_websocket_data() if self.masmorra else None,
            "inventario": [
                i.model_dump()
                for i in self.inventario
            ]
        }
        return ret

    def get_logs(self) -> List[str]:
        """Retorna e limpa os logs do jogo."""
        logs = self.logs.copy()
        self.logs.clear()
        return logs
    
    async def logout(self):
        # TODO: Armazena no banco estado do jogador
        pass

    async def login(self, nome: str, descricao: str, email: str, senha: str, classe: str):
        """Inicializa um novo jogador."""
        classe = Classes[classe]

        inventario_json = """
        [
            {"nome":"faca_de_cozinha","quantidade":1,"em_uso":true}
        ]
        """

        self.inventario = []
        if inventario_json:
            inventario_entrada = json.loads(inventario_json)
            for i in inventario_entrada:
                item_objeto = ITEMS.get(i['nome'], None)
                if not item_objeto:
                    continue
                item_objeto = item_objeto.model_copy()
                item_objeto.quantidade = i['quantidade']
                if i.get('em_uso', False):
                    item_objeto.em_uso = True
                self.inventario.append(item_objeto)

        
        # TODO: Carrega do banco o estado do jogador
        self.jogador = Jogador.primeiro_nivel(
            nome=nome,
            descricao=descricao,
            email=email,
            senha=senha,
            classe=classe,
            inventario_json=inventario_json
        )
        self.masmorra = Masmorra.casa()
        self.iniciar_combate(renascer=True)

    def iniciar_combate(self, renascer: bool = False):
        """Inicia um novo combate na masmorra."""
        if renascer:
            self.jogador = self.jogador.renascido
        inimigo = self.masmorra.inimigo_aleatorio()
        self.combate = Combate(self.jogador, inimigo)
        self.combate_acabou = False

    async def mudar_masmorra(self, nome_masmorra: str):
        """Muda a masmorra atual do jogador."""
        if not self.masmorra:
            return
        nova_masmorra = Masmorra.por_nome(nome_masmorra)
        nova_masmorra.pausado = self.masmorra.pausado if self.masmorra.__class__.__name__ != 'Casa' else False
        self.masmorra = nova_masmorra
        self.iniciar_combate()

    def pausar(self, pausado: bool):
        """Pausa ou despausa o jogo."""
        if self.masmorra:
            self.masmorra.pausado = pausado
            self.pausado = pausado

    def aumentar_atributo(self, atributo: str):
        """Aumenta um atributo do jogador."""
        if self.jogador:
            self.jogador.atribuir_ponto(atributo)

    def set_acao_jogador(self, acao: str, item_indice:int=None):
        """Define a ação do jogador no combate."""
        if self.combate:
            self.combate.acao_jogador = acao
            if item_indice:
                self.combate.acao_jogador_item_indice = int(item_indice)

    def subir_nivel_classe(self, classe: str = None):
        """Sobe o nível da classe do jogador."""
        if self.jogador:
            self.jogador.subir_nivel_classe(classe)

    async def processar_turno(self):
        """Processa um turno do jogo."""
        try:
            if not self.masmorra or not self.combate:
                return

            if self.masmorra.nome == 'Casa':
                cura = math.ceil(self.jogador.vida * 0.2)
                cura_energia = math.ceil(self.jogador.energia * 0.2)
                self.jogador.vida = min(max(1, self.jogador.vida + cura), self.jogador.vida_maxima)
                self.jogador.energia = min(max(1, self.jogador.energia + cura_energia), self.jogador.energia_maxima)
                return

            if self.combate_acabou:
                self.iniciar_combate()
                return

            vencedor = await self.combate.executar_turno()
            if not vencedor:
                return

            if vencedor == 'inimigo':
                self.jogador = self.jogador.renascido
                experiencia_perdida = int(self.combate.inimigo.experiencia * 1.5)
                self.jogador.experiencia = max(0, self.jogador.experiencia - experiencia_perdida)
                self.jogador.ouro = max(0, int(self.jogador.ouro - self.combate.inimigo.ouro/2))
                self.masmorra.passos = 0

            elif vencedor == 'jogador':
                self.jogador.progredir_missao(self.combate.inimigo.nome)

                item_aletorio = self.masmorra.item_aleatorio()
                if item_aletorio:
                    # TODO: Soma quantidade se já estiver no inventário
                    self.adicionar_item(item_aletorio)

                experiencia_ganha = self.combate.inimigo.experiencia
                self.jogador.experiencia += experiencia_ganha
                self.jogador.ouro = max(0, self.jogador.ouro + self.combate.inimigo.ouro)
                self.masmorra.passos += 1
                if self.jogador.deve_subir_nivel:
                    self.jogador.subir_nivel()

            self.combate_acabou = True
            return
        except Exception as ex:
            log.exception(ex)
            pass
        finally:
            self.ultima_execucao = datetime.now()

    def adicionar_item(self, item: UNION_ITEM):
        for inventario_item in self.inventario:
            if inventario_item.nome == item.nome:
                inventario_item.quantidade += item.quantidade
                return
        self.inventario.append(item)

    def remover_item(self, item: UNION_ITEM, quantidade:int=1):
        for inventario_item in self.inventario:
            if inventario_item.nome == item.nome:
                inventario_item.quantidade = max(inventario_item.quantidade - quantidade, 0)
                break
        # Remove itens com quantidade 0
        self.inventario = [i for i in self.inventario if i.quantidade > 0]

    def descartar_item(self, item_indice:int, todos:bool=False):
        if item_indice >= len(self.inventario):
            return
        if todos:
            del self.inventario[item_indice]
            return
        self.remover_item(self.inventario[item_indice].model_copy())

    def usar_item(self, item_indice:int):
        if item_indice >= len(self.inventario):
            return
        
        self.inventario[item_indice].usar(self.jogador)
        self.remover_item(self.inventario[item_indice].model_copy())

    @staticmethod
    def hour() -> str:
        """Retorna a hora atual formatada."""
        return datetime.now().strftime('%H:%M:%S')
