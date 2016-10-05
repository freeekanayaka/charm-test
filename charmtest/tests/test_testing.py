import os

from subprocess import (
    check_output,
    check_call,
)

from charmtest.testing import CharmTest


class MyCharmTest(CharmTest):

    def test_fixtures(self):
        self.assertTrue(self.filesystem)
        self.assertTrue(self.groups)
        self.assertTrue(self.users)
        self.assertTrue(self.processes)

    def test_charm_dir(self):
        self.assertIn("CHARM_DIR", os.environ)
        self.assertTrue(os.path.isdir(os.environ["CHARM_DIR"]))

    def test_juju_config(self):
        self.application.config["foo"] = "bar"
        self.assertEqual(b'{"foo": "bar"}\n', check_output(["config-get"]))

    def test_log(self):
        check_call(["juju-log", "hello world"])
        check_call(["juju-log", "-l", "DEBUG", "how are you?"])
        self.assertEqual("INFO: hello world", self.unit.log[0])
        self.assertEqual("DEBUG: how are you?", self.unit.log[1])

    def test_port(self):
        check_call(["open-port", "1234/TCP"])
        self.assertEqual({1234}, self.unit.ports["TCP"])
