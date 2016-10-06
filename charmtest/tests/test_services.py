from testtools import TestCase

from charmtest.services import Systemctl


class SystemctlTest(TestCase):

    def setUp(self):
        super().setUp()
        self.services = {}
        self.process = Systemctl(self.services)

    def test_stop(self):
        self.process({"args": ["systemctl", "stop", "foo"]})
        self.assertEqual(["stop"], self.services["foo"])

    def test_start(self):
        self.process({"args": ["systemctl", "start", "foo"]})
        self.assertEqual(["start"], self.services["foo"])

    def test_is_active(self):
        self.process({"args": ["systemctl", "start", "foo"]})
        result = self.process({"args": ["systemctl", "is-active", "foo"]})
        self.assertIsNone(result.get("returncode"))

    def test_is_not_active(self):
        result = self.process({"args": ["systemctl", "is-active", "foo"]})
        self.assertEqual(1, result["returncode"])
