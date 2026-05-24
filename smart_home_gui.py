# ---- Header ----
#
# Developer - Robert Hudson
# Contact:
#   Email: rhudsonprojectsoutlook.com
#   GitHub:

# ---- Description ----
""" This program develops the GUI to control a Zigbee smart home system
    The GUI allows control of:
        Tradfri Light Bulb

    More to be added in the future """

# --- Variables ----

"""
menu_frame = Nav Button Frame
dash_frame = Dashboard Frame
lights_frame = Light Control Frame
sensors_frame = Sensor Monitor Frame
"""

# ---- Imports ----

import customtkinter
import device_presets
import button_functions as bf
import ZigbeeSetup as zs
import tkinter as tk



# ---- Zigbee Setup ----


# ---- Creation Functions ----

network = zs.Zigbee_Controller(port = 1883, broker = "localhost")


# ---- App GUI Creation Functions ----
def create_op_frame(app, dictionary, frame_id):
    """
    function that creates a frame at a PREDETERMINED grid spot below the predetermined menu frame
    attaches frame name to frame dictionary - dictionary{}

    CALL: create_op_frame(self, self.dictionaryName, frame_id)
    """

    frame = customtkinter.CTkFrame(app)
    frame.grid(row = 1, column = 0, columnspan = 4, sticky = "nsew", padx = 20, pady = 20)
    frame.configure(corner_radius = 5)
    dictionary[frame_id] = frame

    return frame




# ---- GUI development ----

class App(customtkinter.CTk):

    #preset visual settings
    customtkinter.set_default_color_theme("dark-blue")
    customtkinter.set_appearance_mode("dark") 



    #app init creation
    # need to define n_lights
    def __init__(self, title, size):
        super().__init__()


        # Frame Dictionary
        self.operation_frames = {}

        self.title(title)
        self.geometry(size)
        self.grid_columnconfigure((0,1,2,3,4,5), weight = 1)
        self.grid_rowconfigure(0, weight = 0)
        #self.grid_rowconfigure(1, weight=1)

