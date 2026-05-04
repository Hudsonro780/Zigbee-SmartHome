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


# ---- Imports ----

import customtkinter
import light_presets
import button_functions


# ---- GUI development ----

class App(customtkinter.CTk):

    #preset visual settings
    customtkinter.set_default_color_theme("dark-blue")
    customtkinter.set_appearance_mode("dark") 

    #app init creation
    # need to define n_lights
    def __init__(self, title, size):
        super().__init__()

        self.title(title)
        self.geometry(size)
        self.grid_columnconfigure((0,1,2,3), weight = 1)

        # Setting Main Menu Frame
        self.menu_frame = customtkinter.CTkFrame(self)
        self.menu_frame.grid(row = 0, column = 0, columnspan = 4, sticky = "nsew", padx = 20, pady = 20)
        self.menu_frame.grid_columnconfigure((0,1,2,3), weight = 1) # weight cells

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
            command =button_functions.dashboard_menu_button
            )
        
        self.dashboard_button.grid(row = 0, column = 1, padx = 10, pady = 20, sticky = "ew")

        # CHANGE COMMANDS FOR BUTTONS WHEN MADE
        # Light Page Button
        self.light_menu_button = customtkinter.CTkButton(
            self.menu_frame, 
            text = "Lights", 
            font=customtkinter.CTkFont(size = 20), 
            command =button_functions.light_menu_button
            )
        
        self.light_menu_button.grid(row = 0, column = 2, padx = 10, pady = 20, sticky = "ew")

        # Sensor Page Button
        self.sensor_menu_button = customtkinter.CTkButton(
            self.menu_frame, 
            text = "Sensors", 
            font=customtkinter.CTkFont(size = 20), 
            command =button_functions.sensors_menu_button
            )
        
        self.sensor_menu_button.grid(row = 0, column = 3, padx = 10, pady = 20, sticky = "ew")


        # ---- Frame for Lights on Dashboard ----
        self.light_dash_frame = customtkinter.CTkFrame(self)
        self.light_dash_frame.grid(row = 2, column = 0, columnspan = 2, sticky = "nsew", padx = 20, pady = 20)


app = App("Smart Home Control", "1000x800")
app.mainloop()
