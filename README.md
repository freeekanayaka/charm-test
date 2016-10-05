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
>>> from charmtest import CharmTest
>>>
>>> from charmhelpers.core import hookenv
>>>
>>>
>>> def example_charm_logic():
...     hookenv.log("Hello world!")
...     hookenv.open_port(1234)
...     return hookenv.config()["foo"]
>>>
>>>
>>> class ExampleTest(CharmTest):
...
...    def test_charm_logic(self):
...        """Invoke our charm logic and inspect the resulting backend state."""
...
...        # Setup the fake Juju backend application config.
...        self.application.config["foo"] = "bar"
...
...        # Run our charm code.
...        example_charm_logic()
...
...        # Perform assertions against the fake Juju backend.
...        self.assertEqual("INFO: Hello world!", self.unit.log[0])
...        self.assertEqual("bar", hookenv.config()["foo"])
...        self.assertEqual({1234}, self.unit.ports["TCP"])
>>>
>>>
>>> ExampleTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Filesystem

The `CharmTest` base class also uses a [TempDir](https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/tempdir.py)
fixture to create a temporary directory to use as filesystem "root". The idea
is that charm code should be factored in a way that it writes or reads files
using paths relative to a certain root.

A [MonkeyPatch](https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/monkeypatch.py)
is used to capture calls to Python's `os.chown` and `os.fchown`, so they can
be executed in unit tests, that typically run as unpriviliged user:

```python
>>> import os
>>>
>>>
>>> def example_charm_logic(root):
...     path = root.joinpath("etc", "app", "app.conf")
...     with path.open("w") as fd:
...         fd.write("hello")
...     os.chown(str(path), 0, 0)
>>>
>>>
>>> class ExampleTest(CharmTest):
...
...    def test_charm_logic(self):
...        """Invoke our charm logic and inspect the resulting backend state."""
...
...        # Setup the etc directory in fake filesystem root.
...        self.filesystem.add("etc/app/")
...
...        # Run our charm code.
...        example_charm_logic(self.filesystem.root)
...
...        # Perform assertions against the fake filesystem backend.
...        path = self.filesystem.root.joinpath("etc", "app", "app.conf")
...        with path.open() as fd:
...            self.assertEqual("hello", fd.read())
...        self.assertEqual(0, self.filesystem.uid[str(path)])
...        self.assertEqual(0, self.filesystem.gid[str(path)])
>>>
>>>
>>> ExampleTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Users and groups

The `CharmTest` base class mocks out calls to Python's `grp.getpwnam`
and `grp.getgrnam`.

Like in the Juju hook tools case above, calls to these APIs will be handled
by fake code that modifies fake data:

```python
>>> from charmhelpers.core import host
>>>
>>>
>>> def example_charm_logic(path):
...     host.write_file(path, b"hello")
>>>
>>>
>>> class ExampleTest(CharmTest):
...
...    def test_charm_logic(self):
...        """Invoke our charm logic and inspect the resulting backend state."""
...
...        # Setup the fake system users/groups backend, creating a fake "root"
...        # user and group.
...        self.users.add("root", 123)
...        self.groups.add("root", 456)
...
...        # Run our charm code.
...        path = str(self.filesystem.root.joinpath("foo"))
...        example_charm_logic(path)
...
...        # The file got written for real.
...        with open(path) as fd:
...            self.assertEqual("hello", fd.read())
...
...        # Perform assertions against the filesystem backend.
...        self.assertEqual(123, self.filesystem.uid[path])
...        self.assertEqual(456, self.filesystem.gid[path])
>>>
>>>
>>> ExampleTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Services

The `CharmTest` base class adds a fake `systemctl` process to track starting
and stopping services:

```python
>>> def example_charm_logic():
...     host.service_stop("app")
...     host.service_start("app")
>>>
>>>
>>> class ExampleTest(CharmTest):
...
...    def test_charm_logic(self):
...        """Invoke our charm logic and inspect the resulting backend state."""
...
...        # Run our charm code.
...        example_charm_logic()
...
...        # Perform assertions against the services backend.
...        self.assertEqual(["stop", "start"], self.services["app"])
...        self.assertTrue(host.service_running("app"))
>>>
>>>
>>> ExampleTest(methodName="test_charm_logic").run().wasSuccessful()
True

```
