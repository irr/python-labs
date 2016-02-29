import redis, time, geohash

pool = redis.ConnectionPool(host='localhost', port=6379,
                            db=0, max_connections=100)

red = redis.StrictRedis(connection_pool=pool)

# latitude = 38.115556
# longitude = 13.361389
# redis GEOADD(long, lat)

# 127.0.0.1:6379> monitor
# OK
# 1456770847.500229 [0 127.0.0.1:57960] "MULTI"
# 1456770847.500256 [0 127.0.0.1:57960] "GEOADD" "Sicily" "13.361389" "38.115556" "Palermo"
# 1456770847.500290 [0 127.0.0.1:57960] "GEOADD" "Sicily" "15.087269" "37.502669" "Catania"
# 1456770847.500305 [0 127.0.0.1:57960] "EXEC"
# 1456770847.500573 [0 127.0.0.1:57960] "GEOHASH" "Sicily" "Palermo"
# 1456770847.500835 [0 127.0.0.1:57960] "GEOHASH" "Sicily" "Catania"
# 1456770847.501096 [0 127.0.0.1:57960] "GEORADIUS" "Sicily" "15" "37" "200" "km" "WITHDIST"
# 1456770847.501386 [0 127.0.0.1:57960] "GEORADIUS" "Sicily" "15" "37" "200" "km" "WITHCOORD"
# 1456770847.501827 [0 127.0.0.1:57960] "GEORADIUS" "Sicily" "15" "37" "200" "km" "WITHDIST" "WITHCOORD"
# 1456770847.502271 [0 127.0.0.1:57960] "GEODIST" "Sicily" "Palermo" "Catania" "km"

pipe = red.pipeline()
pipe.execute_command("GEOADD Sicily 13.361389 38.115556 Palermo")
pipe.execute_command("GEOADD Sicily 15.087269 37.502669 Catania")
pipe.execute()

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

def tspush(r, key, values):
    p = r.pipeline()
    p.lpush(key, *values)
    p.ltrim(key, 0, 4) # 5 elements
    p.lrange(key, 0, 4)
    return p.execute()

start = 0
while True:
    print(tspush(red, "ts", range(start, start+10))[2])
    start += 10
    time.sleep(3)


