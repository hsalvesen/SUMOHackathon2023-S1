import matplotlib.pyplot as plt

from map import Map
from solver import Solver

# create map object
map = Map()

# parse csv file into usable data in map object
map.loadMap("Challenge 3\Objective 1,2,3\maze_2.csv")

# parses data into a list of plottable lines representing walls
map.findWalls()

# draw map walls
map.plotMap()

# create solver object parsing in map data from map object
solver = Solver(map)
# Use Depth first search to check if solution is possible
# this method intergrates its own visualisation
print(f'Maze is solvable?: {solver.checkFeas()}')
