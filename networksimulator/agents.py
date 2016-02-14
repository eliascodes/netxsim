"""Agents module

Agents are the primary dynamic component of the network simulation. All nodes are agent objects, and every class of
agents defines a `run` method, which defines the dynamics of the agent as a generator. This `run` method is registered
with the simulation environment object as a SimPy process that yields an event.

Agent objects are intended to be stateless. Any node state should be held as a NetworkX node attribute, rather than
attached as a member of the Agent class. The `run` method has access to the full graph and simulation environment via
arguments, and should perform any state manipulation using those provided arguments.

For example, an agent which examined its own boolean node attribute called 'state', and inverted it based on a uniformly
random sample, could be written as follows:
```
def run(self, graph, env):
    while True:
        if env.draw('uniform') > 0.5:
            graph.node[self]['state'] = not graph.node[self]['state']
        yield env.timeout(1)
```
Note again that the `run` method is a generator that yields SimPy events. In SimPy terms, this is a process. In this
case the process yields an arbitrary number of events, but this need not be the case. See the SimPy process
documentation for more detail.
"""


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
