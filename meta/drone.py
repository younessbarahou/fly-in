from meta.hub import Hub
from typing import List


class Drone:
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        self.path: List[Hub] = []
        self.buffer: str = ""
