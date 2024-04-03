import requests
import folium
import paho.mqtt.client as paho
from paho import mqtt

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

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
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

flight_iata_code, flight_data = planeInfo()

client.publish(f'plane_info/{flight_iata_code}', payload=str(flight_data), qos=1)

client.loop_forever()
