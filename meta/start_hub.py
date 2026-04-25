from meta.hub import Hub


class StartHub(Hub):
    def __init__(
            self, name: str,
            x: int,
            y: int,
            zone: str,
            color: str,
            max_drones: int
    ) -> None:
        super().__init__(name, x, y, zone, color, max_drones)
        self.cost = 0
        self.max_drones = float('inf')
