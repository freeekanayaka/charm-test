class Systemctl(object):

    name = "systemctl"

    def __init__(self, services):
        self._services = services

    def __call__(self, proc_args):
        action, service_name = proc_args["args"][1:]
        actions = self._services.setdefault(service_name, [])
        result = {}
        if action == "is-active":
            if not actions or actions[-1] != "start":
                result = {"returncode": 1}
        else:
            actions.append(action)
        return result
