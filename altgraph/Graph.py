"""
altgraph.Graph - Base Graph class
=================================

.. 
  #--Version 2.1
  #--Bob Ippolito October, 2004

  #--Version 2.0
  #--Istvan Albert June, 2004

  #--Version 1.0
  #--Nathan Denny, May 27, 1999
"""

from altgraph import GraphError
from collections import deque

class Graph(object):
    """
    The Graph class represents a directed graph with *N* nodes and *E* edges.

    Naming conventions:

    - the prefixes such as *out*, *inc* and *all* will refer to methods
      that operate on the outgoing, incoming or all edges of that node.

      For example: :py:meth:`inc_degree` will refer to the degree of the node
      computed over the incoming edges (the number of neighbours linking to
      the node).

    - the prefixes such as *forw* and *back* will refer to the
      orientation of the edges used in the method with respect to the node.

      For example: :py:meth:`forw_bfs` will start at the node then use the outgoing
      edges to traverse the graph (goes forward).
    """

    def __init__(self, edges=None):
        """
        Initialization
        """

        self.next_edge = 0
        self.nodes, self.edges = {}, {}
        self.hidden_edges, self.hidden_nodes = {}, {}

        try:
            # instantiate graph from iterable data
            if edges:
                cols = len(edges[0])
                if cols == 2:
                    for head, tail in edges:
                        self.add_edge(head, tail)
                elif cols == 3:
                    for head, tail, data in edges:
                        self.add_edge(head, tail, data)
        except Exception, exc:
            raise GraphError('%s -> Cannot create graph from edges=%s' %
                (exc, edges))

    def __repr__(self):
        return '<Graph: %d nodes, %d edges>' % (
            self.number_of_nodes(), self.number_of_edges())

    def add_node(self, node, node_data=None):
        """
        Creates a new node with a node.  Arbitrary data can be attached to the
        node via the node_data parameter.  Adding the same node twice will be
        silently ignored.

        The node must be a hashable value.
        """
        #
        # the nodes will contain tuples that will store incoming edges,
        # outgoing edges and data
        #
        # index 0 -> incoming edges
        # index 1 -> outgoing edges
        if node not in self.nodes:
            self.nodes[node] = ([], [], node_data)

    def add_edge(self, head_id, tail_id, edge_data=1, create_nodes=True):
        """
        Adds a directed edge going from head_id to tail_id.
        Arbitrary data can be attached to the edge via edge_data.
        It may create the nodes if adding edges between nonexisting ones.

        :param head_id: head node
        :param tail_id: tail node
        :param edge_data: (optional) data attached to the edge
        :param create_nodes: (optional) creates the head_id or tail_id node in case they did not exist
        """
        # shorcut
        edge = self.next_edge

        # add nodes if on automatic node creation
        if create_nodes:
            self.add_node(head_id)
            self.add_node(tail_id)

        # store edge information
        self.edges[edge] = (head_id, tail_id, edge_data)

        # update the corresponding incoming and outgoing lists in the nodes
        # index 0 -> incoming edges
        # index 1 -> outgoing edges

        try:
            self.nodes[tail_id][0].append(edge)
            self.nodes[head_id][1].append(edge)
        except KeyError:
            raise GraphError('Invalid nodes %s -> %s' % (head_id, tail_id))

        self.next_edge += 1

    def hide_edge(self, edge):
        """
        Hides an edge from the graph. The edge may be unhidden at some later
        time.
        """
        try:
            head_id, tail_id, edge_data = self.hidden_edges[edge] = self.edges[edge]
            self.nodes[tail_id][0].remove(edge)
            self.nodes[head_id][1].remove(edge)
            del self.edges[edge]
        except KeyError:
            raise GraphError('Invalid edge %s' % edge)

    def hide_node(self, node):
        """
        Hides a node from the graph.  The incoming and outgoing edges of the
        node will also be hidden.  The node may be unhidden at some later time.
        """
        try:
            all_edges = self.all_edges(node)
            self.hidden_nodes[node] = (self.nodes[node], all_edges)
            for edge in all_edges:
                self.hide_edge(edge)
            del self.nodes[node]
        except KeyError:
            raise GraphError('Invalid node %s' % node)

    def restore_node(self, node):
        """
        Restores a previously hidden node back into the graph and restores
        all of its incoming and outgoing edges.
        """
        try:
            self.nodes[node], all_edges = self.hidden_nodes[node]
            for edge in all_edges:
                self.restore_edge(edge)
            del self.hidden_nodes[node]
        except KeyError:
            raise GraphError('Invalid node %s' % node)

    def restore_edge(self, edge):
        """
        Restores a previously hidden edge back into the graph.
        """
        try:
            self.edges[edge] = head_id, tail_id, data = self.hidden_edges[edge]
            self.nodes[tail_id][0].append(edge)
            self.nodes[head_id][1].append(edge)
            del self.hidden_edges[edge]
        except KeyError:
            raise GraphError('Invalid edge %s' % edge)

    def restore_all_edges(self):
        """
        Restores all hidden edges.
        """
        for edge in self.hidden_edges.keys():
            self.restore_edge(edge)

    def restore_all_nodes(self):
        """
        Restores all hidden nodes.
        """
        for node in self.hidden_nodes.keys():
            self.restore_node(node)

    def __contains__(self, node):
        """
        Test whether a node is in the graph
        """
        return node in self.nodes

    def edge_by_id(self, edge):
        """
        Returns the edge that connects the head_id and tail_id nodes
        """
        try:
            head, tail, data =  self.edges[edge]
        except KeyError:
            head, tail = None, None
            raise GraphError('Invalid edge %s' % edge)

        return (head, tail)

    def edge_by_node(self, head, tail):
        """
        Returns the edge that connects the head_id and tail_id nodes
        """
        for edge in self.out_edges(head):
            if self.tail(edge) == tail:
                return edge
        return None

    def number_of_nodes(self):
        """
        Returns the number of nodes
        """
        return len(self.nodes)

    def number_of_edges(self):
        """
        Returns the number of edges
        """
        return len(self.edges)

    def __iter__(self):
        """
        Iterates over all nodes in the graph
        """
        return iter(self.nodes)

    def node_list(self):
        """
        Return a list of the node ids for all visible nodes in the graph.
        """
        return self.nodes.keys()

    def edge_list(self):
        """
        Returns an iterator for all visible nodes in the graph.
        """
        return self.edges.keys()

    def number_of_hidden_edges(self):
        """
        Returns the number of hidden edges
        """
        return len(self.hidden_edges)

    def number_of_hidden_nodes(self):
        """
        Returns the number of hidden nodes
        """
        return len(self.hidden_nodes)

    def hidden_node_list(self):
        """
        Returns the list with the hidden nodes
        """
        return self.hidden_nodes.keys()

    def hidden_edge_list(self):
        """
        Returns a list with the hidden edges
        """
        return self.hidden_edges.keys()

    def describe_node(self, node):
        """
        return node, node data, outgoing edges, incoming edges for node
        """
        incoming, outgoing, data = self.nodes[node]
        return node, data, outgoing, incoming

    def describe_edge(self, edge):
        """
        return edge, edge data, head, tail for edge
        """
        head, tail, data = self.edges[edge]
        return edge, data, head, tail

    def node_data(self, node):
        """
        Returns the data associated with a node
        """
        return self.nodes[node][2]

    def edge_data(self, edge):
        """
        Returns the data associated with an edge
        """
        return self.edges[edge][2]

    def head(self, edge):
        """
        Returns the node of the head of the edge.
        """
        return self.edges[edge][0]

    def tail(self, edge):
        """
        Returns node of the tail of the edge.
        """
        return self.edges[edge][1]

    def out_nbrs(self, node):
        """
        List of nodes connected by outgoing edges
        """
        return map(self.tail, self.out_edges(node))

    def inc_nbrs(self, node):
        """
        List of nodes connected by incoming edges
        """
        return map(self.head, self.inc_edges(node))

    def all_nbrs(self, node):
        """
        List of nodes connected by incoming and outgoing edges
        """
        return self.inc_nbrs(node) + self.out_nbrs(node)

    def out_edges(self, node):
        """
        Returns a list of the outgoing edges
        """
        try:
            return list(self.nodes[node][1])
        except KeyError:
            raise GraphError('Invalid node %s' % node)

        return None

    def inc_edges(self, node):
        """
        Returns a list of the incoming edges
        """
        try:
            return list(self.nodes[node][0])
        except KeyError:
            raise GraphError('Invalid node %s' % node)

        return None

    def all_edges(self, node):
        """
        Returns a list of incoming and outging edges.
        """
        return set(self.inc_edges(node) + self.out_edges(node))

    def out_degree(self, node):
        """
        Returns the number of outgoing edges
        """
        return len(self.out_edges(node))

    def inc_degree(self, node):
        """
        Returns the number of incoming edges
        """
        return len(self.inc_edges(node))

    def all_degree(self, node):
        """
        The total degree of a node
        """
        return self.inc_degree(node) + self.out_degree(node)

    def _topo_sort(self, forward=True):
        """
        Topological sort.

        Returns a list of nodes where the successors (based on outgoing and
        incoming edges selected by the forward parameter) of any given node
        appear in the sequence after that node.
        """
        topo_list = []
        queue = deque()
        indeg = {}

        # select the operation that will be performed
        if forward:
            get_edges = self.out_edges
            get_degree = self.inc_degree
        else:
            get_edges = self.inc_edges
            get_degree = self.out_degree

        for node in self.node_list():
            degree = get_degree(node)
            if degree:
                indeg[node] = degree
            else:
                queue.append(node)

        while queue:
            curr_node = queue.popleft()
            topo_list.append(curr_node)
            for edge in get_edges(curr_node):
                tail_id = self.tail(edge)
                indeg[tail_id] -= 1
                if indeg[tail_id] == 0:
                    queue.append(tail_id)

        if len(topo_list) == len(self.node_list()):
            valid = True
        else:
            # the graph has cycles, invalid topological sort
            valid = False

        return (valid, topo_list)

    def forw_topo_sort(self):
        """
        Topological sort.

        Returns a list of nodes where the successors (based on outgoing edges)
        of any given node appear in the sequence after that node.
        """
        return self._topo_sort(forward=True)

    def back_topo_sort(self):
        """
        Reverse topological sort.

        Returns a list of nodes where the successors (based on incoming edges)
        of any given node appear in the sequence after that node.
        """
        return self._topo_sort(forward=False)

    def _bfs_subgraph(self, start_id, forward=True):
        """
        Private method creates a subgraph in a bfs order.

        The forward parameter specifies whether it is a forward or backward
        traversal.
        """
        if forward:
            get_bfs  = self.forw_bfs
            get_nbrs = self.out_nbrs
        else:
            get_bfs  = self.back_bfs
            get_nbrs = self.inc_nbrs

        g = Graph()
        bfs_list = get_bfs(start_id)
        for (hop_num, node) in bfs_list:
            g.add_node(node)

        for (hop_num, node) in bfs_list:
            for nbr_id in get_nbrs(node):
                g.add_edge(node, nbr_id)

        return g

    def forw_bfs_subgraph(self, start_id):
        """
        Creates and returns a subgraph consisting of the breadth first
        reachable nodes based on their outgoing edges.
        """
        return self._bfs_subgraph(start_id, forward=True)

    def back_bfs_subgraph(self, start_id):
        """
        Creates and returns a subgraph consisting of the breadth first
        reachable nodes based on the incoming edges.
        """
        return self._bfs_subgraph(start_id, forward=True)

    def iterdfs(self, start, end=None, forward=True):
        """
        Collecting nodes in some depth first traversal.

        The forward parameter specifies whether it is a forward or backward
        traversal.
        """
        visited, stack = set([start]), deque([start])

        if forward:
            get_edges = self.out_edges
        else:
            get_edges = self.inc_edges

        while stack:
            curr_node = stack.pop()
            yield curr_node
            if curr_node == end:
                break
            for edge in get_edges(curr_node):
                tail = self.tail(edge)
                if tail not in visited:
                    visited.add(tail)
                    stack.append(tail)

    def iterdata(self, start, end=None, forward=True, condition=None):
        visited, stack = set([start]), deque([start])

        if forward:
            get_edges = self.out_edges
        else:
            get_edges = self.inc_edges

        get_data = self.node_data

        while stack:
            curr_node = stack.pop()
            curr_data = get_data(curr_node)
            if curr_data is not None:
                if condition is not None and not condition(curr_data):
                    continue
                yield curr_data
            if curr_node == end:
                break
            for edge in get_edges(curr_node):
                tail = self.tail(edge)
                if tail not in visited:
                    visited.add(tail)
                    stack.append(tail)

    def _dfs(self, start, end=None, forward=True):
        return list(self.iterdfs(start, end=end, forward=forward))

    def _iterbfs(self, start, end=None, forward=True):
        """
        Private method, collecting nodes in some breadth first traversal.

        The forward parameter specifies whether it is a forward or backward
        traversal.  Returns a list of tuples where the first value is the hop
        value the second value is the node id.
        """
        queue, visited = deque([(start, 0)]), set([start])

        # the direction of the bfs depends on the edges that are sampled
        if forward:
            get_edges = self.out_edges
        else:
            get_edges = self.inc_edges

        while queue:
            curr_node, curr_step = queue.popleft()
            yield (curr_node, curr_step)
            if curr_node == end:
                break
            for edge in get_edges(curr_node):
                tail = self.tail(edge)
                if tail not in visited:
                    visited.add(tail)
                    queue.append((tail, curr_step + 1))

    def _bfs(self, start, end=None, forward=True):
        return list(self._iterbfs(start, end=end, forward=forward))

    def forw_bfs(self, start, end=None):
        """
        Returns a list of nodes in some forward BFS order.

        Starting from the start node the breadth first search proceeds along
        outgoing edges.
        """
        return [node for node, step in self._bfs(start, end, forward=True)]

    def back_bfs(self, start, end=None):
        """
        Returns a list of nodes in some backward BFS order.

        Starting from the start node the breadth first search proceeds along
        incoming edges.
        """
        return [node for node, step in self._bfs(start, end, forward=False)]

    def forw_dfs(self, start, end=None):
        """
        Returns a list of nodes in some forward DFS order.

        Starting with the start node the depth first search proceeds along
        outgoing edges.
        """
        return self._dfs(start, end, forward=True)

    def back_dfs(self, start, end=None):
        """
        Returns a list of nodes in some backward DFS order.

        Starting from the start node the depth first search proceeds along
        incoming edges.
        """
        return self._dfs(start, end, forward=False)

    def connected(self):
        """
        Returns :py:data:`True` if the graph's every node can be reached from every
        other node.
        """
        node_list = self.node_list()
        for node in node_list:
            bfs_list = self.forw_bfs(node)
            if len(bfs_list) != len(node_list):
                return False
        return True

    def clust_coef(self, node):
        """
        Computes and returns the local clustering coefficient of node. 

        See <http://en.wikipedia.org/wiki/Clustering_coefficient#Local_clustering_coefficient>
        for a definition.
        """
        num = 0
        nbr_set = set(self.out_nbrs(node))
        nbr_set.remove(node) # loop defense

        for nbr in nbr_set:
            sec_set = set(self.out_nbrs(nbr))
            sec_set.remove(nbr) # loop defense
            num += len(nbr_set & sec_set)

        nbr_num = len(nbr_set)
        if nbr_num:
            clust_coef = float(num) / (nbr_num * (nbr_num - 1))
        else:
            clust_coef = 0.0
        return clust_coef

    def get_hops(self, start, end=None, forward=True):
        """
        Computes the hop distance to all nodes centered around a specified node.

        First order neighbours are at hop 1, their neigbours are at hop 2 etc.
        Uses :py:meth:`forw_bfs` or :py:meth:`back_bfs` depending on the value of the forward
        parameter.  If the distance between all neighbouring nodes is 1 the hop
        number corresponds to the shortest distance between the nodes.

        :param start: the starting node
        :param end: ending node (optional). When not specified will search the whole graph.
        :param forward: directionality parameter (optional). If C{True} (default) it uses L{forw_bfs} otherwise L{back_bfs}.
        :return: returns a list of tuples where each tuple contains the node and the hop.

        Typical usage::

            >>> print graph.get_hops(1, 8)
            >>> [(1, 0), (2, 1), (3, 1), (4, 2), (5, 3), (7, 4), (8, 5)]
            # node 1 is at 0 hops
            # node 2 is at 1 hop
            # ...
            # node 8 is at 5 hops
        """
        if forward:
            return self._bfs(start=start, end=end, forward=True)
        else:
            return self._bfs(start=start, end=end, forward=False)
