import random
import json
from datetime import datetime

import pika
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="orders_queue", durable=True)

available_meals = [
    "chicken",
    "soup",
    "vegetables",
    "broth",
    "salad",
    "steak",
    "pasta",
    "rice",
    "pizza",
    "sandwich",
    "fish",
    "sushi",
    "burger",
    "tacos",
    "burrito",
    "shrimp",
    "lobster",
    "cake",
    "ice cream",
    "fruit",
]


def generate_time():
    now = datetime.now()
    random_minute = random.randint(0, 59)
    return now.replace(minute=random_minute, second=0, microsecond=0)


for _ in range(random.randint(10, 15)):
    id = str(uuid.uuid4())
    time = generate_time()
    meals = []

    random.shuffle(available_meals)
    for j in range(random.randint(1, 7)):
        meal = available_meals[j]
        count = random.randint(1, 5)
        meals.append({"meal": meal, "count": count})

    message = {"id": id, "time": time, "meals": meals}

    channel.basic_publish(
        exchange="", routing_key="orders_queue", body=json.dumps(message)
    )
    print(f" [x] Sent order {id}")

connection.close()
