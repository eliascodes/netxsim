class NetSimCase(object):
    """docstring for NetSimCase"""
    def __init__(self, verbose=False, runtime=0, path_results=''):
        self.grid = self._prepare_grid()
        self.verbose = verbose
        self.runtime = runtime
        self.path = path_results

    def run(self):
        for point in self.grid:
            graph = self._prepare_graph(**point)
            env = self._prepare_env(graph, **point)
            logger = self._prepare_logger(env, **point)
            env.run(until=self.runtime)
            results = logger.stop().get_results()
            if self.verbose:
                results.pprint()
            else:
                results.save(self.path)
        return self.success

    def _prepare_grid(self):
        pass

    def _prepare_graph(self, **kwargs):
        pass

    def _prepare_env(self, graph, **kwargs):
        pass

    def _prepare_logger(self, env, **kwargs):
        pass
