
from map import Map
import numpy as np
import matplotlib.pyplot as plt


class Solver:
    def __init__(self, map: Map):
        self.map = map
        self.xpath = [7.5]
        self.ypath = [7.5]
        self.pauseDuration = 0.001
    
    # finds valid linking coordinates around each cell
    def findLinks(self, visit: list[list[int]], links: list[list[list[int]]]):
        for y in range(len(visit)):
            for x in range(len(visit[0])):

                # check north, east, south, west
                wallChecks = [[[x, x+1], [y, y]], [[x+1, x+1], [y, y+1]], [[x, x+1], [y+1, y+1]], [[x, x], [y, y+1]]]

                for i in range(len(wallChecks)):
                    if not(wallChecks[i] in self.map.walls): # check if wall exists in database
                        np.put(links[y][x], i, 1) # no wall found, a link  
                                      
                                
    # Depth first seach algorithm (self-iterable)
    def DFS(self, currCoords, links, visited, goalCell):
        
        #checks if found or if already landed on
        if (visited[currCoords[1]][currCoords[0]] == 1):
            #removes coords from path
            self.xpath.pop()
            self.ypath.pop()
            return False

        #flag cell as visited
        visited[currCoords[1]][currCoords[0]] = 1
        #adds cell coords to path
        self.xpath.append(currCoords[0]+0.5)
        self.ypath.append(currCoords[1]+0.5)
        
        #loop through each valid node on linkMap
        for i in range(4):
            #checks for valid nodes
            if (links[currCoords[1]][currCoords[0]][i] == 1):
                
                #checks if exit has been found
                if (([currCoords[1],currCoords[0]] == goalCell)):
                    return True

                # assigns new coords
                newCoords = [[currCoords[0], currCoords[1]-1],  #North
                [currCoords[0]+1, currCoords[1]],           #East
                [currCoords[0], currCoords[1]+1],           #South
                [currCoords[0]-1, currCoords[1]]]           #West

                # append new coords
                self.xpath.append(newCoords[i][0]+0.5)
                self.ypath.append(newCoords[i][1]+0.5)

                # plot current path step
                self.plotPath()

                # exits DFS on a success
                if (self.DFS(newCoords[i], links, visited, goalCell)):
                    return True
                else: # on a failure erases path step
                    self.xpath.pop()
                    self.ypath.pop()
                    self.map.ax.lines.remove(self.map.ax.lines[-1])
                    plt.pause(self.pauseDuration)

        return False
    
    # plots new path step
    def plotPath(self):
        plt.plot([self.xpath[-2], self.xpath[-1]], [self.ypath[-2], self.ypath[-1]], color='red')
        plt.pause(self.pauseDuration)

    # uses map data and depth first search algorithm to determine if the maze can be solved
    def checkFeas(self):
        # initialise two maps to be later used for DFS
        visitedMap = [ [0]*15 for i in range(15)]
        linksMap = np.zeros((15,15,4), dtype=int)

        # find linking map
        self.findLinks(visitedMap, linksMap)

        # DFS
        return self.DFS(self.map.startCell, linksMap, visitedMap, self.map.goalCell)
    
    # reconstruct shortest path and find intersection coords using the list of dictionary of Nodes
    def recPath(self, nodes):
        reconstructedPath = [self.map.goalCell]
        currCell = reconstructedPath[0]
        intersections = []

        # loop until startCell is reached
        while reconstructedPath[0] != self.map.startCell:
            # get data of current Cell  
            entry = next(item for item in nodes if currCell in item['Children'])
            parent = entry['Parent']
            children = entry['Children']

            #check if parent is an intersection
            if len(children) > 1:
                # if an intersection, insert parent at front of list
                intersections.insert(0, parent)

            # insert parent at front of reconstructed Path
            reconstructedPath.insert(0, parent)

            # update currCell
            currCell = parent
        return reconstructedPath, intersections
        
            

    # BFS algorithm -> returns list shortest path
    def BFS(self, links, visited, nodes, queue, currCoords, goalCell):

        # check if goal has been reached
        if currCoords == goalCell:
            return self.recPath(nodes)

        # tempNode to append to nodes list later
        tempNode = {'Parent': currCoords, 'Children': []}

        # queue neighbours
        #loop through each valid node on linkMap
        for i in range(4):
            #filters out invalid notes
            if (links[currCoords[1]][currCoords[0]][i] != 1):
                continue

            # assigns new nodes to queue and nodes list
            newCoords = [[currCoords[0], currCoords[1]-1],  #North
                [currCoords[0]+1, currCoords[1]],           #East
                [currCoords[0], currCoords[1]+1],           #South
                [currCoords[0]-1, currCoords[1]]]           #West

            # if already visited skip
            if visited[newCoords[i][1]][newCoords[i][0]] == 1:
                continue
            # if new link, add to nodes database, queue and mark as visited(as is on queue)
            tempNode['Children'].append(newCoords[i])
            queue.append(newCoords[i])
            visited[newCoords[i][1]][newCoords[i][0]] = 1

        # add tempNodes to node list
        nodes.append(tempNode)     
        
        # goal was unreachable; queue ran out
        if len(queue) == 0:
            return [], []
        
        # flag cell as visited and remove from queue
        visited[currCoords[1]][currCoords[0]] = 1
        queue.pop(0)   

        # iterate to next in queue
        return self.BFS(links, visited, nodes, queue, queue[0], goalCell)
    
    def solveIntersections(self, path, intersections):
        guide = []
        for intersection in intersections:
            # find coordinates of intersection in path
            i = path.index(intersection)

            stepBefore = np.array(path[i]) - np.array(path[i-1])
            stepAfter = np.array(path[i+1]) - np.array(path[i])
            
            if stepBefore[0] == stepAfter[0] and stepBefore[1] == stepAfter[1]:
                guide.append("STRAIGHT\n")
                continue
            if stepBefore[1] < 0:
                if stepAfter[0] > 0:
                    guide.append("RIGHT\n")
                else:
                    guide.append("LEFT\n")
                continue
            elif stepBefore[1] > 0:
                if stepAfter[0] < 0:
                    guide.append("RIGHT\n")
                else:
                    guide.append("LEFT\n")
                continue
            elif stepBefore[0] < 0:
                if stepAfter[1] < 0:
                    guide.append("RIGHT\n")
                else:
                    guide.append("LEFT\n")
                continue
            elif stepBefore[0] > 0:
                if stepAfter[1] > 0:
                    guide.append("RIGHT\n")
                else:
                    guide.append("LEFT\n")
                continue
        return guide
            

        
    
    # uses map data and Breadth First Search alogithm to determine the shortest route through the maze
    def shortestPath(self):
        # initialise two maps to be later used for DFS
        visitedMap = [ [0]*15 for i in range(15)]
        linksMap = np.zeros((15,15,4), dtype=int)

        # find linking map
        self.findLinks(visitedMap, linksMap)

        # BFS
        queue = [self.map.startCell]
        nodes = []
        path, intersections = self.BFS(linksMap, visitedMap, nodes, queue, self.map.startCell, self.map.goalCell)

        # determine directions at intersections
        guide = self.solveIntersections(path, intersections)

        #write a file with guide
        with open(r"Challenge 3\directions.txt", 'w') as f:
            f.writelines(guide)

        # animate path
        for i in range(len(path)-1):
            self.map.ax.plot([path[i][0]+0.5, path[i+1][0]+0.5], [path[i][1]+0.5, path[i+1][1]+0.5], color='red')
            plt.pause(self.pauseDuration*2)
        plt.show()

    



