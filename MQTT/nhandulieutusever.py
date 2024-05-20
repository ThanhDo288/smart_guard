import paho.mqtt.client as mqtt
import ssl

# Thông tin broker và topic
broker_address = "fb2dad0fb9ac431fae740d27419cc35d.s1.eu.hivemq.cloud"
broker_port = 8883  # Secure port for MQTT over TLS/SSL
username = "thanhdoo28803"  # Điền username của bạn nếu có
password = "123456and7"  # Điền password của bạn nếu có
topic = "Image"

# Hàm gọi lại khi kết nối thành công
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)  # Đăng ký nhận tin nhắn từ topic

# Hàm gọi lại khi nhận được tin nhắn
def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + ": " + str(msg.payload.decode("utf-8")))

# Tạo và cấu hình client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username, password)

client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)

client.on_connect = on_connect
client.on_message = on_message  # Set callback function for message reception
client.connect(broker_address, broker_port, 60)

# Bắt đầu vòng lặp để xử lý các callback
client.loop_forever()
