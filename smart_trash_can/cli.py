from .servo import Servo
from .usb_camera import UsbCamera
import json

def execute():
    main()
    
def main():
    print('This is smart trash can!')
    json_file = open('config.json', 'r')
    config  = json.load(json_file)
    servo = Servo(config["servo"])
    cam = UsbCamera(config["camera"]) 
    cam.capture()