""" Simulation environment package

This module defines the base class for the network simulation environment. It inherits from and is
based on SimPy's Environment class. It defines the context within which the simulation takes place
and also controls the simulation clock.

An environment is a necessary component of every simulation.
"""

import simpy
from numpy.random import RandomState


class NetworkEnvironment(simpy.Environment):
    """Base class defining simulation environment

    Description ...
    """
    def __init__(self, graph, seed=None, time_start=0):
        """Constructor

        Args:
            graph (Object): NetworkX Graph object on which to perform simulation.
            seed (Optional[int]): Seed for NumPy's RandomState
            time_start (Optional[int]): Time at which to start simulation
        """
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
