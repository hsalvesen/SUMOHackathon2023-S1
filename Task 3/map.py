import csv
import matplotlib.pyplot as plt

class Map:
    
    def __init__(self):
        self.X_COORD_INDEX = 0
        self.Y_COORD_INDEX = 1
        self.WALL_INDEXES = [2,3,4,5] 
        self.rawData = []
        self.walls = []
        self.fig = 0
        self.ax = 0
        self.startCell = [7, 7]
        self.goalCell = [14, 14]


    # parses csv from fileDirectory string into usable data in Self 
    # to reduce the need to keep the file open
    def loadMap(self, fileDirectory: str):
        with open(fileDirectory) as csv_map:
            csv_reader = csv.reader(csv_map, delimiter=',')
            for row in csv_reader:
                self.rawData.append(row)

    # finds a list of plottable lines representing walls of maze 
    def findWalls(self):
        
        # check for header row
        header_check = 0

        # iterate through each data entry from CSV data
        for row in self.rawData:
            # skip header row
            if header_check == 0:
                header_check += 1
                continue
            
            # iterate through each data point from data entry
            for i in self.WALL_INDEXES:
                # skip if wall not detected
                if row[i] != '1':
                    continue
                # wall detected
                match i:
                    case 2: # northern wall
                        x = [int(row[self.X_COORD_INDEX]), int(row[self.X_COORD_INDEX])+1]
                        y = [int(row[self.Y_COORD_INDEX]), int(row[self.Y_COORD_INDEX])]
                        self.walls.append([x,y])
                    
                    case 3: # eastern wall
                        x = [int(row[self.X_COORD_INDEX])+1, int(row[self.X_COORD_INDEX])+1]
                        y = [int(row[self.Y_COORD_INDEX]), int(row[self.Y_COORD_INDEX])+1]
                        self.walls.append([x,y])
                    
                    case 4: # southern wall
                        x = [int(row[self.X_COORD_INDEX]), int(row[self.X_COORD_INDEX])+1]
                        y = [int(row[self.Y_COORD_INDEX])+1, int(row[self.Y_COORD_INDEX])+1]
                        self.walls.append([x,y])

                    case 5: # western wall
                        x = [int(row[self.X_COORD_INDEX]), int(row[self.X_COORD_INDEX])]
                        y = [int(row[self.Y_COORD_INDEX]), int(row[self.Y_COORD_INDEX])+1]
                        self.walls.append([x,y])
        return self.walls
    

    # draw maze from wall data + start and end points
    def plotMap(self):
        self.fig, self.ax = plt.subplots()
        self.ax.xaxis.tick_top()
        plt.xlim(-1, 16)
        plt.ylim(-1, 16)
        plt.gca().invert_yaxis()
    
        for wall in self.walls:
            self.ax.plot(wall[0], wall[1], color='black')

        # plot start and end goal
        self.ax.plot(self.startCell[0]+0.5, self.startCell[1]+0.5, marker='s', markersize='10', color='red')
        self.ax.plot(self.goalCell[0]+0.5, self.goalCell[1]+0.5, marker='s', markersize='10', color='green')
        plt.pause(1)

    