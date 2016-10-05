from testtools import TestCase

from charmtest.juju.application import Application
from charmtest.juju.unit import Unit


class UnitTest(TestCase):

    def setUp(self):
        super().setUp()
        self.application = Application("test")
        self.unit = Unit(self.application, 0)

    def test_name(self):
        self.assertEqual("test/0", self.unit.name)
        self.unit.number = 1
        self.assertEqual("test/1", self.unit.name)
        self.application.name = "app"
        self.assertEqual("app/1", self.unit.name)
