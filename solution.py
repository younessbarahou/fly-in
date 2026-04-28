from typing import List
from meta.start_hub import StartHub
from meta.end_hub import EndHub
from meta.hub import Hub
from meta.path import Path
from meta.connection import Connection


class ReachableError(Exception):
    pass


class Solution:
    """ produces the solutions paths """
    @staticmethod
    def solve(
        start_hub: StartHub, end_hub: EndHub, connections: List[Connection]
    ) -> List[Path]:
        """ returns all possible paths using Dfs algorithm (recursive)"""
        result: List[Path] = []
        path: List[Hub] = []

        def dfs(node: Hub, path: List[Hub]) -> None:
            path.append(node)
            if node is end_hub:
                result.append(Path(path.copy()))
                path.pop()
                return
            for n in node.neighbors:
                if n not in path:
                    dfs(n, path)
            path.pop()
        dfs(start_hub, path)
        if len(result) == 0:
            raise ReachableError(
                "Start zone and End Zone are isolated from each other !")
        # We sort The paths based on the total cost
        result = sorted(result, key=lambda x: x.total_cost)
        # we then label each path with its lowest drones capacity in zones
        for r in result:
            r.max_drones_number = min(r.nodes, key=lambda x: x.max_drones).cost
        # we label each path with its lowest connection capacity
        for r in result:
            index: int = 0
            connection_max: List[int] = []
            while index < len(r.nodes) - 1:
                for c in connections:
                    if (
                        (r.nodes[index].name == c.hub_1.name and r.nodes[
                            index + 1].name == c.hub_2.name)
                        or
                        (r.nodes[index].name == c.hub_2.name and r.nodes[
                            index + 1].name == c.hub_1.name)
                    ):
                        connection_max.append(c.max_link_capacity)
                index += 1
            r.max_connection_capacity = min(connection_max)
        return result
