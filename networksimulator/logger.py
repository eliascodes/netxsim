from networksimulator.results import NetSimResults


class NetSimLogger(object):
    """"""
    def __init__(self):
        self.results = {}

    def start(self, env):
        self.results = NetSimResults()
        return self

    def stop(self, env):
        return self

    def get_results(self):
        return self.results