# ---- Main Menu Frame - Top of Page ---

        self.top_frame = customtkinter.CTkFrame(self)
        self.top_frame.grid(row = 0, column = 0, columnspan = 4, sticky = "nsew", padx = 20, pady = 20)
        self.top_frame.grid_columnconfigure((0,1,2,3,4,5), weight = 1) # weight cells

        # top right frames for network.
        self.network_connect_frame = customtkinter.CTkFrame(self.top_frame)
        self.network_connect_frame.grid(row=0, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
        
        self.network_disconnect_frame = customtkinter.CTkFrame(self.top_frame)
        self.network_disconnect_frame.grid(row=0, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")

        # Menu strip
        self.menu_frame = customtkinter.CTkFrame(self.top_frame)
        self.menu_frame.grid(row=0, column = 2, columnspan = 4, padx = 20, pady = 20, sticky = "nsew")
        self.menu_frame.grid_columnconfigure((0,1,2,3), weight = 1)

        # Connect to Network Button
        self.network_connect_button = customtkinter.CTkButton(
            self.network_connect_frame, text="Connect", 
            command=lambda: bf.connect_button(self, self.network_disconnect_frame, network) # Connects the zigbee network + raises disconnect button
            )
        self.network_connect_button.grid(row=0,column=0,padx = 20, pady = 20)
        # connected text
        self.connected_label = customtkinter.CTkLabel(
            self.network_connect_frame, text = "Disconnected", 
            font=customtkinter.CTkFont(size = 25, weight = "bold"), 
            fg_color="transparent"
            )
        self.connected_label.grid(row = 0, column = 1, padx = 10, pady = 20, sticky = "ew")

        # disconnect from network button
        self.network_disconnect_button = customtkinter.CTkButton(
            self.network_disconnect_frame, 
            text = "Disconnect",
            command = lambda: bf.disconnect_button(self, self.network_connect_frame, network)
            )
        self.network_disconnect_button.grid(row=0,column=0,padx = 20, pady = 20)


        # disconnected text
        self.disconnected_label = customtkinter.CTkLabel(
            self.network_disconnect_frame, text = "Connected", 
            font=customtkinter.CTkFont(size = 25, weight = "bold"), 
            fg_color="transparent"
            )
        self.disconnected_label.grid(row = 0, column = 1, padx = 10, pady = 20, sticky = "ew")

        # Text Label
        self.menu_text = customtkinter.CTkLabel(
            self.menu_frame, text = "Page Selection", 
            font=customtkinter.CTkFont(size = 30, weight = "bold"), 
            fg_color="transparent"
            )
        
        self.menu_text.grid(row = 0, column = 0, padx = 5, pady = 20, sticky = "ew")


        # Dashboard button - Return to home screen
        self.dashboard_button = customtkinter.CTkButton(
            self.menu_frame,
            text = "Dashboard",
            font=customtkinter.CTkFont(size = 20), 
            command =lambda: bf.frame_button(self, self.operation_frames, "Dashboard")
            )
        
        self.dashboard_button.grid(row = 0, column = 1, padx = 10, pady = 20, sticky = "ew")

        # Light Page Button
        self.light_menu_button = customtkinter.CTkButton(
            self.menu_frame, 
            text = "Lights", 
            font=customtkinter.CTkFont(size = 20), 
            command =lambda: bf.frame_button(self, self.operation_frames, "Lights")
            )
        
        self.light_menu_button.grid(row = 0, column = 2, padx = 10, pady = 20, sticky = "ew")

        # Sensor Page Button
        self.sensor_menu_button = customtkinter.CTkButton(
            self.menu_frame, 
            text = "Sensors", 
            font=customtkinter.CTkFont(size = 20), 
            command = lambda: bf.frame_button(self, self.operation_frames, "Sensors")
            )
        
        self.sensor_menu_button.grid(row = 0, column = 3, padx = 10, pady = 20, sticky = "ew")


# ---- Data/App/Action Frames  ----

# ---- >> Dashboard Frame << ----
        # old method
        #self.dash_frame = customtkinter.CTkFrame(self)
        #self.dash_frame.grid(row = 2, column = 0, columnspan = 4, sticky = "nsew", padx = 20, pady = 20)

        dash_frame = create_op_frame(self, self.operation_frames, "Dashboard")
        dash_frame.grid_columnconfigure((0,1,2,3), weight = 1, uniform="column")


# ---- >> >> Dashboard - Connected Devices << << ----
        self.dash_deviceList = customtkinter.CTkFrame(dash_frame)
        self.dash_deviceList.grid(row = 0, column = 0, padx = 20, pady = 20, columnspan = 2, sticky = "ew")
        
        self.device_list_label = customtkinter.CTkLabel(
            self.dash_deviceList, 
            text = "Connected Devices", 
            font=customtkinter.CTkFont(size = 30, weight = "bold")
        )
        self.device_list_label.grid(row = 0, column = 0, padx = 20, pady = 20,columnspan =2, sticky = "") # blank centers the text



# ---- >> >> Dashboard - Sensor Data << << ----
        self.dash_sensorData = customtkinter.CTkFrame(dash_frame)
        self.dash_sensorData.grid(row = 0, column = 2, padx = 20, pady = 20, columnspan = 2, sticky = "ew")

        self.dash_sensorData_Label = customtkinter.CTkLabel(
            self.dash_sensorData, 
            text = "Sensor Data", 
            font=customtkinter.CTkFont(size = 30, weight = "bold")
        )
        self.dash_sensorData_Label.grid(row = 0, column = 0, padx = 20, pady = 20, columnspan = 2, sticky = "")


        # ---- >> Light Control Frame << ----
        light_frame = create_op_frame(self, self.operation_frames, "Lights")
        light_frame.grid_columnconfigure(0, weight = 1)  # device list column
        light_frame.grid_columnconfigure(1, weight = 2)  # controls column
        light_frame.grid_rowconfigure(1, weight = 1)

        #light_frame.grid_columnconfigure((0,1,2,3), weight = 1)
        
        light_label = customtkinter.CTkLabel(light_frame, text = "Light Control", font=customtkinter.CTkFont(size = 30, weight = "bold"))
        light_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        # ---- >> >> Light control device list << << ----
        self.light_device_frame = customtkinter.CTkFrame(light_frame)
        self.light_device_frame.grid(row = 1, column = 0, padx =(20,10), pady = 10, sticky = "nsew")
        self.light_device_frame.grid_columnconfigure(0, weight = 1)

        self.light_list_title = customtkinter.CTkLabel(self.light_device_frame, text = "Lights", font=customtkinter.CTkFont(size=20, weight = "bold"))
        self.light_list_title.grid(row=0, column = 0, padx = 10, pady = 10)

        #tracking selected light to edit ----
        self.selected_light = None
        self.light_buttons = {}

        # ---- >> >> light controls panel << << ----
        # on the right side of the page, selected light will be chosen and updated based on these

        self.light_controls_frame = customtkinter.CTkFrame(light_frame)
        self.light_controls_frame.grid(row=1, column = 1, padx = (10,20), pady = 10, sticky = "nsew")
        self.light_controls_frame.grid_columnconfigure(0, weight =1 )

        self.light_controls_title = customtkinter.CTkLabel(self.light_controls_frame, text = "Settings", font=customtkinter.CTkFont(size=20, weight = "bold"))
        self.light_controls_title.grid(row=0, column = 0, padx = 10, pady = 10)



        # ---- >> Sensor Frame << ----
        # WIP - No sensors to populate or test
        sensor_frame = create_op_frame(self, self.operation_frames, "Sensors")
        sensor_frame.grid_columnconfigure((0,1,2,3), weight = 1)
        sensor_label = customtkinter.CTkLabel(sensor_frame, text = "Sensor Monitor", font=customtkinter.CTkFont(size = 30, weight = "bold"))
        sensor_label.grid(row = 3, column = 2, padx = 20, pady = 20, columnspan = 2, sticky = "w")


        


        # at end of init, raise dashboard frame as main hub
        self.operation_frames["Dashboard"].tkraise()
        self.network_connect_frame.tkraise()

    def list_devices(self,network):
        """
        to be called when pressing the connect button

        integrated into the button_functions.py

        Method designed to accomplish two tasks
        1 - clearing widgets from the device list on the dashbaord
        2 - creating new widgets for each device in the device list
        """
        for widget in self.dash_deviceList.winfo_children():
            if widget != self.device_list_label:
                widget.destroy()
        
        # retreiving friendly device names - pulling from master df
        devices = network.getdevices_names()

        for i,name in enumerate(devices):
            device_block = customtkinter.CTkFrame(self.dash_deviceList)
            device_block.grid(row = i+1, column = 0, columnspan = 2, padx=10,pady = 10, sticky = "nsew")

            label = customtkinter.CTkLabel(device_block, text = name, anchor = "w")
            label.grid(row=0, column=0, padx=10, pady=10, sticky = "nsew")

            #pulling device details and current status
            device_status = network.get_state(name)
            print(device_status)
            if device_status:
                device_status_text = device_status.get("state", "Unknown")
            else:
                device_status_text = "Unknown" #fallback

            status_block = customtkinter.CTkLabel(device_block, text = device_status_text)
            status_block.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "e")

            device_block.grid_columnconfigure(0, weight=1)




    def populate_light_list(self, network):
        """
        Called after connecting to network (alongside list_devices).
        Populates the light page device list with only light-type devices.
        """
        # clear previous entries (keep the header label)
        for widget in self.light_device_frame.winfo_children():
            if widget != self.light_list_title:
                widget.destroy()

        self.light_buttons = {}
        self.selected_light = None
        lights = network.get_lights()

        for i, name in enumerate(lights):
            state = network.get_state(name)
            state_text = state.get("state", "Unknown") if state else "Unknown"

            btn = customtkinter.CTkButton(
                self.light_device_frame,
                text=f"{name}  —  {state_text}",
                font=customtkinter.CTkFont(size=14),
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray75", "gray30"),
                command=lambda n=name: self.select_light(n, network)
            )
            btn.grid(row=i + 1, column=0, padx=5, pady=2, sticky="ew")
            self.light_buttons[name] = btn

        # clear controls since device list just refreshed
        self.clear_light_controls()

    def select_light(self, device_name, network):
        """Highlight the selected device and build its controls."""
        # reset all button colors
        for name, btn in self.light_buttons.items():
            btn.configure(fg_color="transparent")

        # highlight selected
        self.light_buttons[device_name].configure(fg_color=("gray70", "gray35"))
        self.selected_light = device_name

        self.build_light_controls(device_name, network)

    def clear_light_controls(self):
        """Reset the controls panel to its empty state."""
        for widget in self.light_controls_frame.winfo_children():
            widget.destroy()

        self.controls_label = customtkinter.CTkLabel(
            self.light_controls_frame, text="Select a light to control",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.controls_label.grid(row=0, column=0, padx=20, pady=20)

    def build_light_controls(self, device_name, network):
        """Build controls dynamically based on what features the light supports."""
        for widget in self.light_controls_frame.winfo_children():
            widget.destroy()

        features = network.get_light_features(device_name) #tracking availible features for light selected
        state = network.get_state(device_name) or {} # load current state
        row = 0

        # Device header
        name_label = customtkinter.CTkLabel(
            self.light_controls_frame, text=device_name,
            font=customtkinter.CTkFont(size=22, weight="bold")
        )
        name_label.grid(row=row, column=0, padx=20, pady=(20, 10))

        # row control for feature controls. 
        # have to dunamically update in the foor loop
        row += 1 

        # power control
        if "state" in features:
            current_state = state.get("state", "OFF") #default off
            self.state_var = customtkinter.StringVar(value = current_state) #set start state for switch

            # setting switch 
            state_switch = customtkinter.CTkSwitch(
                self.light_controls_frame,
                text = "ON / OFF",
                font=customtkinter.CTkFont(size=16),
                variable = self.state_var, #val
                onvalue = "ON", 
                offvalue = "OFF",
                command=lambda: network.send_command(device_name, {"state": self.state_var.get()})
            )
            state_switch.grid(row=row, column=0, padx=20, pady=15)
            row += 1

        # brightness control - making slider
        if "brightness" in features:
            current_brightness = state.get("brightness", 128)

            bright_label = customtkinter.CTkLabel(self.light_controls_frame, text="Brightness",font=customtkinter.CTkFont(size=16))
            bright_label.grid(row=row, column=0, padx=20, pady=(15, 0))
            row += 1

            self.brightness_slider = customtkinter.CTkSlider(
                self.light_controls_frame,
                from_= 0, 
                to = 254,
                number_of_steps= 254,
                command = lambda val: network.send_command(device_name, {"brightness": int(val)})
            )
            self.brightness_slider.set(current_brightness)
            self.brightness_slider.grid(row=row, column=0, padx=20, pady=(5, 15), sticky="ew")
            row += 1

        # color warmth presets (cool-warm type shii)
        if "color_temp" in features:
            preset_label = customtkinter.CTkLabel(
                self.light_controls_frame, 
                text="Presets",
                font=customtkinter.CTkFont(size=16)
            )
            preset_label.grid(row=row, column=0, padx=20, pady=(15, 5))
            row += 1

            preset_frame = customtkinter.CTkFrame(self.light_controls_frame, fg_color="transparent")
            preset_frame.grid(row=row, column=0, padx=20, pady=(0, 20))

            presets = {"Warm": 370, "Neutral": 250, "Cool": 160}
            for col, (label, temp_val) in enumerate(presets.items()):
                customtkinter.CTkButton(
                    preset_frame, 
                    text = label, 
                    width = 80,
                    command = lambda t=temp_val: bf._apply_preset(self, device_name, t, network) # added button commands to bf
                ).grid(row=0, column=col, padx=5, pady=5)









def on_closing():
    """
    Auto closing the Zigbee network and halts app when closing window
    Added redundancy if never connected
    """
    try:
        network.disconnect()
    except Exception:
        pass
    
    try:
        zs.process.terminate()
        zs.process.wait(timeout=3)
    except Exception:
        pass

    app.destroy()



app = App("Smart Home Control", "1000x800")
# forcing auto cleanup
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
