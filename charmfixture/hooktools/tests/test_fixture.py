from subprocess import (
    check_output,
    check_call,
)

from testtools import TestCase

from charmfixture.hooktools.fixture import HookTools


class HookToolsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.tools = HookTools()
        self.useFixture(self.tools)

    def test_config(self):
        self.assertEqual(b"{}\n", check_output(["config-get"]))

    def test_log(self):
        check_call(["juju-log", "hello world"])
        self.assertEqual("INFO: hello world", self.tools.log[0])
