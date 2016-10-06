from testtools import TestCase
from testtools.matchers import FileContains

from fixtures import TempDir

from charmtest.network import Wget


class ConfigGetTest(TestCase):

    def setUp(self):
        super().setUp()
        self.network = {"http://x": b"data"}
        self.process = Wget(self.network)

    def test_to_stdout(self):
        result = self.process({"args": ["wget", "-O", "-", "http://x"]})
        self.assertEqual(b"data", result["stdout"].getvalue())

    def test_to_file(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("output")
        self.process({"args": ["wget", "-O", path, "http://x"]})
        self.assertThat(path, FileContains("data"))
