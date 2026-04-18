from parsing import Parser, ParsingError, DataBase
from meta.graph import Graph
from meta.hub import Hub
from meta.graph import ReachableError


class Main():
    @staticmethod
    def main() -> None:
        try:
            Data_Parser: Parser = Parser()
            Data_result: DataBase = Data_Parser.parse('input.txt')
            graph: Graph = Graph(Data_result)
            graph.validate()
            for g in graph.get_graph():
                print(g, graph.get_graph()[g].is_visited)
        except ParsingError as e:
            print(e)
        except ReachableError as e:
            print(e)


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
