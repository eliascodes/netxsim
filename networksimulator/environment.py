import simpy
from numpy.random import RandomState


class NetworkEnvironment(simpy.Environment):
    """"""
    def __init__(self, graph, seed=None, time_start=0):
        super().__init__(initial_time=time_start)
        if seed:
            self.rng = RandomState(seed)
        for node in graph:
            self.process(node.run(graph, self))

    def draw(self, distribution):
        arg_dict = {
            'normal': [0, 1]
        }
        args = arg_dict[distribution]
        return getattr(self.rng, distribution)(*args)
