import os

from subprocess import (
    check_output,
    check_call,
)

from fixtures import EnvironmentVariable

from testtools import TestCase

from charmfixture.hooktools.fixture import HookTools

PYTHONPATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class HookToolsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.tools = HookTools()
        self.useFixture(self.tools)
        # Export the python path so the generated script code can
        # import our modules.
        self.useFixture(EnvironmentVariable("PYTHONPATH", PYTHONPATH))

    def test_config(self):
        self.assertEqual(b"{}\n", check_output(["config-get"]))

    def test_log(self):
        check_call(["juju-log", "hello world"])
        self.assertEqual("INFO: hello world", self.tools.log[0])
