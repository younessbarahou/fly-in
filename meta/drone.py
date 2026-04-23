from typing import List


class Drone:
    def __init__(self) -> None:
        self.arrived: bool = False
        self.path: List[str] = []
        self.turns: int = 0
