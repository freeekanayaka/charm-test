from fixtures import FakePopen


class Processes(FakePopen):

    def __init__(self):
        self._registry = {}

    def add(self, process):
        self._registry[process.name] = process

    def get_info(self, proc_args):
        get_info = self._registry[proc_args["args"][0]]
        return get_info(proc_args)
