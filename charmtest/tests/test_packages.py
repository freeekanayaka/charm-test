from testtools import TestCase

from charmtest.packages import Dpkg


class DpkgTest(TestCase):

    def setUp(self):
        super().setUp()
        self.packages = {}
        self.process = Dpkg(self.packages)

    def test_install(self):
        self.process({"args": ["dpkg", "-i", "foo_1.0-1.deb"]})
        self.assertEqual(["install"], self.packages["foo"])
