from testtools import (
    TestCase,
    try_import,
)

from charmfixtures.filesystem import Filesystem
from charmfixtures.users import Users
from charmfixtures.groups import Groups
from charmfixtures.hooktools.fixture import HookTools

hookenv = try_import("from charmhelpers.core.hookenv")


class CharmTest(TestCase):

    def setUp(self):
        super().setUp()
        self.filesystem = self.useFixture(Filesystem())
        self.users = self.useFixture(Users())
        self.groups = self.useFixture(Groups())
        self.hooktools = self.useFixture(HookTools())
        # If charmhelpers is around, clear its config cache
        hookenv and hookenv.cache.clear()
