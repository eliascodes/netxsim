#!/usr/bin/env python3
"""

"""
import networkx as nx
from .. import agents


class Agent(agents.BaseAgent):
    def run(self, graph, env):
        while True:
            yield env.timeout(1)


def test_hashability():
    one = Agent(1)
    two = Agent(2)
    uno = Agent(1)

    assert(one == uno)
    assert(one != two)
    assert(two != uno)


def test_can_populate_graph():
    G = nx.Graph()

    agent1 = Agent(1)
    G.add_node(agent1)

    assert(G.number_of_nodes() == 1)
    assert(G.number_of_edges() == 0)
    assert(G.node[agent1] == {})
    for node in G.nodes():
        assert(node == agent1)

    G.node[agent1]['attribute1'] = True
    assert(G.node[agent1] == {'attribute1': True})

    agent2 = Agent(2)
    G.add_node(agent2, {'attribute2': True})

    G.add_edge(agent1, agent2)

    assert(G.number_of_nodes(), 2)
    assert(G.number_of_edges(), 1)
    assert(G.node[agent2] == {'attribute2': True})
    for node in G.nodes():
        assert(node == agent1 or node == agent2)

    agent3 = Agent(3)
    agent3.testAttr = 2
    assert(getattr(agent3, 'testAttr') == 2)

    G.add_node(agent3)

    assert(G.number_of_nodes(), 3)
    print(G.node[agent3])
    assert(G.node[agent3] == {'testAttr': 2})
