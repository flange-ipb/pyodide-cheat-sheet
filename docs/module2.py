import numpy as np
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF


def calc_det():
    a = np.array([[1, 2], [3, 4]])
    print(f"Determinant is {np.linalg.det(a)}")


def serialize_graph():
    g = Graph()

    alice = URIRef("http://example.org/alice")
    bob = URIRef("http://example.org/bob")

    g.add((alice, FOAF.name, Literal("Alice")))
    g.add((bob, FOAF.name, Literal("Bob")))
    g.add((alice, FOAF.knows, bob))

    return g.serialize()
