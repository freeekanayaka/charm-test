import os


class PortData():
    """Access ports opened by the fake open-port hook tool."""

    def __init__(self):
        """
        @param path: Path to the backend log file.
        """
        with open(self.path(), "w") as fd:
            fd.write("")

    @classmethod
    def path(cls):
        return os.path.join(os.environ["CHARM_DIR"], ".open-port.data")

    def __iter__(self):
        with open(self.path()) as fd:
            for line in fd.readlines():
                yield line.strip()

    def __getitem__(self, index):
        return list(self)[index]
