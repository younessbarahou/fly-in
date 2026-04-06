from typing import List, Dict, Union
import re


class Parser:
    def __init__(self) -> None:
        self.centered_data: Dict[str, int, Union[None, Dict[str, Union[int, s]]]] = {
                    'nb_drones': None,
                    'start_hub': {},
                    'end_hub': {},
                    'hubs': None,
                    'connections': None
                }

    def check_nb_drones(self, lines: List[str]) -> None:
        if self.centered_data['nb_drones'] is not None:
            raise ValueError("nb_drones should not be duplicated !")
        expected_format: re.Pattern = re.compile('nb_drones *: *[0-9]{1,}')
        if re.fullmatch(expected_format, lines[0]):
            nb_drones = int(lines[0].split(':')[1])
            if nb_drones <= 0:
                raise ValueError(
                    "Invalid number of drones ! Expected: nb_drones: <number >= 1>"
                    )
            self.centered_data['nb_drones'] = int(lines[0].split(':')[1])
        else:
            raise ValueError(
                "Invalid number of drones ! Expected: nb_drones: <number >= 1>"
                )

    def check_start_hub(self, start_line: List[str]) -> None:
        print(start_line)
        print(start_line.split(' '))
        if len(self.centered_data['start_hub']) != 0:
            raise ValueError("start hub should not be duplicated !")
        if len(start_line.split(' ')) == 4:
            expected_format: re.Pattern = re.compile(
                'start_hub *: *[a-z]{3,8} *[0-9]{1,} *[0-9]{1,}'
            )
            print(re.fullmatch(expected_format, start_line))
            if re.fullmatch(expected_format, start_line):
                start_values: List[str] = start_line.split(':')[1].strip().split(
                    ' '
                )
                hub_name, x_coord, y_coord = start_values
                self.centered_data['start_hub'].update(
                    {
                        'hub_name': hub_name,
                        'x_coord': x_coord,
                        'y_coord': y_coord
                    }
                )
            else:
                raise ValueError(
                    "Invalid start hub\nexpected=>start_hub: <hub_name(should not contain dashes / spaces)> <x> <y> [](optional)"
                )
        elif len(start_line.split(' ')) >= 5:
            expected_format: re.Pattern = re.compile(
                r'start_hub *: *[a-z]{3,8} *[0-9]{1,} *[0-9]{1,} \[[[a-z]{3,} *= *[a-z0-9]]{1,3}\]'
            )
            if re.fullmatch(expected_format, start_line):
                print(True)
            else:
                print(False)
        else:
            raise ValueError(
                "Invalid start hub\nexpected=>start_hub: <hub_name(should not contain dashes / spaces)> <x> <y> [](optional)"
                )

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
                        "Data entered should contain at least:\n<nb_drones>\n<start_hub>\n<end_hub>\n<hub>\n<connection>"
                    )
                # checking the number of drones
                self.check_nb_drones(lines)
                # removing the first line
                lines = [line for line in lines if line != lines[0]]
                for line in lines:
                    temp_check: List[str] = line.split(':')
                    if (
                        len(temp_check) != 2 or
                        temp_check[0] == "" or
                        temp_check[1] == ""
                    ):
                        raise ValueError(f"Invalid {temp_check[0]} parameter")
                    match temp_check[0].strip():
                        case 'start_hub':
                            self.check_start_hub(line)
                        case 'end_hub':
                            pass
                        case 'connection':
                            pass
                        case 'hub':
                            pass
        except FileNotFoundError:
            raise FileNotFoundError("input file is missing !")
        except PermissionError:
            raise PermissionError(
                "Reading input file failed !\nPermission Error."
            )


if __name__ == "__main__":
    try:
        a = Parser()
        a.parse('input.txt')
        print(a.centered_data)
    except ValueError as e:
        print(e)
