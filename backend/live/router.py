from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import settings
from exceptions import NotFoundException
from db.session import get_session
from auth.controller import get_current_user
from live import controller, schemas
from users.controller import crud as user_crud, schemas as user_schemas


router = APIRouter()


@router.get("/streams")
async def list_streams(
    user=Depends(get_current_user), db: Session = Depends(get_session),
):
    streams = await controller.handle_find_streams(db=db, user=user)
    return streams


@router.get("/is_chat_open/{streamer}")
async def check_if_chat_is_available(
    streamer: str, db: Session = Depends(get_session),
) -> schemas.ChatConfig:
    db_streamer = await user_crud.get_by(db, "username", streamer)
    if not db_streamer:
        raise NotFoundException(
            f"{streamer} isn't hearing whispers. Tell them to join us!"
        )
    streams = await controller.handle_find_streams(
        db=db, user=user_schemas.UserIn.from_orm(db_streamer)
    )
    if not streams:
        raise NotFoundException(
            f"{streamer} isn't streaming right now. Come back later!"
        )
    chats = [
        stream.snippet.live_chat_id for stream in streams if stream.snippet.live_chat_id
    ]
    if not chats:
        raise NotFoundException(
            f"{streamer} is streaming but their stream doesn't have the chat enabled 😭"
        )
    return schemas.ChatConfig(server_url=settings.SERVER_URL, youtube_chat_id=chats[0])
