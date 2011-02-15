import unittest
from altgraph import GraphUtil
from altgraph import Graph


class TestGraphUtil (unittest.TestCase):

    def test_generate_random(self):
        g =  GraphUtil.generate_random_graph(10, 50)
        self.assertEquals(g.number_of_nodes(), 10)
        self.assertEquals(g.number_of_edges(), 50)

        seen = set()

        for e in g.edge_list():
            h, t = g.edge_by_id(e)
            self.assertFalse(h == t)
            self.assertTrue((h, t) not in seen)
            seen.add((h, t))

        g =  GraphUtil.generate_random_graph(5, 30, multi_edges=True)
        self.assertEquals(g.number_of_nodes(), 5)
        self.assertEquals(g.number_of_edges(), 30)

        seen = set()

        for e in g.edge_list():
            h, t = g.edge_by_id(e)
            self.assertFalse(h == t)
            if (h, t) in seen:
                break
            seen.add((h, t))

        else:
            self.fail("no duplicates?")

        g =  GraphUtil.generate_random_graph(5, 21, self_loops=True)
        self.assertEquals(g.number_of_nodes(), 5)
        self.assertEquals(g.number_of_edges(), 21)

        seen = set()

        for e in g.edge_list():
            h, t = g.edge_by_id(e)
            self.assertFalse((h, t) in seen)
            if h == t:
                break
            seen.add((h, t))

        else:
            self.fail("no self loops?")

    @unittest.expectedFailure
    def test_generate_scale_free(self):
        self.fail("missing tests for GraphUtil.generate_scale_free_graph")

    def test_filter_stack(self):
        g = Graph.Graph()
        g.add_node("1", "N.1")
        g.add_node("1.1", "N.1.1")
        g.add_node("1.1.1", "N.1.1.1")
        g.add_node("1.1.2", "N.1.1.2")
        g.add_node("1.1.3", "N.1.1.3")
        g.add_node("1.1.1.1", "N.1.1.1.1")
        g.add_node("1.1.1.2", "N.1.1.1.2")
        g.add_node("1.1.2.1", "N.1.1.2.1")
        g.add_node("1.1.2.2", "N.1.1.2.2")
        g.add_node("1.1.2.3", "N.1.1.2.3")
        g.add_node("2", "N.2")

        g.add_edge("1", "1.1")
        g.add_edge("1.1", "1.1.1")
        g.add_edge("1.1", "1.1.2")
        g.add_edge("1.1", "1.1.3")
        g.add_edge("1.1.1", "1.1.1.1")
        g.add_edge("1.1.1", "1.1.1.2")
        g.add_edge("1.1.2", "1.1.2.1")
        g.add_edge("1.1.2", "1.1.2.2")
        g.add_edge("1.1.2", "1.1.2.3")

        v, r, o =  GraphUtil.filter_stack(g, "1", [
            lambda n: n != "N.1.1.1", lambda n: n != "N.1.1.2.3" ])

        self.assertEqual(v,
            set(["1", "1.1", "1.1.1", "1.1.2", "1.1.3",
                "1.1.1.1", "1.1.1.2", "1.1.2.1", "1.1.2.2",
                "1.1.2.3"]))
        self.assertEqual(r, set([
                "1.1.1", "1.1.2.3"]))

        self.assertEqual(o,
            [
                ("1.1", "1.1.1.1"), 
                ("1.1", "1.1.1.2")
            ])

        v, r, o =  GraphUtil.filter_stack(g, "1", [
            lambda n: n != "N.1.1.1", lambda n: n != "N.1.1.1.2" ])

        self.assertEqual(v,
            set(["1", "1.1", "1.1.1", "1.1.2", "1.1.3",
                "1.1.1.1", "1.1.1.2", "1.1.2.1", "1.1.2.2",
                "1.1.2.3"]))
        self.assertEqual(r, set([
                "1.1.1", "1.1.1.2"]))

        self.assertEqual(o,
            [
                ("1.1", "1.1.1.1"), 
            ])


if __name__ == "__main__": # pragma: no cover
    unittest.main()
