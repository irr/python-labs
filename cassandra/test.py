from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel

import time, datetime

cluster = Cluster(['localhost'])
session = cluster.connect('irr')

for t in range(10):
    print("inserting data... %d" % (t,))
    session.execute(
        "INSERT INTO series (id, ts, value) VALUES (%(id)s,%(ts)s,%(value)s) USING TTL 3600;",
        {'id': "1234ABCD", 'ts': datetime.datetime.now(), 'value': t})
    time.sleep(0.1)

rows = session.execute('SELECT id, ts, value FROM series LIMIT 10')
for row in rows:
    print row[0], row[1], row[2]
