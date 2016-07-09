from cassandra.cluster import Cluster
from cassandra.util import unix_time_from_uuid1
from cassandra import ConsistencyLevel

import time, datetime

cluster = Cluster(['localhost'])
session = cluster.connect('irr')

for t in range(10):
    print("inserting data... %d" % (t,))
    session.execute(
        "INSERT INTO rt_series (id, ts, val) VALUES (%(id)s,now(),%(val)s) USING TTL 3600;",
        {'id': "1234ABCD", 'val': t})
    time.sleep(0.1)

rows = session.execute('SELECT id, ts, val FROM rt_series LIMIT 10')
for row in rows:
    print(row[0], row[1], unix_time_from_uuid1(row[1]), row[2])
