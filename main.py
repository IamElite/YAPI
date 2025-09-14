from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers import api, home
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="YT Audio API")
templates = Jinja2Templates(directory="templates")

# Ensure static directory exists
static_dir = "static"
if not os.path.exists(static_dir):
    logger.warning(f"Static directory {static_dir} not found, creating it")
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(home.router, prefix="")
app.include_router(api.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)
