# Overview

[![Build Status](https://travis-ci.org/freeekanayaka/charmfixture.svg?branch=master)](https://travis-ci.org/freeekanayaka/charmfixture)

Python [fixtures](https://github.com/testing-cabal/fixtures) for faking
out the boundaries of a Juju charm and allow convenient unit-testing.

The boundaries are typically executables (e.g. Juju hook tools), network
and file system.

# Examples

## Hook tools

The HookTools fixture set the PATH environment variable to point
to a temporary directory where fake juju hook tools executables are
saved.

You can programmatically modify the backend juju data that the tools
will return.
    
```python
from testtools import TestCase
    
from charmhelpers.core import hookenv

from charmfixture import HookTools


class MyCharmTest(TestCase):

    def setUp(self):
        super().setUp()
        self.tools = self.useFixture(HookTools())

    def test_log(self):
        """Inspect log lines emitted by your charm code."""
        hookenv.log("Hello world!")
        self.assertEqual("INFO: Hello world!", self.tools.log[0])

    def test_config(self):
        """Set config values for your charm code."""
        self.tools.config["foo"] = "bar"
        self.assertEqual("bar", hookenv.config()["foo"])
```
