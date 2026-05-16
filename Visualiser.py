from pygame import display, Surface, Rect, init, mixer, Color, draw, event, QUIT, image, transform
from parsing import DataBase
from typing import List, Tuple
from meta.hub import Hub
from meta.start_hub import StartHub
from meta.drone import Drone
from meta.connection import Connection


class Visualiser():
    def __init__(self, DataResult: DataBase) -> None:
        self.hubs: List[Hub]= [hub for hub in DataResult.hubs.values()] + [DataResult.start_hub] + [DataResult.end_hub]
        self.drones: List[Drone] = DataResult.drones
        self.connections: List[Connection] = DataResult.connections
        self.max_x: int = max([hub.x for hub in self.hubs])
        self.max_y: int = max([hub.y for hub in self.hubs])

    def formula(self, x: int, y: int) -> Tuple[int, int]:
        scaling_x: int = 1180 * (x / self.max_x) + 50
        scaling_y: int = 620 * (y / self.max_y) + 50
        return (scaling_x, scaling_y)

    def visualise(self) -> None:
        init()
        white: Color = Color(212, 212, 212)
        green: Color = Color(50, 210, 80)
        red: Color = Color(196, 21, 62)
        blue: Color = Color(0, 106, 188)
        screen: Surface = display.set_mode((1280, 720))
        running: bool = True
        while running:
            for connection in self.connections:
                connection1_coordinates: Tuple[int, int] = self.formula(connection.hub_1.x, connection.hub_1.y)
                connection2_coordinates: Tuple[int, int] = self.formula(connection.hub_2.x, connection.hub_2.y)
                draw.line(screen, white, connection1_coordinates, connection2_coordinates, 5)
            for hub in self.hubs:
                draw_coordinates: Tuple[int, int] = self.formula(hub.x, hub.y)
                x, y = draw_coordinates
                match hub.color:
                    case "blue":
                        draw.circle(screen, white, [x, y], 50)
                        draw.circle(screen, blue, [x, y], 48)
                    case "red":
                        draw.circle(screen, white, [x, y], 50)
                        draw.circle(screen, red, [x, y], 48)
                    case _:
                        draw.circle(screen, white, [x, y], 50)
                        draw.circle(screen, green, [x, y], 48)
            for e in event.get():
                if e.type == QUIT:
                    running = False
            display.update()
