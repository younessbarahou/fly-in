from typing import Dict, List
from meta.start_hub import StartHub
from meta.end_hub import EndHub
from meta.hub import Hub


class Solution:
    """ class that provides the shortest path from start to end """
    @staticmethod
    def solve(
        graph: Dict[str, Hub], start_hub: StartHub, end_hub: EndHub
    ) -> List[Hub]:
        """ produces the shortest path using djikstra algorithm """
        current_node: Hub = start_hub
        start_hub.visited_djikstra = True
        queue: List[Hub] = [
            c for c in start_hub.neighbors.values()
            if not c.visited_djikstra
        ]
        for q in queue:
            q.precedent = current_node
            q.total_cost = q.cost
        # sorting based on total cost first, then zone secondly
        queue = sorted(queue, key=lambda x: (
            x.total_cost, 0 if x.zone == 'priority' else 1))
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
                    o.total_cost = current_node.total_cost + o.cost
                    o.precedent = current_node
                queue.append(o)
            queue = sorted(queue, key=lambda x: (
                x.total_cost, 0 if x.zone == 'priority' else 1))
        path_result: List[Hub] = [end_hub]
        while path_result[-1].precedent is not None:
            path_result.append(path_result[-1].precedent)
        path_result.reverse()
        return path_result
