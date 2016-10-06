import os
import yaml

from fixtures import (
    Fixture,
    EnvironmentVariable,
)

from testtools import try_import

from charmtest.juju.hooktools import (
    ConfigGet,
    JujuLog,
    OpenPort,
)

hookenv = try_import("charmhelpers.core.hookenv")


class FakeJuju(Fixture):

    def __init__(self, filesystem, processes):
        super().__init__()
        self._fs = filesystem
        self._processes = processes

    def _setUp(self):
        code_dir = self._find_code_dir()
        unit_name = self._unit_name(code_dir)
        rel_charm_dir = self._rel_charm_dir(unit_name)
        abs_charm_dir = self._fs.join(rel_charm_dir)

        self._fs.add(rel_charm_dir)
        self._create_symlink(code_dir, abs_charm_dir, "metadata.yaml")
        self._create_symlink(code_dir, abs_charm_dir, "templates")

        self.config = self._default_config(code_dir)
        self.log = []
        self.ports = {}

        self.useFixture(EnvironmentVariable("JUJU_UNIT_NAME", unit_name))
        self.useFixture(EnvironmentVariable("CHARM_DIR", abs_charm_dir))

        self._processes.add(ConfigGet(self.config))
        self._processes.add(JujuLog(self.log))
        self._processes.add(OpenPort(self.ports))

        # If charmhelpers is around, clear its config cache.
        hookenv and hookenv.cache.clear()

    def _find_code_dir(self):
        directory = os.getcwd()
        while directory != "/":
            if os.path.exists(os.path.join(directory, "metadata.yaml")):
                return directory
        else:  # pragma: no cover
            raise RuntimeError("This doesn't seem to be a charm code tree")

    def _unit_name(self, code_dir):
        with open(os.path.join(code_dir, "metadata.yaml")) as fd:
            metadata = yaml.safe_load(fd)
        return "{}/{}".format(metadata["name"], 0)

    def _rel_charm_dir(self, unit_name):
        return "var/lib/juju/agents/unit-{}/charm".format(unit_name)

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

    def _create_symlink(self, code_dir, abs_charm_dir, filename):
        os.symlink(
            os.path.join(code_dir, filename),
            os.path.join(abs_charm_dir, filename))
