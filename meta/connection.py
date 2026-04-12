class Connection:
    def __init__(
            self, name_1: str, name_2: str, max_link_capacity: int
    ) -> None:
        self.name_1 = name_1
        self.name_2 = name_2
        self.max_link_capacity = max_link_capacity
