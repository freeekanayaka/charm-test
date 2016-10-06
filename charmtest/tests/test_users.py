import pwd

from testtools import TestCase

from charmtest.users import FakeUsers


class FakeUsersTest(TestCase):

    def setUp(self):
        super().setUp()
        self.users = self.useFixture(FakeUsers())

    def test_getwdname_root(self):
        info = pwd.getpwnam("root")
        self.assertEqual(0, info.pw_uid)

    def test_add(self):
        self.users.add("foo", 123)
        info = pwd.getpwnam("foo")
        self.assertEqual(123, info.pw_uid)
