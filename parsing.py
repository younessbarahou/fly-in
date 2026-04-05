from typing import List, Dict, Union
import re


class Parser:
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.start_hub = []
        self.end_hub = []
        self.hubs = []
        self.connections = []

    def check_nb_drones(self, lines: List[str]) -> None:
        expected_format: re.Pattern = re.compile('nb_drones: [1-9]{1,}')
        if re.fullmatch(expected_format, lines[0]):
            self.nb_drones = lines[0].split(':')[1]
        else:
            raise ValueError(
                "Invalid number of drones ! Expected: nb_drones: <number >= 1>"
                )

    def check_start_hub(self, lines: List[str]) -> None:
        expected_format: re.Pattern = re.compile(
            'start_hub: [a-z]{3,8} [1-9]{1,} [1-9]{1,} ([a-z])'
        )
        if re.fullmatch(expected_format, lines[1]):
            

    def check_end_hub(self) -> None:
        pass

    def parse(self, file_name: str) -> None:
        try:
            with open(file_name, 'r') as file:
                lines: List[str] = file.readlines()
                # removing new lines
                lines = list(map(lambda x: x.strip(), lines))
                # removing empty lines
                lines = [line for line in lines if len(line) != 0]
                # removing comments
                lines = [line for line in lines if line[0] != "#"]
                if len(lines) < 5:
                    raise ValueError(
                        "Data entered should contain at least:\n<nb_drones>\n<start_hub>\n<end_hub>\n<connection>"
                        )
                # checking the number of drones
                self.check_nb_drones(lines)
                # checking start hub
        except FileNotFoundError:
            raise FileNotFoundError("input file is missing !")
        except PermissionError:
            raise PermissionError("Reading input file failed !\nPermission Error.")

    def get_parsed_data(self) -> str:
        return f"{self.nb_drones} {self.start_hub} {self.end_hub} {self.hubs} {self.connections}"


if __name__ == "__main__":
    try:
        a = Parser()
        a.parse('input.txt')
        print(a.get_parsed_data())
    except ValueError as e:
        print(e)
