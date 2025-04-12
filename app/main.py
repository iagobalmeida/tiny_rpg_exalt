import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_config
from app.services.websocket import websocket_manager

app = FastAPI()

# Montar diretório estático para arquivos Vue
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    return FileResponse('static/index.html')

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
    asyncio.create_task(websocket_manager.process_game_loop())

if __name__ == "__main__":
    config = get_config()
    uvicorn.run(
        "app.main:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
        reload=config["server"]["debug"]
    ) 