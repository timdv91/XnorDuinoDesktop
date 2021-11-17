#!/usr/bin/python3
import _thread
import os
import time
from pathlib import Path
#from pytimedinput import timedInput

# Define a function for the thread
def runSerialServer( pThreadName):
    keepRunning = True
    while(keepRunning):
        dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))))
        app_path = dir_path + '/SerialServer/main.py'
        print(pThreadName + ":\tExecuting SerialServer application at: " + app_path + "\n")
        os.system('/home/tim/PyCharm/XnorDuinoDesktop/bin/python3.8 ' + app_path)

        print("Thread encountered an communication issue, restarting in 5 seconds...")
        #userText, timedOut = timedInput("Press any key to abort the restart.")
        #keepRunning = timedOut
        time.sleep(3)
        keepRunning = True
    print("Exiting program loop, press 'ctrl + C' to continue")
    quit()

def runFlaskGUI( pThreadName):
    dir_path = str(Path(os.path.dirname(os.path.realpath(__file__))))
    app_path = dir_path + '/FlaskGUI/main_flask.py'
    print(pThreadName + ":\tExecuting FlaskGUI application at: " + app_path + "\n")
    os.system('/home/tim/PyCharm/XnorDuinoDesktop/bin/python3.8 ' + app_path)
    #os.system('python3 ' + app_path)

# Create two threads as follows
try:
   _thread.start_new_thread( runSerialServer, ("Thread-1", ) )
   _thread.start_new_thread( runFlaskGUI, ("Thread-2", ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass