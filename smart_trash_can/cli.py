from .servo import Servo
from .usb_camera import UsbCamera

def execute():
    main()
    
def main():
    print('This is smart trash can!')
    servo = Servo()
    cam = UsbCamera()
    cam.capture()