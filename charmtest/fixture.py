from fixtures import Fixture

from charmtest.filesystem import FakeFilesystem
from charmtest.users import FakeUsers
from charmtest.groups import FakeGroups
from charmtest.juju import FakeJuju
from charmtest.processes import FakeProcesses
from charmtest.services import Systemctl
from charmtest.network import Wget
from charmtest.packages import Dpkg


class CharmFakes(Fixture):

    def _setUp(self):

        self.fs = self.useFixture(FakeFilesystem())
        self.users = self.useFixture(FakeUsers())
        self.groups = self.useFixture(FakeGroups())
        self.processes = self.useFixture(FakeProcesses())
        self.juju = self.useFixture(FakeJuju(self.fs, self.processes))

        self.services = {}
        self.network = {}
        self.packages = {}

        self.processes.add(Systemctl(self.services))
        self.processes.add(Wget(self.network))
        self.processes.add(Dpkg(self.packages))
