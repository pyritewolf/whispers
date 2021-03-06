from urllib.parse import urlencode
from typing import Dict, Any, List, Optional
import logging

import asyncio
import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, WebSocket
from fastapi.websockets import WebSocketDisconnect

from websocket import ConnectionManager
from config import settings
from exceptions import get_pydanticlike_error
from users.schemas import UserIn
from users.controller import crud as user_crud
from auth.controller import refresh_google_tokens
from live import schemas


async def _request_to_google(
    db: Session, method: str, request_args: Dict[str, Any], user: UserIn
):
    if "headers" not in request_args:
        request_args["headers"] = {}
    request_args["headers"].update(
        {"Authorization": f"Bearer {user.google_auth_token}"}
    )
    response = getattr(requests, method)(**request_args)
    if response.status_code == 401:
        user = await refresh_google_tokens(db, user)
        response = getattr(requests, method)(**request_args)
    return response


async def handle_find_streams(
    db: Session, user: UserIn
) -> List[schemas.YoutubeBroadcast]:
    if not user.has_youtube_auth:
        return []
    data = {"broadcastType": "all", "broadcastStatus": "active", "part": "snippet"}
    data = {
        "url": f"https://www.googleapis.com/youtube/v3/liveBroadcasts?{urlencode(data)}"
    }
    response = await _request_to_google(db, "get", data, user)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_pydanticlike_error(
                "streams", "Something went wrong getting your Youtube streams."
            ),
        )
    result = response.json()
    result = schemas.YoutubeBroadcastResponse.parse_obj(result)
    return result.items


async def handle_get_chat_messages(
    db: Session, chat_id: str, next_page: Optional[str], user: UserIn
) -> schemas.YoutubeChatResponse:
    if not user.has_youtube_auth:
        return []
    data = {
        "liveChatId": chat_id,
        "part": "authorDetails",
    }
    if next_page:
        data["pageToken"] = next_page
    data = {
        "url": f"https://www.googleapis.com/youtube/v3/liveChat/messages?part=snippet&part=id&{urlencode(data)}"  # noqa:
    }
    response = await _request_to_google(db, "get", data, user)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_pydanticlike_error(
                "streams", "Something went wrong getting your Youtube streams.",
            ),
        )
    result = response.json()
    result = schemas.YoutubeChatResponse.parse_obj(result)
    return result


async def handle_chat(
    manager: ConnectionManager,
    websocket: WebSocket,
    db: Session,
    youtube_chat_id: str,
    streamer: str,
):
    await manager.connect(websocket)
    try:
        db_user = await user_crud.get_by(db, "username", streamer)
        user = UserIn.from_orm(db_user)
        queue = asyncio.queues.Queue()

        async def get_chat_messages(manager, db, youtube_chat_id, user):
            next_page = None
            while True:
                messages = await handle_get_chat_messages(
                    db, youtube_chat_id, next_page, user
                )
                data = [
                    schemas.ChatMessage(
                        username=message.author_details.display_name,
                        text=message.snippet.text_message_details.message_text,
                    ).json()
                    for message in messages.items
                ]
                next_page = messages.next_page_token
                if data:
                    queue.put_nowait(f'[{" ,".join(data)}]')
                await asyncio.sleep(settings.CHAT_POLLING_TIME)

        async def send_chat_messages(manager):
            data = await queue.get()
            while True:
                if not queue.empty():
                    data = queue.get_nowait()
                    await manager.broadcast(data)
                await asyncio.sleep(0.2)

        await asyncio.gather(
            get_chat_messages(manager, db, youtube_chat_id, user),
            send_chat_messages(manager),
        )
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except HTTPException as e:
        logging.warning(e)
