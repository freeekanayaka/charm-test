Charm Test
==========

.. image:: https://img.shields.io/pypi/v/charm-test.svg
    :target: https://pypi.python.org/pypi/charm-test
    :alt: Latest Version

.. image:: https://travis-ci.org/freeekanayaka/charm-test.svg?branch=master
    :target: https://travis-ci.org/freeekanayaka/charm-test
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/freeekanayaka/charm-test/badge.svg?branch=master
    :target: https://coveralls.io/github/freeekanayaka/charm-test?branch=master
    :alt: Coverage

.. image:: https://readthedocs.org/projects/charm-test/badge/?version=latest
    :target: http://charm-test.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This package sports a collection of helpers for unit-testing Juju charms.

In particular, it extends systemfixtures_ by faking out hook tools
processes (`config-get`, `juju-log`, etc), so authors have a complete suite
of fakes for the typical "boundaries" of a Juju charm.

.. _systemfixtures: https://github.com/testing-cabal/systemfixtures

.. code:: python

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

Support and Documentation
-------------------------

See the `online documentation <http://charm-test.readthedocs.io//>`_ for
a complete reference.

Developing and Contributing
---------------------------

See the `GitHub project <https://github.com/freeekanayaka/charm-test>`_. Bugs
can be filed in the issues tracker.
