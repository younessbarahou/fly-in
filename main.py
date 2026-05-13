from parsing import Parser, ParsingError, DataBase
from meta.graph import GraphBuilder
from meta.drone import Drone
from typing import List
from solution import PathsGenerator, ReachableError
from engine import Engine
from meta.path import Path


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
                drone: Drone = Drone(f"D{jndex}")
                drones.append(drone)
                jndex += 1
            solution: List[Path] = PathsGenerator.generate(
                Data_result.start_hub,
                Data_result.end_hub, Data_result.connections)
            # for s in solution:
            #     print("======")
            #     print(s.max_drones_number)
            #     for p in s.nodes:
            #         print(p.name)
            #     print("======")
            engine: Engine = Engine(Data_result.start_hub.name, solution, drones, Data_result.connections)
            engine.simulate()
        except ParsingError as e:
            print(e)
        except ReachableError:
            print("Start zone and End Zone are isolated from each other !")


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
