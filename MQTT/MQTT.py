import paho.mqtt.client as mqtt
import ssl
import time
import json

# Connection Information
broker_address = "b509faa6e72f4505a1a3885d80218fe7.s1.eu.hivemq.cloud"
broker_port = 8883  # Secure port for MQTT over TLS/SSL
topic = "App"

# Callback function for successful connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))

# Callback function for received messages
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# Create a new MQTT client instance with the correct callback API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("thanhdoo28803", "123456and7")  # Set your username and password

# Setup TLS/SSL parameters
client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the HiveMQ broker with a secure connection
client.connect(broker_address, broker_port, 60)

# Start the loop to process callbacks
client.loop_start()

# Publish data in a loop
try:
    while True:
        data = {
            "fan_on": 25,
            "light_on": 50,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        json_data = json.dumps(data)

        # Publish JSON data
        client.publish(topic, payload=json_data)
        print("Sent JSON data:", json_data)

        # Wait before sending the next set of data
        time.sleep(10)

except KeyboardInterrupt:
    print("Disconnected!")

finally:
    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()
