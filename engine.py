from meta.path import Path
from meta.drone import Drone
from typing import List


class Engine:
    def __init__(self, paths: List[Path], drones: List[Drone]):
        self.paths = paths
        self.drones = drones

    def simulate(self) -> None:
        drones_for_each_voyage: int = sum([p.decision for p in self.paths])
        queue: List[Drone] = self.drones
        # trippin
        while queue:
            for p in self.paths:
                for _ in range(p.decision):
                    p.drones.append(queue[0])
                    queue.pop(0)
