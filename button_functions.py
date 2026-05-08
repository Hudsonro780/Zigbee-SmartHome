################################################
#
# App Functions
#
# For smart_home_gui.py
#
# Developer: Robert Hudson
#
################################################






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


