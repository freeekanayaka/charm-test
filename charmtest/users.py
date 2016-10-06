import pwd

from fixtures import (
    Fixture,
    MonkeyPatch,
)


class FakeUsers(Fixture):

    def _setUp(self):
        self.data = {"root": ("x", 0, 0, "root", "/root", "/bin/bash")}
        self.useFixture(MonkeyPatch("pwd.getpwnam", self.getpwnam))

    def add(self, name, uid):
        self.data[name] = (
            "x", uid, uid, name, "/home/{}".format(name), "/bin/bash")

    def getpwnam(self, name):
        return pwd.struct_passwd((name,) + self.data[name])
