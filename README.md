# Overview

[![Build Status](https://travis-ci.org/freeekanayaka/charm-test.svg?branch=master)](https://travis-ci.org/freeekanayaka/charm-test)

A collection of Python [fixtures](https://github.com/testing-cabal/fixtures)
to fake out the boundaries of a Juju charm and allow convenient unit-testing.

The boundaries are typically executables (e.g. Juju hook tools), network
and file system.

# Examples

## Hook tools

The `CharmTest` base class uses a [FakePopen](https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/popen.py)
fixture to redirect calls to Python's `subprocess.Popen`.

This means that the execution of Juju hook tools will be handled by fake code
that modifies fake backend data, which is in turn exposed to test methods.

You can programmatically modify such fake backend data to exercise the charm
code under test.

For example, assuming that you're using using the `charmhelpers.core.hookenv`
utilities to execute hook tools, you can have tests like:


```python
>>> from tempfile import gettempdir
>>>
>>> from charmtest import CharmTest
>>>
>>> from charmhelpers.core import hookenv
>>>
>>>
>>> def some_charm_logic():
...     hookenv.log("Hello world!")
...     hookenv.open_port(1234)
...     return hookenv.config()["foo"]
>>>
>>>
>>> class HookToolsTest(CharmTest):
...
...    def test_charm_logic(self):
...        """Invoke our charm logic and inspect the resulting backend state."""
...        # Setup the fake Juju backend application config.
...        self.application.config["foo"] = "bar"
...
...        # Run charm code.
...        some_charm_logic()
...
...        # Perform assertions against the fake Juju backend.
...        self.assertEqual("INFO: Hello world!", self.unit.log[0])
...        self.assertEqual("bar", hookenv.config()["foo"])
...        self.assertEqual({1234}, self.unit.ports["TCP"])
...        self.assertTrue(hookenv.charm_dir().startswith(gettempdir()))
>>>
>>>
>>> HookToolsTest(methodName="test_charm_logic").run().wasSuccessful()
True
>>>
```
