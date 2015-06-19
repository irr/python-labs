import select, psycopg2

# Wait for async access
def wait(conn):
    while 1:
        state = conn.poll()
        if state == psycopg2.extensions.POLL_OK:
            break
        elif state == psycopg2.extensions.POLL_WRITE:
            select.select([], [conn.fileno()], [])
        elif state == psycopg2.extensions.POLL_READ:
            select.select([conn.fileno()], [], [])
        else:
            raise psycopg2.OperationalError("poll() returned %s" % state)

# Connect to an existing database
conn = psycopg2.connect("dbname=postgis user=postgres password=postgres host=localhost", async = 1)
wait(conn)

# Open a cursor to perform database operations
cur = conn.cursor()

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM spatial_ref_sys;")
wait(cur.connection)

print(cur.fetchone())

# Close communication with the database
cur.close()
wait(cur.connection)

conn.close()
