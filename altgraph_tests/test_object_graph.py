import unittest
from altgraph.ObjectGraph import ObjectGraph

class Node (object):
    def __init__(self, graphident):
        self.graphident = graphident

class SubNode (Node):
    pass


class TestObjectGraph (unittest.TestCase):

    @unittest.expectedFailure
    def test_constructor(self):
        self.fail("add tests for ObjectGraph()")

    @unittest.expectedFailure
    def test_flatten(self):
        self.fail("add tests for ObjectGraph.flatten()")

    @unittest.expectedFailure
    def test_get_edges(self):
        self.fail("add tests for ObjectGraph.get_edges()")

    @unittest.expectedFailure
    def test_filterStack(self):
        self.fail("add tests for ObjectGraph.filterStack()")

    @unittest.expectedFailure
    def test_removeNode(self):
        self.fail("add tests for ObjectGraph.removeNode()")

    @unittest.expectedFailure
    def test_removeReference(self):
        self.fail("add tests for ObjectGraph.removeReference()")

    @unittest.expectedFailure
    def test_getIdent(self):
        self.fail("add tests for ObjectGraph.getIdent()")

    @unittest.expectedFailure
    def test_getRawIdent(self):
        self.fail("add tests for ObjectGraph.getRawIdent()")

    @unittest.expectedFailure
    def test_findNode(self):
        self.fail("add tests for ObjectGraph.findNode()")

    @unittest.expectedFailure
    def test_addNode(self):
        self.fail("add tests for ObjectGraph.addNode()")

    @unittest.expectedFailure
    def test_createReference(self):
        self.fail("add tests for ObjectGraph.createReference()")

    @unittest.expectedFailure
    def test_createNode(self):
        self.fail("add tests for ObjectGraph.createNode()")

    @unittest.expectedFailure
    def test_msg(self):
        self.fail("add tests for ObjectGraph.msg(), msgin(), msgout()")


if __name__ == "__main__": # pragma: no cover
    unittest.main()
