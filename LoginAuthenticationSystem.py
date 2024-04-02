import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import json

# Define MQTT broker details
broker_address = "mqtt.example.com"
broker_port = 1883
username = "your_username"
password = "your_password"

# Define topics
auth_topic = "plane/auth"
tracking_topic = "plane/tracking"

# Function to handle connection to MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    # Subscribe to topics
    client.subscribe(auth_topic)
    client.subscribe(tracking_topic)

# Function to handle receiving messages from MQTT broker
def on_message(client, userdata, msg):
    print("Received message: "+msg.topic+" "+str(msg.payload.decode()))
    # Process message based on topic
    if msg.topic == auth_topic:
        handle_authorization(msg.payload)
    elif msg.topic == tracking_topic:
        handle_tracking(msg.payload)

# Function to handle plane authorization
def handle_authorization(payload):
    data = json.loads(payload)
    if data["authorized"]:
        print("Plane {} authorized for flight.".format(data["plane_id"]))
    else:
        print("Unauthorized access for plane {}.".format(data["plane_id"]))

# Function to handle plane tracking
def handle_tracking(payload):
    data = json.loads(payload)
    print("Plane {} current location: Latitude {}, Longitude {}".format(data["plane_id"], data["latitude"], data["longitude"]))

# Function to open MQTT client window
def open_mqtt_client():
    # Initialize MQTT client
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT broker
    client.connect(broker_address, broker_port)

    # Start the MQTT client loop
    client.loop_start()

    # Create MQTT client window (add your GUI code here)

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password match
    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        open_mqtt_client()  # Open MQTT client window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create main window
root = tk.Tk()
root.title("Login")

# Create username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Create password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Create login button
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Run the main event loop
root.mainloop()
