"""Builders module

NetworkX graph objects may be built using the provided graph factories. They make it simple to construct graphs with the
specified randomly or deterministically distributed attributes or edges.

The user-facing interface is defined by the `[Multi[Di]]GraphFactory` classes, but most of the work is done by the two
list-builder classes: NodeListBuilder and EdgeListBuilder. These classes build lists of tuples that can be easily used
to generate a graph using NetworkX's `add_node_from` and `add_edge_from` methods.
"""
import itertools
import networkx as nx
from numpy import random
from scipy import stats
from . import agents


class BaseListBuilder(object):
    """Base class for the node and edge list builders used in GraphFactory classes"""
    __rng__ = None
    __attr_dic__ = {}
    size = 0

    def __init__(self, rng=None):
        """Constructor

        Args:
            rng: Instance of NumPy's RandomState object

        Returns:
            ListBuilder object
        """
        self.__rng__ = rng

    def add(self, **kwargs):
        """Add attribute name/value pairs to the attribute dictionary

        Args:
            kwargs: name/value pairs of arguments to parse. Values may

        """
        for name, value in kwargs.items():
            self.__attr_dic__[name] = self._parse_args(value)

    def _parse_distribution(self, dist):
        """Parses a given distribution input into a callable with the given seed

        Args:
            dist: Callable of scipy.stats, or numpy.random, or a string of either

        Returns:
            Callable distribution function with the given seeded RNG self.__rng__
        """
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
        """Parse the arguments given to .add()

        Args:
            arg: treated as distribution specification if a tuple

        Returns:
            If input is a tuple, returns the same 3-tuple with the first element replaced with the appropriate callable.
            Otherwise, leaves the input unchanged
        """
        if isinstance(arg, tuple):
            dist = self._parse_distribution(arg[0])
            arg = (dist, arg[1], arg[2]) if len(arg) > 2 else (dist, arg[1], {})
        return arg

    def _build_list(self, list_attr, graph):
        """Specific implementation of the list building method
        Takes as inputs the list of sampled or constant attributes as well as the full graph

        Args:
            list_attr: List of dictionaries, where dictionary keys are attributes previously added using .add()
            graph: Full NetworkX graph object

        Returns:
            Iterable object
        """
        raise NotImplementedError

    def build(self, graph):
        """Generic build method, relying on the specific list builder method ._build_list

        Args:
            graph: Full NetworkX graph object

        Returns:
            Iterable object
        """
        samples = {}
        for name, value in self.__attr_dic__.items():
            try:
                samples[name] = value[0](*value[1], size=self.size, **value[2])
            except (IndexError, TypeError):
                samples[name] = [value] * self.size

        list_attr = list(map(dict, zip(*[[(k, v) for v in val] for (k, val) in samples.items()])))

        return self._build_list(list_attr, graph)


class NodeListBuilder(BaseListBuilder):
    """Defines the specific implementation of the list builder for (node, attributes) tuple list"""
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
    """Defines the specific implementation of the list builder for (edge, attributes) tuple list"""
    __edge_dic__ = {}
    __thd__ = 0
    callback = None

    def __init__(self, rng=None):
        super().__init__(rng=rng)

    def from_dist(self, spec, thd):
        """Sets the distribution from which the edge list will be built

        Args:
            spec: distribution specification tuple. Same form as for add() method
            thd: threshold above which the edge will be added
        """
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

        list_edge = [(pair[0], pair[1], dic) for pair, dic in zip(list_edge, list_attr)]
        return list_edge[:self.size] if self.size else list_edge


class BaseGraphFactory(object):
    """Base class for all graph factories.
    Fully specifies functionality; concrete implementations only specify which NetworkX graph object to instantiate.
    """
    def __init__(self, rng=None):
        if rng is not None and not isinstance(rng, random.RandomState):
            raise TypeError
        self.__nbuilder__ = NodeListBuilder(rng)
        self.__ebuilder__ = EdgeListBuilder(rng)

    def build(self):
        """Build a graph object from the node and edge list builders

        Returns:
            NetworkX graph object
        """
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
        """Specify the number of nodes in the graph to be built"""
        self.__nbuilder__.size = number_of_nodes

    def set_edge_limit(self, limit_num_edges):
        """Specify an upper limit on the number of edges in the graph"""
        self.__ebuilder__.size = limit_num_edges

    def set_agent(self, agent_type):
        """Specify the agent class to be used to populate the graph nodes"""
        if not issubclass(agent_type, agents.BaseAgent):
            raise TypeError
        self.__nbuilder__.agent = agent_type

    def set_node_attribute(self, **kwargs):
        """Set node attributes as keyword arguments.
        Tuples are interpreted as random distribution specifications, with the form (dist, args, kwargs), where dist is
        a method of numpy.random or scipy.stats, or a string of the name of either. Non-tuples are left unmodified.
        """
        self.__nbuilder__.add(**kwargs)

    def set_edge_attribute(self, **kwargs):
        """Set edge attributes as keyword arguments.
        Arguments are interpreted in the same way as in .set_node_attribute
        """
        self.__ebuilder__.add(**kwargs)

    def set_edge_by_distribution(self, arg_tuple, threshold):
        """Set the distribution according to which edges should be added.
        The arg_tuple must be a distribution specification (dist, args, kwargs) and the threshold is the value above
        which the edge is added for a given random sample
        """
        if not isinstance(arg_tuple, tuple):
            raise TypeError
        self.__ebuilder__.from_dist(arg_tuple, threshold)

    def set_edge_by_callback(self, cb):
        """Set the edges based on the given callable.
        The callable must have the signature (nodeA, nodeB, graph, rng) and return a boolean indicating whether or not
        the edge between nodeA and nodeB should be added to the graph
        """
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
