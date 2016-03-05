#!/usr/bin/env python3
"""

"""
from .. import results
import numpy as np


FILEPATH = '/Users/elias/projects/networksimulator/networksimulator/tests/data_test_simulation_results.pickle'


def summarise_state(graph):
    return sum([1 for (_, d) in graph.nodes(data=True) if d['sick']])


def test_can_build_from_file_path():
    r = results.from_path(FILEPATH)
    states = np.asarray(r.data)
    mean = np.mean(states)
    np.testing.assert_almost_equal(mean, 50, 1)


def test_can_build_from_file_obj():
    with open(FILEPATH, 'rb') as f:
        r = results.from_file(f)
        states = np.asarray(r.data)
        np.testing.assert_almost_equal(np.mean(states), 50, 1)