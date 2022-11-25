from dataclasses import dataclass

import Station


# Keeps path data
@dataclass(unsafe_hash=True)
class Path:
    start: Station  # Path start station
    end: Station  # Path end station
    cost: float  # Cost of the path
    saving: float  # How much time and money will be saved by using this path
    timeSpentBetween: float = 0  # How much time passed between start and end of the path
