from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

orders = []
connections = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        connections.remove(websocket)


@app.post("/orders/")
async def receive_data(data: dict):
    global orders
    data["id"] = str(data["id"]).split("-")[0]
    orders.insert(0, data)
    # Now, notify all connected clients
    for connection in connections:
        await connection.send_json(orders)