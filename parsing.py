from typing import List
class Parser:
    def __init__(self) -> None:
        pass

    def parse(self, file_name: str) -> None:
        try:
            with open(file_name, 'r') as file:
                lines: List[str] = file.readlines()
                # removing new lines
                for line in lines:
                    line = line.strip()
                    print(line)
        except FileNotFoundError:
            raise FileNotFoundError("input file is missing !")
        except PermissionError:
            raise PermissionError("Reading input file failed !\nPermission Error.")

a = Parser()
a.parse('input.txt')