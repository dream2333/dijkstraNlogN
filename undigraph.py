#!/usr/bin/env python3

class UndiGraph:
    nodes = {}

    # init or add nodes
    def __init__(self, *nodes_name):
        self.add_nodes(*nodes_name)

    def add_nodes(self, *nodes_name):
        for name in nodes_name:
            # Create node if node non-existent
            self.nodes[name] = self.Node(name)

    # set relation between two nodes
    def create_edge(self, node_a_name, node_b_name, weight):
        node_a = self.nodes[node_a_name]
        node_b = self.nodes[node_b_name]
        node_a.set_edge(node_b, weight)

    def update_edge(self, node_a_name, node_b_name, weight):
        if weight == -1:
            self.delete_edge(node_a_name, node_b_name)
            return
        node_name_list = self.nodes.keys()
        # If the corresponding node does not exist, create a new node
        if node_a_name not in node_name_list:
            self.add_nodes(node_a_name)
        if node_b_name not in node_name_list:
            self.add_nodes(node_b_name)
        # If the length of the edge is set to -1, the link between the two nodes will be deleted.
        node_a = self.nodes[node_a_name]
        node_b = self.nodes[node_b_name]
        node_a.update_edge(node_b, weight)

    def delete_edge(self, node_a_name, node_b_name):
        node_a = self.nodes[node_a_name]
        node_b = self.nodes[node_b_name]
        node_a.del_edge(node_b)

    # Iterate over all edges and use set for removing duplicate edges, with time complexity of O(E) for directed graphs and O(2*E) for undirected graphs
    def get_all_edge(self):
        edge_collections = set()
        for start_node in self.nodes.values():
            for weight, end_node in start_node.neighbors:
                # Reconstruct the representation of edges of the undirected graph in alphabetical order make sure all path tuple are the same for de-duplication
                if start_node > end_node:
                    edge_collections.add((end_node, start_node, weight))
                else:
                    edge_collections.add((start_node, end_node, weight))

        return edge_collections

    # More friendly console output
    def __repr__(self):
        return str(list(self.nodes.values()))

    # To make the graph structure easier to understand, use inner class to define nodes
    class Node:
        def __init__(self, name, link_node=None, link_weight=None):
            self.neighbors = []
            self.name = name
            # Automatic sorting using priority queues
            if link_node != None:
                self.neighbors.append((link_weight, link_node))

        def set_edge(self, other_node, weight):
            self.neighbors.append((weight, other_node))
            other_node.neighbors.append((weight, self))

        def update_edge(self, other_node, weight):
            for index, neigh_tuple in enumerate(self.neighbors):
                if other_node == neigh_tuple[1]:
                    self.neighbors[index] = (weight, neigh_tuple[1])
                    break
            for index, neigh_tuple in enumerate(other_node.neighbors):
                if self == neigh_tuple[1]:
                    other_node.neighbors[index] = (weight, neigh_tuple[1])
                    break

        def del_edge(self, other_node):
            for index, neigh_tuple in enumerate(self.neighbors):
                if other_node == neigh_tuple[1]:
                    del self.neighbors[index]
                    break
            for index, neigh_tuple in enumerate(other_node.neighbors):
                if self == neigh_tuple[1]:
                    del other_node.neighbors[index]
                    break

        def __repr__(self):
            # return f"<Node {self.name} with {len(self.neighbors)} neighbors>"
            return f"<Node {self.name}>"

        # Override the __hash__() and __eq__() to remove duplicate Node objects in set
        def __hash__(self):
            # If two node has same name, they should be treated as the same node
            return hash(self.name)

        def __eq__(self, other):
            return self.name == other.name

        def __gt__(self, other):
            if self.name > other.name:
                return True
            else:
                return False

    def __getitem__(self, key) -> Node:
        return self.nodes[key]


# test
if __name__ == "__main__":
    g = UndiGraph()
    print(g)
    g = UndiGraph("X", "Y", "Z", "A")
    g.create_edge("X", "Z", 7)
    g.create_edge("X", "Y", 2)
    g.create_edge("Y", "Z", 1)
    g.delete_edge("X", "Y")
    print(g)
