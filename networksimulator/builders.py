from abc import ABCMeta, abstractmethod
import numpy as np


class AbstractEnsembleBuilder(object):
    """
    Abstract base class for all ensemble builders.

    Ensemble builders create ensembles of objects whose attributes fullfil
    certain statistical properties.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        pass


class AgentEnsembleBuilder(AbstractEnsembleBuilder):
    """
    Base class for all agent ensemble builders.

    Creates an ensemble of agent objects.
    """

    def __init__(self, seed, size):
        self.rng = np.random.RandomState(seed)
        self.size = size
        self.attribute_map = {}

    def set_attribute_distribution(self, attribute, distn):
        self.attribute_map[attribute] = distn

    def build(self):
        for ii in range(self.size):
            
        pass
