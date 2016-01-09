#!/usr/bin/env python3
"""Test module for the generators.py module

1 > Define test fixtures
2 > Define support functions and test stubs
3 > Define functional test methods for agent generator builder
4 > Define functional test methods for attribute generator builder
5 > Define statistical test methods for attribute generator builder

"""
from .. import generators, agents, exceptions
import pytest
import numpy as np
import scipy.stats as scistats
import cProfile


@pytest.fixture
def attr_builder():
    return generators.AttributeGeneratorBuilder(10582)


@pytest.fixture()
def agent_builder():
    return generators.AgentGeneratorBuilder(agents.BaseAgent)


def test_agent_generator_builder_freezes_itself_on_build_call(agent_builder):
    agent_builder.build()
    assert agent_builder.frozen


def test_generated_agents_have_different_object_ids(agent_builder):
    g = iter(agent_builder)
    new = []
    for ii in range(0, 30):
        old = new
        new = next(g)
        assert(id(old) != id(new))


def test_generated_agents_have_incremented_ids(agent_builder):
    g = iter(agent_builder)
    for ii in range(0, 30):
        assert(next(g) == agents.BaseAgent(ii))


def test_attribute_generator_builder_freezes_itself_on_build_call(attr_builder):
    attr_builder.build()
    assert attr_builder.frozen


def test_can_add_constant_attribute(attr_builder):
    attr_builder.add_constant(alpha='a')
    attr_builder.add_constant(beta='b')
    attr_builder.add_constant(gamma='y')

    for (k, v) in attr_builder.__constant__.items():
        assert k in ['alpha', 'beta', 'gamma']
        assert v in ['a', 'b', 'y']


def test_can_add_stochastic_attribute(attr_builder):
    attr_builder.add_stochastic('alpha', norm=[0, 1])
    attr_builder.add_stochastic('beta', pareto=[10])
    attr_builder.add_stochastic('gamma', binom=[20, 0.2])

    for (k, v) in attr_builder.__stochastic__.items():
        assert k in ['alpha', 'beta', 'gamma']
        assert v['distribution'] in ['norm', 'pareto', 'binom']

        if v['distribution'] == 'norm':
            assert v['arguments'] == [0, 1]
        elif v['distribution'] == 'pareto':
            assert v['arguments'] == [10]
        elif v['distribution'] == 'binom':
            assert v['arguments'] == [20, 0.2]


def test_adding_wrong_distribution_throws_exception(attr_builder):
    with pytest.raises(AttributeError) as info:
        attr_builder.add_stochastic('alpha', this_is_not_a_distribution=[0.1])
    assert info.value.args[0] == "this_is_not_a_distribution is not a valid method of scipy.stats"


def test_modifying_attribute_builder_after_build_throws_exception(attr_builder):
    attr_builder.add_constant(alpha=True)
    attr_builder.build()

    with pytest.raises(exceptions.FrozenException):
        attr_builder.add_constant(beta=True)


def test_generated_attribute_dictionaries_have_different_object_ids(attr_builder):
    g = attr_builder.build()
    new = []
    for ii in range(0, 30):
        old = new
        new = next(g)
        assert(id(old) != id(new))


def test_attributes_generated_from_continuous_distributions_have_correct_cdf(attr_builder):
    num_samples = 10000
    tol_p_val = 0.03
    dist_args = {
        'norm': [0, 1],
        'gamma': [5],
        'chi2': [2],
    }

    compare_distributions(dist_args, attr_builder, num_samples, tol_p_val)


def test_attributes_generated_from_discrete_distributions_have_correct_cdf(attr_builder):
    num_samples = 10000
    tol_p_val = 0.08
    dist_args = {
        'binom': [200, 0.1],
        'poisson': [4],
        'geom': [0.5],
    }

    compare_distributions(dist_args, attr_builder, num_samples, tol_p_val)


def profilefunc(f):
    def f_profiled(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = f(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return f_profiled


def compare_distributions(dist_args, builder, num_samples, tol):

    for (dist, args) in dist_args.items():
        builder.add_stochastic(dist, **{dist: args})

    g = builder.build()

    samples = get_samples(num_samples, dist_args, g)

    for (name, vals) in samples.items():
        sample_xvals = np.sort(vals)
        sample_yvals = np.linspace(0, 1, len(sample_xvals), endpoint=False)

        distribution = getattr(scistats, name)
        theoretical_yvals = distribution.cdf(sample_xvals, *dist_args[name])

        p1, p2 = scistats.pearsonr(sample_yvals, theoretical_yvals)

        assert tol > 1 - p1
        assert tol > p2


@profilefunc
def get_samples(num_samples, dist_args, g):
    samples = {k: [] for k in dist_args}
    for ii in range(0, num_samples):
        for (dist, val) in next(g).items():
            samples[dist].append(val)
    return samples
