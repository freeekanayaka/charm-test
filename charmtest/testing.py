from testtools import (
    TestCase,
    try_import,
)

from fixtures import (
    EnvironmentVariable,
    TempDir,
)

from charmtest.filesystem import Filesystem
from charmtest.users import Users
from charmtest.groups import Groups
from charmtest.services import Systemctl
from charmtest.processes import Processes
from charmtest.juju import (
    Application,
    Unit,
    ConfigGet,
    JujuLog,
    OpenPort,
)

hookenv = try_import("charmhelpers.core.hookenv")


class CharmTest(TestCase):

    def setUp(self):
        super().setUp()
        self.filesystem = self.useFixture(Filesystem())
        self.users = self.useFixture(Users())
        self.groups = self.useFixture(Groups())
        self.processes = self.useFixture(Processes())
        temp_dir = self.useFixture(TempDir())
        self.useFixture(EnvironmentVariable("CHARM_DIR", temp_dir.path))

        self.application = Application()
        self.unit = Unit()
        self.services = {}

        self.processes.add(ConfigGet(self.application.config))
        self.processes.add(JujuLog(self.unit.log))
        self.processes.add(OpenPort(self.unit.ports))
        self.processes.add(Systemctl(self.services))

        # If charmhelpers is around, clear its config cache.
        hookenv and hookenv.cache.clear()
