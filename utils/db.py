import sqlite3


async def init():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS 
                    'pool'(
                        'id' integer primary key AUTOINCREMENT,
                        'name' varchar(40),
                        'file_id' text null,
                        'file_type' varchar(10) null,
                        'text' text,
                        'button' varchar(40),
                        'check_user' boolean,
                        'message_id' integer null
                    )
            """)
    cur.execute("""
                 CREATE TABLE IF NOT EXISTS 
                    'pool_field'(
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
    cur.execute("""
                 CREATE TABLE IF NOT EXISTS 
                    'question'(
                        'id' integer primary key AUTOINCREMENT,
                        'name' varchar(40),
                        'file_id' text null,
                        'file_type' varchar(10),
                        'text_visible' text null,
                        'text_hidden' varchar(100),
                        'button' varchar(40),
                        'check_user' boolean,
                        'message_id' integer null
                    )
            """)
    con.close()


async def create(table, data):
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


async def delete(table, key, value):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    try:
        if type(value) == int:
            back_data = cur.execute(f"""
                            DELETE FROM {table} WHERE {key} = {value}
                        """).rowcount
        else:
            back_data = cur.execute(f"""
                            DELETE FROM {table} WHERE {key} = '{value}'
                        """).rowcount
        con.commit()
    except sqlite3.Error as e:
        print(e)
        back_data = None
    con.close()
    return back_data


async def get_all(table, fields):
    fields_str = ", ".join(fields)
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(
                f"""
                    SELECT {fields_str} FROM {table}
                """
            ).fetchall()
    con.close()
    return data


async def get_all_by(table, fields, key, value, additional: str = ""):
    fields_str = ", ".join(fields)
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    if type(value) == int:
        data = cur.execute(
                f"""
                    SELECT {fields_str} FROM {table} WHERE {key} = {value}
                """+additional
            ).fetchall()
    else:
        data = cur.execute(
            f"""
                SELECT {fields_str} FROM {table} WHERE {key} = '{value}'
            """+additional
        ).fetchall()
    con.close()
    return data


async def get_one(table, fields, key, value):
    fields_str = ", ".join(fields)
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    if type(value) == int:
        data = cur.execute(
                f"""
                    SELECT {fields_str} FROM {table} WHERE {key} = {value}
                """
            ).fetchone()
    else:
        data = cur.execute(
            f"""
                SELECT {fields_str} FROM {table} WHERE {key} = '{value}'
            """
        ).fetchone()
    con.close()
    return data


async def set_message_id(table, new_value, where):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    try:
        status = cur.execute(f"""
                    UPDATE {table} SET message_id = {new_value} WHERE id = {where}
                """)
        con.commit()
        # test
        # raise sqlite3.Error("dwd")
    except sqlite3.Error as e:
        print(e)
        status = None
    con.close()
    return status


async def set_vote(field_id, user_id, message_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    try:
        cur.execute(f"""
                   UPDATE pool_field SET voted = voted + 1 WHERE id = {field_id}
               """)
        cur.execute(f"""
                   INSERT INTO vote('user_id', 'message_id') VALUES({user_id}, {message_id})
               """)
        con.commit()
        data = True
    except sqlite3.Error as e:
        print(e)
        data = None
    con.close()
    return data


async def get_voted(user_id, mess_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
            SELECT * FROM vote WHERE user_id = {user_id} AND message_id = {mess_id} 
        """).fetchone()
    con.close()
    return data
