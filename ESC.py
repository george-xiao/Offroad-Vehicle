# ESC Python program to run the ESC

import os
import time

# Launching GPIO library
os.system("sudo pigpiod")
# Will cause errors if this delays are removed
time.sleep(1)
import pigpio

class ElectronicSpeedController:
    # Constructor
    def __init__(self, gpio_pin_number):
        self.ESC = gpio_pin_number
        self.pi = pigpio.pi()
        self.pi.set_servo_pulsewidth(self.ESC, 1500)

        # Max and min pulse width values of ESC
        self.max_value = 1900
        self.min_value = 1100
        self.arm()


    # Function to control the speed of the motor
    def control(self, speed):
        if speed < self.min_value:
            speed = self.min_value
        elif speed > self.max_value:
            speed = self.max_value
        self.pi.set_servo_pulsewidth(self.ESC, speed)
        

    # Function to arm Blue Robotics Basic ESC
    def arm(self):
        self.pi.set_servo_pulsewidth(self.ESC, 1500)

         
    # Function to stop every action the Pi is performing for the ESC.
    def stop(self):
        self.pi.set_servo_pulsewidth(self.ESC, 1500)
        self.pi.stop()
