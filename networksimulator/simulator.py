"""Simulation case and utility functions

"""
import datetime


class BaseSimCase(object):
    """Base class for simulation case specification

    In order to define a simulation case, this class must be sub-classed, and the _prepare_* methods
    must be redefined.

    Arguments:
        runtime : (int) [optional] : The runtime of the simulation
    """

    def __init__(self, runtime=0):
        self.grid = None
        self.runtime = runtime
        self.success = False
        self.timestamp = {
            'start': None,
            'end': None
        }

    def run(self):
        """Execute the simulation

        Runs the simulation for each point in the grid and logs the outputs
        """
        self.timestamp['start'] = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

        for point in self._prepare_grid():
            graph = self._prepare_graph(**point)
            env = self._prepare_env(graph, **point)
            log = self._prepare_logger(graph, env, **point)

            try:
                env.run(until=self.runtime)
            except Exception as e:
                print(e)
            log.close()

            # self.timestamp[grid.hash_grid_point(point)].append(datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))

        self.timestamp['end'] = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

    def _prepare_grid(self):
        """Creates and returns the parameter grid determining the parameters of each sim case.

        This method should be deterministic
        """
        raise NotImplementedError

    def _prepare_graph(self, **kwargs):
        """Creates and returns the NetworkX graph object on which each sim case is run.

        This method should be deterministic

        Arguments:
            kwargs : (dict) : key-value pairs determining the grid point parameters
        """
        raise NotImplementedError

    def _prepare_env(self, graph, **kwargs):
        """Creates and returns the SimPy Environment object defining the simulation context.

        This method should be deterministic

        Arguments:
            kwargs : (dict) : key-value pairs determining the grid point parameters
        """
        raise NotImplementedError

    def _prepare_logger(self, graph, env, **kwargs):
        """Creates and returns the NetworkX graph object on which each sim case is run

        This method should be deterministic

        Arguments:
            kwargs : (dict) : key-value pairs determining the grid point parameters
        """
        raise NotImplementedError
