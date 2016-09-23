import json

from testtools import TestCase
from fixtures import (
    TempDir,
    EnvironmentVariable,
)

from charmfixtures.hooktools.config import ConfigData


class ConfigDataTest(TestCase):

    def setUp(self):
        super().setUp()
        charm_dir = self.useFixture(TempDir())
        self.useFixture(EnvironmentVariable("CHARM_DIR", charm_dir.path))
        self.data = ConfigData()

    def test_set_item(self):
        self.data["foo"] = "bar"
        with open(self.data.path()) as fd:
            self.assertEqual({"foo": "bar"}, json.load(fd))

    def test_clear(self):
        self.data["foo"] = "bar"
        self.data.clear()
        with open(self.data.path()) as fd:
            self.assertEqual({}, json.load(fd))

    def test_update_keyword(self):
        self.data.update(foo="bar")
        with open(self.data.path()) as fd:
            self.assertEqual({"foo": "bar"}, json.load(fd))

    def test_update_dict(self):
        self.data.update({"foo": "bar"})
        with open(self.data.path()) as fd:
            self.assertEqual({"foo": "bar"}, json.load(fd))
