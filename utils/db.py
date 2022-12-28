import sqlite3


def init():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
            'governor'(
                'id' integer primary key AUTOINCREMENT,
                'name' varchar(150),
                'vote' integer
            )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
            'voted'(
                'id' integer primary key AUTOINCREMENT,
                'user_id' integer,
                'mess_id' integer
            )
    """)
    con.close()


def get_governors():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute("""
        SELECT * FROM governor ORDER BY -vote
    """).fetchall()
    con.close()
    return data


def set_vote(gov_id, user_id, message_id):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    status = None
    try:
        old_id = cur.execute(f"""
                SELECT vote FROM governor WHERE id={gov_id}
            """).fetchone()
        new_id = old_id[0] + 1
        cur.execute(f"""
                    UPDATE governor SET vote = {new_id} WHERE id={gov_id}
                """)
        cur.execute(f"""
            INSERT INTO voted('user_id', 'mess_id') VALUES({user_id}, {message_id})
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
            SELECT user_id FROM voted WHERE user_id = {user_id} AND mess_id = {mess_id} 
        """).fetchone()
    con.close()
    return data
