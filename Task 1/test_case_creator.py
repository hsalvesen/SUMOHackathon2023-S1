import random

num_sensors = 23  # number of sensors
num_laps = 4     # number of laps
track_length = 1000  # length of the track
x_array = [20, 450, 410, 470, 450, 380, 360, 450, 450, 270, 220, 160, 0, 5, 80, 120, 170, 250, 300, 290, 320, 200, 140] # x coordinates of sensors
y_array = [300, 300, 270, 255, 210, 200, 160, 130, 100, 20, 130, 110, 125, 180, 200, 160, 200, 150, 160, 190, 220, 280, 255]  # y coordinates of sensors
# Generate sensor positions as integer x and y coordinates
sensors = []
for i in range(num_sensors):
    x = x_array[i]
    y = y_array[i]
    sensors.append((x, y, []))

time = 0

for j in range(num_laps):
    for i in range(num_sensors):
        time += random.uniform(3, 9)
        sensors[i][2].append(time)

# put values into  a text file
f = open("splits.txt", "w")
# first two values in file should be number of laps followed by number of sensors, put a space at the end
f.write(str(num_sensors) + ", " + str(num_laps) + "\n")
for i in range(num_sensors):
    f.write(str(sensors[i][0]) + ", " + str(sensors[i][1]) + ", ")
    for lap_time in sensors[i][2]:
        f.write(str(lap_time) + ", ")
    # f.write("\n")
f.close()

# print file
f = open("splits.txt", "r")
print("File contents:")
print(f.read())
f.close()

