from typing import List, Dict, Union, Tuple, Set
from meta.start_hub import StartHub
from meta.hub import Hub
from meta.end_hub import EndHub
from meta.connection import Connection
import re


class ParsingError(Exception):
    pass


class Data():
    def __init__(
            self,
            nb_drones: int,
            start_hub: StartHub,
            end_hub: EndHub,
            hubs: List[Hub],
            connections: List[Connection]
    ) -> None:
        self.nb_drones = nb_drones
        total_hubs_names: List[str] = [h.name for h in hubs] + [start_hub.name, end_hub.name]
        total_hubs_coordinates: List[Tuple[int, int]] = [(h.x, h.y) for h in hubs] + [(start_hub.x, start_hub.y), (end_hub.x, end_hub.y)]
        set_hub_names: Set[str] = set(total_hubs_names)
        set_hub_coordinates: Set[Tuple[int, int]] = set(total_hubs_coordinates)
        if len(total_hubs_names) != len(set_hub_names):
            raise ParsingError("hubs names should not be duplicated !")
        if len(set_hub_coordinates) != len(total_hubs_coordinates):
            raise ParsingError("hubs coordinates should not be duplicated")
        for connection in connections:
            if connection.name_1 not in total_hubs_names:
                raise ParsingError(f"Invalid hub '{connection.name_1}' in connection '{connection.name_1}-{connection.name_2}'!")
            if connection.name_2 not in total_hubs_names:
                raise ParsingError(f"Invalid hub '{connection.name_2}' in connection '{connection.name_1}-{connection.name_2}'!")
        total_connections: List[Tuple[str, str]] = [(c.name_1, c.name_2) for c in connections]
        temp_index: int = 0
        while temp_index < len(total_connections) - 1:
            temp_jndex: int = temp_index + 1
            while temp_jndex < len(total_connections):
                cname_1, cname_2 = total_connections[temp_index]
                cname_3, cname_4 = total_connections[temp_jndex]
                if total_connections[temp_index][0] == total_connections[temp_jndex][0] and total_connections[temp_index][1] == total_connections[temp_jndex][1]:
                    raise ParsingError(f"{cname_1}-{cname_2} and {cname_3}-{cname_4} are the same connection")
                if total_connections[temp_index][0] == total_connections[temp_jndex][1] and total_connections[temp_index][1] == total_connections[temp_jndex][0]:
                    raise ParsingError(f"{cname_1}-{cname_2} and {cname_3}-{cname_4} are the same connection")
                temp_jndex += 1
            temp_index += 1
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.hubs = hubs
        self.connections = connections


