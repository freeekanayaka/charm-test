from charmfixtures.testing import CharmTest


class MyCharmTest(CharmTest):

    def test_fixtures(self):
        self.assertTrue(self.filesystem)
