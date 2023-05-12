import matplotlib.pyplot as plt

from map import Map
from solver import Solver

# create map object
map = Map()

# parse csv file into usable data in map object
map.loadMap(r"Challenge 3\Objective 4\obj4_maze_3.csv")

# parses data into a list of plottable lines representing walls
map.findWalls()

# draw map walls
map.plotMap()

# create solver object
solver = Solver(map)

# run shortestPath
solver.shortestPath()

