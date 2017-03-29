import os
import json

from subprocess import (
    check_output,
    check_call,
)

from testtools import TestCase
from testtools.matchers import DirExists

from systemfixtures import (
    FakeFilesystem,
    FakeProcesses,
)

from charmtest.juju.fixture import FakeJuju


class FakeJujuTest(TestCase):

    def setUp(self):
        super(FakeJujuTest, self).setUp()
        self.fs = self.useFixture(FakeFilesystem())
        self.processes = self.useFixture(FakeProcesses())
        self.juju = self.useFixture(FakeJuju(self.fs, self.processes))

    def test_charm_dir(self):
        self.assertThat(os.environ["CHARM_DIR"], DirExists())

    def test_juju_config_default(self):
        config = json.loads(check_output(["config-get"]).decode("utf-8"))
        self.assertEqual({"foo": "abc", "bar": 123}, config)

    def test_juju_config(self):
        self.juju.config["foo"] = "bar"
        config = json.loads(check_output(["config-get"]).decode("utf-8"))
        self.assertEqual("bar", config["foo"])

    def test_log(self):
        check_call(["juju-log", "hello world"])
        check_call(["juju-log", "-l", "DEBUG", "how are you?"])
        self.assertEqual("INFO: hello world", self.juju.log[0])
        self.assertEqual("DEBUG: how are you?", self.juju.log[1])

    def test_port(self):
        check_call(["open-port", "1234/TCP"])
        self.assertEqual({1234}, self.juju.ports["TCP"])

    def test_unit_get(self):
        self.assertEqual(
            b"10.1.2.3\n", check_output(["unit-get", "private-address"]))
