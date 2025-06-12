from fastapi import FastAPI
import models
from database import engine
from routes import router as api_router
from websocket import earnings_ws

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)

@app.websocket("/ws/earnings")
async def websocket_endpoint(websocket):
    await earnings_ws(websocket)
