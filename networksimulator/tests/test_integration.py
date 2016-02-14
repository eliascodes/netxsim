#!/usr/bin/env python3
"""

"""
import networkx as nx
from .. import agents, builders, environment, grid, logger, results, simulator
from matplotlib import pyplot as plt
from numpy import random


class Agent(agents.BaseAgent):
    def run(self, graph, env):
        while True:
            if env.draw('normal') > 0:
                graph.node[self]['state'] = not graph.node[self]['state']
            yield env.timeout(1)


class Logger(logger.BaseLogger):
    def get_state(self, graph):
        return sum([1*attr['state'] for (_, attr) in graph.nodes(data=True)])


class Case(simulator.BaseSimCase):
    def __init__(self, runtime=0):
        super().__init__(runtime=runtime)

    def _prepare_grid(self):
        self.grid = grid.BaseGrid().add_dimensions(seed=[0, 1, 2, 3, 4])
        return self.grid

    def _prepare_env(self, graph, **kwargs):
        return environment.NetworkEnvironment(graph, seed=kwargs['seed'])

    def _prepare_graph(self, **kwargs):
        rng = random.RandomState(kwargs['seed'])
        num_nodes = 100

        b = builders.GraphFactory(rng)
        b.set_size(num_nodes)
        b.set_agent(Agent)
        b.set_node_attribute(alive=True, sick=False)
        b.set_node_attribute(carrier=('normal', [0, 1], {'loc': 0}), immune=('binomial', [40, 0.05]))
        b.set_node_attribute(vulnerable=(random.beta, [0.1, 0.2]))
        b.set_edge_by_distribution(('normal', [0, 1], {}), threshold=0)
        b.set_edge_attribute(contact_frequency=('uniform', [0, 1]))

        return b.build()

    def _prepare_logger(self, graph, env, **kwargs):
        factory = logger.LoggerFactory(Logger, '/Users/elias/projects/networksimulator/_results/')
        factory.name = 'sandbox'
        factory.prefix = 'results'
        factory.id = grid.hash_grid_point(kwargs)
        factory.buffer_size = 1024 * 1024 * 100  # 100 MB
        factory.replace_previous = True
        log = factory.build()
        log.register(graph, env)
        return log


def test_full_simulation_flow():
    s = Case(100)
    s.run()
    r = results.from_grid(s.grid.subgrid_from_values(seed=[4]), '/Users/elias/projects/networksimulator/_results/')
    plt.plot(r[0].data)
    plt.show(block=True)