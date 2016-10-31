from testtools import TestCase

from charmtest.testing import CharmTest
from charmtest.fixture import CharmFakes


class CharmTestTest(TestCase):

    def setUp(self):
        super(CharmTestTest, self).setUp()
        self.test = CharmTest(methodName="setUp")

    def test_setUp(self):
        self.test.setUp()
        self.assertIsInstance(self.test.fakes, CharmFakes)
