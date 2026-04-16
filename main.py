from parsing import Parser, ParsingError, Data


class Main():
    def main() -> None:
        try:
            Data_Parser: Parser = Parser()
            Data_result: Data = Data_Parser.parse('input.txt')
            print(Data_result)
        except ParsingError as e:
            print(e)


if __name__ == "__main__":
    main: Main = Main()
    Main.main()
