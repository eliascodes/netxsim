"""

"""
import os
import glob
import pickle
from . import grid as nsg


class BaseResults(object):
    """

    """
    def __init__(self, data):
        self.open = True
        self.data = data

    def finalize(self):
        self.open = False

    @classmethod
    def from_grid(cls, grid):
        pass

    @classmethod
    def from_id(cls, id):
        pass

    @classmethod
    def from_dir(cls, path):
        pass

    @classmethod
    def from_file(cls, file):
        data = []
        try:
            with file as f:
                while True:
                    data += pickle.load(f)
        except EOFError:
            pass  # Reach end of saved data
        except FileNotFoundError as e:
            print(e)

        return cls(data)

    @classmethod
    def from_path(cls, path):
        file = open(os.path.normcase(path), 'rb')
        return cls.from_file(file)


def from_path(path):
    return BaseResults.from_path(path)

def from_file(file):
    return BaseResults.from_file(file)

def from_dir(path):
    pass


def from_grid(grid, root):
    results = []
    for point in grid:
        pattern = '*' + nsg.hash_grid_point(point) + '*'
        path = glob.glob(os.path.join(root, pattern))[0]
        results.append(BaseResults.from_path(path))

    return results
