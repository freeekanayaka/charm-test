STATES = {
    "start": "started",
    "stop": "stopped",
}


class Systemctl(object):

    name = "systemctl"

    def __init__(self, services):
        self._services = services

    def __call__(self, proc_args):
        action, service_name = proc_args["args"][1:]
        if action == "is-active":
            returncode = int(self._services.get(service_name) != "started")
            result = {"returncode": returncode}
        else:
            self._services[service_name] = STATES[action]
            result = {}
        return result
