from fastapi import APIRouter, Request, HTTPException
from starlette.responses import StreamingResponse
import yt_dlp
import requests
import os
from config import API_KEY
from database import insert_audio_id
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Load cookies
COOKIE_FILE = 'cookies.txt'
if not os.path.exists(COOKIE_FILE):
    logger.info("Creating cookies.txt file")
    with open(COOKIE_FILE, 'w') as f:
        f.write('')

@router.get("/yt-audio-video")
async def yt_audio_video(request: Request):
    url = request.query_params.get("url")
    quality = request.query_params.get("quality", "audiobest")
    info_mode = request.query_params.get("info", "false").lower() == "true"
    api_key = request.headers.get("X-API-Key")

    if api_key != API_KEY:
        logger.warning("Invalid API key attempt")
        return {"error": "Invalid API Key"}, 401

    if not url:
        logger.error("Missing URL parameter")
        return {"error": "Missing 'url' parameter"}, 400

    try:
        ydl_opts = {
            "cookiefile": COOKIE_FILE,
            "quiet": True,
            "format_sort": ["ext:mp4:m4a"] if "audiobest" in quality else ["ext:mp4"],
            "merge_output_format": "mp4" if "best" in quality else "mp3",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info.get('formats', [info])
        audio_format = next((f for f in formats if f.get('acodec') != 'none'), None)
        video_format = next((f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none'), None)

        audio_url = audio_format["url"] if audio_format else None
        video_url = video_format["url"] if video_format else None

        audio_id = info.get("id", "unknown_id")
        insert_audio_id(audio_id)

        # ✅ If info mode requested → return JSON metadata
        if info_mode:
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "audio_stream_url": audio_url,
                "video_stream_url": video_url,
                "original_url": url,
                "is_live": info.get("is_live"),
                "uploader": info.get("uploader"),
                "view_count": info.get("view_count")
            }

        # ✅ Otherwise → return actual stream
        def stream_content():
            with requests.get(audio_url if "audio" in quality else video_url, stream=True, timeout=10) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk

        return StreamingResponse(
            stream_content(),
            media_type="audio/mp3" if "audio" in quality else "video/mp4",
            headers={"Content-Disposition": f"inline; filename={audio_id}.{('mp3' if 'audio' in quality else 'mp4')}"}
        )

    except Exception as e:
        logger.error(f"Error streaming media: {str(e)}")
        return {"error": f"Error: {str(e)}"}, 500
        
@router.get("/yt-download")
async def yt_download(request: Request):
    url = request.query_params.get("url")
    format_type = request.query_params.get("format", "mp3")
    api_key = request.headers.get("X-API-Key")

    if api_key != API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if not url:
        logger.error("Missing URL parameter")
        raise HTTPException(status_code=400, detail="Missing 'url' parameter")

    try:
        ydl_opts = {
            "format": format_type,
            "cookiefile": COOKIE_FILE,
            "quiet": True,
            "outtmpl": f"%(title)s.{format_type}",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_id = info.get("id", "unknown_id")
            insert_audio_id(audio_id)
            logger.info(f"Downloading media for audio ID: {audio_id}")

            with open(f"{info['title']}.{format_type}", "rb") as f:
                content = f.read()

            os.remove(f"{info['title']}.{format_type}")  # Clean up file after download
            return Response(
                content=content,
                media_type=f"audio/{format_type}" if format_type == "mp3" else "video/mp4",
                headers={"Content-Disposition": f"attachment; filename={info['title']}.{format_type}"}
            )

    except Exception as e:
        logger.error(f"Error downloading media: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/ping")
async def ping():
    logger.info("Ping endpoint accessed")
    return {"status": "active"}

@router.get("/user-panel")
async def user_panel():
    logger.info("User panel accessed")
    return {"message": "User Panel - API Key: BadApiYt"}

@router.get("/owner-login")
async def owner_login():
    logger.info("Owner login accessed")
    return {"message": "Owner Login"}
