import psycopg2
conn = cur = None

def connect():
    global con, cur, db
    try:
        conn = psycopg2.connect(
            host = hostname,
            database = database,
            user = username,
            password = password,
            port = port
        )

        cur = conn.cursor()
        db = cur.execute

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:   
            conn.close()

def get_db():
    if not (con and cur and db):
        connect()
    return (con, cur, db)