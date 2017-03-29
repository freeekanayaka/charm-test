from testtools import TestCase

from charmtest.juju.hooktools import (
    ConfigGet,
    JujuLog,
    UnitGet,
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


class UnitGetTest(TestCase):

    def setUp(self):
        super(UnitGetTest, self).setUp()
        self.unit_data = {"private-address": "10.1.2.3"}
        self.process = UnitGet(self.unit_data)

    def test_invoke(self):
        result = self.process({"args": ["unit-get", "private-address"]})
        self.assertEqual(b'10.1.2.3\n', result["stdout"].getvalue())

    def test_format_json(self):
        result = self.process(
            {"args": ["unit-get", "--format=json", "private-address"]})
        self.assertEqual(b'"10.1.2.3"', result["stdout"].getvalue())

    def test_format_yaml(self):
        result = self.process(
            {"args": ["unit-get", "--format=yaml", "private-address"]})
        self.assertEqual(b'10.1.2.3\n...\n', result["stdout"].getvalue())

    def test_unknown_setting(self):
        result = self.process({"args": ["unit-get", "foo"]})
        self.assertEqual(1, result["returncode"])
