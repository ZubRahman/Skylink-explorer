import tkinter as tk
from tkinter import *
import requests
import folium
import paho.mqtt.client as paho
from paho import mqtt


def plane_tracking_labels(flightDetails,country):
    api_key = 'a90c4182b3d6f0099ca68e53d0b06386'  # api key
    weather_function = weather(api_key, country)  # calls the function

    flightDetails_label = Label(window, text=flightDetails)
    #WeatherDetails_label = Label(window, text=weather_function)
    WeatherDetails_label = Label(window, text=weather_function)
    save = Button(window, text="save information", command=lambda: hashdata(flightDetails_label,WeatherDetails_label))

    for pack_ in (flightDetails_label,WeatherDetails_label, save):
        pack_.pack()

def weather(api_key, country):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'  # url for the OpenWeatherMap api

    # parameters for the api request
    params = {
        'q': country,  # name of country
        'appid': api_key,  # api key
        'units': 'metric'  # units of the temp
    }

    # Make a GET request to the API
    response = requests.get(base_url, params=params)  # request to the API

    if response.status_code == 200:  # checks to see if the request was successful
        weatherData = response.json()  # Parse the JSON response

        # relevant weather information
        cityName = weatherData['name']
        temperature = weatherData['main']['temp']
        weatherDescription = weatherData['weather'][0]['description']

        cn = f"Weather in {cityName}:"
        tp = f"Temperature: {temperature}°C"
        wd = f"Description: {weatherDescription}"

        #return weatherData
        return cn,tp,wd

        # weather info
        print(f"Weather in {cityName}:")
        print(f"Temperature: {temperature}°C")
        print(f"Description: {weatherDescription}")
    else:
        print(
            f"Failed to retrieve weather data. Status Code: {response.status_code}")  # fail message if the code doesnt work.
        print(response.text)

def login(username_entry,password_entry):
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password match
    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        root.destroy()
        #open_mqtt_client()  # Open MQTT client window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def login_window():
    # Create main window
    global root
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
    login_button = tk.Button(root, text="Login", command=lambda: login(username_entry,password_entry))
    login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Run the main event loop
    root.mainloop()

def hashdata(flightdetails, weatherdetails):
    import random
    dict = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
    newword = ""
    for x in range(len(flightdetails)):
        newword += random.choice(dict)
    try:
        file = open("data.txt", "a")
        file2 = open("Uncrypted data.txt", "a")
        try:
            file.write("\n" + newword)
            file2.write("\n" + flightdetails)
        except:
            print("something went wrong")
        finally:
            file.close()
            file2.close()
    except:
        print("something went wrong")

    for x in range(len(weatherdetails)):
        newword += random.choice(dict)
    try:
        file = open("data.txt", "a")
        file2 = open("Uncrypted data.txt", "a")
        try:
            file.write("\n" + newword)
            file2.write("\n" + weatherdetails)
        except:
            print("something went wrong")
        finally:
            file.close()
            file2.close()
    except:
        print("something went wrong")

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


#client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5, callback_api_version=1)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# Client Username and Password
client.username_pw_set("AirControl", "Password123")
# Connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("3304243d6499474ea584cbe3d25c4102.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("#", qos=1)


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
                folium.Marker(location=[point['latitude'], point['longitude']], popup=f"Altitude: {point['altitude']}",
                              icon=folium.Icon(color='blue')).add_to(my_map)

            # Save the map to an HTML file or display it
            my_map.save('flight_track_map.html')
            print("Flight track map saved to 'flight_track_map.html'")

        except KeyError:
            print("Flight track information not found in the response.")
    else:
        print(f"Failed to retrieve flight data. Status Code: {response.status_code}")
        print(response.text)

    return flight_iata_code, flight_data


flight_iata_code, flight_data = planeInfo()

client.publish(f'plane_info/{flight_iata_code}', payload=str(flight_data), qos=1)

client.loop_forever()


#create windows
login_window = login_window()
window = tk.Tk()
window.geometry("1280x720")

country = input("Enter the name of the country: ")
plane_tracking_labels(flight_data,country)

window.mainloop()
