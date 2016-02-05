#!/usr/bin/env python3
"""

"""
from .. import results


FILEPATH = '/Users/elias/projects/networksimulator/_results/results_sandbox_9197928360327774_20160104T181208.pickle'


def summarise_state(graph):
    return sum([1 for (_, d) in graph.nodes(data=True) if d['state']])


def test_can_build_from_file():
    r = results.from_file(FILEPATH)
    states = map(summarise_state, r.data)
    print(states)