
import sys
import time
import RPi.GPIO as GPIO
import pigpio
from threading import Thread

# sleep time set
INTERVAL = 1
# angle
ORIGIN = 90
ANGLE_RED = 45
ANGLE_GREEN = 135
# LED
LED_RED = 16  
LED_GREEN = 19  
# SW
SW_RED = 6
SW_GREEN = 5
# SERVO
SERVO = 18

class Servo(Thread):
    def __init__(self) -> None:
        super().__init__()
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_RED, GPIO.OUT)
        GPIO.setup(LED_GREEN, GPIO.OUT)
        GPIO.setup(SW_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        GPIO.setup(SW_GREEN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        self.pi = pigpio.pi()
        self.set_angle(ORIGIN)
        GPIO.output(LED_RED, GPIO.LOW)
        GPIO.output(LED_GREEN, GPIO.LOW)
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
        self.pi.set_servo_pulsewidth(SERVO, pulse_width)


    def run(self):
        while self.alive:
            if GPIO.input(SW_RED) == GPIO.LOW:
                print("SW_RED pushed")    
                GPIO.output(LED_RED, GPIO.HIGH)  
                self.set_angle(ANGLE_RED)
                time.sleep(INTERVAL)
                GPIO.output(LED_RED, GPIO.LOW)
                self.set_angle(ORIGIN)
            
            elif GPIO.input(SW_GREEN) == GPIO.LOW:
                print("SW_GREEN pushed")
                GPIO.output(LED_GREEN, GPIO.HIGH)  
                self.set_angle(ANGLE_GREEN)  
                time.sleep(INTERVAL)
                GPIO.output(LED_GREEN, GPIO.LOW)
                self.set_angle(ORIGIN)

            time.sleep(0.1)