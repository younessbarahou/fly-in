from parsing import DataBase
from typing import Dict
from meta.hub import Hub


class Graph:
    def __init__(self, data: DataBase) -> None:
        self.graph: Dict[str, Hub] = data.hubs
        self.graph.update({data.start_hub.name: data.start_hub})
        self.graph.update({data.end_hub.name: data.end_hub})
        for c in data.connections:
            self.graph[c.hub_1.name].neighbors.update({c.hub_2.name: c.hub_2})
            self.graph[c.hub_2.name].neighbors.update({c.hub_1.name: c.hub_1})

    def get_graph(self) -> Dict[str, Hub]:
        return self.graph
