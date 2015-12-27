from ABC import abstractmethod
from enum import Enum
import os
import pickle
from networksimulator.results import NetSimResults


class SaveFormat(Enum):
    NONE = 0
    PICKLE = 1
    JSON = 2
    CSV = 3


class DataFormat(Enum):
    RAW = 1
    CUSTOM = 2


class BaseLogger(object):
    """Base class for logging simulation signals

    Attributes:
        interval_log : (int, Default = 1) : Simulation time interval at which to record system
                                            state. Used to set the timeout event.
        interval_dump : (int, Default = None) : Multiple of logging intervals to batch into a single
                                                save file. A falsy value means to collect all
                                                logging intervals into a single batch.
        format_save : (SaveFormat) : Determines save format.
        format_data : (DataFormat) : Determines data archive format.
        path_save : (string) : System directory in which to save logged results. If path_save is the
                               empty string and format_save is not SaveFormat.NONE, the results will
                               be saved to the current working directory (pwd).

    Arguments:
        period : (int) : multiple of timesteps at which to dump results
    """

    _state_hist = []

    interval_log = 1
    interval_dump = None

    format_save = SaveFormat.NONE
    format_data = DataFormat.RAW

    path_save = ''
    name_save = ''

    def __init__(self):
        self.io = FileWriter()

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

        Yeilds:
            SimPy.Event object, a timeout after one logging interval

        Returns:
            None
        """
        while True:
            self.store_state(self.get_state(graph))
            yield env.timeout(self.interval_log)

    def save(self, in_parts=False):
        """
        """
        if format_save == SaveFormat.NONE:
            return self._state_hist

        if not self.path_save:
            self.path_save = os.getcwd()

        try:
            os.makedirs(self.path_save, exist_ok=True)
        except Exception as e:
            print 'Could not save file to specified directory, returning results instead'
            return self._state_hist

        name_base = self.name_save if self.name_save else 'results_'
        name_base += datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        suffix = ''

    def store_state(self, state):
        """
        """
        self._state_hist.append(state)
        if self.interval_dump and len(self._state_hist) > self.interval_dump:
            self.save()
            self._state_hist = []
