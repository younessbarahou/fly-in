from typing import List


class Drone:
    def __init__(self) -> None:
        self.id: str = ""
        self.arrived: bool = False
        self.path: List[str] = []
        self.turns: int = 0


class Hub:
    def __init__(
            self, name: str,
            x: int,
            y: int,
            zone: str,
            color: str,
            max_drones: float
    ) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone: str = zone
        self.color: str = color
        self.max_drones: float = max_drones
        self.drones: List[Drone] = []
        self.neighbors: List[Hub] = []
        self.visited: bool = False
        self.cost: int = 1.5
        if self.zone == 'restricted':
            self.cost = 2
        elif self.zone == 'priority':
            self.cost = 1
