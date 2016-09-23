import pwd

from testtools import TestCase

from charmfixture.users import Users


class UsersTest(TestCase):

    def setUp(self):
        super().setUp()
        self.users = self.useFixture(Users())

    def test_getwdname_root(self):
        info = pwd.getpwnam("root")
        self.assertEqual(0, info.pw_uid)

    def test_add(self):
        self.users.add("foo", 123)
        info = pwd.getpwnam("foo")
        self.assertEqual(123, info.pw_uid)
