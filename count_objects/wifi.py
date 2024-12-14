import zmq
import cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
# SSID: lessons Pasword: robolab123
port = 5555
socket.connect("tcp://192.168.0.100:%s" % port)
cv2.namedWindow("Client recv", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("hsv", cv2.WINDOW_GUI_NORMAL)
count = 0
position = []
def on_mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        position = [y,x]
cv2.setMouseCallback("Client recv", on_mouse_callback)
flimit = 100
slimit = 200
def fupdate(value):
    global flimit
    flimit = value
def supdate(value):
    global slimit
    slimit = value
cv2.createTrackbar("F", "hsv", flimit, 255, fupdate)
cv2.createTrackbar("S", "hsv", slimit, 255, supdate)

while True:
    msg = socket.recv()
    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ret, thresh = cv2.threshold(hsv[:, :, 1], 90, 255, cv2.THRESH_BINARY)
    gray = cv2.GaussianBlur(thresh, (7, 7), 0)
    # contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = cv2.Canny(gray, flimit, slimit)
    box, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(len(box))
    # contours = cv2.Canny(gray, flimit, slimit)
    # cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)
    cv2.imshow("hsv", contours)

    if position:
        # pixel_bgr = frame[position[0], position[1]]
        pixel_hsv = hsv[position[0], position[1]]
        # print(pixel_bgr)
        cv2.circle(frame, (position[1], position[0]), 7, (255, 255, 0), 2)
        cv2.putText(frame, f"Color HSV = {pixel_hsv}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))



    key = cv2.waitKey(100)
    if key == ord('q'):
        break

    cv2.putText(frame, f"Count {count}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0), 1)

    cv2.imshow("Client recv", frame)