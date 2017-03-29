import os
import yaml

from fixtures import (
    Fixture,
    EnvironmentVariable,
)

from testtools import try_import

from charmtest.paths import find_code_dir
from charmtest.juju.hooktools import (
    ConfigGet,
    JujuLog,
    OpenPort,
    UnitGet,
)

hookenv = try_import("charmhelpers.core.hookenv")


class FakeJuju(Fixture):

    def __init__(self, filesystem, processes):
        super(Fixture, self).__init__()
        self._fs = filesystem
        self._processes = processes

    def _setUp(self):
        code_dir = find_code_dir()
        unit_name = self._unit_name(code_dir)
        charm_dir = self._charm_dir(unit_name)

        self.config = self._default_config(code_dir)

        self._fs.add("/var")
        os.makedirs(charm_dir)
        self._create_symlink(code_dir, charm_dir, "metadata.yaml")
        self._create_symlink(code_dir, charm_dir, "templates")

        self.log = []
        self.ports = {}
        self.unit_data = {
            "private-address": "10.1.2.3",
            "public-address": "",
        }

        self.useFixture(EnvironmentVariable("JUJU_UNIT_NAME", unit_name))
        self.useFixture(EnvironmentVariable("CHARM_DIR", charm_dir))

        self._processes.add(ConfigGet(self.config))
        self._processes.add(JujuLog(self.log))
        self._processes.add(OpenPort(self.ports))
        self._processes.add(UnitGet(self.unit_data))

        # If charmhelpers is around, clear its config cache.
        hookenv and hookenv.cache.clear()

    def _unit_name(self, code_dir):
        with open(os.path.join(code_dir, "metadata.yaml")) as fd:
            metadata = yaml.safe_load(fd)
        return "{}/{}".format(metadata["name"], 0)

    def _charm_dir(self, unit_name):
        return "/var/lib/juju/agents/unit-{}/charm".format(unit_name)

    def _default_config(self, code_dir):
        with open(os.path.join(code_dir, "config.yaml")) as fd:
            data = yaml.safe_load(fd)

        config = {}
        for name, metadata in data["options"].items():
            value = metadata["default"]
            if metadata["type"] == "int":
                value = int(value)
            config[name] = value
        return config

    def _create_symlink(self, code_dir, charm_dir, filename):
        os.symlink(
            os.path.join(code_dir, filename),
            os.path.join(charm_dir, filename))
