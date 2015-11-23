from abc import ABCMeta, abstractmethod


class AbstractAgent(object):
    """
    Abstract base class for all agents.

    Agents are the active, dynamic components of a network simulation. In any simulation, there is a
    one-to-one correspondence between agents and nodes.

    Agents are endowed with a method "run", which computes new states as a function of old states.
    At this level of abstraction, we make no restriction on the states that the agent has access to
    both read and write.
    """
    __metaclass__ = ABCMeta

    def __init__(self, agent_id):
        self.agent_id = agent_id

    def __hash__(self):
        return hash(self.agent_id) ^ hash(str(self.__class__))

    def __eq__(self, other):
        return isinstance(other, type(self)) and hash(self) == hash(other)

    @abstractmethod
    def run(self, graph, env):
        pass


class DeterministicAgent(AbstractAgent):
    """"""
    def __init__(self, agent_id):
        super().__init__(agent_id)


class StochasticAgent(AbstractAgent):
    """"""
    def __init__(self, agent_id):
        super().__init__(agent_id)
