#!/usr/bin/env python3
"""

"""
import networkx as nx
from .. import agents, builders, environment, generators, grid, logger, results, simulator
from matplotlib import pyplot as plt
import pickle


class Builder(builders.BaseGraphBuilder):
    def _prepare_build(self, **kwargs):
        g_agent = generators.AgentGenerator(Agent)
        g_attr = generators.AttributeGenerator(0)
        g_attr.set_deterministic('state', True)
        self.set(size=100, gen_agent=iter(g_agent), gen_attr=iter(g_attr))

    def _construct(self, **kwargs):
        graph = nx.Graph()
        while graph.number_of_nodes() < self.size:
            node_agent = next(self.gen_agent)
            node_attr = next(self.gen_attr)
            graph.add_node(node_agent, node_attr)
        return graph


class Agent(agents.BaseAgent):
    def run(self, graph, env):
        while True:
            if env.draw('normal') > 0:
                graph.node[self]['state'] = not graph.node[self]['state']
            yield env.timeout(1)


class Logger(logger.BaseLogger):
    def get_state(self, graph):
        return pickle.dumps(sum([1*attr['state'] for (_, attr) in graph.nodes(data=True)]))


class Case(simulator.BaseSimCase):
    def __init__(self, runtime=0):
        super().__init__(runtime=runtime)

    def _prepare_grid(self):
        self.grid = grid.BaseGrid().add_dimensions(seed=[0, 1, 2, 3, 4])
        return self.grid

    def _prepare_env(self, graph, **kwargs):
        return environment.NetworkEnvironment(graph, seed=kwargs['seed'])

    def _prepare_graph(self, **kwargs):
        return Builder().build(**kwargs)

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
    s = Case(5)
    s.run()
    r = results.from_grid(s.grid.subgrid_from_values(seed=[4]), '/Users/elias/projects/networksimulator/_results/')
    plt.plot(r[0].data)
    plt.show(block=True)