from dataclasses import dataclass


# Holds truck data
@dataclass(unsafe_hash=True)
class Truck:
    capacity: float  # Capacity of the truck
    rent: float  # The cost of rental
    fuelPerKm: float  # Fuel consumption per km
