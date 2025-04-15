import asyncio
import json
from datetime import datetime
from logging import getLogger
from typing import Any, Dict

from config import get_config
from fastapi import WebSocket
from models.masmorras import MASMORRAS
from services.game_state import GameState

log = getLogger('uvicorn')


class WebSocketManager:
    def __init__(self):
        self.connected_players: Dict[int, WebSocket] = {}
        self.ip_to_player_id: Dict[str, int] = {}
        self.game_states: Dict[int, GameState] = {}
        self.game_states_last_payloads: Dict[int, dict] = {}
        self.config = get_config()

    async def connect(self, websocket: WebSocket) -> int:
        """Aceita uma nova conexão WebSocket e retorna seu ID."""
        client_ip = websocket.client.host

        # Bloquear múltiplas conexões do mesmo IP
        if client_ip in self.ip_to_player_id:
            await websocket.close(code=4001)
            raise Exception(f"IP {client_ip} já conectado")

        await websocket.accept()
        player_id = id(websocket)

        self.connected_players[player_id] = websocket
        self.ip_to_player_id[client_ip] = player_id
        self.game_states[player_id] = GameState(self.config["combat"]["timeout_turno"])

        return player_id

    async def disconnect(self, player_id: int):
        """Remove uma conexão WebSocket e seu estado de jogo."""
        if player_id in self.connected_players:
            client_ip = self.connected_players[player_id].client.host
            self.ip_to_player_id.pop(client_ip, None)
            del self.connected_players[player_id]

        if player_id in self.game_states:
            await self.game_states[player_id].logout()
            del self.game_states[player_id]

    async def send_message(self, player_id: int, message: Dict[str, Any]):
        """Envia uma mensagem para um jogador específico."""
        if player_id in self.connected_players:
            await self.connected_players[player_id].send_json(message)

    async def broadcast(self, message: Dict[str, Any], exclude: int = None):
        """Envia uma mensagem para todos os jogadores conectados, exceto o especificado."""
        for player_id, websocket in self.connected_players.items():
            if player_id != exclude:
                await websocket.send_json(message)

    async def handle_message(self, player_id: int, message: Dict[str, Any]):
        """Processa uma mensagem recebida de um jogador."""
        game_state = self.game_states[player_id]

        try:
            if message["type"] == "mudar_masmorra":
                await game_state.mudar_masmorra(message["data"]["masmorra"])

            elif message["type"] == "login":
                await game_state.login(
                    email=message["data"]["email"],
                    senha=message["data"]["senha"]
                )

            elif message["type"] == "signup":
                await game_state.signup(
                    nome=message["data"]["nome"],
                    email=message["data"]["email"],
                    senha=message["data"]["senha"],
                    confirmar_senha=message["data"]["confirmar_senha"],
                )

            elif message["type"] == "pausar":
                game_state.pausar(message["data"]["pausado"])

            elif message["type"] == "aumentar_atributo":
                game_state.aumentar_atributo(message["data"]["atributo"])

            elif message["type"] == "acao_jogador":
                game_state.set_acao_jogador(message["data"]["acao"])

            elif message["type"] == "usar_item":
                item_id = message["data"].get("item_indice", None)
                if item_id:
                    game_state.usar_item(int(item_id))

            elif message["type"] == "descartar_item":
                item_id = message["data"].get("item_indice", None)
                if item_id:
                    game_state.descartar_item(int(item_id))

            elif message["type"] == "descartar_item_todos":
                item_id = message["data"].get("item_indice", None)
                if item_id:
                    game_state.descartar_item(int(item_id), todos=True)

            elif message["type"] == "subir_nivel_classe":
                game_state.subir_nivel_classe(message["data"].get("classe", None))

            # Envia atualização do estado do jogo para o jogador
            await self.send_update(player_id)

        except Exception as e:
            log.exception(e)
            print(f"Erro ao processar mensagem: {e}")
            await self.send_message(player_id, {
                "type": "error",
                "message": str(e)
            })

    async def send_update(self, player_id: int):
        game_state = self.game_states[player_id]
        update_payload = {
            "type": "update",
            **game_state.get_websocket_data(),
            "masmorras": [
                {
                    "chave": chave,
                    "nome": masmorra.nome
                }
                for chave, masmorra in MASMORRAS.items()
            ],
            "logs": game_state.get_logs()
        }

        # TODO: Só manda update das coisas que foram alteradas

        # if self.game_states_last_payloads.get(player_id):
        #     for key, value in self.game_states_last_payloads.items():
        #         if update_payload.get(key, None) == value:
        #             del update_payload[key]

        await self.send_message(player_id, update_payload)

        self.game_states_last_payloads[player_id] = update_payload

    async def process_game_loop(self):
        """Processa o loop principal do jogo para todos os jogadores."""
        while True:
            for player_id, game_state in self.game_states.items():
                if not game_state.pausado and game_state.deve_executar:
                    await game_state.processar_turno()
                    await self.send_update(player_id)
            await asyncio.sleep(0.1)


# Instância global do gerenciador de WebSocket
websocket_manager = WebSocketManager()
