"""
curl -v -X POST -H 'Content-Type: application/json' https://identity-dbtest.cluster-czkfhyvgzymk.us-east-1.neptune.amazonaws.com:8182/system -d '{ "action" : "initiateDatabaseReset" }'

pip install -U setuptools
pip install wheel
pip install gremlinpython
"""

import os

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.structure.graph import Graph

graph = Graph()

remoteConn = DriverRemoteConnection(os.getenv('GRAPH_DB'),'g')
g = graph.traversal().withRemote(remoteConn)


def add_node(g, p):
    person = get_node(g, p['id'])
    if person:
        return person
    o = g.addV(p['label']).property(T.id, p['id']).next()
    for n, v in p.items():
        if n not in ['id', 'label']:
            g.V(o).property(n, v).next()
    return o


def get_node(g, pid):
    return [{**node.__dict__, **properties} for node in g.V(pid)
            for properties in g.V(node).valueMap()]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # cleanup database
    g.V().drop().iterate()

    # clean properties
    # g.V(person).properties().drop().iterate()

    add_node(g, {"id": "irrlab", "label": "person", "name": "Ivan Rocha", "login": "irr"})
    add_node(g, {"id": "irrlab2", "label": "person", "name": "Ivan Ribeiro Rocha", "login": "irocha"})

    print(get_node(g, "irrlab"))
    print(get_node(g, "irrlab2"))
