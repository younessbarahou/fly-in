from meta.path import Path
from meta.drone import Drone
from meta.connection import Connection
from typing import List, Dict


class Engine:
    def __init__(self, start_hub: str, paths: List[Path], drones: List[Drone], connections: List[Connection]):
        self.paths = paths
        self.drones = drones
        self.start_hub = start_hub

    def simulate(self) -> None:
        live_stats: Dict[str, str] = {drone.identifier: self.start_hub for drone in self.drones}
        # the queue is for the drones with path
        queue: list[Drone] = self.drones
        while queue:
            for drone in [drone for drone in queue if not drone.path]:
                for path in self.paths:
                    drones_at_zone: int = len([zone for zone in live_stats.values() if zone == path.nodes[0].name])
                    
                    if drones_at_zone + 1 > path.nodes[0].max_drones:
                        continue
                    drone.path = path.nodes
                    break
            turn: str = ""
            for drone in [drone for drone in queue if drone.path]:
                if drone.buffer:
                    turn += drone.buffer
                    drone.buffer = ""
                    continue
                drones_at_same_zone: int = len([zone for zone in live_stats.values() if zone == drone.path[0].name])
                if drones_at_same_zone + 1 > drone.path[0].max_drones:
                    continue
                if drone.path[0].zone == "restricted":
                    turn += f"{drone.identifier}-{live_stats[drone.identifier]}-{drone.path[0].name} "
                    drone.buffer = f"{drone.identifier}-{drone.path[0].name}"
                    live_stats[drone.identifier] = drone.path[0].name
                    drone.path = drone.path[1:]
                else:
                    live_stats[drone.identifier] = drone.path[0].name
                    turn += f"{drone.identifier}-{drone.path[0].name} "
                    drone.path = drone.path[1:]
                if len(drone.path) == 0:
                    live_stats[drone.identifier] = ""
                    queue.remove(drone)
            if turn:
                print(turn)
