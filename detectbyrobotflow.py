import json
from roboflow import Roboflow

# Khởi tạo Roboflow với API key
rf = Roboflow(api_key="jRJfDI9kcN7jQh83c9tj")
project = rf.workspace().project("light_fan")
model = project.version(4).model

# Đường dẫn tới ảnh để dự đoán
image_path = "/home/thanhdo/iot/train2/20240513_112659.jpg"

# Thực hiện dự đoán trên ảnh
prediction_results = model.predict(image_path, confidence=40, overlap=30).json()

# Lưu hình ảnh với dự đoán
predicted_image_path = image_path.replace(".jpg", "-prediction.jpg")
model.predict(image_path, confidence=40, overlap=30).save(predicted_image_path)

# Lưu kết quả dự đoán vào file JSON
json_file_path = image_path.replace(".jpg", ".json")
with open(json_file_path, 'w') as json_file:
    json.dump(prediction_results, json_file, indent=4)

print(f"Saved predicted image to {predicted_image_path}")
print(f"Saved prediction data to {json_file_path}")

# In kết quả dự đoán
for prediction in prediction_results['predictions']:
    obj_class = prediction['class']
    x = prediction['x']
    y = prediction['y']
    width = prediction['width']
    height = prediction['height']
    confidence = prediction['confidence']
    print(f"Class: {obj_class}, X: {x}, Y: {y}, Width: {width}, Height: {height}, Confidence: {confidence:.2f}")
