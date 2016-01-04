#!/usr/bin/env python3
"""

"""
from networksimulator import generators
import numpy as np
from scipy.stats import kstest


class Agent(generators.AgentGenerator):
    pass


def test_can_generate_agents():
    g = generators.AgentGenerator(Agent)
    g = iter(g)

    for ii in range(0, 30):
        assert(next(g) == Agent(ii))


def test_can_generate_normally_distributed_attributes():
    SEED = 10024
    g = generators.AttributeGenerator(SEED)

    mean = 0
    std = 1
    g.set_stochastic('normal_attribute', distribution='normal', arguments=[mean, std])

    g = iter(g)

    num_samples_total = 1500
    results = []
    for ii in range(0, num_samples_total):
        sample = next(g)
        results.append(sample['normal_attribute'])

    _, pval = kstest(np.asarray(results), 'norm', (mean, std))
    assert(pval > 0.3)


def test_can_generate_logistic_distributed_attributes():
    SEED = 3208
    g = generators.AttributeGenerator(SEED)

    location = 9
    scale = 3
    g.set_stochastic('attribute', distribution='logistic', arguments=[location, scale])

    g = g.build()

    num_samples_total = 1500
    results = []
    for ii in range(0, num_samples_total):
        sample = next(g)
        results.append(sample['attribute'])

    _, pval = kstest(np.asarray(results), 'logistic', (location, scale))
    assert(pval > 0.3)
