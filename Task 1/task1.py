import os 

# write code to check if splits.txt exists
if not os.path.exists("splits.txt"):
    print("File does not exist")
    exit()

f = open("splits.txt", "r")
# read number of sensors and laps
line1 = f.readline()
line1_split = line1.split(",")

# seperate into number of sensors and number of laps 
num_sensors = int(line1_split[1])
num_laps = int(line1_split[0])
packet_size = num_laps + 2

# read rest of data
newline = f.readline()
times_str = ""

while newline:
    times_str += newline
    newline = f.readline()

# read the rest of the data in the file, storing every 5 numbers in a list called input_lines

times = times_str.split(',')

input_separated = [[] for _ in range(num_sensors)]

# Deal with trailing comma
if not times[-1].isnumeric():
    times = times[:-1]

if packet_size * num_sensors != len(times):
    print(f"Number of Laps or Number of Sensors is wrong!, {packet_size} * {num_sensors} =/= {len(times)}")
    exit()

for (i, time) in enumerate(times):
    if i // packet_size >= len(input_separated):
        break
    input_separated[i // (packet_size)].append(time)

input_lines = [', '.join(line) for line in input_separated]

print(f"\n\ninput_lines: {input_lines}\n\n")

sensor_data = [(int(line[0]), int(line[1]), float(line[2]), float(line[3]), float(line[4])) for line in input_separated]
print(f"sensor_data: {sensor_data}\n\n")

# check if any of the times are negative
for sensor in sensor_data:
    for j in range(num_laps):
        if sensor[j+2] < 0:
            print("Negative time detected")
            exit()

# check if any of the times are out of order
for sensor in sensor_data:
    for j in range(num_laps-1):
        if sensor[j+2] > sensor[j+3]:
            print("Times out of order")
            exit()

import matplotlib.pyplot as plt

# Define lists to store x and y positions of sensors
x_positions = []
y_positions = []

# Extract x and y positions of sensors from sensor_data
for sensor in sensor_data:
    x_positions.append(sensor[0])
    y_positions.append(sensor[1])

# Plot the sensors as red dots and car's path as green line
plt.scatter(x_positions, y_positions, color='red', label='Sensor')
plt.plot(x_positions, y_positions, color='green', label='Path')

# Add labels and legend to the plot
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Path of the Car')
for i, sensor in enumerate(sensor_data):
    plt.annotate(str(i+1), (sensor[0]+10, sensor[1]+10))
plt.legend()

# Show the plot
plt.show()


