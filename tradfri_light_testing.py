

# ---- packages ----

import paho.mqtt.client as mqtt
import json
import time

# ---- Config ----

broker = "localhost"
port = 1883
light = "office_lamp"

topic = f"zigbee2mqtt/{light}/set" # sending commands
monitor_topic = f"zigbee2mqtt/{light}" # updates to system for current status

# ---- MQTT process functions ----

def on_connect(client, userdata, flags, code, properties):
    """Called when connected to MQTT intermedate to ID current state of light"""
    print(f"Connected to MQTT with code {code}")
    client.subscribe(monitor_topic)
    print(f"listening for updates on {monitor_topic}")

def on_message(client,userdata, msg):
    """Called when an update is received from MQTT. Updating the status of the light."""

    payload = json.loads(msg.payload)
    print(f"Received update: {payload}")
    if "state" in payload:
        state = payload["state"]
        print(f"Light is currently: {state}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to {broker}:{port}")
client.connect(broker, port)

client.loop_start() # Running listen in background
time.sleep(4)

# Turn on
client.publish(topic, json.dumps({"state": "ON"}))
time.sleep(1)
print("Light ON")
time.sleep(4)

# Set brightness to 50% (value is 1-254)
client.publish(topic, json.dumps({"brightness": 127}))
time.sleep(1)
print("Brightness 50%")
time.sleep(4)

# Set color to red
client.publish(topic, json.dumps({"color": {"r": 255, "g": 0, "b": 0}}))
time.sleep(1)
print("Color: Red")
time.sleep(4)

# Set color to blue
client.publish(topic, json.dumps({"color": {"r": 0, "g": 0, "b": 255}}))
time.sleep(1)
print("Color: Blue")
time.sleep(4)

# Set color to green
client.publish(topic, json.dumps({"color": {"r": 0, "g": 255, "b": 0}}))
time.sleep(1)
print("Color: Green")
time.sleep(2)

# Set warm white color temperature
client.publish(topic, json.dumps({"color_temp": 400}))
time.sleep(1)
print("Warm white")
time.sleep(4)

# Set warm white color temperature
client.publish(topic, json.dumps({"color_temp": 153}))
time.sleep(1)
print("white")
time.sleep(4)

# Turn off
client.publish(topic, json.dumps({"state": "OFF"}))
time.sleep(1)
print("Light OFF")

client.loop_stop()
client.disconnect()