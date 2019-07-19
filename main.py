from bluedot import BlueDot
from ESC import ElectronicSpeedController as ESC
from signal import pause

bd = BlueDot()
robot = ElectronicSpeedController()


def move(pos):
    if pos.top:
        robot.control(1500 + pos.distance * 400)
    elif pos.bottom:
        robot.control(1500 - pos.distance * 400)
    elif pos.right:
        pass
    elif pos.left:
        pass


def stop():
    robot.control(1500)


def shutdown():
    robot.stop()


def rotate():
    robot.rotate()


bd.set_when_pressed(move)
bd.set_when_double_press(shutdown)
bd.set_when_rotated(rotate)
bd.set_when_moved(move)
bd.set_when_released(stop)

pause()