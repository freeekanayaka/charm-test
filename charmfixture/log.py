import os
import argparse


class LogData():
    """Access logs written by the fake juju-log hook tool."""

    def __init__(self, path):
        """
        @param path: Path to the backend log file.
        """
        self._path = path
        with open(self._path, "w") as fd:
            fd.write("")

    def __iter__(self):
        with open(self._path) as fd:
            for line in fd.readlines():
                yield line.strip()

    def __getitem__(self, index):
        return list(self)[index]


class LogTool():

    def __init__(self, tools_dir):
        self._tools_dir = tools_dir

    @classmethod
    def path(cls, tools_dir):
        return os.path.join(tools_dir, ".juju.log")

    def run(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("message")
        parser.add_argument("-l", default="INFO", dest="level")
        args = parser.parse_args(args)

        with open(self.path(self._tools_dir), "w") as fd:
            fd.write("{}: {}\n".format(args.level, args.message))
