from dataclasses import dataclass
from Station import Station


# List of stations in order determines the route for the truck
@dataclass(unsafe_hash=True)
class Route:
    inner_stations: [Station]
