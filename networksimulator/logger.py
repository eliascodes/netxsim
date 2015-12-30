"""Logging module

Very simple logging just to get going: store full graph state in memory every timestep and pickle
and dump at the end.


"""

import os
import sys
import math
import pickle
import datetime


class BaseLogger(object):
    """Base class for logging simulation signals

    Attributes:
        name: (string) : Name of simulation case to append to results filename.
        interval_log: (int) : Simulation time interval at which to record system state. Used to set the timeout event.
        path_save: (string) : System directory in which to save logged results. If path_save is the empty string and
                               format_save is not SaveFormat.NONE, the results will be saved to the current working
                               directory (pwd).
        _state_hist: (list) : List of stored states in simulation-chronological order.
    """

    _state_hist = []

    def __init__(self, name, interval_log, path_save=''):
        self.name = name
        self.interval_log = interval_log
        self.path_save = path_save

    def register(self, graph, env):
        """Creates process instance of log method to run along with the simulation

        Arguments:
            graph : (NetworkX.Graph) : Graph object - subject of simulation
            env : (SimPy.Environment) : Simulation environment

        Returns:
            None
        """
        env.process(self.log(graph, env))

    def log(self, graph, env):
        """Process for logging signals for each logging interval

        Arguments:
            graph : (NetworkX.Graph) : Graph object - subject of simulation
            env : (SimPy.Environment) : Simulation environment

        Yields:
            SimPy.Event object, a timeout after one logging interval

        Returns:
            None
        """
        while True:
            self.store_state(self.get_state(graph))
            yield env.timeout(self.interval_log)

    def flush(self):
        """Empty the state history stored in the logger
        """
        self._state_hist = []

    def save(self):
        """Saves the state history as a pickled file with a timestamp
        """

        if not self.path_save:
            self.path_save = os.getcwd()

        try:
            os.makedirs(self.path_save, exist_ok=True)
        except Exception as e:
            print('Could not save file to specified directory, returning results instead')
            return self._state_hist

        name = 'results_' + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        path = os.path.join(self.path_save, name)
        with open(path, 'wb') as f:
            pickle.dump(self._state_hist, f)

    def get_state(self, graph):
        """Transforms the graph object at a given simulator time-step into the data-structure describing the state of the
        simulator, then passed to `store_state`. Default behaviour is to simply return the graph object itself.
        Overwrite this method to alter the data-structure that gets passed to `store_state`.

        Args:
            graph: (NetworkX.Graph) : Graph object - subject of simulation

        Returns:
            Object describing the instantaneous state of the simulator

        """
        return graph

    def store_state(self, state):
        """Stores the state of the simulator for retrieval at a later point. Default behaviour of BaseLogger is simply
        to hold a list of states in internal memory. See StateLimitedLogger and MemoryLimitedLogger for loggers
        providing more control over how the states are stored, or overwrite this method.

        Args:
            state: (mixed) : Object describing the instantaneous state of the simulator

        Returns:

        """
        self._state_hist.append(state)


class StateLimitedLogger(BaseLogger):
    """Limits the number of states that can be stored in memory before writing them to file
    """
    def __init__(self, name, interval_log, limit_num_states=100):
        """
        Keyword Args:
            limit_num_states: (int) | Default=100 | Limit for number of simulator states to keep in memory before saving
        """
        super().__init__(name, interval_log)
        self.limit_num_states = limit_num_states

    def store_state(self, state):
        """If the number of states stored in memory is greater than or equal to the limit attribute, the states are
        saved to disk and flushed from memory.

        Args:
            state: (mixed) | Object describing the instantaneous state of the simulator, to be stored
        """
        if len(self._state_hist) >= self.limit_num_states:
            self.save()
            self.flush()
        self._state_hist.append(state)


class MemoryLimitedLogger(StateLimitedLogger):
    """Limits the memory that stored states can use before writing them to file
    """
    def __init__(self, name, interval_log, limit_bytes_states=1024):
        """
        Keyword Args:
            limit_bytes_states: (int) | Default=1024 | Maximum memory limit on simulator states before saving
        """
        super().__init__(name, interval_log, limit_num_states=0)
        self.limit_bytes_states = limit_bytes_states
        self.est_bytes_state = None

    def store_state(self, state):
        """When storing the first state, calculate the size of the pickled string and use it to estimate the number of
        states that can be stored before exceeding the memory limit

        Args:
            state: (mixed) | Object describing the instantaneous state of the simulator, to be stored
        """
        if len(self._state_hist) > 0 and self.est_bytes_state is None:
            self.est_bytes_state = sys.getsizeof(pickle.dumps(self._state_hist[0]))
            self.limit_num_states = math.floor(self.limit_bytes_states / self.est_bytes_state)
        super().store_state(state)
