from testtools import TestCase
from fixtures import (
    TempDir,
    EnvironmentVariable,
)

from charmfixture.hooktools.log import LogData


class LogDataTest(TestCase):

    def setUp(self):
        super().setUp()
        charm_dir = self.useFixture(TempDir())
        self.useFixture(EnvironmentVariable("CHARM_DIR", charm_dir.path))
        self.data = LogData()

    def test_no_entries(self):
        self.assertEqual([], list(self.data))

    def test_first_entry(self):
        with open(self.data.path(), "w") as fd:
            fd.write("hello world\n")
        self.assertEqual("hello world", self.data[0])
