import sqlite3


def init():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()

    cur.execute("""
            CREATE TABLE IF NOT EXISTS 
                'pool'(
                    'id' integer primary key AUTOINCREMENT,
                    'name' varchar(40),
                    'text' text,
                    'message_id' integer null
                )
        """)
    cur.execute("""
             CREATE TABLE IF NOT EXISTS 
                    'field'(
                        'id' integer primary key AUTOINCREMENT,
                        'name' varchar(40),
                        'voted' integer,
                        'bind' integer
                    )
        """)
    cur.execute("""
                 CREATE TABLE IF NOT EXISTS 
                        'vote'(
                            'id' integer primary key AUTOINCREMENT,
                            'user_id' integer,
                            'message_id' integer
                        )
            """)
    con.close()


def create(table, data):
    keys = tuple(data.keys())
    values = tuple(data.values())
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    try:
        back_data = cur.execute(f"""
                INSERT INTO {table}{keys} VALUES{values}
            """).lastrowid
        con.commit()
    except sqlite3.Error as e:
        print(e)
        back_data = None
    con.close()
    return back_data


def delete(table, field, row_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    try:
        back_data = cur.execute(f"""
                    DELETE FROM {table} WHERE {field}={row_id}
                """)
        con.commit()
    except sqlite3.Error as e:
        print(e)
        back_data = None

    con.close()
    return back_data


def get_pool(pool_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
               SELECT p.name, p.text, p.id, f.name, f.voted, f.id FROM pool p
               INNER JOIN field f ON f.bind = p.id WHERE p.id = {pool_id} ORDER BY -f.voted
            """).fetchall()
    con.close()
    return data


def get_all_pool():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                   SELECT name, id, message_id FROM pool
                """).fetchall()
    con.close()
    return data


def set_mes_id(pool_id, message_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    try:
        back_data = cur.execute(f"""
                           UPDATE pool SET message_id={message_id} WHERE id={pool_id}
                        """)
        con.commit()
    except sqlite3.Error as e:
        print(e)
        back_data = None
    con.close()
    return back_data


def set_vote(field_id, user_id, message_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    try:
        cur.execute(f"""
                UPDATE field SET voted = voted + 1 WHERE id = {field_id}
            """)
        cur.execute(f"""
                INSERT INTO vote('user_id', 'message_id') VALUES({user_id}, {message_id})
            """)
        con.commit()
        status = 201
    except sqlite3.Error as e:
        print(e)
        status = 400
    con.close()
    return status


def get_voted(user_id, mess_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
            SELECT user_id FROM vote WHERE user_id = {user_id} AND message_id = {mess_id} 
        """).fetchone()
    con.close()
    return data


def get_pool_for_del(pool_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                SELECT message_id FROM pool WHERE id={pool_id}
            """).fetchone()
    con.close()
    return data

