from testtools import (
    TestCase,
    try_import,
)

from fixtures import (
    EnvironmentVariable,
    TempDir,
    MonkeyPatch,
)

from charmtest.filesystem import Filesystem
from charmtest.users import Users
from charmtest.groups import Groups
from charmtest.processes import Processes
from charmtest.juju import (
    Application,
    Unit,
    ConfigGet,
    JujuLog,
    OpenPort,
)

hookenv = try_import("charmhelpers.core.hookenv")

PLATFORM = ('Ubuntu', '16.04', 'xenial')


class CharmTest(TestCase):

    def setUp(self):
        super().setUp()
        self.filesystem = self.useFixture(Filesystem())
        self.users = self.useFixture(Users())
        self.groups = self.useFixture(Groups())
        self.processes = self.useFixture(Processes())
        temp_dir = self.useFixture(TempDir())
        self.useFixture(EnvironmentVariable("CHARM_DIR", temp_dir.path))

        # Force Ubuntu as platform, since charmhelpers doesn't like
        # 'debian' (which is what you get on Travis).
        self.useFixture(
            MonkeyPatch("platform.linux_distribution", lambda: PLATFORM))

        self.application = Application()
        self.unit = Unit()

        self.processes.add(ConfigGet(self.application.config))
        self.processes.add(JujuLog(self.unit.log))
        self.processes.add(OpenPort(self.unit.ports))

        # If charmhelpers is around, clear its config cache.
        hookenv and hookenv.cache.clear()
