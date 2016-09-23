import os


class LogData():
    """Access logs written by the fake juju-log hook tool."""

    def __init__(self):
        """
        @param path: Path to the backend log file.
        """
        with open(self.path(), "w") as fd:
            fd.write("")

    @classmethod
    def path(cls):
        return os.path.join(os.environ["CHARM_DIR"], ".juju-log.data")

    def __iter__(self):
        with open(self.path()) as fd:
            for line in fd.readlines():
                yield line.strip()

    def __getitem__(self, index):
        return list(self)[index]
