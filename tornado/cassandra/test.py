# BEGIN PyInstaller dependencies
import cassandra.cqltypes
import cassandra.connection
import cassandra.cython_deps
import cassandra.encoder
import cassandra.io
import cassandra.io.asyncorereactor
import cassandra.marshal
import cassandra.metadata
import cassandra.policies
import cassandra.pool
import cassandra.protocol
import cassandra.query
import cassandra.type_codes
import cassandra.util
import decimal
import six
import uuid
# END PyInstaller dependencies

from cassandra.cluster import Cluster
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.concurrent import Future


def get_session():
    cluster = Cluster(["127.0.0.1"])
    session = cluster.connect()
    return session


def prepare_schema(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS demo_cassandra
            WITH REPLICATION =
            {
                'class': 'SimpleStrategy',
                'replication_factor': 1
            }""")

    session.execute("USE demo_cassandra")

    session.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id int PRIMARY KEY,
            name varchar,
            age int
        )""")


def populate_users(session):
    users = [
        (101, 'Alex', 30),
        (103, 'Kim', 23),
        (107, 'Jenny', 41),
    ]

    for user in users:
        session.execute(
            "insert into users (id, name, age) values (%s, %s, %s)",
            user)


def wrap_cassandra_execute(session, io_loop, cql, parameters=None, trace=False):
    """
    Wraps Cassandra async call into Tornado future object
    :param io_loop: Tornado IOLoop to post the Future result on
    :param cql: Cassandra cql query
    :return: tornado Future
    """
    tornado_future = Future()
    cassandra_future = session.execute_async(cql, parameters, trace)

    def _result(res):
        # For thread-safety the add_callback() is important. This is because
        # Cassandra sends the result from different thread.
        io_loop.add_callback(tornado_future.set_result, res)

    def _error(e):
        # For thread-safety the add_callback() is important. This is because
        # Cassandra sends the result from different thread.
        io_loop.add_callback(tornado_future.set_exception, e)

    cassandra_future.add_callbacks(_result, _error)
    return tornado_future


@gen.coroutine
def list_users(session, i):
    ids = yield wrap_cassandra_execute(
        session,
        IOLoop.current(),
        "select id from users")
    print('%d: IDs are ready - %s' % (i, ids))


def main():
    session = get_session()
    prepare_schema(session)
    populate_users(session)

    # Scheduling callback to do async "list_users()" 10 times
    for i in range(10):
        IOLoop.current().add_callback(list_users, session, i)

    IOLoop.current().start()

if __name__ == "__main__":
    main()
