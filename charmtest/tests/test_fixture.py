from testtools import TestCase

from charmtest.fixture import CharmFakes


class CharmFakesTest(TestCase):

    def setUp(self):
        super(CharmFakesTest, self).setUp()
        self.fakes = self.useFixture(CharmFakes())

    def test_attributes(self):
        self.assertTrue(self.fakes.fs)
        self.assertTrue(self.fakes.groups)
        self.assertTrue(self.fakes.users)
        self.assertTrue(self.fakes.processes)
