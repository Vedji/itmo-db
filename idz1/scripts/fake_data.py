from faker import Faker
import random


fake = Faker('ru_RU')

statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
sql_request = []

for i in range(1000):
    products = random.sample([
        ('Ноутбук', 85000), ('Мышь', 1500), ('Коврик', 500),
        ('Монитор', 25000), ('Клавиатура', 3000), ('Наушники', 5000)
    ], k=random.randint(1, 3))
    
    names = ', '.join(p[0] for p in products)
    prices = ', '.join(str(p[1]) for p in products)
    qtys = [random.randint(1, 3) for _ in products]
    total = sum([qtys[p] * products[p][1] for p in range(len(products))])
    content = """INSERT INTO orders_raw VALUES ({},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}');\n""".format(i, fake.date_this_year(),
    fake.name(), fake.email(), fake.phone_number(),
    fake.address(), names, prices, 
    ', '.join(map(lambda x: str(x), qtys)),
    total, random.choice(statuses))
    sql_request.append(content)

with open("./sql/raw_fake_data.sql", "w", encoding="utf-8") as f:
    f.writelines(sql_request)

