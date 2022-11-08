from math import inf
from dijkstra.command import Command
from dijkstra.undigraph import UndiGraph
import heapq


class DijkstraN2:
    def __init__(self):
        self.graph = UndiGraph()
        self.path = []

    def caculate_path(
        self,
        start: str = "A",
    ):
        def find_min_node():
            min_node = min(node_dist,key=lambda x:node_dist[x])
            return (node_dist[min_node],self.graph[min_node])
        # Using hashmap to improve addressing speed
        node_dist = {}
        result_path = []
        for node_name in self.graph.nodes:
            node_dist[node_name] =inf
        # The first node is not involved in sorting and inserted directly
        node_dist[start] = 0
        while len(node_dist) > 0:
            # Select the nearest node in the path
            now_node_tuple = find_min_node()
            now_node = now_node_tuple[1]
            result_path.append(now_node_tuple)
            # If a node has found the shortest path, del the key
            del node_dist[now_node.name]
            now_edge = now_node_tuple[0]
            # Iterate over each neighboring node
            for neighbor in now_node.neighbors:
                next_node = neighbor[1]
                next_edge = now_edge + neighbor[0]
                # Use a min heap make sure the nearest node is always at the top of the heap
                if next_node.name in node_dist and next_edge < node_dist[next_node.name]:
                    node_dist[next_node.name] = next_edge
        self.path = result_path
        return result_path

    # Return all nodes and their weight as a list
    def get_neighbors(self, node_names):
        return self.graph[node_names].neighbors

    # Return the LSDB as a list
    def get_LSDB(self, node_names):
        if (len(self.graph[node_names].neighbors)) == 0:
            return []
        return self.graph.get_all_edge()

    # Return the routing table as a list
    def get_routing_table(self, node_name):
        path = self.caculate_path(node_name)
        result = []
        for dist, destination in path[1:]:
            result.append((destination, path[1][1], dist))
        return result
