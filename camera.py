import cv2
import pickle
from imutils.video import WebcamVideoStream


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        self.stream = WebcamVideoStream(src=0).start()

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        image = self.stream.read()

        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        return data