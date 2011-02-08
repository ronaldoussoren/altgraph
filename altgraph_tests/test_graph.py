import unittest

from altgraph import GraphError
from altgraph.Graph import Graph

class TestGraph (unittest.TestCase):

    def test_nodes(self):
        graph = Graph()

        self.assertEqual(graph.node_list(), [])

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

        self.assertEqual(list(sorted(graph.node_list())), [1, 2, 3])

        v = graph.describe_node(1)
        self.assertEqual(v, (1, o1, [], []))

    def test_edges(self):
        graph = Graph()
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)
        graph.add_node(5)

        self.assertIsInstance(graph.edge_list(), list)

        graph.add_edge(1, 2)
        graph.add_edge(4, 5, 'a')

        self.assertRaises(GraphError, graph.add_edge, 'a', 'b', create_nodes=False)

        self.assertEqual(graph.number_of_hidden_edges(), 0)
        self.assertEqual(graph.number_of_edges(), 2)
        e = graph.edge_by_node(1, 2)
        self.assertIsInstance(e, int)
        graph.hide_edge(e)
        self.assertEqual(graph.number_of_hidden_edges(), 1)
        self.assertEqual(graph.number_of_edges(), 1)
        e2 = graph.edge_by_node(1, 2)
        self.assertTrue(e2 is None)

        graph.restore_edge(e)
        e2 = graph.edge_by_node(1, 2)
        self.assertEqual(e, e2)
        self.assertEqual(graph.number_of_hidden_edges(), 0)

        self.assertEqual(graph.number_of_edges(), 2)

        e1 = graph.edge_by_node(1, 2)
        e2 = graph.edge_by_node(4, 5)
        graph.hide_edge(e1)
        graph.hide_edge(e2)

        self.assertEqual(graph.number_of_edges(), 0)
        graph.restore_all_edges()
        self.assertEqual(graph.number_of_edges(), 2)

        self.assertEqual(graph.edge_by_id(e1), (1,2))
        self.assertRaises(GraphError, graph.edge_by_id, (e1+1)*(e2+1)+1)

        self.assertEquals(list(sorted(graph.edge_list())), [e1, e2])
        
        self.assertEqual(graph.describe_edge(e1), (e1, 1, 1, 2))
        self.assertEqual(graph.describe_edge(e2), (e2, 'a', 4, 5))

        self.assertEqual(graph.edge_data(e1), 1)
        self.assertEqual(graph.edge_data(e2), 'a')

        self.assertEqual(graph.head(e2), 4)
        self.assertEqual(graph.tail(e2), 5)

        graph.add_edge(1, 3)
        graph.add_edge(1, 5)
        graph.add_edge(4, 1)

        self.assertEqual(list(sorted(graph.out_nbrs(1))), [2, 3, 5])
        self.assertEqual(list(sorted(graph.inc_nbrs(1))), [4])
        self.assertEqual(list(sorted(graph.inc_nbrs(5))), [1, 4])
        self.assertEqual(list(sorted(graph.all_nbrs(1))), [2, 3, 4, 5])

        graph.add_edge(5, 1)
        self.assertEqual(list(sorted(graph.all_nbrs(5))), [1, 4])

        self.assertEquals(graph.out_degree(1), 3)
        self.assertEquals(graph.inc_degree(2), 1)
        self.assertEquals(graph.inc_degree(5), 2)
        self.assertEquals(graph.all_degree(5), 3)

        v = graph.out_edges(4)
        self.assertTrue(isinstance(v, list))
        self.assertEqual(graph.edge_by_id(v[0]), (4, 5))

        v = graph.out_edges(1)
        for e in v:
            self.assertEqual(graph.edge_by_id(e)[0], 1)

        v = graph.inc_edges(1)
        self.assertTrue(isinstance(v, list))
        self.assertEqual(graph.edge_by_id(v[0]), (4, 1))

        v = graph.inc_edges(5)
        for e in v:
            self.assertEqual(graph.edge_by_id(e)[1], 5)

        v = graph.all_edges(5)
        for e in v:
            self.assertTrue(graph.edge_by_id(e)[1] == 5 or graph.edge_by_id(e)[0] == 5)

        e1 = graph.edge_by_node(1, 2)
        self.assertTrue(isinstance(e1, int))
        graph.hide_node(1)
        self.assertRaises(GraphError, graph.edge_by_node, 1, 2)
        graph.restore_node(1)
        e2 = graph.edge_by_node(1, 2)
        self.assertEqual(e1, e2)



    @unittest.expectedFailure
    def test_toposort(self):
        graph = Graph()
        self.fail("add tests for forw_topo_sort and back_topo_sort")

    @unittest.expectedFailure
    def test_bfs_subgraph(self):
        self.fail("add tests for forw_bfs_subgraph and back_bfs_subgraph")

    @unittest.expectedFailure
    def test_iterdfs(self):
        self.fail("add tests for iterdfs")

    @unittest.expectedFailure
    def test_iterdata(self):
        self.fail("add tests for iterdata")

    @unittest.expectedFailure
    def test_bfs(self):
        self.fail("add tests for forw_bfs and back_bfs")

    @unittest.expectedFailure
    def test_dfs(self):
        self.fail("add tests for forw_dfs and back_dfs")

    def test_connected(self):
        graph = Graph()
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)

        self.assertFalse(graph.connected())

        graph.add_edge(1, 2)
        graph.add_edge(3, 4)
        self.assertFalse(graph.connected())

        graph.add_edge(2, 3)
        graph.add_edge(4, 1)
        self.assertTrue(graph.connected())

    @unittest.expectedFailure
    def test_clust_coef(self):
        self.fail("add tests for clust_coef")

    @unittest.expectedFailure
    def test_get_hops(self):
        self.fail("add tests for get_hops")


    @unittest.expectedFailure
    def test_constructor(self):
        self.fail("add test for Graph()")


if __name__ == "__main__":
    unittest.main()
