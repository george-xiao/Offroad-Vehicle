#Main changes:
#   i) added try and catches whenever int casting was done
#  ii) got rid of calibration as our ESC does not (cannot?) perform one
# iii) changed arm to work with our current ESC
#Notes:
#   i) we could get rid of manual drive as it is just a more restrictive control after the changes that you made
#  ii) imo we can just automatically run arm at first with enter and switch to control after that...really dont need to give user any more option after that 
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
ESC = 4 #Change to appropriate number later

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) #Really dont know what this means...the numbers have to be between 1100 and 1900...maybe arm here instead?

# Max and min pulse width values of ESC
max_value = 1900
min_value = 1100
print("Type the exact word for the function you want")
print("manual OR control OR arm OR stop")


# Manually program your ESC if required (Kinda pointless cuz our control already does this)
def manual_drive():
    print("You have selected manual option so provide a value between 1100 and 1900")
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
            try:
                inp = int(inp)
                if inp < min_value:
                    inp = min_value
                elif inp > max_value:
                    inp = max_value
                pi.set_servo_pulsewidth(ESC, inp)
                print("Current speed is: " + inp)
            except:
                print("Please enter a valid command")

def control(): 
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
        else:
            try:
                inp = int(inp)
                if -800 <= inp <= 800:
                    speed += inp
                    if speed < min_value:
                        speed = min_value
                    elif speed > max_value:
                        speed = max_value
                elif 1100 <= int(inp) <= 1900:
                    speed = input
                pi.set_servo_pulsewidth(ESC, speed)
                print("Current speed is: " + speed)
            except:
                print("Please enter a valid command")


# This is how to arm our ESC
def arm():
    print("Connect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 1500)
        time.sleep(1)
        control() 


# This will stop every action your Pi is performing for the ESC.
def stop():
    pi.set_servo_pulsewidth(ESC, 1500)
    pi.stop()


# This is the start of the program.
inp = input()
if inp == "manual":
    manual_drive()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("You entered an invalid command, you must now restart the program :(") #Very good use of emojis...PogS
