import os
import doctest


def load_tests(loader, standard_tests, pattern):
    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern=pattern)
    standard_tests.addTests(package_tests)
    standard_tests.addTest(doctest.DocFileSuite("../../README.md"))
    return standard_tests
