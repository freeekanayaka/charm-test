import grp

from testtools import TestCase

from charmtest.groups import FakeGroups


class FakeGroupsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.groups = self.useFixture(FakeGroups())

    def test_getgrname_root(self):
        info = grp.getgrnam("root")
        self.assertEqual(0, info.gr_gid)

    def test_add(self):
        self.groups.add("foo", 123)
        info = grp.getgrnam("foo")
        self.assertEqual(123, info.gr_gid)
