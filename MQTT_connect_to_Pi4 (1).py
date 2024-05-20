import paho.mqtt.client as mqtt
import ssl

# Thay đổi với thông tin của bạn
broker_address = "broker.hivemq.com"  # Thay đổi nếu bạn có địa chỉ broker riêng
broker_port = 8883
username = "thanhdoo28803"  # Điền username của bạn nếu có
password = "123456and7"  # Điền password của bạn nếu có
topic = "App"  # Điền vào topic bạn muốn gửi tới
ca_cert_path = r"C:\path\to\your\certificate\ca.crt"# Đường dẫn đến file CA certificate của bạn nếu cần

# Khởi tạo client MQTT
# Khởi tạo client MQTT và chỉ định phiên bản callback API
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


# Đặt cấu hình username và password nếu server yêu cầu xác thực
client.username_pw_set(username, password)

# Đặt cấu hình TLS/SSL
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ca_certs=None)
#client.tls_set(ca_cert_path, tls_version=ssl.PROTOCOL_TLS)

# Định nghĩa hàm callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Đặt hàm callback khi kết nối
client.on_connect = on_connect

# Kết nối đến broker
client.connect(broker_address, port=broker_port)

# Bắt đầu loop để xử lý các callbacks
client.loop_start()

# Publish một thông điệp
client.publish(topic, "Hello HiveMQ from Python!")

# Kết thúc
client.loop_stop()
client.disconnect()
