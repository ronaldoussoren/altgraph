import unittest

from altgraph import Dot
from altgraph import Graph

class TestDot (unittest.TestCase):

    @unittest.expectedFailure
    def test_missing(self):
        self.fail("add tests for altgraph.Dot")


    def test_constructor(self):

        g = Graph.Graph()


if __name__ == "__main__": # pragma: no cover
    unittest.main()
