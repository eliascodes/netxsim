import numpy.random as np_rand
import copy
from . import agents


class BaseGeneratorBuilder(object):
    """Base class for generator builders
    Defines the common interface, and the freezing functionality
    """
    def __init__(self):
        self.__frozen__ = False

    def __iter__(self):
        raise NotImplementedError

    def build(self):
        return iter(self)

    @property
    def frozen(self):
        return self.__frozen__

    def freeze(self):
        self.__frozen__ = True

    def unfreeze(self):
        self.__frozen__ = False


class AgentGeneratorBuilder(BaseGeneratorBuilder):
    """Builds an Agent generator that yields agents of a given type
    """
    def __init__(self, agent_type):
        """
        Args:
            agent_type: <class> defines the agent type to be instantiated and yielded
        """
        if not issubclass(agent_type, agents.BaseAgent):
            raise TypeError("Input must be an Agent type")

        super().__init__()
        self.agent_type = agent_type

    def __iter__(self):
        count = 0
        while True:
            yield self.agent_type(count)
            count += 1


class AttributeGeneratorBuilder(BaseGeneratorBuilder):
    """Builds an node attribute generator that yields attribute dictionaries
    """
    def __init__(self, seed):
        """
        Args:
            seed: <int> Seed for numpy's RandomState RNG
        """
        super().__init__()
        self.__rng__ = np_rand.RandomState(seed)
        self.__constant__ = {}
        self.__stochastic__ = {}

    def add_constant(self, **kwargs):
        """Adds an attribute with a constant value for each iteration

        Args:
            kwargs: <dict> Name-value pairs of constant attributes
        """
        if self.frozen:
            raise BaseException("frozen")
        for (attr, val) in kwargs.items():
            self.__constant__[attr] = val
        return self

    def add_stochastic(self, attr, **kwargs):
        """Adds an attribute with a randomly varying value for each iteration
        Utilises numpy's random number generators and RandomState object

        Args:
            attr: <string> Name of the attribute to be generated
            kwargs: <dict> Distribution-argument pairs, matching methods of numpy's RandomState

        Example: add_stochastic('hasFlu', binomial=[n, p])
        """
        if self.frozen:
            raise BaseException("frozen")
        for (k, v) in kwargs.items():
            if not hasattr(self.__rng__, k):
                raise AttributeError('{0} is not a valid method of {1}'.format(k, self.__rng__))
            self.__stochastic__[attr] = {'distribution': k, 'arguments': v}
        return self

    def __iter__(self):
        self.freeze()
        while True:
            attr_dic = copy.deepcopy(self.__constant__)
            for key in self.__stochastic__:
                dist = self.__stochastic__[key]['distribution']
                args = self.__stochastic__[key]['arguments']
                attr_dic[key] = getattr(self.__rng__, dist)(*args)
            yield attr_dic
