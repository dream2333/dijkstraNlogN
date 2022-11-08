
from math import inf
from dijkstra.command import Command
from dijkstra.undigraph import UndiGraph
import heapq


class DijkstraNlogN:

    def __init__(self):
        self.graph = UndiGraph()
        self.path = []

    def caculate_path(
        self,
        start: str = "A",
    ):
        # Using hashmap to improve addressing speed
        node_state = {}
        result_path = []
        # Using the heap to get the nearest node
        temp_heap = []
        for node_name in self.graph.nodes:
            node_state[node_name] = {"nearest": False, "dist": inf}
        # The first node is not involved in sorting and inserted directly
        heapq.heappush(temp_heap, (0, self.graph[start]))
        while len(temp_heap) > 0:
            # Select the nearest node in the path
            now_node_tuple = heapq.heappop(temp_heap)
            now_node = now_node_tuple[1]
            # If the node is duplicated, skip directly
            if node_state[now_node.name]["nearest"] == True:
                continue
            result_path.append(now_node_tuple)
            # If a node has found the shortest path, set its status to true
            node_state[now_node.name]["nearest"] = True
            now_edge = now_node_tuple[0]
            # Iterate over each neighboring node
            for neighbor in now_node.neighbors:
                next_node = neighbor[1]
                next_edge = now_edge + neighbor[0]
                # Use a min heap make sure the nearest node is always at the top of the heap
                if (
                    node_state[next_node.name]["nearest"] == False
                    and next_edge < node_state[next_node.name]["dist"]
                ):
                    node_state[next_node.name]["dist"] = next_edge
                    heapq.heappush(temp_heap, (next_edge, next_node))
        self.path = result_path
        return result_path

    # Return all nodes and their weight as a list
    def get_neighbors(self, node_names):
        return self.graph[node_names].neighbors

    # Return the LSDB as a list
    def get_LSDB(self, node_names):
        if (len(self.graph[node_names].neighbors))==0:
            return []
        return self.graph.get_all_edge()

    # Return the routing table as a list
    def get_routing_table(self, node_name):
        path = self.caculate_path(node_name)
        result = []
        for dist, destination in path[1:]:
            result.append((destination, path[1][1], dist))
        return result


def test_graph():
    # Generate test nodes
    graph = UndiGraph("X", "Y", "Z")
    graph.create_edge("X", "Z", 7)
    graph.create_edge("X", "Y", 2)
    graph.create_edge("Y", "Z", 1)
    graph.update_edge("Y", "Z", -1)
    graph.update_edge("X", "Z", 5)
    return graph


if __name__ == "__main__":
    dijk = DijkstraNlogN()
    dist = dijk.caculate_path(start="X")
    print(dist)
    neighbors = dijk.get_neighbors("X")
    print(neighbors)
