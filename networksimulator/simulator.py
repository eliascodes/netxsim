"""Simulation case and utility functions

"""
import datetime
import collections
import networkx
import simpy


class BaseSimCase(object):
    """Base class for simulation case specification

    In order to define a simulation case, this class must be sub-classed, and the _prepare_* methods
    must be redefined.

    Arguments:
        runtime : (int) [optional] : The runtime of the simulation
    """

    timestamp_start = ''
    timestamp_case = []
    timestamp_end = ''

    def __init__(self, runtime=0):
        self.runtime = runtime
        self.success = False

    def run(self):
        """Exectue the simulation

        Runs the simulation for each point in the grid and logs the outputs
        """
        self.timestamp_start = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

        for point in self._prepare_grid():
            graph = self._prepare_graph(**point)
            env = self._prepare_env(graph, **point)
            logger = self._prepare_logger(env, **point)

            try:
                env.run(until=self.runtime)
            except Exception as e:
                print(e)
            logger.save()

            self.timestamp_case.append(datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))

        self.timestamp_end = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        return (logger, graph)

    def _prepare_grid(self):
        """Creates and returns the parameter grid determining the parameters of each sim case.
        """
        return collections.Iterable()

    def _prepare_graph(self, **kwargs):
        """Creates and returns the NetworkX graph object on which each sim case is run.

        Arguments:
            kwargs : (dict) : key-value pairs determining the grid point parameters
        """
        return networkx.Graph()

    def _prepare_env(self, graph, **kwargs):
        """Creates and returns the SimPy Environment object defining the simulation context.

        Arguments:
            kwargs : (dict) : key-value pairs determining the grid point parameters
        """
        return simpy.Environment()

    def _prepare_logger(self, env, **kwargs):
        """Creates and returns the NetworkX graph object on which each sim case is run

        Arguments:
            env : (SimPy.Environment) : Environment object
            kwargs : (dict) : key-value pairs determining the grid point parameters
        """
        pass


def run_simulation(simcase):
    """Run simulation

    Arguments:
        simcase : (NetSimCase) : Simcase object
    """
    return simcase.run()
