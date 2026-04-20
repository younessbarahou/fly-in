from parsing import DataBase
from typing import Dict, List
from meta.hub import Hub
from meta.start_hub import StartHub
from random import choice


class ReachableError(Exception):
    pass


class Graph:
    def __init__(self, data: DataBase) -> None:
        self.data = data
        self.graph: Dict[str, Hub] = data.hubs
        self.graph.update({data.start_hub.name: data.start_hub})
        self.graph.update({data.end_hub.name: data.end_hub})
        for c in data.connections:
            if c.hub_1.zone == 'blocked' or c.hub_2.zone == 'blocked':
                continue
            self.graph[c.hub_1.name].neighbors.update({c.hub_2.name: c.hub_2})
            self.graph[c.hub_2.name].neighbors.update({c.hub_1.name: c.hub_1})

    def validate(self) -> None:
        temp_stack: List[Hub] = []
        for g in self.graph:
            if type(self.graph[g]) is StartHub:
                temp_stack.append(self.graph[g])
        temp_stack[-1].visited_dfs = True
        while len(temp_stack) > 0:
            unvisited_neighbors: List[Hub] = [
                n for n in temp_stack[-1].neighbors.values()
                if n.visited_dfs is False
            ]
            if len(unvisited_neighbors) == 0:
                temp_stack.pop()
            else:
                choice_result = choice(unvisited_neighbors)
                temp_stack.append(choice_result)
                choice_result.visited_dfs = True
                if choice_result == self.data.end_hub:
                    break
        if self.data.end_hub.visited_dfs is False:
            raise ReachableError("Graph's end zone is not reached at all !")

    def get_graph(self) -> Dict[str, Hub]:
        return self.graph
