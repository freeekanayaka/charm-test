[![Build Status](https://travis-ci.org/freeekanayaka/charm-test.svg?branch=master)](https://travis-ci.org/freeekanayaka/charm-test) [![Coverage Status](https://coveralls.io/repos/github/freeekanayaka/charm-test/badge.svg?branch=master)](https://coveralls.io/github/freeekanayaka/charm-test?branch=master)

# Overview

This package sports a collection of helpers for unit-testing Juju charms.

In particular, it extends [systemfixtures](https://github.com/freeekanayaka/system-fixtures)
by faking out hook tools processes (`config-get`, `juju-log`, etc), so
authors have a complete suite of fakes for the typical "boundaries"
of a Juju charm.

The examples below cover the Juju-related boundaries part, for documentation
about the rest of fake boundaries (file system, processes, network, users,
groups, etc) see the `systemfixtures` [home page](https://github.com/freeekanayaka/system-fixtures).

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

## Processes, network, file system, users, groups, etc.

The `CharmTest` base class also sets up a number of useful fixtures from
the `systemfixtures` package. See [here](https://github.com/freeekanayaka/system-fixtures)
for further documentation:

```python
>>> class ExampleCharmTest(CharmTest):
...
...    def test_other_fakes(self):
...        self.assertTrue(self.fakes.processes)
...        self.assertTrue(self.fakes.fs)
...        self.assertTrue(self.fakes.users)
...        self.assertTrue(self.fakes.groups)
>>>
>>> ExampleCharmTest(methodName="test_other_fakes").run().wasSuccessful()
True

```
