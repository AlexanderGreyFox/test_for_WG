import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()



# Создание таблицы
cursor.execute("""CREATE TABLE weapons
                  (weapon text, reload_speed integer , rotational_speed integer,
                   diameter integer, power_volley integer, count integer, 
                   primary key (weapon))
               """)
conn.commit()

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE hulls
                  (hull text, armor integer , type integer ,
                   capacity integer, primary key (hull))
               """)
conn.commit()

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE engines
                  (engine text, power integer , type integer ,
                   primary key (engine))
               """)
conn.commit()

# Создание таблицы
cursor.execute("""CREATE TABLE ships
                  (ship text, weapon text , hull text,
                   engine text , primary key (ship), foreign key (weapon) references weapons(weapon), foreign key 
                   (hull) references hulls(hull), foreign key (engine) references engines(engine))
               """)
conn.commit()

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
conn.close()
