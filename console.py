from dijkstra.command import Command
from dijkstra.DijkstraNlogN import DijkstraNlogN

class Console:
    dijk = DijkstraNlogN()

    @staticmethod
    def show_router_list_info(node_name_list):
        for node_name in node_name_list:
            Console.show_router_info(node_name)

    @staticmethod
    def show_router_info(node_name):
        neighbors = Console.dijk.get_neighbors(node_name)
        neighbors = sorted(neighbors, key=lambda tup: tup[1])
        lsdb = Console.dijk.get_LSDB(node_name)
        lsdb = sorted(lsdb, key=lambda tup: tup[0].name + tup[1].name)
        routing_table = Console.dijk.get_routing_table(node_name)
        routing_table = sorted(routing_table, key=lambda tup: tup[0].name + tup[1].name)
        print(f"{node_name} Neighbour Table:")
        for neighbor_tup in neighbors:
            print(f"{neighbor_tup[1].name},{neighbor_tup[0]}")
        print()
        print(f"{node_name} LSDB:")
        for path_tup in lsdb:
            print(f"{path_tup[0].name},{path_tup[1].name},{path_tup[2]}")
        print()
        print(f"{node_name} Routing Table:")
        for path_tup in routing_table:
            print(f"{path_tup[0].name},{path_tup[1].name},{path_tup[2]}")
        print()

    @staticmethod
    @Command(str, call_back=None, end_flag="LINKSTATE")
    def add_nodes(name: str):
        Console.dijk.graph.add_nodes(name)

    @staticmethod
    @Command(
        str,
        str,
        int,
        Command.comma_sep_list,
        call_back=show_router_list_info,
        end_flag="UPDATE",
    )
    def add_edges(node_a_name, node_b_name, weight, optional_info=[]):
        Console.dijk.graph.create_edge(node_a_name, node_b_name, weight)
        return optional_info

    @staticmethod
    @Command(
        str,
        str,
        int,
        Command.comma_sep_list,
        call_back=show_router_list_info,
        end_flag="END",
    )
    def update_edges(node_a_name, node_b_name, weight, optional_info=[]):
        Console.dijk.graph.update_edge(node_a_name, node_b_name, weight)
        return optional_info


if __name__ == "__main__":
    Console.add_nodes()
    Console.add_edges()
    Console.update_edges()
