from typing import List
from meta.hub import Hub


class Path:
    def __init__(self, nodes: List[Hub]) -> None:
        self.nodes = nodes
        self.max_connection_capacity: int = 0
        self.real_cost: int = sum([n.cost for n in nodes])
        self.total_cost: float = 0
        for node in nodes:
            if node.zone == 'priority':
                self.total_cost += 1
            elif node.zone == 'normal':
                self.total_cost += 1.5
            else:
                self.total_cost += 2
