from subprocess import (
    check_output,
    check_call,
)

from testtools import TestCase

from charmfixtures.hooktools.fixture import HookTools


class HookToolsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.tools = self.useFixture(HookTools())

    def test_config(self):
        self.assertEqual(b"{}\n", check_output(["config-get"]))

    def test_log(self):
        check_call(["juju-log", "hello world"])
        self.assertEqual("INFO: hello world", self.tools.log[0])

    def test_port(self):
        check_call(["open-port", "1234/TCP"])
        self.assertEqual("1234/TCP", self.tools.port[0])
