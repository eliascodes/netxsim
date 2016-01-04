from networkx import Graph


class BaseGraphBuilder(object):
    """

    """

    _attr_teardown = {}

    def __init__(self):
        pass

    def set(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
            self._attr_teardown[key] = None

    def build(self, **kwargs):
        self._prepare_build(**kwargs)
        result = self._construct(**kwargs)
        self._teardown_build(**kwargs)
        return result

    def _prepare_build(self, **kwargs):
        pass

    def _construct(self, **kwargs):
        return Graph()

    def _teardown_build(self, **kwargs):
        for key in self._attr_teardown:
            delattr(self, key)
        self._attr_teardown = {}
