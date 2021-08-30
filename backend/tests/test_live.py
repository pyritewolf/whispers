from typing import Any, Dict, List, Optional
import pytest
from datetime import datetime

from sqlalchemy.orm import Session

from live.schemas import ChatConfig
from tests.utils import seed_user, get_auth_for
from config import settings


def _get_youtube_broadcast(chat_id: Optional[str] = "wild_chat_id") -> Dict[str, Any]:
    return {
        "etag": "str",
        "id": "video_id",
        "kind": "str",
        "snippet": {
            "actual_start_time": datetime.now(),
            "channel_id": "wild_channel_id",
            "description": "cool stream yooo",
            "is_default_broadcast": True,
            "live_chat_id": chat_id,
            "published_at": datetime.now(),
            "scheduled_start_time": datetime.now(),
            "thumbnails": {
                "default": {"height": 1, "width": 1, "url": "http://animage.png.yey"},
                "high": {"height": 1, "width": 1, "url": "http://animage.png.yey"},
                "medium": {"height": 1, "width": 1, "url": "http://animage.png.yey"},
                "maxres": {"height": 1, "width": 1, "url": "http://animage.png.yey"},
                "standard": {"height": 1, "width": 1, "url": "http://animage.png.yey"},
            },
            "title": "super cool stream 100% speedrun",
        },
    }


def _get_youtube_broadcast_response(items: List[Any] = []) -> Dict[str, Any]:
    return {
        "etag": "str",
        "items": items,
        "kind": "str",
        "page_info": {"total_results": len(items), "results_per_page": 5},
    }


def test_is_chat_open_with_no_auth(setup, db: Session):
    seed_user(db)
    response = setup.get("/api/live/is_chat_open", headers=get_auth_for())
    assert response.status_code == 401


def test_is_chat_open_with_no_youtube_auth(setup, db: Session):
    user = seed_user(db)
    response = setup.get("/api/live/is_chat_open", headers=get_auth_for(user))
    assert response.status_code == 404


@pytest.mark.parametrize(
    "patched_requests",
    [{"method": "get", "response": _get_youtube_broadcast_response()}],
    indirect=["patched_requests"],
)
def test_is_chat_open_with_no_open_stream(patched_requests, setup, db: Session):
    user = seed_user(
        db, {"google_auth_token": "a token", "google_refresh_token": "another token"}
    )
    response = setup.get("/api/live/is_chat_open", headers=get_auth_for(user))
    assert response.status_code == 404


@pytest.mark.parametrize(
    "patched_requests",
    [
        {
            "method": "get",
            "response": _get_youtube_broadcast_response([_get_youtube_broadcast(None)]),
        },
    ],
    indirect=["patched_requests"],
)
def test_is_chat_open_with_no_chat(patched_requests, setup, db: Session):
    user = seed_user(
        db, {"google_auth_token": "a token", "google_refresh_token": "another token"}
    )
    response = setup.get("/api/live/is_chat_open", headers=get_auth_for(user))
    assert response.status_code == 404


@pytest.mark.parametrize(
    "patched_requests",
    [
        {
            "method": "get",
            "response": _get_youtube_broadcast_response([_get_youtube_broadcast()]),
        },
    ],
    indirect=["patched_requests"],
)
def test_is_chat_open(patched_requests, setup, db: Session):
    user = seed_user(
        db, {"google_auth_token": "a token", "google_refresh_token": "another token"}
    )
    response = setup.get("/api/live/is_chat_open", headers=get_auth_for(user))
    assert response.status_code == 200
    configs = ChatConfig.parse_obj(response.json())
    assert configs.server_url == settings.SERVER_URL
    assert configs.youtube_chat_id == "wild_chat_id"
