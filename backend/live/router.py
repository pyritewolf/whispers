from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import settings
from exceptions import NotFoundException
from db.session import get_session
from auth.controller import get_current_user
from live import controller, schemas
from users.controller import schemas as user_schemas


router = APIRouter()


@router.get("/is_chat_open")
async def check_if_chat_is_available(
    streamer: user_schemas.UserIn = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> schemas.ChatConfig:
    streams = await controller.handle_find_streams(db=db, user=streamer)
    if not streams:
        raise NotFoundException(
            f"{streamer.username} isn't streaming right now. Come back later!"
        )
    chats = [
        stream.snippet.live_chat_id for stream in streams if stream.snippet.live_chat_id
    ]
    if not chats:
        raise NotFoundException(
            f"{streamer.username} is streaming but \
their stream doesn't have the chat enabled 😭"
        )
    return schemas.ChatConfig(server_url=settings.SERVER_URL, youtube_chat_id=chats[0])
