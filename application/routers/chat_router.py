from typing import List

from fastapi import Request, Depends, WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from application.db_dir.database import get_async_session
from application.repositories.chat_repository import ChatRepository
from application.db_dir.schemas import MessagesModel

router = APIRouter()
templates = Jinja2Templates(directory='application/templates')


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, save_to_db: bool = False):
        if save_to_db:
            await ChatRepository().add_messages_to_database(message=message)
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", save_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


@router.get('/chat')
def chat(request: Request):
    return templates.TemplateResponse('chat_page.html', {'request': request})


@router.get("/chat/last_messages", response_model=list[MessagesModel])
async def get_last_messages(session: AsyncSession = Depends(get_async_session)) -> List[MessagesModel]:
    result = await ChatRepository().get_last_10_messages(session=session)
    return result
