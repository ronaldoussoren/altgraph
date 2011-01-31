Release history
===============

0.7.2
-----

This is a minor bugfix release

Bugfixes:

- distutils didn't include the documentation subtree

0.7.1
-----

This is a minor feature release

Features:

- Documentation is now generated using `sphinx <http://pypi.python.org/pypi/sphinx>`_
  and can be viewed at <http://packages.python.org/altgraph>.

- The repository has moved to bitbucket 

- ``altgraph.GraphStat.avg_hops`` is no longer present, the function had no
  implementation and no specified behaviour.

- the module ``altgraph.compat`` is gone, which means altgraph will no
  longer work with Python 2.3.


0.7.0
-----

This is a minor feature release.

Features:

- Support for Python 3

- It is now possible to run tests using 'python setup.py test'

  (The actual testsuite is still very minimal though)
