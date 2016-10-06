# Overview

[![Build Status](https://travis-ci.org/freeekanayaka/charm-test.svg?branch=master)](https://travis-ci.org/freeekanayaka/charm-test)

A collection of Python [fixtures](https://github.com/testing-cabal/fixtures)
to fake out the boundaries of a Juju charm and allow convenient unit-testing.

The boundaries are typically executables (e.g. Juju hook tools), network
and file system.

# Examples

## Juju environment variables

The `CharmTest` base class uses an [EnvironmentVariable](https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/environ.py)
fixture to set the environment variables that the charm code runtime
expects (for instance when calling the associated `charmhelpers` APIs):


```python
>>> from testtools.matchers import DirExists
>>>
>>> from charmtest import CharmTest
>>>
>>> from charmhelpers.core import hookenv
>>>
>>>
>>> def example_charm_logic():
...     return {
...         "service-name": hookenv.service_name(),
...         "local-unit": hookenv.local_unit(),
...         "charm-dir": hookenv.charm_dir(),
...     }
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...        result = example_charm_logic()
...        self.assertEqual("test", result["service-name"])
...        self.assertEqual("test/0", result["local-unit"])
...        self.assertThat(result["charm-dir"], DirExists())
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Juju hook tools

The `CharmTest` base class uses a [FakePopen](https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/popen.py)
fixture to redirect calls to Python's `subprocess.Popen`.

This means that the execution of Juju hook tools will be handled by fake code
that modifies fake backend data, which is in turn exposed to test methods.

You can programmatically modify such fake backend data to exercise the charm
code under test.

For example, assuming that you're using using the `charmhelpers.core.hookenv`
utilities to execute hook tools, you can have tests like:


```python
>>> def example_charm_logic():
...     hookenv.log("Hello world!")
...     hookenv.open_port(1234)
...     return hookenv.config()["foo"]
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...        self.fakes.juju.config["foo"] = "bar"
...        result = example_charm_logic()
...        self.assertEqual("INFO: Hello world!", self.fakes.juju.log[0])
...        self.assertEqual("bar", result)
...        self.assertEqual({1234}, self.fakes.juju.ports["TCP"])
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Charm metadata, config and templates

The `CharmTest` base class will traverse the process' all ancestors of the
current working directory, until it finds a directory containing a file
named "metadata.yaml". That directory will be considered the code tree of the
charm under test. Charm metadata, default config values and templates will
be made available to the underlying tests:

```python
>>> import os
>>>
>>> def example_charm_logic():
...     return {
...        "summary": hookenv.metadata()["summary"],
...        "config-foo": hookenv.config()["foo"],
...        "has-templates-dir": os.path.exists(os.path.join(hookenv.charm_dir(), "templates")),
...     }
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...        result = example_charm_logic()
...        self.assertEqual({
...            "summary": "Test charm",
...            "config-foo": "abc",
...            "has-templates-dir": True},
...            result)
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Filesystem

The `CharmTest` base class uses a [TempDir](https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/tempdir.py)
fixture to create a temporary directory to use as filesystem "root". The idea
is that charm code should be factored in a way that it writes or reads files
using paths relative to a certain root.

A [MonkeyPatch](https://github.com/testing-cabal/fixtures/blob/master/fixtures/_fixtures/monkeypatch.py)
is used to capture calls to Python's `os.chown` and `os.fchown`, so they can
be executed in unit tests, that typically run as unpriviliged user:

```python
>>> from charmhelpers.core import templating
>>>
>>> from testtools.matchers import FileContains
>>>
>>>
>>> def example_charm_logic(root):
...     path = os.path.join(root, "etc", "app", "app.conf")
...     templating.render("app.conf", path, {"user": "John"})
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...        self.fakes.fs.add("etc/app/")  # Create the etc/app directory
...        example_charm_logic(str(self.fakes.fs.root))
...        path = self.fakes.fs.join("etc", "app", "app.conf")
...        self.assertThat(path, FileContains("Hello John!"))
...        self.assertThat(path, self.fakes.fs.hasOwner(0, 0))
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
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
...     host.write_file(path, b"hello", group="nogroup")
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...
...        # Setup the fake system groups backend, creating a fake "nogroup"
...        # group. The "root" user is already set up by default.
...        self.fakes.groups.add("nogroup", 9999)
...
...        path = str(self.fakes.fs.root.joinpath("foo"))
...        example_charm_logic(path)
...
...        self.assertThat(path, FileContains("hello"))
...        self.assertThat(path, self.fakes.fs.hasOwner(0, 9999))
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## System services

The `CharmTest` base class adds a fake `systemctl` process to track starting
and stopping services:

```python
>>> def example_charm_logic():
...     host.service_stop("app")
...     host.service_start("app")
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...        example_charm_logic()
...        self.assertEqual(["stop", "start"], self.fakes.services["app"])
...        self.assertTrue(host.service_running("app"))
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Network

The `CharmTest` base class adds a fake `wget` process to simulate downloading
URLs from the network:

```python
>>> import subprocess
>>>
>>>
>>> def example_charm_logic():
...     return subprocess.check_output(("wget", "-O", "-", "http://x"))
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...        self.fakes.network["http://x"] = b"data"
...        result = example_charm_logic()
...        self.assertEqual(b"data", result)
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
True

```

## Packages

The `CharmTest` base class adds a fake `dpkg` process to simulate installing
Debian packages:

```python
>>> import subprocess
>>>
>>>
>>> def example_charm_logic():
...     return subprocess.check_output(("dpkg", "-i", "foo_1.0-1.deb"))
>>>
>>>
>>> class ExampleCharmTest(CharmTest):
...
...    def test_charm_logic(self):
...        example_charm_logic()
...        self.assertEqual(["install"], self.fakes.packages["foo"])
>>>
>>>
>>> ExampleCharmTest(methodName="test_charm_logic").run().wasSuccessful()
True

```
