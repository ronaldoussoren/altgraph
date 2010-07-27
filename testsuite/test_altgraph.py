#!/usr/bin/env py.test
import os
import sys

from altgraph import Graph, GraphAlgo
import unittest

import altgraph.compat 

class BasicTests (unittest.TestCase):
    def test_altgraph(self):

        # these are the edges
        edges = [ (1,2), (2,4), (1,3), (2,4), (3,4), (4,5), (6,5), (6,14), (14,15), (6, 15),
        (5,7), (7, 8), (7,13), (12,8), (8,13), (11,12), (11,9), (13,11), (9,13), (13,10) ]

        store = {}
        g = Graph.Graph()
        for head, tail in edges:
            store[head] = store[tail] = None
            g.add_edge(head, tail)

        # check the parameters
        self.assertEquals(g.number_of_nodes(), len(store))
        self.assertEquals(g.number_of_edges(), len(edges))


        # do a forward bfs
        self.assertEquals( g.forw_bfs(1), [1, 2, 3, 4, 5, 7, 8, 13, 11, 10, 12, 9])


        # diplay the hops and hop numbers between nodes
        self.assertEquals(g.get_hops(1, 8), [(1, 0), (2, 1), (3, 1), (4, 2), (5, 3), (7, 4), (8, 5)])

        self.assertEquals(GraphAlgo.shortest_path(g, 1, 12), [1, 2, 4, 5, 7, 13, 11, 12])

    def test_compat(self):
        self.assertEquals(list(altgraph.compat.ireversed([1,2,3])), [3,2,1])
        self.assertEquals("".join(altgraph.compat.ireversed("asd")), "dsa")


if __name__ == "__main__":
    unittest.main()
