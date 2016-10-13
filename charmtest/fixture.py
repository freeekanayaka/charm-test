from fixtures import Fixture

from systemfixtures import (
    FakeFilesystem,
    FakeUsers,
    FakeGroups,
    FakeProcesses,
    FakeNetwork,
)
from systemfixtures.processes import (
    Systemctl,
    Wget,
    Dpkg,
)

from charmtest.juju import FakeJuju


class CharmFakes(Fixture):

    def _setUp(self):

        self.fs = self.useFixture(FakeFilesystem())
        self.users = self.useFixture(FakeUsers())
        self.groups = self.useFixture(FakeGroups())
        self.processes = self.useFixture(FakeProcesses())
        self.network = self.useFixture(FakeNetwork())
        self.juju = self.useFixture(FakeJuju(self.fs, self.processes))

        self.processes.add(Systemctl())
        self.processes.add(Wget())
        self.processes.add(Dpkg())
