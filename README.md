# Overview

[![Build Status](https://travis-ci.org/freeekanayaka/charm-fixtures.svg?branch=master)](https://travis-ci.org/freeekanayaka/charm-fixtures)

Python [fixtures](https://github.com/testing-cabal/fixtures) for faking
out the boundaries of a Juju charm and allow convenient unit-testing.

The boundaries are typically executables (e.g. Juju hook tools), network
and file system.

# Example

The `CharmTest` base class sets up all available charm fixtures, so you can
for example programmatically modify backend juju data that hook tools
will return, create fake system users or groups, etc.
    
```python
from charmfixtures import CharmTest

from charmhelpers.core import hookenv


class MyCharmTest(CharmTest):

    def test_log(self):
        """Inspect log lines emitted by your charm code."""
        hookenv.log("Hello world!")
        self.assertEqual("INFO: Hello world!", self.unit.log[0])

    def test_config(self):
        """Set config values for your charm code."""
        self.application.config["foo"] = "bar"
        self.assertEqual("bar", hookenv.config()["foo"])
```
