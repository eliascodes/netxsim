from numpy.random import RandomState
from . import agents


class AgentGenerator(object):
    """"""
    def __init__(self, agent_type):
        if issubclass(agent_type, agents.BaseAgent):
            self.agent_type = agent_type
        else:
            raise TypeError("Input must be an Agent type")

    def build(self):
        return iter(self)

    def __iter__(self):
        count = 0
        while True:
            yield self.agent_type(count)
            count += 1


class AttributeGenerator(object):
    """"""
    def __init__(self, seed):
        if seed is None:
            seed = 0
        self.rng = RandomState(seed)
        self.attr_deterministic = {}
        self.attr_stochastic = {}
        self._frozen = False

    def set_deterministic(self, attr, value):  # TODO change to kwargs
        if self._frozen:
            raise BaseException("Frozen")
        self.attr_deterministic[attr] = value
        return self

    def set_stochastic(self, attr, distribution=None, arguments=None):  # TODO change to kwargs
        if self._frozen:
            raise BaseException("Frozen")
        elif distribution is not None and arguments is not None:
            if hasattr(self.rng, distribution):
                self.attr_stochastic[attr] = {'distribution': distribution, 'arguments': arguments}
            else:
                raise AttributeError('{0} is not a valid method of {1}'.format(distribution, self.rng))
        else:
            raise TypeError("Inputs must not be NoneType")
        return self

    def freeze(self):
        self._frozen = True
        return self

    def unfreeze(self):
        self._frozen = False
        return self

    def build(self):
        return iter(self)

    def __iter__(self):
        self.freeze()
        while True:
            attr_dic = self.attr_deterministic
            for key in self.attr_stochastic:
                distn = self.attr_stochastic[key]['distribution']
                args = self.attr_stochastic[key]['arguments']
                attr_dic[key] = getattr(self.rng, distn)(*args)
            attr_dic = copy.deepcopy(self.__constant__)
            yield attr_dic
