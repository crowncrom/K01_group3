#USBカメラを使用します
import cv2
from threading import Thread

class UsbCamera(Thread):
    def __init__(self, config):
        super().__init__()
        self.device_id = config['deviceId']
        self.cap = cv2.VideoCapture(self.device_id)
        self.alive = True
        self.start()
        print("Camera initialized")

    def __del__(self):
        self.finalize()

    def finalize(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.alive = False
        self.join()

    def run(self):
        # カメラを起動
        if not self.cap.isOpened():
            print("カメラが見つかりません")
            return None
        print("カメラが起動しました")

        while self.alive:
            # フレームを読み込む
            ret, self.frame = self.cap.read()
            if not ret:
                print("フレームの読み込みに失敗しました")
                break

    def capture(self, img_path):
        cv2.imwrite(img_path, self.frame)
        return self.frame