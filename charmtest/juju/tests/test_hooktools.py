from testtools import TestCase

from charmtest.juju.hooktools import (
    ConfigGet,
    JujuLog,
)


class ConfigGetTest(TestCase):

    def setUp(self):
        super(ConfigGetTest, self).setUp()
        self.config = {}
        self.process = ConfigGet(self.config)

    def test_invoke(self):
        self.config["foo"] = "bar"
        result = self.process({})
        self.assertEqual(b'{"foo": "bar"}\n', result["stdout"].getvalue())


class JujuLogTest(TestCase):

    def setUp(self):
        super(JujuLogTest, self).setUp()
        self.log = []
        self.process = JujuLog(self.log)

    def test_no_entries(self):
        self.assertEqual([], self.log)

    def test_first_entry(self):
        self.process({"args": ["juju-log", "hello world"]})
        self.assertEqual("INFO: hello world", self.log[0])
