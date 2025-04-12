import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from dados import lista_masmorras
from dados.tipos import Jogador

app = FastAPI()

# Montar diretório estático para arquivos Vue
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get():
    return FileResponse('static/index.html')

# Armazenamento temporário dos jogadores conectados
connected_players = {}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    player_id = id(websocket)
    connected_players[player_id] = websocket

    masmorra = None
    try:
        while True:
            logs = []
            combate_acabou = False
            # Tenta receber mensagem do cliente, mas não bloqueia
            try:
                data_json = await asyncio.wait_for(websocket.receive_json(), timeout=0.25)
                if data_json["type"] == "mudar_masmorra":
                    __masmorra = lista_masmorras[data_json["data"]["masmorra"]].clone()
                    __masmorra.iniciar_combate(masmorra.jogador)
                    __masmorra.pausado = masmorra.pausado if masmorra.__class__.__name__ != 'Casa' else False
                    masmorra = __masmorra

                if data_json["type"] == "login":
                    jogador = Jogador.primeiro_nivel(
                        nome=data_json["data"]["nome"],
                        descricao=data_json["data"]["descricao"],
                        email=data_json["data"]["email"],
                        senha=data_json["data"]["senha"],
                        classe=data_json["data"]["classe"]
                    )
                    masmorra = lista_masmorras[0]
                    masmorra.iniciar_combate(jogador.renascido)
                    await websocket.send_json({'type': 'update', **masmorra.websocket_data, 'logs': []})

                if data_json["type"] == "pausar":
                    masmorra.pausado = data_json["data"]["pausado"]

                if data_json["type"] == "aumentar_atributo":
                    masmorra.jogador.atribuir_ponto(data_json["data"]["atributo"])

                if data_json["type"] == "acao_jogador":
                    masmorra.combate.acao_jogador = data_json["data"]["acao"]

                if data_json["type"] == "subir_nivel_classe":
                    masmorra.jogador.subir_nivel_classe(data_json["data"].get("classe", None))

                if masmorra.jogador:
                    await websocket.send_json({
                        'type': 'action_response',
                        **masmorra.websocket_data,
                        'logs': logs,
                        'masmorras': [
                            {
                                "chave": i,
                                "nome": masmorra.nome
                            } for i, masmorra in enumerate(lista_masmorras)
                        ]
                    })
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(e)
                break
            finally:
                if not masmorra or not masmorra.jogador:
                    continue
                # Executa o turno independentemente de ter recebido mensagem
                if not masmorra.pausado:
                    if masmorra.__class__.__name__ == 'Casa' and masmorra.jogador.vida >= masmorra.jogador.vida_maxima and masmorra.jogador.energia >= masmorra.jogador.energia_maxima:
                        masmorra.pausado = True

                    combate_acabou = masmorra.combate_acabou
                    if combate_acabou:
                        masmorra.iniciar_combate(masmorra.jogador)
                    else:
                        logs = await masmorra.executar_turno()
                await websocket.send_json({
                    'type': 'paused' if masmorra.pausado else 'update',
                    **masmorra.websocket_data,
                    'logs': logs,
                    'masmorras': [
                        {
                            "chave": i,
                            "nome": masmorra.nome
                        } for i, masmorra in enumerate(lista_masmorras)
                    ]
                })
                if combate_acabou:
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(0.25)

    except Exception as e:
        raise e
    finally:
        del connected_players[player_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