class Parser:
    def __init__(self) -> None:
        pass

    def check_nb_drones(self, lines: List[str]) -> int:
        expected_format: re.Pattern = re.compile('nb_drones *: *[0-9]{1,}')
        if re.fullmatch(expected_format, lines[0]):
            nb_drones = int(lines[0].split(':')[1])
            if nb_drones <= 0:
                raise ParsingError(
                    "Invalid number of drones ! Expected: nb_drones: <number >= 1>"
                    )
            return (nb_drones)
        raise ParsingError(
            "Invalid number of drones ! Expected: nb_drones: <number >= 1> in the first line"
        )

    def check_hub(
            self, start_line: List[str], parameter: str
            ) -> Hub:
        result: Dict[str, Union[str, int, None]] = {
            'name': None,
            'x': None,
            'y': None,
            'zone': 'normal',
            'color': 'blue',
            'max_drones': 1
        }
        try:
            if len(start_line.split(':')) == 2:
                start_data: str = start_line.split(':')[1]
                expected_optional: re.Pattern = re.compile(r' *[a-zA-Z_]{1,}([0-9]{1,})? {1,}[0-9]{1,} {1,}[0-9]{1,} {1,}\[ *[a-zA-Z_]{1,}=[a-zA-Z0-9]{1,}( {1,}[a-zA-Z_]{1,}=[a-zA-Z0-9]{1,}){0,2} *\]')
                expected_mandatory: re.Pattern = re.compile(r' *[a-zA-Z_]{1,}([0-9]{1,})? {1,}[0-9]{1,} {1,}[0-9]{1,} *')
                if re.fullmatch(expected_mandatory, start_data) or re.fullmatch(expected_optional, start_data):
                    formatted_data = start_data.replace(
                        '[', '').replace(']', '')
                    start_splitted: List[str] = formatted_data.split()
                    start_name: str = ""
                    x_coord: int = int(start_splitted[1])
                    y_coord: int = int(start_splitted[2])
                    start_name = start_splitted[0]
                    result['name'] = start_name
                    result['x'] = x_coord
                    result['y'] = y_coord
                    if re.fullmatch(expected_optional, start_data):
                        metadata_check: List[List[str]] = start_splitted[3:]
                        for data in metadata_check:
                            temp_split: List[str] = data.split("=")
                            match temp_split[0].lower():
                                case 'zone':
                                    match temp_split[1]:
                                        case 'normal':
                                            pass
                                        case 'blocked':
                                            result['zone'] = 'blocked'
                                        case 'restricted':
                                            result['zone'] = 'restricted'
                                        case 'priority':
                                            result['zone'] = 'priority'
                                        case _:
                                            raise ParsingError(f"Invalid hub {temp_split[1]}")
                                case 'color':
                                    match temp_split[1]:
                                        case 'green':
                                            result['color'] = 'green'
                                        case 'blue':
                                            result['color'] = 'blue'
                                        case 'red':
                                            result['color'] = 'red'
                                        case _:
                                            raise ParsingError(f"Invalid hub {temp_split[1]}")
                                case 'max_drones':
                                    temp_nb: int = int(temp_split[1])
                                    if temp_nb == 0:
                                        raise ParsingError()
                                    result['max_drones'] = temp_nb
                                case _:
                                    raise ParsingError(f"Invalid hub {temp_split[1]}")
                    if parameter == 'start_hub':
                        return (
                            StartHub(
                                result['name'],
                                result['x'],
                                result['y'],
                                result['zone'],
                                result['color'],
                                result['max_drones'])
                            )
                    elif parameter == 'end_hub':
                        return (
                            EndHub(
                                result['name'],
                                result['x'],
                                result['y'],
                                result['zone'],
                                result['color'],
                                result['max_drones'])
                            )
                    elif parameter == 'hub':
                        return (
                            Hub(
                                result['name'],
                                result['x'],
                                result['y'],
                                result['zone'],
                                result['color'],
                                result['max_drones'])
                            )
                else:
                    raise ParsingError()
            else:
                raise ParsingError()
        except ParsingError:
            raise ParsingError(f"Invalid {parameter} '{start_line}';\nexpected=> {parameter}: hub_name x y [metadata](Optional)>\n[ hub_name: valid string with no dashes / spaces + name can contain numbers in the end\n'x': valid positive integer\n'y': valid positive integer\nmetadata(Optional):\n'color'=red | green | blue\n'zone'=normal| blocked | restricted | priority\n'max_drones'= valid positive integer\n] example:\n{parameter}: hub1 0 0 [color=green zone=normal]")

    def check_connection(self, line: List[str]) -> Connection:
        try:
            if len(line.split(":")) == 2:
                connection_value: List[str] = line.split(":")[1]
                expected_mandatory: re.Pattern = re.compile(" *[a-zA-Z]{1,}([0-9]{1,})?-[a-zA-Z]{1,}([0-9]{1,})?")
                expected_optional: re.Pattern = re.compile(r" *[a-zA-Z]{1,}([0-9]{1,})?-[a-zA-Z]{1,}([0-9]{1,})? \[max_link_capacity *= *[0-9]{1,}\]")
                if re.fullmatch(expected_mandatory, connection_value) or re.fullmatch(expected_optional, connection_value):
                    formatted_connection: List[str] = connection_value.replace(
                        ']', '').replace('[', '').split()
                    name_1: str = formatted_connection[0].split('-')[0]
                    name_2: str = formatted_connection[0].split('-')[1]
                    if name_1 == name_2:
                        raise ParsingError()
                    max_link_capacity: int = 1
                    if re.fullmatch(expected_optional, connection_value):
                        max_link_capacity: int = int(
                            formatted_connection[1].split('=')[1]
                        )
                        if max_link_capacity == 0:
                            raise ParsingError()
                    return Connection(name_1, name_2, max_link_capacity)
                else:
                    raise ParsingError()
            else:
                raise ParsingError()
        except ParsingError:
            raise ParsingError(f"Invalid connection {line}; expected=> connection: hub1-hub2 [metadata](Optional)>\nhub1 and hub2: valid strings name that can contain numbers in the end + different from each other\n'max_drones'= valid positive integer\n metadata(Optional):\n max_link_capacity: valid positive integer\nexample:\nconnection: hub1-hub2 [max_link_capacity=5]")

    def parse(self, file_name: str) -> Data:
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
                    raise ParsingError(
                        "Data entered should contain at least:\n<nb_drones>\n<start_hub>\n<end_hub>\n<hub>\n<connection>"
                    )
                # checking the number of drones
                nb_drones: int = self.check_nb_drones(lines)
                # removing the first line
                lines = lines[1:]
                start_result: StartHub | None = None
                end_result: EndHub | None = None
                hub_result: List[Hub] = []
                connection_result: List[Connection] = []
                for line in lines:
                    temp_check: List[str] = line.split(':')
                    if (
                        len(temp_check) != 2 or
                        temp_check[0] == "" or
                        temp_check[1] == ""
                    ):
                        raise ParsingError(f"Invalid {temp_check[0]} parameter! expected format <parameter>: <values>")
                    match temp_check[0].strip():
                        case 'start_hub':
                            if start_result is not None:
                                raise ParsingError("start_hub should not be duplicated !")
                            start_result = self.check_hub(line, 'start_hub')
                        case 'end_hub':
                            if end_result is not None:
                                raise ParsingError("end_hub should not be duplicated !")
                            end_result = self.check_hub(line, 'end_hub')
                        case 'hub':
                            hub_result.append(self.check_hub(line, 'hub'))
                        case 'connection':
                            connection_result.append(self.check_connection(line))
                        case _:
                            raise ParsingError(f"Invalid '{line}'")
                if start_result is None:
                    raise ParsingError("start_hub parameter is missing !")
                if end_result is None:
                    raise ParsingError("end_hub parameter is missing !")
                if len(hub_result) == 0:
                    raise ParsingError("should be at least one hub !")
                if len(connection_result) == 0:
                    raise ParsingError("should be at least one connection !")
                result_data: Data = Data(
                    nb_drones,
                    start_result,
                    end_result,
                    hub_result,
                    connection_result
                    )
                return result_data
        except FileNotFoundError:
            raise FileNotFoundError("input file is missing !")
        except PermissionError:
            raise PermissionError(
                "Reading input file failed !\nPermission Error."
            )
        except ParsingError as e:
            raise ParsingError(e)


if __name__ == "__main__":
    try:
        a = Parser()
        print(a.parse('input.txt'))
    except ParsingError as e:
        print(e)
