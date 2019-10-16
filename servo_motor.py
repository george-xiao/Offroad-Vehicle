import RPi.GPIO as GPIO

max_angle = 45
min_angle = -45

class ServoMotor():

    def __init__(self, pin_num):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(pin_num, GPIO.OUT)

        self.servo = GPIO.PWM(pin_num, 50)

        self.servo.start(1.5)
        self.servo.ChangeDutyCycle(1.5)

    
    def calculate_length(self, angle):
        if angle > max_angle:
            angle = max_angle
        elif angle < min_angle:
            angle = min_angle
            
        return (-1 / 90) * angle + 1.5
    

    def calculate_cycle(self, length):
        return (length / 20) * 100
    

    def set_angle(self, angle):
        cycle = self.calculate_cycle(self.calculate_length(angle))
        self.servo.ChangeDutyCycle(cycle)
        
