import os

from pathlib import Path

from fixtures import (
    Fixture,
    EnvironmentVariable,
    TempDir,
    MonkeyPatch,
)


class Filesystem(Fixture):
    """A temporary filesystem tree."""

    def _setUp(self):
        self.root = Path(self.useFixture(TempDir()).path)
        self.useFixture(EnvironmentVariable("ROOT_DIR", str(self.root)))

        self.uid = {}
        self.gid = {}
        self._real_fchown = os.fchown
        self.useFixture(MonkeyPatch("os.fchown", self.fchown))

    def add(self, *paths):
        """Add one or more paths to the tree.

        @param paths: A list of paths, with or without leading slash (they'll
            be created relative to the root directory in any case).
        """
        for path in paths:
            os.makedirs(str(self.root.joinpath(path.lstrip(os.sep))))

    def contains(self, path):
        """Return True if path is a subpath of this filesystem."""
        return self.root in Path(path).parents

    def fchown(self, fileno, uid, gid):
        """Run fake fchown code if fileno points to a sub-path of our tree.

        The ownership set with this fake fchown can be inspected by looking
        at the self.uid/self.gid dictionaries.
        """
        path = os.readlink("/proc/self/fd/{}".format(fileno))
        if self.contains(path):
            self.uid[path] = uid
            self.gid[path] = gid
        else:
            self._real_fchown(fileno, uid, gid)
