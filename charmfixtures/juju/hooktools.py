import io
import json
import argparse


class ConfigGet(object):
    """
    """

    name = "config-get"

    def __init__(self, data):
        self._data = data

    def __call__(self, proc_args):
        stdout = json.dumps(self._data) + "\n"
        return {"stdout": io.BytesIO(stdout.encode("utf-8"))}


class JujuLog(object):

    name = "juju-log"

    def __init__(self, entries):
        """
        """
        self._entries = entries

    def __call__(self, proc_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("message")
        parser.add_argument("-l", default="INFO", dest="level")
        args = parser.parse_args(proc_args["args"][1:])
        self._entries.append("{}: {}".format(args.level, args.message))
        return {}


class OpenPort():
    """Access ports opened by the fake open-port hook tool."""

    name = "open-port"

    def __init__(self, ports):
        """
        @param path: Path to the backend log file.
        """
        self._ports = ports

    def __call__(self, proc_args):
        port, protocol = proc_args["args"][1].split("/")
        self._ports.setdefault(protocol, set()).add(int(port))
        return {}
