import os

from fixtures import (
    Fixture,
    EnvironmentVariable,
    TempDir,
)

from .config import ConfigData
from .log import LogData
from .port import PortData

BIN = os.path.join(os.path.dirname(__file__), "bin")


class HookTools(Fixture):
    """Provide fake versions of juju hook tools."""

    def log(self):
        with open(self._tools_dir.join(".log")) as fd:
            return [line.strip() for line in fd.readlines()]

    def _setUp(self):
        self._charm_dir = self.useFixture(TempDir())

        self.useFixture(EnvironmentVariable("CHARM_DIR", self._charm_dir.path))
        self.useFixture(EnvironmentVariable(
            "PATH", "{}:{}".format(BIN, os.environ["PATH"])))

        self.config = ConfigData()
        self.log = LogData()
        self.port = PortData()
