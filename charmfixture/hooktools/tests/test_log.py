from testtools import TestCase
from fixtures import TempDir

from charmfixture.hooktools.log import LogData


class LogDataTest(TestCase):

    def setUp(self):
        super().setUp()
        temp_dir = self.useFixture(TempDir())
        self.path = temp_dir.join("test.log")
        self.data = LogData(self.path)

    def test_no_entries(self):
        self.assertEqual([], list(self.data))

    def test_first_entry(self):
        with open(self.path, "w") as fd:
            fd.write("hello world\n")
        self.assertEqual("hello world", self.data[0])
