from typing import List
from meta.hub import Hub
from meta.drone import Drone


class Path:
    def __init__(self, nodes: List[Hub]) -> None:
        self.nodes = nodes
        self.max_drones_number: int = 0
        self.max_connection_capacity: int = 0
        self.real_cost: int = sum([n.cost for n in nodes])
        self.total_cost: float = 0
        for n in nodes:
            if n.zone == 'priority':
                self.total_cost += 1
            elif n.zone == 'normal':
                self.total_cost += 1.5
            else:
                self.real_cost += 2
        self.decision: int = min(self.max_drones_number,
                                 self.max_connection_capacity)
        self.drones: List[Drone] = []
