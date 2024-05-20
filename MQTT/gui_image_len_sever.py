
import paho.mqtt.client as mqtt
import cv2
import base64
import time
import ssl
# Thông tin broker và topic
broker_address = "b509faa6e72f4505a1a3885d80218fe7.s1.eu.hivemq.cloud"
broker_port = 8883  # Secure port for MQTT over TLS/SSL
topic = "Image"

# Hàm gọi lại khi kết nối thành công
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))

# Hàm gọi lại khi nhận phản hồi từ broker
def on_publish(client, userdata, mid):
    print("Message Published...")


# Tạo và cấu hình client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("thanhdoo28803", "123456and7")  # Set your username and password
client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker_address, broker_port, 60)
client.loop_start()

# Đọc và mã hóa hình ảnh
image_path = "light_detect.jpg"
image = cv2.imread(image_path)
image_resized = cv2.resize(image, (640, 480))  # Giảm độ phân giải
_, buffer = cv2.imencode('.jpg', image_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  # Giảm chất lượng
jpg_as_text = base64.b64encode(buffer).decode('utf-8')

# Gửi hình ảnh
client.publish(topic, jpg_as_text)

# Đợi cho đến khi tin nhắn được gửi xong
time.sleep(1)
print(jpg_as_text)
# Ngắt kết nối và dừng loop
client.loop_stop()
client.disconnect()
