import matplotlib.pyplot as plt
from sense_hat import SenseHat
from time import sleep

class DataLogging:
    def __init__(self):
        self.data = []
        self.time = []
        self.start_time = datetime.datetime.now().time()
        
    def logging_data(self):
        self.data.append()
        self
        
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.ylabel('Speed (m/s)')
    plt.xlabel('Time(s)')
    plt.savefig('foo.png')
    plt.savefig('foo.pdf')
    plt.show()
