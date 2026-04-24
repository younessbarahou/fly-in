from parsing import Parser, ParsingError, DataBase
from meta.graph import Graph
from meta.hub import Hub, Drone
from meta.graph import ReachableError
from typing import List
from solution import Solution


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
            jndex: int = 0
            while jndex < nb_drones:
                drone: Drone = Drone()
                drone.id = f"D{jndex}"
                drone.path.append(Data_result.start_hub.name)
                drones.append(drone)
                jndex += 1
            solution: List[Hub] = Solution.solve(
                graph_result, Data_result.start_hub, Data_result.end_hub)
            index: int = 1
            turns: list[str] = []
            while index < len(solution):
                drones[0].path.append(solution[index].name)
                if solution[index].zone == 'restricted':
                    turns.append(f"{drones[0].id}-{solution[index - 1].name}-{solution[index].name}")
                turns.append(f"{drones[0].id}-{solution[index].name}")
                index += 1
            print(drones[0].path)
            for t in turns:
                print(t)
        except ParsingError as e:
            print(e)
        except ReachableError as e:
            print(e)


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
