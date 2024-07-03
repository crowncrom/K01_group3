import json
import time
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
    
    while True:
        user_command = input()
        if user_command == "c":
            img_name = "k01_group03_smart-trash-can_capture_"+str(time.time())+".jpg"
            cam.capture(img_name)
            pred.prediction(img_name)