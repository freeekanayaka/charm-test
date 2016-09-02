import json

from testtools import TestCase
from fixtures import TempDir

from charmfixture.hooktools.config import ConfigData


class ConfigDataTest(TestCase):

    def setUp(self):
        super().setUp()
        temp_dir = self.useFixture(TempDir())
        self.path = temp_dir.join("test.json")
        self.data = ConfigData(self.path)

    def test_set_item(self):
        self.data["foo"] = "bar"
        with open(self.path) as fd:
            self.assertEqual({"foo": "bar"}, json.load(fd))

    def test_clear(self):
        self.data["foo"] = "bar"
        self.data.clear()
        with open(self.path) as fd:
            self.assertEqual({}, json.load(fd))

    def test_update_keyword(self):
        self.data.update(foo="bar")
        with open(self.path) as fd:
            self.assertEqual({"foo": "bar"}, json.load(fd))

    def test_update_dict(self):
        self.data.update({"foo": "bar"})
        with open(self.path) as fd:
            self.assertEqual({"foo": "bar"}, json.load(fd))
