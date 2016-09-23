from charmfixtures.testing import CharmTest


class MyCharmTest(CharmTest):

    def test_fixtures(self):
        self.assertTrue(self.filesystem)
        self.assertTrue(self.groups)
        self.assertTrue(self.users)
        self.assertTrue(self.hooktools)
