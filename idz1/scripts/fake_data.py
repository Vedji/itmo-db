from faker import Faker
import random, psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


fake = Faker('ru_RU')
conn = psycopg2.connect(
    host="localhost",
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

for i in range(1000):
    products = random.sample([
        ('Ноутбук', 85000), ('Мышь', 1500), ('Коврик', 500),
        ('Монитор', 25000), ('Клавиатура', 3000), ('Наушники', 5000)
    ], k=random.randint(1, 3))
    
    names = ', '.join(p[0] for p in products)
    prices = ', '.join(str(p[1]) for p in products)
    qtys = [random.randint(1, 3) for _ in products]
    total = sum([qtys[p] * products[p][1] for p in range(len(products))])
    
    cur.execute("""INSERT INTO orders_raw VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (i, fake.date_this_year(),
         fake.name(), fake.email(), fake.phone_number(),
         fake.address(), names, prices, 
         ', '.join(map(lambda x: str(x), qtys)),
         total, random.choice(statuses)))

conn.commit()
