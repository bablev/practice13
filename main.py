import sqlite3
from datetime import datetime, timezone
connection = sqlite3.connect('database.db')
# ТУТ ПРОСТО ЗАПОЛНЯЕТСЯ ДАННЫМИ БАЗА ДАННЫХ!!!!!!!
with open('schema.sql') as f:
    connection.executescript(f.read())
time = datetime.now().date()
cur = connection.cursor()
cur.execute("INSERT INTO Invoice(created, consignee) VALUES (?, ?)", (time,'Глобал групп'))
cur.execute("INSERT INTO Invoice(created, consignee) VALUES (?, ?)", (time,'Премиум групп'))
cur.execute("INSERT INTO Invoice(created, consignee) VALUES (?, ?)", (time,'Лайт групп'))
cur.execute("INSERT INTO Nomenclature(title,unit) VALUES (?,?)", ('Помидоры','кг'))
cur.execute("INSERT INTO Item (title, amount, unit, invoiceId) VALUES (?,?,?,?)", ('Помидоры', 5, 'кг', 1))
connection.commit()
connection.close()