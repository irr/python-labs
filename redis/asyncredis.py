import asyncio
import aioredis


def main():
    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def go(params):
        conn = yield from aioredis.create_connection(
            ('localhost', 6379), encoding='utf-8')

        ok = yield from conn.execute(*params)
        print("%s = %s" % (params, ok,))

        conn.close()

    loop.run_until_complete(go(["GEOADD", "Sicily", "13.361389", "38.115556", "Palermo"]))
    loop.run_until_complete(go(["GEOADD", "Sicily", "15.087269", "37.502669", "Catania"]))
    loop.run_until_complete(go(["GEOHASH", "Sicily", "Palermo"]))
    loop.run_until_complete(go(["GEORADIUS","Sicily","15","37","200","km", "WITHDIST", "WITHCOORD"]))


if __name__ == '__main__':
    main()
