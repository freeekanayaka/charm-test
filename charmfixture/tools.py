import os

from fixtures import (
    Fixture,
    EnvironmentVariable,
    TempDir,
)

from .config import (
    ConfigData,
    ConfigTool,
)

from .log import (
    LogData,
    LogTool,
)


HOOK_TOOL_CODE = """#!/usr/bin/python3
import sys

from {module} import {klass}

tool = {klass}("{tools_dir}")
tool.run(sys.argv[1:])
"""


class JujuHookTools(Fixture):
    """Provide fake versions of juju hook tools."""

    _tools = {
        "config-get": ConfigTool,
        "juju-log": LogTool,
    }

    def log(self):
        with open(self._tools_dir.join(".log")) as fd:
            return [line.strip() for line in fd.readlines()]

    def _setUp(self):
        self._tools_dir = self.useFixture(TempDir())
        self._charm_dir = self.useFixture(TempDir())

        self.useFixture(EnvironmentVariable("CHARM_DIR", self._charm_dir.path))
        self.useFixture(EnvironmentVariable(
            "PATH", "{}:{}".format(self._tools_dir.path, os.environ["PATH"])))

        for name, code in self._tools.items():
            self._write_tool(name, code)

        self.config = ConfigData(self._tools_dir.join(".config.json"))
        self.log = LogData(LogTool.path(self._tools_dir.path))

    def _write_tool(self, name, klass):

        code = HOOK_TOOL_CODE.format(
            module=klass.__module__, klass=klass.__name__,
            tools_dir=self._tools_dir.path)

        with open(self._tools_dir.join(name), "w") as fd:
            os.fchmod(fd.fileno(), 0o755)
            fd.write(code)
