import os
import yaml

from testtools import (
    TestCase,
    try_import,
)

from fixtures import EnvironmentVariable

from charmtest.filesystem import Filesystem
from charmtest.users import Users
from charmtest.groups import Groups
from charmtest.services import Systemctl
from charmtest.network import Wget
from charmtest.processes import Processes
from charmtest.packages import Dpkg
from charmtest.juju import (
    Application,
    Unit,
    ConfigGet,
    JujuLog,
    OpenPort,
)

hookenv = try_import("charmhelpers.core.hookenv")

CHARM_DIR = "var/lib/juju/agents/unit-{}/charm"


class CharmTest(TestCase):

    def setUp(self):
        super().setUp()

        code_dir = _code_dir()

        self.application = Application(_application_name(code_dir))
        self.application.config.update(_default_config(code_dir))
        self.unit = Unit(self.application, 0)

        charm_dir = CHARM_DIR.format(self.unit.name.replace("/", "-"))

        self.filesystem = self.useFixture(Filesystem())
        self.filesystem.add(charm_dir)

        self.users = self.useFixture(Users())
        self.users.add("root", 0)

        self.groups = self.useFixture(Groups())
        self.groups.add("root", 0)

        self.services = {}
        self.network = {}
        self.packages = {}

        self.useFixture(
            EnvironmentVariable("CHARM_DIR", self.filesystem.join(charm_dir)))
        self.useFixture(EnvironmentVariable("JUJU_UNIT_NAME", self.unit.name))

        self.processes = self.useFixture(Processes())
        self.processes.add(ConfigGet(self.application.config))
        self.processes.add(JujuLog(self.unit.log))
        self.processes.add(OpenPort(self.unit.ports))
        self.processes.add(Systemctl(self.services))
        self.processes.add(Wget(self.network))
        self.processes.add(Dpkg(self.packages))

        _create_symlink(code_dir, "metadata.yaml")
        _create_symlink(code_dir, "templates")

        # If charmhelpers is around, clear its config cache.
        hookenv and hookenv.cache.clear()


def _code_dir():
    directory = os.getcwd()
    while directory != "/":
        if os.path.exists(os.path.join(directory, "metadata.yaml")):
            return directory
    else:  # pragma: no cover
        raise RuntimeError("This doesn't seem to be a charm code tree")


def _application_name(code_dir):
    with open(os.path.join(code_dir, "metadata.yaml")) as fd:
        return yaml.safe_load(fd)["name"]


def _default_config(code_dir):
    with open(os.path.join(code_dir, "config.yaml")) as fd:
        data = yaml.safe_load(fd)

    config = {}
    for name, metadata in data["options"].items():
        value = metadata["default"]
        if metadata["type"] == "int":
            value = int(value)
        config[name] = value

    return config


def _create_symlink(code_dir, filename):
    charm_dir = os.environ["CHARM_DIR"]
    os.symlink(
        os.path.join(code_dir, filename), os.path.join(charm_dir, filename))
