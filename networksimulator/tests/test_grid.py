#!/usr/bin/env python3
from networksimulator.grid import Grid


def test_create_grid():
    g = Grid()

    assert(isinstance(g, Grid))

    x = range(0, 10)
    g.add_dimension('x', x)
    for ii in x:
        assert(g.grid['x'][ii] == x[ii])

    y = range(0, 10)
    g.add_dimension('y', y)
    for ii in x:
        assert(g.grid['y'][ii] == y[ii])

    g.add_description('x', 'X-axis')
    assert(g.meta['x'] == 'X-axis')

    g.add_description('y', 'Y-axis')
    assert(g.meta['y'] == 'Y-axis')


def test_create_subgrid_from_grid():
    g = Grid()
    g.add_dimension('x', range(0, 20))
    g.add_dimension('y', range(0, 20))

    h = g.subgrid_from_indices(x=[1, 2, 4, 8, 16], y=[12, 15, 19])
    k = g.subgrid_from_range(x=[0, 10], y=[15, 19])
    l = g.subgrid_from_values(x=[5, 6, 9], y=[0, 14, 19])

    h_exp = Grid().add_dimension('x', [1, 2, 4, 8, 16]).add_dimension('y', [12, 15, 19])
    k_exp = Grid().add_dimension('x', range(0, 10)).add_dimension('y', range(15, 19))
    l_exp = Grid().add_dimension('x', [5, 6, 9]).add_dimension('y', [0, 14, 19])

    assert(h == h_exp)
    assert(k == k_exp)
    assert(l == l_exp)
