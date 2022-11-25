from dataclasses import dataclass


# Holds station data
@dataclass(unsafe_hash=True)
class Station:
    stationNum: int  # Unique id of the station
    demand: float  # Demand requested by the station
    earliest_time: float = 0  # Earliest convenience time arrival for trucks
    latest_time: float = 0  # Latest convenience time arrival for trucks
    time_to_spend: float = 0  # Required time to be spent when trucks arrive
