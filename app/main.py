import asyncio
import os

import uvicorn
from config import get_config
from fastapi import FastAPI, Form, Request, WebSocket
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
    ws_url = str(request.url_for('websocket_endpoint'))
    if not 'localhost' in os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/tinyrpg'):
        ws_url = ws_url.replace('ws://', 'wss://')
    return templates.TemplateResponse('jogar.html', {'request': request, 'body_class': 'opacity-0', 'ws_url': ws_url})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    player_id = await websocket_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await websocket_manager.handle_message(player_id, data)
    except:
        await websocket_manager.disconnect(player_id)


@app.get("/link_pagamento")
async def get_link_pagamento(request: Request, email: str = Form()):
    db_usuario = db.get_usuario_by_email(email)
    if not db_usuario:
        db_usuario = db.create_usuario(email=email)
    pass


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
