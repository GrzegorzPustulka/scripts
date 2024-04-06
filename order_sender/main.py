import random
import json
from datetime import datetime, timedelta

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

notes = [
    "Herbatę proszę bez cukru.",
    "Stek medium rare, proszę.",
    "Bez cebuli w burgerze.",
    "Dodatkowy ser do pizzy.",
    "Frytki zamiast ryżu.",
    "Sos czosnkowy na boku.",
    "Bez soli w zupie.",
    "Espresso z podwójnym shotem.",
    "Sałatka bez dressingu.",
    "Extra pikantne curry.",
    "Pieczone ziemniaki zamiast purée.",
    "Brak lodu w napoju.",
    "Makaron al dente.",
    "Pierś z kurczaka, nie udziec.",
    "Bez glutenu, proszę."
]

for _ in range(random.randint(10, 15)):
    id = str(uuid.uuid4())
    note = random.choice(notes)
    orderDateTime = str(datetime.now())
    meals = []

    random.shuffle(available_meals)
    for j in range(random.randint(1, 7)):
        meal = available_meals[j]
        count = random.randint(1, 5)
        meals.append({"meal": meal, "count": count})

    message = {"id": id, "orderDateTime": orderDateTime, "notes": note, "meals": meals}

    channel.basic_publish(
        exchange="", routing_key="orders_queue", body=json.dumps(message)
    )
    print(f" [x] Sent order {id}")

connection.close()
