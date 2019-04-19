import random
import sqlite3


def script_db_insert():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    #weapons 20 записей
    i = 1
    while i <= 20:
        weapon = 'Weapon' + str(i)
        reload_speed = random.randint(1, 50)
        rotation_speed = random.randint(1,50)
        diameter = random.randint(1,50)
        power_volley = random.randint(1,50)
        count = random.randint(1,50)
        cursor.execute("""INSERT OR REPLACE INTO weapons
                              VALUES (?, ?, ?, ?, ?, ?)""", (weapon, reload_speed, rotation_speed, diameter,
                                                             power_volley, count)
                       )
        conn.commit()
        i+=1

    #hulls 5
    i = 1
    while i <= 5:
        hull = 'Hull' + str(i)
        armor = random.randint(1,50)
        type = random.randint(1,50)
        capasity = random.randint(1,50)
        cursor.execute("""INSERT INTO hulls
                              VALUES (?, ?, ?, ?)""", (hull, armor, type, capasity)
                       )
        conn.commit()
        i += 1
    #engines 6
    i = 1
    while i <= 6:
        engine = 'Engine' + str(i)
        power = random.randint(1, 50)
        type = random.randint(1, 50)
        cursor.execute("""INSERT INTO engines
                              VALUES (?, ?, ?)""", (engine, power, type)
                       )
        conn.commit()
        i += 1

    #ships 200 записей
    i = 1
    while i <= 200:
        ship = 'Ship'+str(i)
        weapon = 'Weapon'+str(random.randint(1,20))
        hull = 'Hull'+str(random.randint(1,5))
        engine = 'Engine'+str(random.randint(1,6))
        cursor.execute("""INSERT INTO ships
                          VALUES (?, ?, ?, ?)""", (ship, weapon, hull, engine))
        conn.commit()
        i += 1
    conn.close()


if __name__ == "__main__":
    script_db_insert()