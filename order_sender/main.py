import random
import json
from datetime import datetime

import pika
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="orders_queue", durable=True)

available_meals = [
    "Zupa z Kurczaka",
    "Sałatka Warzywna",
    "Stek Grillowany",
    "Makaron Carbonara",
    "Tacos z Rybą",
    "Brownie Czekoladowe",
    "Pizza Margherita",
    "Curry Wegańskie",
    "Klasyczna Sałatka Cezar",
    "Naleśniki z Jagodami",
    "Szakszuka",
    "Pad Thai",
    "Risotto z Grzybami",
    "Gazpacho",
    "Ratatouille",
    "Bibimbap",
    "Tiramisu",
    "Falafel",
    "Musaka",
]

meal_id = [
    "c398f5e1-3b11-4c12-b35d-281ad5eaa06e",
    "e89327cb-d28c-4760-85d0-290d2ac1b012",
    "a798527c-b8b1-4b08-9ff1-4d6ac964ecf3",
    "e72d8b73-2181-4605-92f7-5a6f4d2b8dbb",
    "bea1f7a4-20df-4d05-8817-0675cd7b02b1",
    "f4959e7d-04da-4fb9-b2b0-5ecff36540da",
    "be78114d-f8ef-41b2-9ea2-6550c0c09d46",
    "7c1a66b3-741a-4f7e-8182-989d78f731ef",
    "2e5cdefa-6c3f-43c2-9086-c79a5a7da9f2",
    "43c64d3d-396a-4eb5-bc5e-0c0059ecde46",
    "3ef2b883-065b-4f8a-95e5-36f4cc9e4cf3",
    "4d78f9c0-ec30-4851-968a-9d8e5a4b21d7",
    "9fbb905f-b01a-4c7e-b51b-85e26bf0c4b2",
    "94f18e8d-fb3c-4ff7-a3e7-17fc3f9f4b2b",
    "bfda20c7-6b2d-41f4-ba1b-d77692418b97",
    "5d0c1853-e0d4-4b0b-8580-ee334f2589d7",
    "9b22c7f0-df97-46a7-8b79-8ef415ac1b2b",
    "18e2e6d8-5a5a-44ed-88ad-4f63af3a991b",
    "ccf45b6f-4d9a-449f-b77b-0e69dadd19dd",
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
    "Bez glutenu, proszę.",
]

for _ in range(random.randint(10, 15)):
    id = str(uuid.uuid4())
    note = random.choice(notes)
    orderDateTime = str(datetime.now())
    meals = []

    random.shuffle(available_meals)
    for j in range(random.randint(1, 7)):
        meal = available_meals[j]
        count = random.randint(1, 3)
        meals.append({"mealId": meal_id[j], "meal": meal, "count": count})

    message = {"id": id, "orderDateTime": orderDateTime, "notes": note, "meals": meals}

    channel.basic_publish(
        exchange="", routing_key="orders_queue", body=json.dumps(message)
    )
    print(f" [x] Sent order {id}")

connection.close()
