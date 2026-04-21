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
        for q in queue:
            q.precedent = current_node
            q.total_cost = int(q.cost)
        queue = sorted(queue, key=lambda x: x.total_cost)
        while True:
            # selecting and poping from the queue
            current_node = queue[0]
            queue = queue[1:]
            if current_node.visited_djikstra is True:
                continue
            current_node.visited_djikstra = True
            if current_node == end_hub:
                break
            optimal_neighbors: List[Hub] = [
                c for c in current_node.neighbors.values()
                if not c.visited_djikstra
            ]
            for o in optimal_neighbors:
                if o.total_cost > current_node.total_cost + o.cost:
                    o.total_cost = current_node.total_cost + int(o.cost)
                    o.precedent = current_node
                queue.append(o)
            queue = sorted(queue, key=lambda x: x.total_cost)
            path_result: List[Hub] = []
