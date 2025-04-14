from typing import Any, Dict

# Configurações do servidor
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": True
}

# Configurações do jogo
GAME_CONFIG = {
    "experiencia_por_level": 15,
    "experiencia_incremento_por_level": 15,
    "pontos_atributo_por_level": 3,
    "vida_base_por_level": 5,
    "energia_base_por_level": 8,
    "chance_acerto_base": 50,
    "dano_minimo": 1,
    "fator_aleatorio_min": 0.8,
    "fator_aleatorio_max": 1.2,
    "diferenca_agilidade_limite": 8
}

# Configurações de sprites
SPRITE_CONFIG = {
    "tamanho": 32,
    "escala": 3
}

# Configurações de combate
COMBAT_CONFIG = {
    "timeout_turno": 0.75,
    "tempo_entre_acoes": 1.5
}


def get_config() -> Dict[str, Any]:
    """Retorna todas as configurações do jogo."""
    return {
        "server": SERVER_CONFIG,
        "game": GAME_CONFIG,
        "sprite": SPRITE_CONFIG,
        "combat": COMBAT_CONFIG
    }
