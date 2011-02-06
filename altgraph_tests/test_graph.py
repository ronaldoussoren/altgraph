import unittest

from altgraph import GraphError
from altgraph.Graph import Graph

class TestGraph (unittest.TestCase):

    @unittest.expectedFailure
    def test_missing(self):
        self.fail("add tests for algraph.Graph")

    def test_nodes(self):
        graph = Graph()

        o1 = object()
        o1b = object()
        o2 = object()
        graph.add_node(1, o1)
        graph.add_node(1, o1b)
        graph.add_node(2, o2)
        graph.add_node(3)

        self.assertRaises(TypeError, graph.add_node, [])

        self.assertTrue(graph.node_data(1) is o1)
        self.assertTrue(graph.node_data(2) is o2)
        self.assertTrue(graph.node_data(3) is None)

        self.assertTrue(1 in graph)
        self.assertTrue(2 in graph)
        self.assertTrue(3 in graph)

        self.assertEqual(graph.number_of_nodes(), 3)
        self.assertEqual(graph.number_of_hidden_nodes(), 0)
        self.assertEqual(graph.hidden_node_list(), [])
        self.assertEqual(list(sorted(graph)), [1, 2, 3])

        graph.hide_node(1)
        graph.hide_node(2)
        graph.hide_node(3)

        self.assertEqual(graph.number_of_nodes(), 0)
        self.assertEqual(graph.number_of_hidden_nodes(), 3)
        self.assertEqual(list(sorted(graph.hidden_node_list())), [1, 2, 3])
        
        self.assertFalse(1 in graph)
        self.assertFalse(2 in graph)
        self.assertFalse(3 in graph)

        graph.restore_node(1)
        self.assertTrue(1 in graph)
        self.assertFalse(2 in graph)
        self.assertFalse(3 in graph)

        graph.restore_all_nodes()
        self.assertTrue(1 in graph)
        self.assertTrue(2 in graph)
        self.assertTrue(3 in graph)

if __name__ == "__main__":
    unittest.main()
