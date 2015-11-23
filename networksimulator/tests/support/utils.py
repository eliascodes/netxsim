def compare_grids(gridA, gridB):
    for key in gridA.grid:
        compare_dimension(gridB, key, gridA.grid[key])


def compare_array(grid, dimension, lst):
    for ii in lst:
        assert(grid.grid[dimension][ii] == lst[ii])
