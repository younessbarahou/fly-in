from meta.hub import Hub


class Connection:
    def __init__(
            self, hub_1: Hub, hub_2: Hub, max_link_capacity: int
    ) -> None:
        self.hub_1 = hub_1
        self.hub_2 = hub_2
        self.max_link_capacity = max_link_capacity
