from time import perf_counter
from utils import get_input_data, timing_decorator
from collections import defaultdict, deque
from functools import cache


class Dags():
    def __init__(self):
        self.network = set()
    
    def add_dag(self, dag):
        if any([d.startswith("t") for d in dag]):
            dag = self.normalize(tuple(dag))
            self.network.add(dag)

    @cache
    def normalize(self, dag):
        smallest = min(dag)
        dq = deque(dag)
        dq.rotate(-dag.index(smallest))

        dag2 = tuple(reversed(dag))
        steps = dag2.index(smallest)
        dq2 = deque(dag2)
        steps = dq2.index(smallest)
        dq2.rotate(-steps)

        dq_l = tuple(dq)
        dq2_l = tuple(dq2)
        return min(dq_l, dq2_l)

        


def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    network = defaultdict(list)
    all_nodes = set()
    for d in data:
        from_node, to_node = d.split("-")
        network[from_node].append(to_node)
        network[to_node].append(from_node)
        all_nodes.add(from_node)
        all_nodes.add(to_node)
    return network, all_nodes



dags = Dags()

def find_circuits(network, all_nodes, target_depth):

    def find_x_depth_circuit(network, start_node, path_so_far, target_depth, remaining_depth):
        current_node = path_so_far[-1]
        if remaining_depth == 0:
            if start_node in network[current_node]:
                dags.add_dag(path_so_far)
            return
        for next_node in network[current_node]:
            if next_node not in path_so_far:
                find_x_depth_circuit(network, start_node, path_so_far + [next_node], target_depth, remaining_depth-1)

    for node in all_nodes:
        find_x_depth_circuit(network, node, [node], target_depth-1, target_depth-1)

def find_fully_connected(network, all_nodes):
    


def main():
    data = get_input_data(2024, 23, sample=1)
    network, all_nodes = read_input(data)

    find_circuits(network, all_nodes,3)
    # find_circuits(network, ['aq'], 3)

    print(f'Part 1: {len(dags.network)}')
       


if __name__ == "__main__":
    main()
