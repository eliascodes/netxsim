from abc import ABCMeta, abstractmethod
import numpy.random as nprand


class AgentGenerator(AbstractGenerator):
    """"""
    def __init__(self, agent_type):
        if issubclass(agent_type, AbstractAgent):
            self.agent_type = agent_type
        else:
            raise TypeError("Input must be an Agent type")

    def get_next(self):
        count = 0
        while True:
            yield self.agent_type(count)
            count += 1


class AttributeGenerator(AbstractGenerator):
    """"""
    def __init__(self, seed):
        self.rng = nprand.RandomState(seed)
        self.attr_deterministic = {}
        self.attr_stochastic = {}
        self._frozen = False

    def set_deterministic(self, attr, value):
        raise BaseException("Frozen") if self._frozen
        self.attr_deterministic[attr] = value
        return self

    def set_stochastic(self, attr, params):
        raise BaseException("Frozen") if self._frozen
        if hasattr(self.rng, params['distribution']):
            self.attr_stochastic[attr] = params
        else:
            raise AttributeError('{0} is not a valid method of {1}'
                                 .format(params['distribution'], self.rng))
        return self

    def get_next(self):
        self._frozen = True
        while True:
            attr_dic = self.attr_deterministic
            for key in self.attr_stochastic:
                distn = self.attr_stochastic[key]['distribution']
                args = self.attr_stochastic[key]['arguments']
                attr_dic[attr] = getattr(self.rng, distn)(*args)
            yield attr_dic
