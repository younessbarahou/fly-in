from typing import List  


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
        self.neighbors: List[Hub] = []
        self.visited: bool = False
        self.cost: int = 1
        if self.zone == 'restricted':
            self.cost = 2
