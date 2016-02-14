#!/usr/bin/env python3
import pytest
import math
import networkx as nx
from .. import builders, agents
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt


@pytest.fixture
def node_builder_setup():
    return builders.NodeListBuilder(), nx.Graph()


@pytest.fixture
def node_builder_setup_rng():
    seed = 103208
    rng = np.random.RandomState(seed)
    return builders.NodeListBuilder(rng), nx.Graph()


def test_build_node_list_without_agents_without_attributes(node_builder_setup):
    b, g = node_builder_setup
    b.size = 10

    nlist = b.build(g)

    for ii in range(0, b.size):
        assert nlist[ii] == ii


def test_build_node_list_with_agents_without_attributes(node_builder_setup):
    b, g = node_builder_setup
    b.size = 10
    b.agent = agents.NodeAgent

    nlist = b.build(g)

    for ii in range(0, b.size):
        assert nlist[ii] == agents.NodeAgent(ii)


def test_build_node_list_without_agents_with_constant_attributes(node_builder_setup):
    b, g = node_builder_setup
    attributes = {'a': 1, 'b': 'e', 'c': 6}
    b.add(**attributes)
    b.size = 10

    nlist = b.build(g)

    for ii in range(0, b.size):
        assert nlist[ii][0] == ii
        assert nlist[ii][1] == attributes


def test_build_node_list_with_agents_with_constant_attributes(node_builder_setup):
    b, g = node_builder_setup
    attributes = {'a': 1, 'b': '$', 'c': -1}
    b.add(**attributes)
    b.size = 10
    b.agent = agents.NodeAgent

    nlist = b.build(g)

    for ii in range(0, b.size):
        assert nlist[ii][0] == agents.NodeAgent(ii)
        assert nlist[ii][1] == attributes


def test_build_node_list_without_rng_with_random_attributes_raises_exception(node_builder_setup):
    b, g = node_builder_setup

    with pytest.raises(TypeError):
        b.add(a=(np.random.normal, [0, 1], {}))


def test_build_node_list_without_agents_with_random_attributes(node_builder_setup_rng):
    b, g = node_builder_setup_rng
    b.size = 10
    b.add(a=(np.random.normal, [0, 1], {}))

    nlist = b.build(g)

    for ii in range(0, b.size):
        assert nlist[ii][0] == ii
        assert isinstance(nlist[ii][1], dict)
        assert 'a' in nlist[ii][1]
        # simplified sanity check - assert sample is within 6-sigma
        assert nlist[ii][1]['a'] > -3
        assert nlist[ii][1]['a'] < 3


def test_build_node_list_with_agents_with_mixed_attributes(node_builder_setup_rng):
    b, g = node_builder_setup_rng
    b.size = 10
    b.add(a=8, b=('gamma', [1.99], {}))

    nlist = b.build(g)

    for ii in range(0, b.size):
        assert nlist[ii][0] == ii
        assert isinstance(nlist[ii][1], dict)
        assert 'a' in nlist[ii][1]
        assert nlist[ii][1]['a'] == 8
        # simplified sanity check - assert sample is within 6-sigma
        assert nlist[ii][1]['b'] < 6 * math.sqrt(1.99)


def test_build_node_list_with_continuously_distributed_random_attributes_with_statistically_correct_properties(node_builder_setup_rng):
    b, g = node_builder_setup_rng
    b.size = 10000
    b.add(a=(np.random.normal, [0, 1], {}), b=(stats.bernoulli, [0.2], {}), c=('rayleigh', [], {'loc': 3, 'scale': 1.3}))

    nlist = b.build(g)

    samples = {}
    for node_tuple in nlist:
        for k, v in node_tuple[1].items():
            try:
                samples[k].append(v)
            except KeyError:
                samples[k] = [v]

    for attr, vals in samples.items():
        sample_xvals = np.sort(vals)
        sample_yvals = np.linspace(0, 1, len(sample_xvals), endpoint=False)

        if attr == 'a':
            theoretical_yvals = stats.norm.cdf(sample_xvals, 0, 1)
        elif attr == 'b':
            theoretical_yvals = stats.bernoulli.cdf(sample_xvals, 0.2)
        elif attr == 'c':
            theoretical_yvals = stats.rayleigh.cdf(sample_xvals, loc=3, scale=1.3)
        else:
            theoretical_yvals = 0

        p1, p2 = stats.pearsonr(sample_yvals, theoretical_yvals)

        tol = 0.01
        assert tol > 1 - p1
        assert tol > p2


def test_build_node_list_with_discretely_distributed_random_attributes_with_statistically_correct_properties(node_builder_setup_rng):
    pass


@pytest.fixture
def edge_builder_setup():
    return builders.EdgeListBuilder(), nx.Graph()


@pytest.fixture
def edge_builder_setup_rng():
    SEED = 734865
    rng = np.random.RandomState(SEED)
    return builders.EdgeListBuilder(rng), nx.Graph()

def test_can_add_constant_attributes_to_edge_list_builder():
    pass


def test_adding_random_attributes_to_edge_list_builder_without_rng_throws_exception():
    pass


def test_can_add_random_attributes_to_edge_list_builder():
    pass


def test_adding_random_attributes_to_edge_list_builder_gives_statistically_correct_results():
    pass


def test_can_build_edge_list_from_callback():
    pass


def test_can_build_edge_list_from_distribution():
    pass


def test_building_edge_list_from_distribution_gives_statistically_correct_results():
    pass