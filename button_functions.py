################################################
#
# App Functions
#
# For smart_home_gui.py
#
# Developer: Robert Hudson
#
################################################


import threading
import time


# ---- Button Functions ----

def frame_button(app, dictionary, frame_id):
    """ 
    telling main app to .tkraise specified frame
    referencing the show_frame function from app class
    """
    #pass self.dictionary name in the argument to make it robust
    # in app pass:
    # command = lambda: button_functions.frame_button(self, self.operation_frames, "frame_name")
    dictionary[frame_id].tkraise()


def connect_button(app, disconnect_frame, network):
    """
    Raise the Disconnect option 
    And 
    Start the zigbee network

    Use: self.disconnect_frame is the disconnect_frame call

    Flow - Switch Frames, background starts to run network.connect(), when done it builds the list.
    """
    disconnect_frame.tkraise()

    def connect_delay():
        
        network.connect()

        time.sleep(5)
        app.after(0, lambda: app.list_devices(network))
        print(f"Device count: {len(network.devices)}")

    threading.Thread(target = connect_delay, daemon= True).start()


def disconnect_button(app, connect_frame, network):
    """
    Raise the connect option to top
    and
    Close the Zigbee network
    """

    connect_frame.tkraise()
    network.disconnect()