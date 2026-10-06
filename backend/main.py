from fastapi import FastAPI

from backend.database import Base, engine
from backend.routes import router

# Для минимального примера таблицы создаются автоматически при старте.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wallet API")
app.include_router(router)
