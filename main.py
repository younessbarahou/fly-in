from parsing import Parser, ParsingError, DataBase
from meta.graph import Graph


class Main():
    @staticmethod
    def main() -> None:
        try:
            Data_Parser: Parser = Parser()
            Data_result: DataBase = Data_Parser.parse('input.txt')
            g = Graph(Data_result)
            print(g.graph)
        except ParsingError as e:
            print(e)


if __name__ == "__main__":
    main_t: Main = Main()
    main_t.main()
