
import sys
import time
import RPi.GPIO as GPIO
import pigpio
from threading import Thread

class Servo(Thread):
    def __init__(self, config) -> None:
        super().__init__()
        self.interval = config["interval"]
        self.led_red = config["gpio"]["led"]["red"]
        self.led_green = config["gpio"]["led"]["green"]
        self.sw_red = config["gpio"]["sw"]["red"]
        self.sw_green = config["gpio"]["sw"]["green"]
        self.angle_origin = config["angle"]["origin"]
        self.angle_red = config["angle"]["red"]
        self.angle_green = config["angle"]["green"]
        self.mortar = config["gpio"]["mortar"]
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_red, GPIO.OUT)
        GPIO.setup(self.led_green, GPIO.OUT)
        GPIO.setup(self.sw_red, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        GPIO.setup(self.sw_green, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        self.pi = pigpio.pi()
        self.set_angle(self.angle_origin)
        GPIO.output(self.led_red, GPIO.LOW)
        GPIO.output(self.led_green, GPIO.LOW)
        self.alive = True
        self.start()
        print("Servo initialized")

    def __del__(self):
        self.finalize()

    def finalize(self):
        self.alive = False
        self.join()

    def set_angle(self, angle):
        'Ensure the input angle is within the valid range (0 to 180 degrees) '
        assert 0 <= angle <= 180
    
        'Map the input angle (0 to 180 degrees) to a pulse width (500 to 2500 microseconds)'
        pulse_width = (angle / 180) * (2500 - 500) + 500
        
        'Set the servo pulse width on the specified SERVO_PIN  '
        self.pi.set_servo_pulsewidth(self.mortar, pulse_width)

    def trun_on(self, val):
        if val == 0:
            GPIO.output(self.led_red, GPIO.HIGH)
            self.set_angle(self.angle_red)
            time.sleep(self.interval)
            GPIO.output(self.led_red, GPIO.LOW)
            self.set_angle(self.angle_origin)
        elif val == 1:
            GPIO.output(self.led_green, GPIO.HIGH)
            self.set_angle(self.angle_green)
            time.sleep(self.interval)
            GPIO.output(self.led_green, GPIO.LOW)
            self.set_angle(self.angle_origin)

    def run(self):
        while self.alive:
            if GPIO.input(self.sw_red) == GPIO.LOW:
                print("self.sw_red pushed")
                trun_on(0)

            elif GPIO.input(self.sw_green) == GPIO.LOW:
                print("self.sw_green pushed")
                trun_on(1)

            time.sleep(0.1)