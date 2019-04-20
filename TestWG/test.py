import os
import random
import sqlite3
from nose.tools import with_setup

from shutil import copyfile


def setup_fun():
    """Copy database and start randomisation new database"""

    copyfile("mydatabase.db", "database_for_test.db")

    conn = sqlite3.connect("database_for_test.db")
    cursor = conn.cursor()

    keys = random.sample(['reload_speed', 'rotational_speed', 'diameter', 'power_volley', 'count'], random.randint(1,5))

    for k in keys:
        i = 1
        while i <= 20:
            # here and after in all UPDATE sql requests I used .format becouse because the column is not known and
            # standard methods with ?,?,? does not work
            cursor.execute("""UPDATE "main"."weapons" SET {k}={v} WHERE "_rowid_"={i};""".format(k=k,
                                                                                                 v=random.randint(1,50),
                                                                                                 i = str(i)))

            i += 1
            conn.commit()

    keys = random.sample(['armor', 'type', 'capacity'], random.randint(1,3))

    for k in keys:
        i = 1
        while i <= 5:

            cursor.execute("""UPDATE "main"."hulls" SET {k}={v} WHERE "_rowid_"={i};""".format(k=k,
                                                                                               v=random.randint(1,50),
                                                                                               i = str(i)))

            i += 1
            conn.commit()

    keys = random.sample(['power', 'type'], random.randint(1,2))

    for k in keys:
        i = 1
        while i <= 6:

            cursor.execute("""UPDATE "main"."engines" SET {k}={v} WHERE "_rowid_"={i};""".format(k=k,
                                                                                                 v=random.randint(1,50),
                                                                                                 i = str(i)))

            i += 1
            conn.commit()

    keys = random.sample(['weapon', 'hull', 'engine'], 1)

    for k in keys:
        i = 1

        while i <= 200:
            if k == 'weapon':
                value = 'Weapon' + str(random.randint(1, 20))
            elif k == 'hull':
                value = 'Hull' + str(random.randint(1, 5))
            else:
                value = 'Engine' + str(random.randint(1, 6))
            cursor.execute("""UPDATE "main"."ships" SET {k}='{v}' WHERE "_rowid_"={i};""".format(k=k,
                                                                                                 v=str(value),
                                                                                                 i=str(i)))

            i += 1
            conn.commit()
    conn.close()


def teardown_fun():
    """Delete test database"""

    my_database = "database_for_test.db"

    if os.path.isfile(my_database):
        os.remove(my_database)
    else:
        print("Error: %s file not found" % my_database)


@with_setup(setup_fun, teardown_fun)
def test_generator():
    """t is a column number in ships table
    i is a row number in ships table"""
    for t in range(1, 4):

        for i in range(1, 201):
            s = 'Ship' + str(i)
            yield some_fun, s, t


def some_fun(a, b):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    # check the identity of the data in the ships table
    cursor.execute("""SELECT * from ships where ship = ?""", (a,))
    expected_result = cursor.fetchall()
    expected_result = expected_result[0][b]
    conn.close()

    conn = sqlite3.connect("database_for_test.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * from ships where ship = ?""", (a,))
    actual_result = cursor.fetchall()
    actual_result = actual_result[0][b]
    conn.close()

    assert expected_result == actual_result, f'{a} expected {expected_result}, was {actual_result}'

    # check the identity of the data in the 3 other tables
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    if b == 1:
        cursor.execute("""select * from weapons where weapon = ?""", (actual_result,))
    elif b == 2:
        cursor.execute("""select * from hulls where hull = ?""", (actual_result,))
    else:
        cursor.execute("""select * from engines where engine = ?""", (actual_result,))

    expected_result = cursor.fetchall()
    expected_result = expected_result[0]

    conn.close()

    conn = sqlite3.connect("database_for_test.db")
    cursor = conn.cursor()
    if b == 1:
        fields = ('weapon', 'reload_speed', 'rotation_speed', 'diameter', 'power_volley', 'count')
        cursor.execute("""select * from weapons where weapon = ?""", (actual_result,))
    elif b == 2:
        fields = ('hull', 'armor', 'type', 'capasity')
        cursor.execute("""select * from hulls where hull = ?""", (actual_result,))
    else:
        fields = ('engine', 'power', 'type')
        cursor.execute("""select * from engines where engine = ?""", (actual_result,))

    actual_result = cursor.fetchall()
    actual_result = actual_result[0]

    conn.close()
    # all possible changes are collected from the table row
    s = ''
    try:
        for i in range(len(actual_result)):
            assert expected_result[i] == actual_result[i]
    except AssertionError:
        s = s + f'{a}, {expected_result[i]}, expected {fields[i]} {expected_result[i]}, ' \
                f'was {fields[i]} {actual_result[i]}\n'

    if s:
        raise AssertionError(s)
