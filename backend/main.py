from fastapi import FastAPI

from backend.database import Base, engine
from backend.routes import wellcome_router, user_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wallet API")

app.include_router(wellcome_router)
app.include_router(user_router)
