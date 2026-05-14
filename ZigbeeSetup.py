# ---- Header ----
#
# Developer - Robert Hudson
# Contact:
#   Email: rhudsonprojectsoutlook.com
#   GitHub:

# ---- Description ----

# Setting up the Zigbee connection for the smarthome application in
# self.devices = []


# ---- Imports ----
import subprocess
import json
import paho.mqtt.client as mqtt
import time
import shutil

# Start
#try:
#    subprocess.Popen(['pnpm','start'], cwd = "C:\zigbee2mqtt", shell = True, creationflags=subprocess.CREATE_NEW_CONSOLE)
#except subprocess.CalledProcessError as e:
#    print(f"Error starting Zigbee2MQTT: {e}")

pnpm_dir = shutil.which("pnpm")
#process = subprocess.Popen([pnpm_dir,'start'], cwd = "C:\zigbee2mqtt", creationflags= subprocess.CREATE_NEW_CONSOLE)
process = subprocess.Popen(f'{pnpm_dir} start', cwd = "C:\zigbee2mqtt", creationflags= subprocess.CREATE_NEW_CONSOLE)



# Testing pnpm
#if process.poll is not None:
#    print(f"Process exited with code: {process.returncode}")
#    print(process.stderr.read().decode())


# ---- MQTT Processing ----

class Zigbee_Controller:

    def __init__(self, broker, port = 1883, start_topic = "zigbee2mqtt"):
        self.broker = broker
        self.port = port
        self.start_topic = start_topic
        self.devices = []
        self.states = {}
        self.received = False

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # On Connect and On Message are there to monitor device list
    # Treating Grouped devices. Singular commands later. 
    def on_connect(self,client, userdata, flags, code, properties):
        client.subscribe(f"{self.start_topic}/bridge/devices")

    # when message comes in
    def on_message(self, client, userdata, msg):
        # message on bulletin board of devices - full list
        if msg.topic == f"{self.start_topic}/bridge/devices":
            self.devices = json.loads(msg.payload)
            # device data capture flag
            self.received = True

            for device in self.devices:
                client.subscribe(f"{self.start_topic}/{device['friendly_name']}")
            return # escape, objectives reached for message on devices.

        device_name = msg.topic.removeprefix(f"{self.start_topic}/")

        try:
            payload = json.loads(msg.payload)
            self.states[device_name] = payload
            print(f"[{device_name}]{payload}")
            
        except json.JSONDecodeError:
            pass

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        self.getdevices()

    def getdevices(self, timer = 5):
        self.received = False
        self.client.publish(f"{self.start_topic}/bridge/request/devices","")
        while not self.received and timer > 0:
            time.sleep(0.1)
            timer -=0.1

    def getdevices_names(self):
        return [d["friendly_name"] for d in self.devices]
    
    def send_command(self, device_name, payload):
        self.client.publish(f"{self.start_topic}/{device_name}/set", json.dumps(payload))
        
    def get_state(self, device_name):
        return self.states.get(device_name)
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


# ---- testing ----

#controller = Zigbee_Controller(port = 1883, broker = "localhost")
#controller.connect()

# list for your GUI
#for name in controller.getdevices_names():
#   print(f"  {name}")

# Program Killing
#time.sleep(10)
#input("Newline to kill process: ")
#controller.disconnect()
#process.terminate()
#process.wait()


