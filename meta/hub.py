from typing import Dict
from typing import Optional


class Hub:
    def __init__(
            self, name: str,
            x: int,
            y: int,
            zone: str,
            color: str,
            max_drones: int
    ) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone: str = zone
        self.color: str = color
        self.max_drones: int = max_drones
        self.neighbors: Dict[str, Hub] = {}
        self.visited_dfs: bool = False
        self.visited_djikstra: bool = False
        self.precedent: Optional[Hub] = None
        self.cost: float = 1.5
        self.total_cost: float = float('inf')
        if self.zone == 'priority':
            self.cost = 1
        elif self.zone == 'restricted':
            self.cost = 2
