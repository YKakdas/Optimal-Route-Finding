# Optimal-Route-Finding

This project aims to find optimum routes for given set of stations.

## Components:
-   Station
    -   Declares how much goods they need in daily basis as demand.
    -   Has service time for truck to unload
    -   Has earliest & latest convenience timeline for trucks to unload
    -   Base station where all trucks starts and end.
-   Truck: Two types, small & big
    -   Has maximum capacity
    -   Has rent price
    -   Has fuel consumption per km

## Input format:

This project reads the necessary information via excel file. The following workbook structure should be followed to be able to run the algorithm:
<br></br>
1.  Truck Sheet (3 rows x 3 columns) (First row is header)
    -   Columns:
        1.  Capacity
        2.  Rent
        3.  Fuel per km
    -   Rows:
        1.  Small Truck
        2.  Big Truck
<br></br>
2.  Time Sheet(N x N) where N is total number of stations
    -   Matrix that shows how much time would pass departing from a stations to arrive in another. Diagonal is 0.
<br></br>
3.  Demand Sheet((N - 1) x 1)
    -   Shows demand of stations excluding the base station. Base station does not have any demand, it is start and end point of the trucks.
<br></br>
4.  Distance Sheet(N x N)
    -   Matrix that shows the distance between all stations
<br></br>
5.  Station Timeline((N + 1) x 3) (First row is header)
    -   Columns:
        1.  Earliest Time
        2.  Latest Time
        3.  Service Time
    -   Rows: Stations
<br></br>
6.  General Info((2 x 3)) (First row is header)
    - In second row, columns respectively are:
        -   Number of trucks
        -   Number of stations(Excluding the base station)
        -   Truck Speed
