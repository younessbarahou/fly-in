from meta.path import Path
from meta.drone import Drone
from typing import List


class Engine:
    def __init__(self, start_hub: str, paths: List[Path], drones: List[Drone]):
        self.paths = paths
        self.drones = drones
        self.start_hub = start_hub

    def simulate(self) -> None:
        queue: List[Drone] = self.drones
        simulation_queue: List[Drone] = []
        # trippin
        while queue:
            # we assign for each drone a path
            for p in self.paths:
                for _ in range(min(p.max_connection_capacity, p.max_drones_number)):
                    if len(queue):
                        queue[0].path = p.nodes
                        simulation_queue.append(queue[0])
                        queue = queue[1:]
        live_state: Dict[str, str] = {drone.identifier: self.start_hub for drone in simulation_queue}
        while simulation_queue:
            turn: str = ""
            for drone in simulation_queue:
                if len(drone.path):
                    # if drone.buffer:
                    #     turn += drone.buffer
                    #     drone.buffer = ""
                    #     continue
                    drones_in_same_zone: int = len([zone for zone in live_state.values() if zone == drone.path[0].name])
                    if drones_in_same_zone + 1 > drone.path[0].max_drones:
                        continue
                    # if drone.path[0].zone == "restricted":
                    #     turn += f"{drone.identifier}-{live_state[drone.identifier]}-{drone.path[0].name} "
                    #     drone.buffer += f"{drone.identifier}-{drone.path[0].name} "
                    #     live_state[drone.identifier] = drone.path[0].name
                    #     drone.path = drone.path[1:]
                    # else:
                    turn += f"{drone.identifier}-{drone.path[0].name} "
                    live_state[drone.identifier] = drone.path[0].name
                    drone.path = drone.path[1:]
                else:
                    simulation_queue.remove(drone)
                    live_state[drone.identifier] = ""
            if turn:
                print(turn)
