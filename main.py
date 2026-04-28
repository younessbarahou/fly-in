from parsing import Parser, ParsingError, DataBase
from meta.graph import GraphBuilder
from meta.hub import Hub, Drone
from typing import List
from solution import PathsGenerator, ReachableError
from engine import Engine


class Main():
    @staticmethod
    def main() -> None:
        try:
            Data_Parser: Parser = Parser()
            Data_result: DataBase = Data_Parser.parse('input.txt')
            graph: GraphBuilder = GraphBuilder(Data_result)
            graph.setup()
            drones: List[Drone] = []
            nb_drones: int = Data_result.nb_drones
            jndex: int = 0
            while jndex < nb_drones:
                drone: Drone = Drone()
                drone.identifier = f"D{jndex}"
                drone.path.append(Data_result.start_hub.name)
                drones.append(drone)
                jndex += 1
            solution: List[List[Hub]] = PathsGenerator.solve(
                Data_result.start_hub,
                Data_result.end_hub, Data_result.connections)
        except ParsingError as e:
            print(e)
        except ReachableError:
            print("Start zone and End Zone are isolated from each other !")


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
