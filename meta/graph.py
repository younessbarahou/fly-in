from parsing import DataBase
from typing import Dict
from meta.hub import Hub


class GraphBuilder:
    """ """
    def __init__(self, data: DataBase) -> None:
        self.data = data
        self.graph: Dict[str, Hub] = self.data.hubs
    
    def setup(self) -> None:
        """ """
        self.graph.update({self.data.start_hub.name: self.data.start_hub})
        self.graph.update({self.data.end_hub.name: self.data.end_hub})
        for c in self.data.connections:
            if c.hub_1.zone == 'blocked' or c.hub_2.zone == 'blocked':
                continue
            self.graph[c.hub_1.name].neighbors.append(c.hub_2)
            self.graph[c.hub_2.name].neighbors.append(c.hub_1)
