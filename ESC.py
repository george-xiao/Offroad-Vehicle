# ESC Python program to run the ESC
# Make sure your battery is not connected if you are going to calibrate it at first.

import os
import time
# Launching GPIO library
os.system("sudo pigpiod")
# Will cause errors if this delays are removed
time.sleep(1)
import pigpio

# Connect the ESC in this GPIO pin
ESC = 4

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) 

# Max and min pulse width values of ESC
max_value = 1900
min_value = 1100
print("If you are launching for the first time, select calibrate")
print("Type the exact word for the function you want")
print("calibrate OR manual OR control OR arm OR stop")


# Manually program your ESC if required
def manual_drive():
    print("You have selected manual option so provide a value between 0 and you max value")
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        elif inp == "arm":
            arm()
            break
        else:
            pi.set_servo_pulsewidth(ESC, inp)


# This is the auto calibration procedure of a normal ESC
def calibrate():
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery. You will here two beeps, then wait for a gradual falling tone. Once this has occurred, press Enter")
        inp = input()
        if inp == '':
            print('This process should take around 20 seconds')
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Sent pulse to ESC with a width value of " + min_value)
            time.sleep(12)
            print("Sending the next pulse with a width of 0")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("Arming ESC now, sending another pulse with a width of " + min_value)
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            control()


def control(): 
    print("Starting the motor. If it is not calibrated and armed, restart by giving 'x'")
    time.sleep(1)
    # Initial speed, 1500 = 0
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
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break
        elif -800 <= int(inp) <= 800:
            speed += inp
            if speed < min_value:
                speed = min_value
            elif speed > max_value:
                speed = max_value
        elif 1100 <= int(inp) <= 1900:
            speed = inp
        else:
            print("Please enter a valid command")


# This is the arming procedure of an ESC
def arm():
    print("Connect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        control() 


# This will stop every action your Pi is performing for the ESC.
def stop():
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()


# This is the start of the program.
inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("You entered an invalid command, you must now restart the program :(")
