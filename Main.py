import tkinter as tk
from tkinter import messagebox
import requests
import folium
import paho.mqtt.client as mqtt
import json
from EncryptUnecryptData import encryptdata
from LoginAuthenticationSystem import login_window

# MQTT Configuration
broker_address = "mqtt.example.com"
broker_port = 1883
username = "your_username"
password = "your_password"
auth_topic = "plane/auth"
tracking_topic = "plane/tracking"

# Function to handle connection to MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to topics
    client.subscribe(auth_topic)
    client.subscribe(tracking_topic)

# Function to handle receiving messages from MQTT broker
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload.decode()))
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

# Function to open MQTT client
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

def planeInfo():
    # Aviation Stack API key
    api_key = '6028486d33c86158f4d7913afe8931d0'
    base_url = 'http://api.aviationstack.com/v1/flights'

    # Flight IATA code
    flight_iata_code = 'UA951'

    # Make a request to get flight data
    params = {'access_key': api_key, 'flight_iata': flight_iata_code}
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        flight_data = response.json()['data'][0]

        # Print the entire response to inspect its structure
        print("Flight Data:", flight_data)

        # Attempt to access the flight track information
        try:
            flight_track = flight_data['flight']['flight_track']

            # Display the flight track on a map using Folium
            map_center = [flight_track['latitude'], flight_track['longitude']]
            my_map = folium.Map(location=map_center, zoom_start=8)

            # Add markers for the flight track
            for point in flight_track['data']:
                folium.Marker(location=[point['latitude'], point['longitude']], popup=f"Altitude: {point['altitude']}", icon=folium.Icon(color='blue')).add_to(my_map)

            # Save the map to an HTML file or display it
            my_map.save('flight_track_map.html')
            print("Flight track map saved to 'flight_track_map.html'")

        except KeyError:
            print("Flight track information not found in the response.")
    else:
        print(f"Failed to retrieve flight data. Status Code: {response.status_code}")
        print(response.text)

    return flight_iata_code, flight_data

def weather(api_key, country):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': country,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        weatherData = response.json()
        cityName = weatherData['name']
        temperature = weatherData['main']['temp']
        weatherDescription = weatherData['weather'][0]['description']
        
        print(f"Weather in {cityName}:")
        print(f"Temperature: {temperature}°C")
        print(f"Description: {weatherDescription}")
    else:
        print(f"Failed to retrieve weather data. Status Code: {response.status_code}")
        print(response.text)

def login():
    username = login_window.username_entry.get()
    password = login_window.password_entry.get()

    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        open_mqtt_client()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def plane_tracking_labels(flightdate, flightstatus, departure, airport, timezone, terminal, gate, delay, scheduled, estimated, arrivaldestination, timezone2, terminal2, gate2):
    flight_date = tk.Label(window, text=flightdate)
    flight_date.pack()

    flightstatus_label = tk.Label(window, text=flightstatus)
    flightstatus_label.pack()

    departure_label = tk.Label(window, text=departure)
    departure_label.pack()

    airport_label = tk.Label(window, text=airport)
    airport_label.pack()

    timezone_label = tk.Label(window, text=timezone)
    timezone_label.pack()

    terminal_label = tk.Label(window, text=terminal)
    terminal_label.pack()

    gate_label = tk.Label(window, text=gate)
    gate_label.pack()

    delay_label = tk.Label(window, text=delay)
    delay_label.pack()

    scheduled_label = tk.Label(window, text=scheduled)
    scheduled_label.pack()

    estimated_label = tk.Label(window, text=estimated)
    estimated_label.pack()

    arrival_destination_label = tk.Label(window, text=arrivaldestination)
    arrival_destination_label.pack()

    arrival_ = tk.Label(window, text="arrival :")
    arrival_.pack()

    timezone2_label = tk.Label(window, text=timezone2)
    timezone2_label.pack()

    terminal2_label = tk.Label(window, text=terminal2)
    terminal2_label.pack()

    gate2_label = tk.Label(window, text=gate2)
    gate2_label.pack()

def weather_labels(country):
    api_key = 'a90c4182b3d6f0099ca68e53d0b06386'
    country = country

    blank = tk.Label(window, text="")
    blank.pack()

    country_label = tk.Label(window, text=f"Weather in {country}:")
    country_label.pack()

    Temperature_label = tk.Label(window, text=f"Temperature: {temperature} °C ")
    Temperature_label.pack()

    Description_label = tk.Label(window, text=f"Description: {weatherDescription}")
    Description_label.pack()

    encryptdata(f"Weather in {country}:")
    encryptdata(f"Temperature: {temperature} °C ")
    encryptdata(f"Description: {weatherDescription}")

    save_button = tk.Button(window, text="Save Information", command=lambda: encryptdata)
    save_button.pack()

# Main GUI window
window = tk.Tk()
window.geometry("1280x720")
window.title("Flight Information")

# Example weather information
weather_labels("England")

# Run the main event loop
window.mainloop()
