from typing import Dict, Any
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime

from app.config import get_config
from app.services.game_state import GameState

class WebSocketManager:
    def __init__(self):
        self.connected_players: Dict[int, WebSocket] = {}
        self.game_states: Dict[int, GameState] = {}
        self.config = get_config()

    async def connect(self, websocket: WebSocket) -> int:
        """Aceita uma nova conexão WebSocket e retorna seu ID."""
        await websocket.accept()
        player_id = id(websocket)
        self.connected_players[player_id] = websocket
        self.game_states[player_id] = GameState()
        return player_id

    async def disconnect(self, player_id: int):
        """Remove uma conexão WebSocket e seu estado de jogo."""
        if player_id in self.connected_players:
            del self.connected_players[player_id]
        if player_id in self.game_states:
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
                    nome=message["data"]["nome"],
                    descricao=message["data"]["descricao"],
                    email=message["data"]["email"],
                    senha=message["data"]["senha"],
                    classe=message["data"]["classe"]
                )
            
            elif message["type"] == "pausar":
                game_state.pausar(message["data"]["pausado"])
            
            elif message["type"] == "aumentar_atributo":
                game_state.aumentar_atributo(message["data"]["atributo"])
            
            elif message["type"] == "acao_jogador":
                game_state.set_acao_jogador(message["data"]["acao"])
            
            elif message["type"] == "subir_nivel_classe":
                game_state.subir_nivel_classe(message["data"].get("classe", None))

            # Envia atualização do estado do jogo para o jogador
            await self.send_message(player_id, {
                "type": "update",
                **game_state.get_websocket_data(),
                "logs": game_state.get_logs()
            })

        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            await self.send_message(player_id, {
                "type": "error",
                "message": str(e)
            })

    async def process_game_loop(self):
        """Processa o loop principal do jogo para todos os jogadores."""
        while True:
            for player_id, game_state in self.game_states.items():
                if not game_state.pausado:
                    await game_state.processar_turno()
                    await self.send_message(player_id, {
                        "type": "update",
                        **game_state.get_websocket_data(),
                        "logs": game_state.get_logs()
                    })
            
            await asyncio.sleep(self.config["combat"]["timeout_turno"])

# Instância global do gerenciador de WebSocket
websocket_manager = WebSocketManager() 