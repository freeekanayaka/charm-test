# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Distutils installer for charm-test."""

from setuptools import setup, find_packages


install_requires = [
    "fixtures >= 0.3.6",
    ]

setup(
    name="charmtest",
    version="0.1.0",
    packages=find_packages(),

    install_requires=install_requires,
    extras_require=dict(
        test=[
            "testtools",
            "coverage",
            "codecov",
        ],
    ),

    author="Free Ekanayaka",
    author_email="<free.ekanayaka@canonical.com>",
    description="Create fake juju hook tools for charm unit testing",
    license="AGPL",
    keywords="fixtures juju charm",
    url="https://github.com/freeekanayaka/charm-test",
)
