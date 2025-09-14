from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_stats

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    stats = get_stats()
    return templates.TemplateResponse("index.html", {"request": request, "stats": stats})

@router.get("/yt-player", response_class=HTMLResponse)
async def yt_player(request: Request):
    return templates.TemplateResponse("yt_api.html", {"request": request})
