# ESC Python program to run the ESC

import os
import time
# Launching GPIO library
os.system("sudo pigpiod")
# Will cause errors if this delays are removed
time.sleep(1)
import pigpio

class ESC:
# Function to control the speed of the motor; both incrementally and exactly
    def __init(self, gpio_pin_number)__:
        self.ESC = gpio_pin_number
        self.pi = pigpio.pi()
        self.pi.set_servo_pulsewidth(ESC, 1500)
        # Max and min pulse width values of ESC
        self.max_value = 1900
        self.min_value = 1100
        self.arm()


    # Function to control the speed of the motor
    def control(self, speed):
        pi.set_servo_pulsewidth(ESC, speed)


    # Function to arm Blue Robotics Basic ESC
    def arm():
        self.pi.set_servo_pulsewidth(ESC, 1500)

         
    # Function to stop every action the Pi is performing for the ESC.
    def stop():
        pi.set_servo_pulsewidth(ESC, 1500)
        pi.stop()
