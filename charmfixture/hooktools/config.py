import os
import json


class ConfigData():
    """A dict-like object that syncs its values back to a json file.

    The public APIs are write-only, since the backend json file is
    meant to be read by the fake config-get hook tool.
    """

    def __init__(self, path):
        """
        @param path: Path to the backend json file.
        """
        self._path = path
        self._data = {}
        self._write()

    def __setitem__(self, key, value):
        self._read()
        self._data[key] = value
        self._write()

    def clear(self):
        self._data.clear()
        self._write()

    def update(self, *args, **kwargs):
        self._data.update(*args, **kwargs)
        self._write()

    def _write(self):
        with open(self._path, "w") as fd:
            fd.write(json.dumps(self._data))

    def _read(self):
        with open(self._path) as fd:
            self._data = (json.loads(fd.read()))


class ConfigTool():

    def __init__(self, tools_dir):
        self._tools_dir = tools_dir

    @classmethod
    def path(cls, tools_dir):
        return os.path.join(tools_dir, ".config.json")

    def run(self, args):
        with open(self.path(self._tools_dir)) as fd:
            print(fd.read())
