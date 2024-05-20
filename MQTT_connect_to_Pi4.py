import paho.mqtt.client as mqtt

# Thông tin kết nối
broker = 'broker.hivemq.com'
port = 1883
topic = "App"

# Hàm callback khi client kết nối tới server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

# Hàm callback khi nhận được tin nhắn từ server
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# Khởi tạo client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Kết nối tới broker
client.connect(broker, port, 60)

# Gửi dữ liệu
client.publish(topic, "Hello from Raspberry Pi")

# Vòng lặp để xử lý các callback
client.loop_forever()
