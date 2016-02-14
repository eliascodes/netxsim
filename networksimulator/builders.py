import itertools
import networkx as nx
from numpy import random
from scipy import stats

from . import agents


class BaseListBuilder(object):
    """Base class for the node and edge list builders used in the GraphFactory class

    """
    __rng__ = None
    __attr_dic__ = {}
    size = 0

    def __init__(self, rng=None):
        self.__rng__ = rng

    def add(self, **kwargs):
        for name, value in kwargs.items():
            self.__attr_dic__[name] = self._parse_args(value)

    def _parse_distribution(self, dist):
        try:
            dist.random_state = self.__rng__
            dist = dist.rvs
        except AttributeError:
            try:
                dist = getattr(self.__rng__, dist.__name__)
            except AttributeError:
                dist = getattr(stats, dist, getattr(self.__rng__, dist))
                dist = self._parse_distribution(dist)
        return dist

    def _parse_args(self, arg):
        if isinstance(arg, tuple):
            dist = self._parse_distribution(arg[0])
            arg = (dist, arg[1], arg[2]) if len(arg) > 2 else (dist, arg[1], {})
        return arg

    def _build_list(self, list_attr, graph):
        raise NotImplementedError

    def build(self, graph):
        samples = {}
        for name, value in self.__attr_dic__.items():
            try:
                samples[name] = value[0](*value[1], size=self.size, **value[2])
            except (IndexError, TypeError):
                samples[name] = [value] * self.size

        list_attr = list(map(dict, zip(*[[(k, v) for v in val] for (k, val) in samples.items()])))

        return self._build_list(list_attr, graph)


class NodeListBuilder(BaseListBuilder):
    agent = None

    def _build_list(self, list_attr, graph):
        if callable(self.agent):
            if len(list_attr) > 0:
                return [(self.agent(ii), list_attr[ii]) for ii in range(0, self.size)]
            else:
                return [self.agent(ii) for ii in range(0, self.size)]
        else:
            if len(list_attr) > 0:
                return [(ii, list_attr[ii]) for ii in range(0, self.size)]
            else:
                return list(range(0, self.size))


class EdgeListBuilder(BaseListBuilder):
    __edge_dic__ = {}
    __thd__ = 0
    callback = None

    def __init__(self, rng=None):
        super().__init__(rng=rng)

    def from_dist(self, spec, thd):
        self.__edge_dic__['edges'] = self._parse_args(spec)
        self.__thd__ = thd
        self.callback = None

    def _build_list(self, list_attr, graph):
        list_edge = []
        nodes = graph.nodes()
        if callable(self.callback):
            for pair in itertools.product(nodes, nodes):
                if self.callback(pair[0], pair[1], graph, self.__rng__):
                    list_edge.append(pair)
        else:
            vals = self.__edge_dic__['edges']
            samples = vals[0](*vals[1], size=graph.number_of_nodes()**2, **vals[2])
            for pair, sample in zip(itertools.product(nodes, nodes), samples):
                if sample > self.__thd__:
                    list_edge.append(pair)

        return [(pair[0], pair[1], dic) for pair, dic in zip(list_edge, list_attr)]


class BaseGraphFactory(object):
    def __init__(self, rng=None):
        if rng is not None and not isinstance(rng, random.RandomState):
            raise TypeError
        self.__nbuilder__ = NodeListBuilder(rng)
        self.__ebuilder__ = EdgeListBuilder(rng)

    def build(self):
        graph = self.init_graph()

        # build list of (node, attrdict) node tuples
        list_nodes = self.__nbuilder__.build(graph)
        graph.add_nodes_from(list_nodes)

        # build list of (nodeFrom, nodeTo, attrdict) edge tuples
        list_edges = self.__ebuilder__.build(graph)
        graph.add_edges_from(list_edges)

        return graph

    def init_graph(self):
        raise NotImplementedError

    def set_size(self, number_of_nodes):
        self.__nbuilder__.size = number_of_nodes

    def set_edge_limit(self, limit_num_edges):
        self.__ebuilder__.size = limit_num_edges

    def set_agent(self, agent_type):
        if not issubclass(agent_type, agents.BaseAgent):
            raise TypeError
        self.__nbuilder__.agent = agent_type

    def set_node_attribute(self, **kwargs):
        self.__nbuilder__.add(**kwargs)

    def set_edge_attribute(self, **kwargs):
        self.__ebuilder__.add(**kwargs)

    def set_edge_by_distribution(self, arg_tuple, threshold):
        if not isinstance(arg_tuple, tuple):
            raise TypeError
        self.__ebuilder__.from_dist(arg_tuple, threshold)

    def set_edge_by_callback(self, cb):
        if not callable(cb):
            raise TypeError
        self.__ebuilder__.callback = cb


class GraphFactory(BaseGraphFactory):
    def init_graph(self):
        return nx.Graph()


class DiGraphFactory(BaseGraphFactory):
    def init_graph(self):
        return nx.DiGraph()


class MultiGraphFactory(BaseGraphFactory):
    def init_graph(self):
        return nx.MultiGraph()


class MultiDiGraphFactory(BaseGraphFactory):
    def init_graph(self):
        return nx.MultiDiGraph()
