# ESC Python program to run the ESC

import os
import time
# Launching GPIO library
os.system("sudo pigpiod")
# Will cause errors if this delays are removed
time.sleep(1)
import pigpio

# Connect the ESC in this GPIO pin
ESC = 4 # Change to appropriate number later

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 1500)

# Max and min pulse width values of ESC
max_value = 1900
min_value = 1100

# Funtion to control the speed of the motor; both incrementally and exactly
def control(): 
    # Initial speed: 1500 (0 m/s)
    speed = 1500
    print("How To Control The Motor: Initial speed is 1500 (translates to 0 m/s).")
    print("Enter a motor pulse width (1100-1900) or a speed to increase/decrease by.")
    print("A pulse width of 1100 and 1900 represents the fastest backwards and forwards speeds respectively")
    print("If a value between -800 and 800 is input, the value will be added to the current pulse width value, with overflows leading to the min_value or max_value")
    print("If a value between 1100 and 1900 is input, the value will become the new pulse width value")

    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()

        if inp == "stop":
            stop()
            break
        elif inp == "arm":
            arm()
            break
        else:
            try:
                inp = int(inp)
                if -800 <= inp <= 800:
                    speed += inp
                    if speed < min_value:
                        speed = min_value
                    elif speed > max_value:
                        speed = max_value
                elif 1100 <= inp <= 1900:
                    speed = inp
                pi.set_servo_pulsewidth(ESC, speed)
                print("Current speed is: ", speed)
            except:
                print("Please enter a valid command")


# Function to arm Blue Robotics Basic ESC
def arm():
    while True:
        print("Connect the battery and press Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, 1500)
            time.sleep(1)
            control()
            break
        else:
            print("Please enter a valid command")
            

# Function to stop every action the Pi is performing for the ESC.
def stop():
    pi.set_servo_pulsewidth(ESC, 1500)
    pi.stop()


# Start of the program.
while True:
    print("Type the exact word for the function you want")
    print("control OR arm OR stop")

    inp = input()
    if inp == "arm":
        arm()
    elif inp == "control":
        control()
    elif inp == "stop":
        print("Goodbye!")
        stop()
        break
    else:
        print("Please enter a valid command") 
