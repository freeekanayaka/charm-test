import grp

from fixtures import (
    Fixture,
    MonkeyPatch,
)


class Groups(Fixture):

    def _setUp(self):
        self.data = {"root": ("x", 0, [])}
        self.useFixture(MonkeyPatch("grp.getgrnam", self.getgrnam))

    def add(self, name, gid):
        self.data[name] = ("x", gid, [])

    def getgrnam(self, name):
        return grp.struct_group((name,) + self.data[name])
