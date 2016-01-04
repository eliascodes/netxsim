"""

"""
import os
import pickle


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
    def from_file(cls, path):
        data = []
        try:
            with open(os.path.normcase(path), 'rb') as file:
                while True:
                    data.append(pickle.load(file))
        except EOFError:
            pass
        except FileNotFoundError as e:
            print(e)

        return cls(data)


def from_file(path):
    return BaseResults.from_file(path)