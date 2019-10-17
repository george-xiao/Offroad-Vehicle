from sense_hat import SenseHat
from datetime import datetime
import matplotlib.pyplot as plt
import math

class DataLogging:
    def __init__():
        self.timestamp = datetime.now()
        self.delay = 3 # Delay in seconds
        self.sense = SenseHat()
        self.time = []
        self.temp = []
        self.humidity = []
        self.yaw = []
        self.pitch = []
        self.roll = []
        self.north = []
        self.acc = []
        self.gyro_x = []
        self.gyro_y = []
        self.gyro_z = []


    # Gathers necessary information from Sense Hat
    # Returns data in form of an array
    def get_sense_data(self):
        orientation = self.sense.get_orientation()
        acc = self.sense.get_accelerometer_raw()
        gyro = self.sense.get_gyroscope_raw()

        return [
                datetime.now(),
                self.sense.get_temperature(),
                self.sense.get_pressure(),
                self.sense.get_humidity(),
                orientation['yaw'],
                orientation['pitch'],
                orientation['roll'],
                self.sense.get_compass_raw(),
                acc['x'],
                acc['y'],
                acc['z'],
                gyro['x'],
                gyro['y'],
                gyro['z']
        ]


    # Stores the data from get_sense_data() in individual arrays
    # Arrays will be used to graph data later
    def store_sense_data(self, data):
        acceleration = math.sqrt(data[8]**2 + data[9]**2 + data[10]**2) * 9.81 #Converting Gs to m/s^2
        
        self.time.append(data[0])
        self.temp.append(data[1])
        self.humidity.append(data[3])
        self.yaw.append(data[4])
        self.pitch.append(data[5])
        self.roll.append(data[6])
        self.north.append(data[7])
        self.acc.append(acceleration)
        self.gyro_x.append(data[11])
        self.gyro_y.append(data[12])
        self.gyro_z.append(data[13])


    # Graphs the different data sets versus time
    # Saves the graphs as pdfs
    def data_representation(self):
        self.graph_one_line(self.temp, 'Temperature (°C)')
        self.graph_one_line(self.temp, 'Humidity (%rH)')
        self.graph_three_lines(self.yaw, self.pitch, self.roll, 'Yaw', 'Pitch', 'Roll', 'Orientaion (°)')
        self.graph_one_line(self.north, 'North (°)')
        self.graph_one_line(self.acc, 'Acceleration (m/s^2)')
        self.graph_three_lines(self.gyro_x, self.gyro_y, self.gyro_z, 'x', 'y', 'z', 'Angular Velocity (rads/s)')


    # Graphs the one data set versus time
    # Saves the graph as pdf    
    def graph_one_line(self, data, y_axis_label):
        plt.plot(data, self.time)
        plt.ylabel(y_axis_label)
        plt.xlabel('Time (s)')
        plt.title(y_axis_label + ' vs Time Graph')
        plt.savefig(y_axis_label.split(' ', 1)[0] + 'vsTimeGraph.pdf')


    # Graphs the three data sets versus time
    # Saves the graph as pdf    
    def graph_three_lines(self, data1, data2, data3, data_label1, data_lable2, data_label3, y_axis_label):
        plt.plot(data1, self.time, marker='', color='#3969b1', linewidth=1, alpha=0.9, label = data_label1)
        plt.plot(data2, self.time, marker='', color='#da7c30', linewidth=1, alpha=0.9, label = data_label2)
        plt.plot(data3, self.time, marker='', color='#3e9651', linewidth=1, alpha=0.9, label = data_label3)
        plt.legend(loc=2, ncol=2)
        plt.ylabel(y_axis_label)
        plt.xlabel('Time (s)')
        plt.title(y_axis_label.split(' ', 1)[0] + ' vs Time Graph')
        plt.savefig(y_axis_label.split(' ', 1)[0] + 'vsTimeGraph.pdf')
        
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['datetime', 'temperature','pressure','humidity', 'yaw','pitch','roll', 'north', 'acc_x','acc_y','acc_z', 'gyro_x', 'gyro_y', 'gyro_z'])
    while True:
        delta = datetime.now() - timestamp
        if delta.seconds > delay:
            data = get_sense_data()
            writer.writerow(data)
            timestamp = datetime.now()


