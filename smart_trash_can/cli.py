import json
import time
import cv2
from .servo import Servo
from .usb_camera import UsbCamera
from .prediction import Prediction

def print_console_help():
    print("--- Conlole ---")
    print("c:Capture")
    print("q:Quit")

def execute():
    main()
    
def main():
    print('This is smart trash can!')
    json_file = open('config.json', 'r')
    config  = json.load(json_file)
    servo = Servo(config["servo"])
    cam = UsbCamera(config["camera"]) 
    pred = Prediction(config["prediction"])
    if config["prediction"]["isLearning"]:
        pred.learning()
    pred.load()
    cv2.namedWindow("Preview")

    while True:
        user_command = input()
        if user_command == "c":
            img_name = "k01_group03_smart-trash-can_capture_"+str(time.time())+".jpg"
            cv2.imshow('Preview', cam.capture(img_name))
            pred.prediction(img_name)
            cv2.waitKey(1000)
        elif user_command == "q":
            cam.finalize()
            servo.finalize()
            break
        else:
            print_console_help()

    print("---Bye---")