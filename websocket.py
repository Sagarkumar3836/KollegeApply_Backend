from fastapi import WebSocket

async def earnings_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text("Earnings update coming soon (demo only)")
