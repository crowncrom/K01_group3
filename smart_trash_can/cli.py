from .usb_camera import UsbCamera

def execute():
    main()
    
def main():
    print('This is smart trash can!')
    cam = UsbCamera()
    cam.capture()