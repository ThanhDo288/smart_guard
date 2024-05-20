import cv2
from picamera2 import Picamera2
import time
import json
from roboflow import Roboflow

# Initialize Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Initialize Roboflow
rf = Roboflow(api_key="jRJfDI9kcN7jQh83c9tj")
project = rf.workspace().project("light_fan")
model = project.version("4").model

# Capture image from camera
image = picam2.capture_array()
cv2.imwrite('/home/pi/image.jpg', image)
print("Image captured and saved.")

# Close camera preview
cv2.destroyAllWindows()
picam2.stop()

image_path = "/home/pi/image.jpg"


# Predict using Roboflow
prediction_results = model.predict(image_path, confidence=40, overlap=30).json()

predicted_image_path = image_path.replace(".jpg", "-prediction.jpg")

model.predict(image_path, confidence=40, overlap=30).save(predicted_image_path)

# Save prediction results to JSON
json_file_path = image_path.replace(".jpg", ".json")
with open(json_file_path, 'w') as json_file:
    json.dump(prediction_results, json_file, indent=4)

print("Saved predicted image and JSON results.")

# Print prediction results
for prediction in prediction_results['predictions']:
    obj_class = prediction['class']
    x = prediction['x']
    y = prediction['y']
    width = prediction['width']
    height = prediction['height']
    confidence = prediction['confidence']
    print(f"Class: {obj_class}, X: {x}, Y: {y}, Width: {width}, Height: {height}, Confidence: {confidence:.2f}")
