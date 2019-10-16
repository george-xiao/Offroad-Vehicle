from bluedot import BlueDot
from ESC import ElectronicSpeedController
from servo_motor import ServoMotor
from signal import pause

bd = BlueDot()
running = True
# pin 13 for GPIO 27
robot = ElectronicSpeedController(27)
# pin 12
servo = ServoMotor(12)

# Function to move and steer the car
# Uses the distance of the touch from the center of the Dot to determine the car's speed
# Uses the placement of the finger to determine steering direction
# Uses the angle from 0 degrees to determine how hard to steer
def move(pos):
    if running:
        servo.set_angle(pos.angle)
        robot.control(1500 + pos.y * 400)


# Function to stop the motor
# Will stop all motors as soon as there is not input detected from the Blue Dot
def stop():
    robot.control(1500)


# Function to toggle between power on and power off
# Double tap to toggle between the power states
# Power on: Button will be blue
# Power off: Button will be red
def power_button():
    global running
    running = not running
    if running:
        bd.color = 'blue'
    else:
        bd.color = 'red'


# Allows pairing of other devices for a minute after startup
bd.allow_pairing(60)
    
bd.set_when_pressed(move)
bd.set_when_moved(move)
bd.set_when_released(stop)
bd.set_when_double_pressed(power_button)

pause()
