import redis, geohash

pool = redis.ConnectionPool(host='localhost', port=6379,
                            db=0, max_connections=100)

red = redis.StrictRedis(connection_pool=pool)

# latitude = 38.115556
# longitude = 13.361389
# redis GEOADD(long, lat)
red.execute_command("GEOADD Sicily 13.361389 38.115556 Palermo")
red.execute_command("GEOADD Sicily 15.087269 37.502669 Catania")

print("redis-geohash  (Palermo):", red.execute_command("GEOHASH Sicily Palermo"))
# redis GEOADD(long, lat)
# geohash.encode(lat, long)
print("python-geohash (Palermo):", geohash.encode(38.115556, 13.361389, precision=10))

print("redis-geohash  (Catania):", red.execute_command("GEOHASH Sicily Catania"))
# redis GEOADD(long, lat)
# geohash.encode(lat, long)
print("python-geohash (Catania):", geohash.encode(37.502669, 15.087269, precision=10))

print(red.execute_command("GEORADIUS Sicily 15 37 200 km WITHDIST"))

print(red.execute_command("GEORADIUS Sicily 15 37 200 km WITHCOORD"))

print(red.execute_command("GEORADIUS Sicily 15 37 200 km WITHDIST WITHCOORD"))

print(red.execute_command("GEODIST Sicily Palermo Catania km"))
