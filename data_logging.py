from sense_hat import SenseHat
from datetime import datetime
import matplotlib.pyplot as plt

timestamp = datetime.now()
# Delay in seconds
delay = 3
sense = SenseHat()

class DataLogging:
        def get_sense_data():
                orientation = sense.get_orientation()
                mag = sense.get_compass_raw()
                acc = sense.get_accelerometer_raw()
                gyro = sense.get_gyroscope_raw()
                return [
                        datetime.now(),
                        sense.get_temperature(),
                        sense.get_pressure(),
                        sense.get_humidity(),
                        orientation['yaw'],
                        orientation['pitch'],
                        orientation['roll'],
                        mag["x"],
                        mag["y"],
                        mag["z"],
                        acc["x"],
                        acc["y"],
                        acc["z"],
                        gyro["x"],
                        gyro["y"],
                        gyro["z"]
                ]


        def data_representation(self, x_axis, y_axis):
                plt.plot(x_axis, y_axis)
        
with open('data.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(['datetime', 'temperature','pressure','humidity', 'yaw','pitch','roll', 'mag_x','mag_y','mag_z', 'acc_x','acc_y','acc_z', 'gyro_x', 'gyro_y', 'gyro_z'])
	while True:
		delta = datetime.now() - timestamp
		if delta.seconds > delay:
			data = get_sense_data()
			writer.writerow(data)
			timestamp = datetime.now()


