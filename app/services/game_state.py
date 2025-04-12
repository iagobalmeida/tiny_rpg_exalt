from typing import List, Dict, Any
from datetime import datetime

from app.config import get_config
from app.models.jogador import Jogador
from app.models.masmorra import Masmorra
from app.services.combate import Combate

class GameState:
    def __init__(self):
        self.config = get_config()
        self.jogador: Jogador = None
        self.masmorra: Masmorra = None
        self.combate: Combate = None
        self.pausado: bool = False
        self.logs: List[str] = []

    def get_websocket_data(self) -> Dict[str, Any]:
        """Retorna os dados necessários para o frontend."""
        return {
            "jogador": self.jogador.dict() if self.jogador else None,
            "inimigo": self.combate.inimigo.dict() if self.combate else None,
            "masmorra": self.masmorra.dict() if self.masmorra else None
        }

    def get_logs(self) -> List[str]:
        """Retorna e limpa os logs do jogo."""
        logs = self.logs.copy()
        self.logs.clear()
        return logs

    async def login(self, nome: str, descricao: str, email: str, senha: str, classe: str):
        """Inicializa um novo jogador."""
        self.jogador = Jogador.primeiro_nivel(
            nome=nome,
            descricao=descricao,
            email=email,
            senha=senha,
            classe=classe
        )
        self.masmorra = Masmorra.casa()
        self.masmorra.iniciar_combate(self.jogador.renascido)

    async def mudar_masmorra(self, nome_masmorra: str):
        """Muda a masmorra atual do jogador."""
        if not self.masmorra:
            return

        nova_masmorra = Masmorra.por_nome(nome_masmorra)
        nova_masmorra.iniciar_combate(self.jogador.renascido)
        nova_masmorra.pausado = self.masmorra.pausado if self.masmorra.__class__.__name__ != 'Casa' else False
        self.masmorra = nova_masmorra

    def pausar(self, pausado: bool):
        """Pausa ou despausa o jogo."""
        if self.masmorra:
            self.masmorra.pausado = pausado
            self.pausado = pausado

    def aumentar_atributo(self, atributo: str):
        """Aumenta um atributo do jogador."""
        if self.jogador:
            self.jogador.atribuir_ponto(atributo)

    def set_acao_jogador(self, acao: str):
        """Define a ação do jogador no combate."""
        if self.combate:
            self.combate.acao_jogador = acao

    def subir_nivel_classe(self, classe: str = None):
        """Sobe o nível da classe do jogador."""
        if self.jogador:
            self.jogador.subir_nivel_classe(classe)

    async def processar_turno(self):
        """Processa um turno do jogo."""
        if not self.masmorra or not self.combate:
            return

        combate_acabou, logs = await self.combate.executar_turno()
        self.logs.extend(logs)

        if combate_acabou:
            if self.combate.inimigo.vida <= 0:
                self.jogador.experiencia += self.combate.inimigo.experiencia
                self.jogador.ouro += self.combate.inimigo.ouro
                self.logs.append(f"{self.hour()} - {self.jogador.nome} derrotou {self.combate.inimigo.nome}!")
            
            self.masmorra.iniciar_combate(self.jogador.renascido)

    @staticmethod
    def hour() -> str:
        """Retorna a hora atual formatada."""
        return datetime.now().strftime('%H:%M:%S') 