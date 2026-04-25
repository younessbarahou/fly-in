from parsing import Parser, ParsingError, DataBase
from meta.graph import Graph
from meta.hub import Hub, Drone
from typing import List
from solution import Solution, ReachableError


class Main():
    @staticmethod
    def main() -> None:
        try:
            Data_Parser: Parser = Parser()
            Data_result: DataBase = Data_Parser.parse('input.txt')
            Graph(Data_result)
            drones: List[Drone] = []
            nb_drones: int = Data_result.nb_drones
            jndex: int = 0
            while jndex < nb_drones:
                drone: Drone = Drone()
                drone.id = f"D{jndex}"
                drone.path.append(Data_result.start_hub.name)
                drones.append(drone)
                jndex += 1
            solution: List[List[Hub]] = Solution.solve(
                Data_result.start_hub, Data_result.end_hub)
            for s in solution:
                print(sum([a.cost for a in s]))
        except ParsingError as e:
            print(e)
        except ReachableError as e:
            print(e)


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
