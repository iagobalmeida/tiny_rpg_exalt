import asyncio

import uvicorn
from config import get_config
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import db
from services.db import create_db_and_tables, criar_usuarios_de_teste
from services.websocket import websocket_manager

app = FastAPI()

# Montar diretório estático para arquivos Vue
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'placar_de_lideres': db.get_placar_de_lideres()})


@app.get("/jogar")
async def get_jogar(request: Request):
    criar_usuarios_de_teste()
    return templates.TemplateResponse('jogar.html', {'request': request, 'body_class': 'opacity-0', 'ws_url': request.url_for('websocket_endpoint')})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    player_id = await websocket_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await websocket_manager.handle_message(player_id, data)
    except:
        await websocket_manager.disconnect(player_id)


@app.on_event("startup")
async def startup_event():
    # Inicia o loop do jogo em background
    create_db_and_tables()
    asyncio.create_task(websocket_manager.process_game_loop())

if __name__ == "__main__":
    config = get_config()
    uvicorn.run(
        "main:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
        reload=config["server"]["debug"]
    )
