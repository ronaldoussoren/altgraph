#!/usr/bin/env python


try:
    import setuptools

except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()

from setuptools import setup
import sys

VERSION = '0.7.1'
DESCRIPTION = "Python graph (network) package"
LONG_DESCRIPTION = """
altgraph is a fork of graphlib: a graph (network) package for constructing
graphs, BFS and DFS traversals, topological sort, shortest paths, etc. with
graphviz output.

altgraph includes some additional usage of Python 2.3+ features and
enhancements related to modulegraph and macholib.

NEWS
====

0.7.0
-----

This is a minor feature release.

Features:

- Support for Python 3

- It is now possible to run tests using 'python setup.py test'

  (The actual testsuite is still very minimal though)
"""

CLASSIFIERS = filter(None, map(str.strip,
"""                 
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Visualization
""".splitlines()))

if sys.version_info[0] == 3:
    extra_args = dict(use_2to3=True)
else:
    extra_args = dict()

setup(
    name="altgraph",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    author="Bob Ippolito",
    author_email="bob@redivi.com",
    maintainer="Ronald Oussoren",
    maintainer_email="ronaldoussoren@mac.com",
    url="http://undefined.org/python/#altgraph",
    license="MIT License",
    packages=['altgraph'],
    platforms=['any'],
    test_suite='testsuite',
    zip_safe=True,
    **extra_args
)
