#USBカメラを使用します
import cv2

class UsbCamera():
    def __init__(self):
        pass

    def capture(self):
        # カメラを起動
        cap = cv2.VideoCapture(0)  # カメラIDを変更して試してください
        if not cap.isOpened():
            print("カメラが見つかりません")
            return None

        print("カメラが起動しました。Sキーを押して撮影します。")

        while True:
            # フレームを読み込む
            ret, frame = cap.read()
            if not ret:
                print("フレームの読み込みに失敗しました")
                break

            # フレームを表示
            cv2.imshow('Camera', frame)

            # キーボードの入力を待つ
            key = cv2.waitKey(1) & 0xFF

            # 's'キーが押された場合、フレームをnumpy配列として返す
            if key == ord('s'):
                print("撮影されました")
                cap.release()
                cv2.destroyAllWindows()
                return frame

            # 'q'キーが押された場合、終了
            elif key == ord('q'):
                print("プログラムを終了します")
                break

        # カメラとウィンドウを解放
        cap.release()
        cv2.destroyAllWindows()
        return None
