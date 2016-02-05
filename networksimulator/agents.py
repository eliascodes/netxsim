class BaseAgent(object):
    """
    Base class for all agents.

    Agents are the active, dynamic components of a network simulation. In any simulation, there is a
    one-to-one correspondence between agents and nodes.

    Agents are endowed with a method "run", which computes new states as a function of old states.
    At this level of abstraction, we make no restriction on the states that the agent has access to
    both read and write.
    """
    def __init__(self, agent_id):
        self.agent_id = agent_id

    def __hash__(self):
        return hash(self.agent_id) ^ hash(str(self.__class__))

    def __eq__(self, other):
        return isinstance(other, type(self)) and hash(self) == hash(other)

    def run(self, graph, env):
        raise NotImplementedError


class NodeAgent(BaseAgent):
    def run(self, graph, env):
        yield env.timeout(1)