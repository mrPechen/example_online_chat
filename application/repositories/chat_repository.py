from sqlalchemy import insert, select

from application.db_dir.database import async_session_maker
from application.db_dir.models import Message


class ChatRepository:
    def __init__(self):
        self.session_maker = async_session_maker()
        self.model = Message

    async def add_messages_to_database(self, message: str):
        async with self.session_maker as session:
            stmt = insert(Message).values(
                message=message
            )
            await session.execute(stmt)
            await session.commit()

    async def get_last_10_messages(self, session):
        query = select(self.model).order_by(self.model.id.desc()).limit(10)
        messages = await session.execute(query)
        return messages.scalars().all()[::-1]
