#!/usr/bin/env python3
from networksimulator.tests.support import toyclasses
import networkx as nx


def test_hashability():
    one = toyclasses.ToyDeterministicAgent(1)
    two = toyclasses.ToyDeterministicAgent(2)
    uno = toyclasses.ToyDeterministicAgent(1)

    assert(one == uno)
    assert(one != two)
    assert(two != uno)


def test_can_populate_graph():
    G = nx.Graph()

    agent1 = toyclasses.ToyDeterministicAgent(1)
    G.add_node(agent1)

    assert(G.number_of_nodes() == 1)
    assert(G.number_of_edges() == 0)
    assert(G.node[agent1] == {})
    for node in G.nodes():
        assert(node == agent1)

    G.node[agent1]['attribute1'] = True
    assert(G.node[agent1] == {'attribute1': True})

    agent2 = toyclasses.ToyDeterministicAgent(2)
    G.add_node(agent2, {'attribute2': True})

    G.add_edge(agent1, agent2)

    assert(G.number_of_nodes(), 2)
    assert(G.number_of_edges(), 1)
    assert(G.node[agent2] == {'attribute2': True})
    for node in G.nodes():
        assert(node == agent1 or node == agent2)

    agent3 = toyclasses.ToyDeterministicAgent(3)
    agent3.testAttr = 2
    assert(getattr(agent3, 'testAttr') == 2)

    G.add_node(agent3)

    assert(G.number_of_nodes(), 3)
    print(G.node[agent3])
    assert(G.node[agent3] == {'testAttr': 2})
