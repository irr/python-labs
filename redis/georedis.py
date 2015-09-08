import redis

pool = redis.ConnectionPool(host='localhost', port=6379,
                            db=0, max_connections=100)

red = redis.StrictRedis(connection_pool=pool)

red.execute_command("GEOADD Sicily 13.361389 38.115556 Palermo")
red.execute_command("GEOADD Sicily 15.087269 37.502669 Catania")

print red.execute_command("GEOHASH Sicily Palermo")

print red.execute_command("GEORADIUS Sicily 15 37 200 km WITHDIST")

print red.execute_command("GEORADIUS Sicily 15 37 200 km WITHCOORD")

print red.execute_command("GEORADIUS Sicily 15 37 200 km WITHDIST WITHCOORD")

print red.execute_command("GEODIST Sicily Palermo Catania km")
