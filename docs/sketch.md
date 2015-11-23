options:

1. agent instances as attributes of nodes
2. agents as nodes (since nodes can be any hashable object). this seems more natural. then the
agent objects must be immutable once created, and not change their own internal state. this is
probably fine since the agent will only define the dynamic rules as a function of the node state
(which are the node attributes). this was the paradigm i was already pursuing with the sub-class
based approach. any model involving a mutation of the dynamic rules would have to encode this either
with branching within the dynamics method, or with an alternative parameterisation of the dynamics.

option 2 means agents are simple, having just a "run" method, with G and env as inputs...they cannot
be attributes of the agent since they are by definition of a simulation liable to change (although
this may not actually be true...since python variables are actually references...so as long as the
memory location doesn't change it might be ok, but static with inputs is probably simpler).

each agent will need a unique id for convenience/access

the ensemble creation of nodes will still work with option 2. the internal states of each agent
instance are determined by the RNG at creation and then not changed again.

this should all eventually generalise to multi-di-graphs with arbitrary edge attributes.

to access own attributes, have to do G[self][attribute]


builders:
now that the agents ARE the nodes, how do we want to do the node population?
should graph creation happen concurrently with agent creation? then agent creation cannot depend on
topological features. but the whole graph will be ready in O(VE) instead of O(V^2E^2).
for simplicity implement the builders so they accept a graph and replace nodes with agents. this can
be made better later.

sim use cases:
1. have a graph, populate with agents, run one shot sim
2. have a graph, populate with ensemble of agents, run many sims
3. have a graph ensemble, populate with ensemble of agents, run many sims

a graph ensemble is a set of graphs with the same number of nodes; essentially the only things that
differ are the edges. edges can be distributed deterministically or according to a stochastic
process.

a simulation then requires a graph ensemble, an agent ensemble and a seed for the dynamics RNG.
this is a 2-D parameter space though, since we define an agent ensemble as a set of agents rather
than a set of sets of agents. So with our current definitions, there is a one-to-one relationship
between nodes and agents and a one-to-many relationship between a set of agents and graphs in the
ensemble. I think this is fine; edges will be changing in for every graph in the ensemble so while
the set of agents is fixed, their topological significance in each graph is variable.

problem! if agents are created independently of nodes, cannot set node attributes in the agent
builder.

maybe i havent abstracted this properly.

lets say agents have no attributes (other than id), only methods. They are ACTIVE objects, they don't have any
state. In fact, agents only need a run method (but may have others I guess). All state information
is encoded in node attributes. If the run method depends on some parameter, that parameter should be
an attribute of the node.

so then the ensemble is the ensemble of agent/attribute-dictionary pairs.

need a graph builder though really...one with traceability and repeatability.

ND = n-grid of seeds/indices. Should be dict of arrays.

ND['edge_seed'][0] = seed for generating the first topology of the graph
ND['node_seed'][0] = seed for generating the node attributes of the graph
ND['dynamics_seed'][0] = seed for dynamics for the first run

This structure works if edges and nodes are independent of each other. If attributes and edges are
functions of each other, there needs to be an iterative method of building, starting with one node.

ND['graph_seed'][0] = seed for the first building process

This implies the need to a build_graph_from_grid_point method, where the precise implementation is
up to the user.

User needs to say how to build the graph (provide graph builder)
User needs to say how to build the grid (provide grid builder)

So a sim case will contain two builders, some summary stuff
import netsim_case_001 as case001
import netsim.simulator as sim

grid = case001.grid_builder()
logger = case001.logging()

simObj = sim.Simulator(grid, case001.graph_builder(), logger)
simObj.runAll()
or
simObj.run(grid.points([0,1,2], [33,2,20]))
or
simObj.run(grid.points({'dim1': range(0,20), 'dim2': range(32,1000), 'dim3': [1,231,22]}))

Sketch:


class ZombieGraphBuilder(GraphBuilder):
    def __init__(self, size):
        super().__init__(size)

    def build(self, attribute_seed, edge_seed):
        G = nx.Graph()

        agnt = AgentGenerator(ZombieAgent)

        attr = AttributeGenerator(attribute_seed)
        attr.set_stochastic('zombified', {'distribution': 'binomial', 'arguments': [2, 3]})
        attr.set_deterministic('human', True)
        attr.set_stochastic('weak', {'distribution': 'exponential', 'arguments': [0.01, 0.32]})

        while G.number_of_nodes() < self.size:
            G.add_node(agnt.get_next(), attr.get_next())

        for nodeA in G.nodes():
            for nodeB in G.nodes():
                if nodeA != nodeB:
                    G = apply_rule(G, nodeA, nodeB)


    def build(self, attribute_seed, edge_seed):
        agent = self.get_agent_generator()
        attr = self.get_attribute_generator()
        graph = self.initialise_graph()
        graph = self.populate_nodes()
        graph = self.populate_edges()
or
    def build(self, ...):
        agent = self.get_agent_generator()
        attr = self.get_attribute_generator()
        graph = self.initialise_graph()
        graph = self.populate_graph()


class ZombieNetworkSimGrid(NetSimGridBuilder):
    def __init__(self):
        super().__init__()

    def build(self):
        grid = NetSimGrid()
        grid.add_dimension('attribute_seed', range(0,1000))
        grid.add_dimension('edge_seed', range(0,1000))
        grid.add_dimension('dynamics_seed', range(0,200))
        return grid


class Simulator
    def run(self, graph_builder, grid_builder):
        grid = grid_builder.build()
        self.validate_grid(grid)
        self.validate_graph(graph)
