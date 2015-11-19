#!/usr/bin/env python3
from networksimulator.tests.testdata import toyclasses


def test_Hashability():
    one = toyclasses.ToyDeterministicAgent(1)
    two = toyclasses.ToyDeterministicAgent(2)
    uno = toyclasses.ToyDeterministicAgent(1)

    assert(one == uno)
    assert(one != two)
    assert(two != uno)
