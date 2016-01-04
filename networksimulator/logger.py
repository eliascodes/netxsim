"""Logging module

Very simple logging just to get going: store full graph state in memory every timestep and pickle
and dump at the end.


"""

import os
import io
import re
import pickle
import datetime


class BaseLogger(io.BufferedWriter):
    """Base class for logging simulation signals
    """

    def __init__(self, filepath, interval_log, buffer_size=io.DEFAULT_BUFFER_SIZE):
        """Constructor

        Args:
            filepath: (string) absolute path of results file
            interval_log: (int) interval at which to log model state
            buffer_size: (int) number of bytes to keep in memory before writing to file
        """
        raw = io.FileIO(os.path.normcase(filepath), 'ab')
        super().__init__(raw, buffer_size=buffer_size)
        self.interval_log = interval_log

    def register(self, graph, env):
        """Creates process instance of log method to run along with the simulation

        Args:
            graph : (NetworkX.Graph) : Graph object - subject of simulation
            env : (SimPy.Environment) : Simulation environment
        """
        env.process(self.log(graph, env))

    def log(self, graph, env):
        """Process for logging signals for each logging interval

        Args:
            graph : (NetworkX.Graph) : Graph object - subject of simulation
            env : (SimPy.Environment) : Simulation environment

        Yields:
            SimPy.Event object, a timeout after one logging interval
        """
        while True:
            self.save(self.get_state(graph))
            yield env.timeout(self.interval_log)

    def save(self, data=None):
        """Alias for flush

        Args:
            data: (bytes) : data to be written to stream
        """
        if data is not None:
            self.write(bytes(data))
        else:
            self.flush()

    def get_state(self, graph):
        """Transforms the graph object at a given simulator time-step into the data-structure describing the state of the
        simulator, then passed to `store_state`. Default behaviour is to simply return the graph object itself.
        Overwrite this method to alter the data-structure that gets passed to `store_state`.

        Args:
            graph: (NetworkX.Graph) : Graph object - subject of simulation

        Returns:
            Object describing the instantaneous state of the simulator

        """
        return pickle.dumps(graph)


class LoggerFactory(object):
    """

    """

    def __init__(self, logger_class, dir_results):
        self.dir_results = dir_results
        self.prefix = 'log'
        self.name = 'simulation'
        self.id = ''
        self.timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        self.fext = 'pickle'
        self.logger_class = logger_class
        self.interval_log = 1
        self.buffer_size = io.DEFAULT_BUFFER_SIZE
        self.replace_previous = False

    def build_file_prefix(self):
        pre = [self.prefix, self.name, self.id]
        return '_'.join(filter(lambda x: x, pre))

    def build_file_path(self):
        pre = [self.prefix, self.name, self.id, self.timestamp]
        pre = '_'.join(filter(lambda x: x, pre))
        if self.fext:
            pre += '.' + self.fext
        return os.path.join(self.dir_results, pre)

    def build(self):
        os.makedirs(os.path.normcase(self.dir_results), exist_ok=True)

        contents = os.listdir(os.path.normcase(self.dir_results))
        contents = [f for f in contents if os.path.isfile(os.path.join(self.dir_results, f))]

        fprefix = self.build_file_prefix()

        if len(contents) > 0 and self.replace_previous:
            for file in contents:
                if re.match(fprefix, file):
                    os.remove(file)

        return self.logger_class(self.build_file_path(), self.interval_log, buffer_size=self.buffer_size)
