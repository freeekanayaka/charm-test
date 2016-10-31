from testtools import TestCase

from charmtest import CharmFakes


class CharmTest(TestCase):

    def setUp(self):
        super(CharmTest, self).setUp()
        self.fakes = self.useFixture(CharmFakes())
