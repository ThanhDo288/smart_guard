import cv2
import numpy as np

backSub = cv2.createBackgroundSubtractorMOG2()

capture = cv2.VideoCapture('test.mp4')

while True:
    _, frame = capture.read()
    if not _:
        break

    fgMask = backSub.apply(frame)
    fgMask = cv2.cvtColor(fgMask, 0)

    kernel = np.ones((5, 5), np.uint8)
    fgMask = cv2.erode(fgMask, kernel, iterations=1)
    fgMask = cv2.dilate(fgMask, kernel, iterations=1)
    fgMask = cv2.GaussianBlur(fgMask, (3, 3), 0)
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
    _, fgMask = cv2.threshold(fgMask, 130, 255, cv2.THRESH_BINARY)

    fgMask = cv2.Canny(fgMask, 20, 200)
    contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        (x, y, w, h) = cv2.boundingRect(contours[i])
        area = cv2.contourArea(contours[i])
        if area > 300:
            cv2.drawContours(fgMask, contours[i], 0, (0, 0, 255), 6)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)

    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
