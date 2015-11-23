from abc import ABCMeta, abstractmethod
import numpy as np


class AbstractBuilder(object):
    """"""
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def build(self):
        pass


class GraphBuilder(AbstractBuilder):
    """"""
    def __init__(self):
        super().__init__()
