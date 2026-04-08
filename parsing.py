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
        try:
            if len(self.centered_data['start_hub']) != 0:
                raise ValueError("start hub should not be duplicated!")
            if len(start_line.split(':')) == 2:
                start_splitted: List[str] = start_line.split(':')[1].split(' ', 4)
                # remove spaces
                start_splitted = [s for s in start_splitted if s != '']
                if len(start_splitted) == 3 or len(start_splitted) == 4:
                    nb_format: re.Pattern = re.compile('[0-9]{1,}')
                    start_name: str = ""
                    x_coord: int = -1
                    y_coord: int = -1
                    if (
                        re.fullmatch(nb_format, start_splitted[0]) or
                        type(start_splitted[0]) is not str or
                        '-' in start_splitted[0] or
                        ' ' in start_splitted[0]
                    ):
                        raise ValueError()
                    try:
                        x_coord = int(start_splitted[1])
                        y_coord = int(start_splitted[2])
                        if x_coord < 0 or y_coord < 0:
                            raise ValueError()
                    except ValueError:
                        raise ValueError()
                    start_name = start_splitted[0]
                    self.centered_data['start_hub'].update({
                        'name': start_name,
                        'x': x_coord,
                        'y': y_coord,
                        'zone_type': 'normal',
                        'color': None,
                        'max_drones': 1
                        }
                    )
                    if len(start_splitted) == 4:
                        buffer_start: List[str] = start_splitted[3]
                        expected_format: re.Pattern = re.compile(r'\[[a-z_]{1,}=[a-z1-9]{1,}( [a-z_]{1,}=[a-z1-9]{1,}){0,2}\]')
                        if re.fullmatch(expected_format, buffer_start):
                            buffer_start = buffer_start.replace('[', '')
                            buffer_start = buffer_start.replace(']', '')
                            metadata_check: List[List[str]] = buffer_start.split(' ')
                            for data in metadata_check:
                                temp_split: List[str] = data.split("=")
                                match temp_split[0]:
                                    case 'zone':
                                        match temp_split[1]:
                                            case 'normal':
                                                pass
                                            case 'blocked':
                                                self.centered_data['start_hub'].update({'zone': 'blocked'})
                                            case 'restricted':
                                                self.centered_data['start_hub'].update({'zone': 'restricted'})
                                            case 'priority':
                                                self.centered_data['start_hub'].update({'zone': 'priority'})
                                            case _:
                                                raise ValueError()
                                    case 'color':
                                        match temp_split[1]:
                                            case 'green':
                                                self.centered_data['start_hub'].update({'color': 'green'})
                                            case 'blue':
                                                self.centered_data['start_hub'].update({'color': 'blue'})
                                            case 'red':
                                                self.centered_data['start_hub'].update({'color': 'red'})
                                            case _:
                                                raise ValueError()
                                    case 'max_drones':
                                        temp_nb: int = int(temp_split[1])
                                        self.centered_data['start_hub'].update({'max_drones': temp_nb})
                                    case _:
                                        raise ValueError()
                        else:
                            raise ValueError()
                    else:
                        raise ValueError()
        except ValueError:
            raise ValueError("Invalid start_hub; expected=> <start_hub: hub_name x y [metadata](Optional)>\nhub_name: valid string with no dashes / spaces\n'x': valid positive integer\n'y': valid positive integer\nmetadata(Optional):\n'color'=red | green | blue\n'zone'=normal| blocked | restricted | priority\n'max_drones'= valid positive integer\n example:\nstart_hub: hub1 0 0 [color=green zone=normal]")

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
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    try:
        a = Parser()
        a.parse('input.txt')
        print(a.centered_data)
    except ValueError as e:
        print(e)
