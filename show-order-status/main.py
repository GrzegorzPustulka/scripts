from fastapi import FastAPI

app = FastAPI()

orders = []


@app.post("/orders/change_order_status")
async def receive_data(data: dict):
    global orders
    orders.append(data)


@app.get("/orders")
async def get_orders():
    return orders
