from fastapi import FastAPI, Request, Depends, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import router
from websocket import ConnectionManager
from config import settings
from exceptions import NotFoundException
from db.session import get_session
from live import controller as live_controller


async def homepage(request, exec):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


app = FastAPI(exception_handlers={404: homepage})

templates = Jinja2Templates(directory="templates")


app.include_router(router.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(
    request: Request, exc: NotFoundException,
):
    return JSONResponse(status_code=404, content={"detail": exc.message},)


manager = ConnectionManager()


@app.websocket("/api/live/chat/{token}")
async def livechat_websocket(
    websocket: WebSocket,
    token: str,
    youtube_chat_id: str,
    db: Session = Depends(get_session),
):
    await live_controller.handle_chat(manager, websocket, db, youtube_chat_id, token)
