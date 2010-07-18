#!/usr/bin/env python


try:
    import setuptools

except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()

from setuptools import setup
import sys

VERSION = '0.7.0'
DESCRIPTION = "Python graph (network) package"
LONG_DESCRIPTION = """
altgraph is a fork of graphlib: a graph (network) package for constructing
graphs, BFS and DFS traversals, topological sort, shortest paths, etc. with
graphviz output.

altgraph includes some additional usage of Python 2.3+ features and
enhancements related to modulegraph and macholib.
"""

CLASSIFIERS = filter(None, map(str.strip,
"""                 
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
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
    url="http://undefined.org/python/#altgraph",
    license="MIT License",
    packages=['altgraph'],
    platforms=['any'],
    zip_safe=True,
    **extra_args
)
