from testtools import TestCase

from charmfixtures.filesystem import Filesystem
from charmfixtures.users import Users
from charmfixtures.groups import Groups
from charmfixtures.hooktools.fixture import HookTools


class CharmTest(TestCase):

    def setUp(self):
        super().setUp()
        self.filesystem = self.useFixture(Filesystem())
        self.users = self.useFixture(Users())
        self.groups = self.useFixture(Groups())
        self.hooktools = self.useFixture(HookTools())
