from meta.graph import Graph
from typing import Union, Dict, List
from meta.start_hub import StartHub
from meta.end_hub import EndHub
from meta.hub import Hub


class Solution:
    @staticmethod
    def solve(graph: Dict[str, Hub], start_hub: StartHub, end_hub: EndHub) -> None:
        current_node: Hub = start_hub
        start_hub.visited_djikstra = True
        queue: List[Hub] = [
            c for c in start_hub.neighbors.values()
            if not c.visited_djikstra
        ]
        queue = sorted(queue, key=lambda x: x.total_cost)
        while True:
            current_node = queue[0]
            current_node.visited_djikstra = True
            if current_node == end_hub:
                break
            queue = queue[1:]
            optimal_neighbors: List[Hub] = [
                c for c in current_node.neighbors.values()
                if not c.visited_djikstra
            ]
            for o in optimal_neighbors:
                if o.total_cost > current_node.total_cost + o.cost:
                    o.total_cost = current_node.total_cost + o.cost
                    o.precedent = current_node
                # we check for duplicate
                if o in queue:
                    clone: List[Hub] = [q for q in queue if q.name == o.name]
                    # we remove the duplicated element
                    queue = list(
                            filter(lambda x: x.name != clone[0].name, queue))
                    # we add the smallest element
                    queue.append(min(o, clone[0], key=lambda x: x.total_cost))
                else:
                    queue.append(o)
            queue = sorted(queue, key=lambda x: x.total_cost)
