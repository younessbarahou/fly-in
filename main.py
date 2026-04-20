from parsing import Parser, ParsingError, DataBase
from meta.graph import Graph
from meta.hub import Hub
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
            Solution.solve(graph_result, Data_result.start_hub, Data_result.end_hub)
            for g in graph_result.values():
                print(g.precedent)
        except ParsingError as e:
            print(e)
        except ReachableError as e:
            print(e)


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
