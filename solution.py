from typing import List
from meta.start_hub import StartHub
from meta.end_hub import EndHub
from meta.hub import Hub


class Solution:
    """  """
    @staticmethod
    def solve(
        start_hub: StartHub, end_hub: EndHub
    ) -> List[Hub]:
        result: List[List[Hub]] = []
        path: List[Hub] = []

        def dfs(node: Hub, path: List[Hub]) -> None:
            path.append(node)
            if node is end_hub:
                result.append(path.copy())
                path.pop()
                return
            for n in node.neighbors:
                if n not in path:
                    dfs(n, path)
            path.pop()
        dfs(start_hub, path)
        result = sorted(result, key=lambda x: min(x, key=lambda y: y.cost).cost)
        return result
