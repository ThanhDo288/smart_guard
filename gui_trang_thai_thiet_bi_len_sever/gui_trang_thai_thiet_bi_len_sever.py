import cv2
import numpy as np
import json
from picamera2 import Picamera2
import paho.mqtt.client as mqtt
import ssl
import time

piCam = Picamera2()
preview_config = piCam.create_preview_configuration()
piCam.configure(preview_config)
piCam.start()

rois = []
labels = []
backSubs = []

# MQTT setup
broker_address = "mqtt-dashboard.com"
broker_port = 8883  # Secure port for MQTT over TLS/SSL
topic = "App"


def save_rois(filename="rois.json"):
    data = {'rois': rois, 'labels': labels}
    with open(filename, 'w') as f:
        json.dump(data, f)


def load_rois(filename="rois.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    rois[:] = data['rois']
    labels[:] = data['labels']
    backSubs[:] = [cv2.createBackgroundSubtractorMOG2() for _ in rois]


def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        roi = (ix, iy, x - ix, y - iy)
        label = input("Enter the label for this ROI (lamp/fan): ")
        rois.append(roi)
        labels.append(label)
        backSubs.append(cv2.createBackgroundSubtractorMOG2())
        save_rois()


if input("Do you want to load previous ROIs? (yes/no): ").lower() == 'yes':
    load_rois()
else:
    img = piCam.capture_array()
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1600, 1200)
    cv2.setMouseCallback('image', draw_rectangle)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("thanhdoo28803", "123456and7")  # Set your username and password
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
client.connect(broker_address, broker_port, 60)
client.loop_start()


def process_frame(frame):
    lamp_count = 0
    fan_count = 0
    fan_motion = 0
    for roi, label, backSub in zip(rois, labels, backSubs):
        x, y, w, h = roi
        roi_frame = frame[y:y + h, x:x + w]
        hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if label == 'lamp':
            mask = cv2.inRange(hsv, np.array([0, 0, 150]), np.array([0, 50, 255]))
            if cv2.countNonZero(mask) > 30:
                lamp_count += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, 'Light ON', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        elif label == 'fan':
            fgMask = backSub.apply(roi_frame)
            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    fan_motion += 1
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x + x1, y + y1), (x + w1 + x1, y1 + h1 + y), (255, 0, 0), 2)
                    cv2.putText(frame, 'Fan ON', (x + x1, y1 + y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            if fan_motion > 0: fan_count += 1

    return frame, lamp_count, fan_count


cv2.namedWindow('Processed Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Processed Frame', 1600, 1200)
last_time = time.time()
try:
    while True:
        frame = piCam.capture_array()
        processed_frame, lamp_count, fan_count = process_frame(frame)
        cv2.imshow('Processed Frame', processed_frame)
        currrent_time = time.time()
        if currrent_time - last_time >= 2:
            # Send the counts over MQTT
            data = {
                "lamp_on": lamp_count,
                "fan_on": fan_count,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            json_data = json.dumps(data)
            client.publish(topic, payload=json_data)
            print("Sent JSON data:", json_data)
            last_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    piCam.stop()
    cv2.destroyAllWindows()

