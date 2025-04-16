import asyncio
import json
import math
from datetime import datetime
from logging import getLogger
from typing import Any, Dict, List, Optional

from config import get_config
from data import itens
from fastapi import HTTPException
from models.item import UNION_ITEM
from models.jogador import Jogador
from models.masmorra import Masmorra
from services import db
from services.combate import Combate

log = getLogger('uvicorn')

TAMANHO_SLOT_INVENTARIO = 16


class GameState:
    def __init__(self, timeout_turno: float):
        self.config = get_config()
        self.jogador: Jogador = None
        self.inventario: List[UNION_ITEM] = []
        self.tamanho_inventario: Optional[int] = 8
        self.masmorra: Masmorra = None
        self.combate: Combate = None
        self.combate_acabou: bool = False
        self.pausado: bool = False
        self.logs: List[str] = []
        self.ultima_execucao: datetime = None
        self.timeout_turno = timeout_turno

    @property
    def deve_executar(self):
        if not self.ultima_execucao:
            return True
        return (datetime.now() - self.ultima_execucao).total_seconds() > self.timeout_turno

    def get_websocket_data(self) -> Dict[str, Any]:
        """Retorna os dados necessários para o frontend."""
        ret = {
            "jogador": self.jogador.get_websocket_data() if self.jogador else None,
            "atributos_equipamentos_jogador": self.atributos_equipamentos_jogador if self.jogador else None,
            "inimigo": self.combate.inimigo.model_dump() if self.combate else None,
            "masmorra": self.masmorra.get_websocket_data() if self.masmorra else None,
            "tamanho_inventario": self.tamanho_inventario,
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

    async def signup(self, nome: str, email: str, senha: str, confirmar_senha: str):
        if senha != confirmar_senha:
            raise ValueError('As senhas não batem!')
        db.create_usuario(nome, email, senha)
        return await self.login(email=email, senha=senha)

    async def login(self, email: str, senha: str):
        """Inicializa um novo jogador."""

        usuario_registro = db.get_usuario_by_email(email=email)
        if not usuario_registro or usuario_registro.senha != senha:
            raise HTTPException(401, 'Não autorizado')

        inventario_registros = db.get_inventario_by_usuario_id(usuario_registro.id)

        self.jogador = Jogador.a_partir_de_usuario(usuario_registro)
        self.masmorra = Masmorra.casa()
        self.iniciar_combate(renascer=True)

        if '@teste.com' in usuario_registro.email:
            # Adiciona todos os itens do jogo para o jogador
            self.tamanho_inventario = 64
            self.inventario = []

            for variavel_nome in dir(itens):
                variavel = getattr(itens, variavel_nome)
                if getattr(variavel, 'identificador', None):
                    item = variavel.model_copy()
                    if item.tipo == 'CONSUMIVEL':
                        item.quantidade = 25
                    self.adicionar_item(item)
        else:
            self.tamanho_inventario = usuario_registro.tamanho_inventario
            self.inventario = []
            for i in inventario_registros:
                item_objeto = getattr(itens, i.item_nome.lower(), None)
                if not item_objeto:
                    continue
                item_objeto = item_objeto.model_copy()
                item_objeto.quantidade = i.quantidade
                if getattr(i, 'em_uso', False):
                    item_objeto.em_uso = True
                self.inventario.append(item_objeto)

        await asyncio.sleep(0.75)

    async def logout(self):
        if self.jogador:
            payload = self.jogador.model_dump()
            payload['missoes'] = json.dumps(payload['missoes'])
            payload['classe'] = self.jogador.classe.nome
            payload['energia'] = self.jogador.energia_maxima
            payload['vida'] = self.jogador.vida_maxima
            db.update_usuario(self.jogador.id, payload)

        if self.inventario:
            inventario_registros = [
                db.UsuarioInventario(
                    usuario_id=self.jogador.id,
                    item_nome=i.identificador,
                    quantidade=i.quantidade,
                    em_uso=getattr(i, 'em_uso', False)
                )
                for i in self.inventario
            ]
            db.update_inventario_by_usuario_id(self.jogador.id, inventario_registros)

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

    def set_acao_jogador(self, acao: str, item_indice: int = None):
        """Define a ação do jogador no combate."""
        if self.combate:
            self.combate.acao_jogador = acao
            if item_indice:
                self.combate.acao_jogador_item_indice = int(item_indice)

    def subir_nivel_classe(self, classe: str = None):
        """Sobe o nível da classe do jogador."""
        if self.jogador:
            self.jogador.subir_nivel_classe(classe)

    @property
    def atributos_equipamentos_jogador(self):
        retorno = {
            'forca': 0,
            'resistencia': 0,
            'agilidade': 0,
            'inteligencia': 0
        }
        for i in self.inventario:
            if not i.tipo == 'EQUIPAMENTO' or not i.em_uso:
                continue
            retorno['forca'] += i.forca
            retorno['resistencia'] += i.resistencia
            retorno['agilidade'] += i.agilidade
            retorno['inteligencia'] += i.inteligencia
        return retorno

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
                self.jogador.estado_nome = None
                self.jogador.estado_duracao = 0
                return

            if self.combate_acabou:
                self.iniciar_combate()
                return

            vencedor = await self.combate.executar_turno(self.atributos_equipamentos_jogador)
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
                if inventario_item.tipo == 'CONSUMIVEL':  # Só soma consumível, equipamentos e outros só pode 1 por slot
                    if inventario_item.quantidade < TAMANHO_SLOT_INVENTARIO:
                        inventario_item.quantidade = min(TAMANHO_SLOT_INVENTARIO, inventario_item.quantidade+item.quantidade)
                return

        if len(self.inventario) < self.tamanho_inventario:
            self.inventario.append(item)

    def remover_item(self, item: UNION_ITEM, quantidade: int = 1):
        for inventario_item in self.inventario:
            if inventario_item.nome == item.nome:
                inventario_item.quantidade = max(inventario_item.quantidade - quantidade, 0)
                break
        self.inventario = [i for i in self.inventario if i.quantidade > 0]

    def descartar_item(self, item_indice: int, todos: bool = False):
        if item_indice >= len(self.inventario):
            return
        if todos:
            del self.inventario[item_indice]
            return
        self.remover_item(self.inventario[item_indice].model_copy())

    def usar_item(self, item_indice: int):
        if item_indice >= len(self.inventario):
            return

        item = self.inventario[item_indice]

        if item.tipo == 'EQUIPAMENTO':
            if item.em_uso:
                item.em_uso = False
            else:
                equipamento_tipo = item.equipamento_tipo
                for i in self.inventario:
                    if i.tipo == 'EQUIPAMENTO' and i.em_uso and i.equipamento_tipo == equipamento_tipo:
                        i.em_uso = False
                item.em_uso = True
        elif item.tipo == 'CONSUMIVEL':
            usado = self.inventario[item_indice].usar(self.jogador)
            if usado:
                self.remover_item(self.inventario[item_indice].model_copy())
