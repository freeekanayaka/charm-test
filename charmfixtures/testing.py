from testtools import (
    TestCase,
    try_import,
)

from charmfixtures.filesystem import Filesystem
from charmfixtures.users import Users
from charmfixtures.groups import Groups
from charmfixtures.processes import Processes
from charmfixtures.juju import (
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

        self.application = Application()
        self.unit = Unit()

        self.processes.add(ConfigGet(self.application.config))
        self.processes.add(JujuLog(self.unit.log))
        self.processes.add(OpenPort(self.unit.ports))

        # If charmhelpers is around, clear its config cache.
        hookenv and hookenv.cache.clear()
