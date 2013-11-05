from geventmemcache.client import Memcache

servers = [(("127.0.0.1", 11211), 100)]

client = Memcache(servers)

client.set("TestKey", 123)
result = client.get("TestKey")

print "Result is", result