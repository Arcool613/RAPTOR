import tkinter as tk
import RPi.GPIO as gpio
from tkinter import simpledialog
import light_control
import cv2
import Car_Detection as ct
import threading
import time

gpio.setmode(gpio.BCM)
# Define the passcode
passcode = "1234"  # Change this to your desired passcode

# Define a variable to signal whether the traffic light control function should stop
stop_traffic_lights = threading.Event()

# Define a variable to keep track of whether the traffic light control function is running
traffic_lights_running = False

def start_traffic_lights():
    global traffic_lights_running
    if not traffic_lights_running:
        # Start the traffic light control function in a separate thread
        traffic_lights_thread = threading.Thread(target=light_control.light_control, args=(3600,))
        traffic_lights_thread.start()
        traffic_lights_running = True

def stop_button_click():
    if traffic_lights_running:
        # Stop the traffic light control function when the Stop button is clicked
        stop_traffic_lights.set()
        print("Stop button clicked")
    else:
        print("Traffic lights are not running.")

def light():
    light_control.light_test()
    print("Light button clicked")

def check_connected_cameras():
    build_info = cv2.getBuildInformation()
    num_cams = 0
    for line in build_info.split('\n'):
        if 'Video I/O:' in line:
            num_cams = int(line.split(':')[1].strip())

    # Display the number of connected cameras in a separate tkinter window
    camera_window = tk.Toplevel()
    camera_window.title("Connected Cameras")
    camera_label = tk.Label(camera_window, text=f"Number of connected cameras: {num_cams}")
    camera_label.pack(pady=10)

def override_traffic_lights():
    # Prompt the user for the passcode
    user_passcode = simpledialog.askstring("Passcode", "Enter the passcode:", show='*')

    if user_passcode == passcode:
        # If the passcode is correct, ask the user which lane to override
        lane_to_override = simpledialog.askinteger("Override Lane", "Enter the lane to override (1, 2, 3, or 4):")
        if lane_to_override in [1, 2, 3, 4]:
            # Stop the traffic light control function before overriding
            stop_traffic_lights.set()

            # Wait for the function to stop (you can adjust the duration as needed)
            time.sleep(2)

            # Call the function to control the traffic lights based on user input
            light_control.light_on_red(lane_to_override - 1)  # Adjust the index
            print(f"Lane {lane_to_override} is now green. Others are red.")
        else:
            print("Invalid lane number. Please enter a valid lane (1, 2, 3, or 4).")
    else:
        print("Invalid passcode. Access denied")

# Create the main window
window = tk.Tk()
window.title("Traffic Light Control")
window.geometry("300x300")

# Create the Start button
start_button = tk.Button(window, text="Start Traffic Lights", command=start_traffic_lights)
start_button.pack(pady=10)

# Create the Stop button
stop_button = tk.Button(window, text="Stop Traffic Lights", command=stop_button_click)
stop_button.pack(pady=10)

# Create the Light button
light_button = tk.Button(window, text="Light Test", command=light)
light_button.pack(pady=10)

# Create the Camera button
camera_button = tk.Button(window, text="Check Connected Cameras", command=check_connected_cameras)
camera_button.pack(pady=10)

# Create the Override button
override_button = tk.Button(window, text="Override Traffic Lights", command=override_traffic_lights)
override_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
