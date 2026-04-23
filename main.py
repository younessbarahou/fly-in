from parsing import Parser, ParsingError, DataBase
from meta.graph import Graph
from meta.hub import Hub
from meta.graph import ReachableError
from typing import List
from solution import Solution
from meta.drone import Drone


class Main():
    @staticmethod
    def main() -> None:
        try:
            Data_Parser: Parser = Parser()
            Data_result: DataBase = Data_Parser.parse('input.txt')
            graph: Graph = Graph(Data_result)
            graph.validate()
            graph_result = graph.get_graph()
            drones: List[Drone] = []
            nb_drones: int = Data_result.nb_drones
            while nb_drones > 0:
                drone: Drone = Drone()
                drones.append(drone)
                nb_drones -= 1
            solution: List[Hub] = Solution.solve(
                graph_result, Data_result.start_hub, Data_result.end_hub)
            for s in solution:
                print(s.name)
            for s in solution:
                drones[0].path.append(s.name)
                print(f"+{s.cost}")
            print(drones[0].path)
        except ParsingError as e:
            print(e)
        except ReachableError as e:
            print(e)


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
