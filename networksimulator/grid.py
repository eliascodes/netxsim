import itertools as itt


class Grid(object):
    """"""
    def __init__(self):
        self.grid = {}
        self.meta = {}

    def __eq__(self, other):
        return self.grid == other.grid and self.meta == other.meta

    def __iter__(self):
        names = list(self.grid.keys())
        grid = list(self.grid.values())
        for point in itt.product(*grid):
            out = {names[ii]: point[ii] for ii in range(0, len(names))}
            yield out

    def add_dimension(self, name, points, description=None):
        self.grid[name] = points
        self.meta[name] = description
        return self

    def add_description(self, name, description):
        self.meta[name] = description
        return self

    def _subgrid(self, filt, kwargs):
        grid_new = type(self)()
        for name in kwargs:
            grid_new.add_dimension(name, filt(self.grid[name], kwargs[name]))
        return grid_new

    def subgrid_from_range(self, **kwargs):
        return self._subgrid(
                            lambda pts, inputs: pts[inputs[0]:inputs[1]],
                            kwargs
                            )

    def subgrid_from_indices(self, **kwargs):
        return self._subgrid(
                            lambda pts, inputs: [pts[ii] for ii in inputs],
                            kwargs
                            )

    def subgrid_from_values(self, **kwargs):
        return self._subgrid(
                            lambda pts, inputs: [pt for pt in pts if pt in inputs],
                            kwargs
                            )

    def number_of_dimensions(self):
        return len(self.grid.keys())
