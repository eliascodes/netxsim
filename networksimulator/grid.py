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

    def add_dimensions(self, **kwargs):
        self.grid.update(kwargs)
        return self

    def add_description(self, **kwargs):
        self.meta.update(kwargs)
        return self

    def _subgrid(self, filt, kwargs):
        grid_new = type(self)()
        dims = {k: filt(self.grid[name], v) for k, v in kwargs}
        return grid_new.add_dimensions(**dims)

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

    def subgrid_from_dimensions(self, *args):
        return self._subgrid(
            lambda pts, inputs: pts,
            {k: None for k in args}
        )

    def number_of_dimensions(self):
        return len(self.grid.keys())
