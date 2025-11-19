from fastapi import FastAPI
from database import Base, engine
from scheduler import start_scheluder
import asyncio
import datetime
from bot import run_bot

app = FastAPI()

@app.on_event("startup")
async def start_app():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    start_scheluder()
    import threading
    threading.Thread(target=run_bot, daemon=True).start()
