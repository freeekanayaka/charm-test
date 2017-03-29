import io
import json
import yaml
import argparse


class ConfigGet(object):

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


class OpenPort(object):
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


class UnitGet(object):
    """Return information about the local unit."""

    name = "unit-get"

    def __init__(self, unit_data):
        self.unit_data = unit_data

    def __call__(self, proc_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("setting")
        parser.add_argument("--format")
        args = parser.parse_args(proc_args["args"][1:])
        if args.setting not in self.unit_data:
            error = 'error: unknown setting "{}"'.format(args.setting)
            return {
                "returncode": 1,
                "stderr": io.BytesIO(error.encode("utf-8"))
            }
        stdout = self.unit_data[args.setting]
        if args.format:
            converter = json.dumps if args.format == "json" else yaml.dump
            stdout = converter(stdout)
        else:
            stdout += "\n"
        return {"stdout": io.BytesIO(stdout.encode("utf-8"))}
