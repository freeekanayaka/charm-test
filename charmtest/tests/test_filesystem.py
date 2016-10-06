import os

from testtools import TestCase
from fixtures import TempDir

from charmtest.filesystem import FakeFilesystem


class FakeFilesystemTest(TestCase):

    def setUp(self):
        super().setUp()
        self.filesystem = self.useFixture(FakeFilesystem())

    def test_root_dir_environment_variable(self):
        self.assertEqual(
            str(self.filesystem.root), os.environ["TEST_ROOT_DIR"])

    def test_add(self):
        self.filesystem.add("foo/bar", "egg")
        self.assertTrue(self.filesystem.root.joinpath("foo", "bar").exists())
        self.assertTrue(self.filesystem.root.joinpath("egg").exists())

    def test_fchown(self):
        path = str(self.filesystem.root.joinpath("foo"))
        with open(path, "w") as fd:
            os.fchown(fd.fileno(), 123, 456)
        self.assertEqual(123, self.filesystem.uid[path])
        self.assertEqual(456, self.filesystem.gid[path])

    def test_fchown_real(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("foo")
        with open(path, "w") as fd:
            self.assertRaises(
                PermissionError, os.fchown, fd.fileno(), 12345, 9999)

    def test_chown(self):
        path = str(self.filesystem.root.joinpath("foo"))
        os.makedirs(path)
        os.chown(path, 123, 456)
        self.assertEqual(123, self.filesystem.uid[path])
        self.assertEqual(456, self.filesystem.gid[path])

    def test_chown_real(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("foo")
        os.makedirs(path)
        self.assertRaises(PermissionError, os.chown, path, 12345, 9999)
