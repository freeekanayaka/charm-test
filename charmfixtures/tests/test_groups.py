import grp

from testtools import TestCase

from charmfixtures.groups import Groups


class GroupsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.groups = self.useFixture(Groups())

    def test_getgrname_root(self):
        info = grp.getgrnam("root")
        self.assertEqual(0, info.gr_gid)

    def test_add(self):
        self.groups.add("foo", 123)
        info = grp.getgrnam("foo")
        self.assertEqual(123, info.gr_gid)
