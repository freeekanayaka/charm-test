from fixtures import FakePopen


class FakeProcesses(FakePopen):

    def __init__(self):
        self._registry = {}

    def add(self, process, name=None):
        name = name or process.name
        self._registry[name] = process

    def get_info(self, proc_args):
        get_info = self._registry[proc_args["args"][0]]
        return get_info(proc_args)
