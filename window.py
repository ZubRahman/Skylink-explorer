import tkinter as tk
from tkinter import *
#from PlaneTracker_2 import planeInfo


window = tk.Tk()
window.geometry("1280x720")

#example
def plane_tracking_labels(flightdate, flightstatus, departure, airport, timezone, terminal, gate, delay, scheduled, estimated, arrivaldestination, timezone2, terminal2, gate2):
    flight_date = Label(window, text = flightdate)
    flight_date.pack()

    flightstatus_label = Label(window, text = flightstatus)
    flightstatus_label.pack()

    departure_label = Label(window, text = departure)
    departure_label.pack()

    airport_label = Label(window, text = airport)
    airport_label.pack()

    timezone_label = Label(window, text = timezone)
    timezone_label.pack()

    terminal_label = Label(window, text = terminal)
    terminal_label.pack()

    gate_label = Label(window, text = gate)
    gate_label.pack()

    delay = Label(window, text = delay)
    delay.pack()

    scheduled_label = Label(window, text = scheduled)
    scheduled_label.pack()

    estimated_label = Label(window, text = estimated)
    estimated_label.pack()

    arrival_destination_label = Label(window, text = arrivaldestination)
    arrival_destination_label.pack()

    #arrival

    arrival_ = Label(window, text= "arrival :")
    arrival_.pack()

    timezone2_label = Label(window, text = timezone2)
    timezone2_label.pack()

    terminal2_label = Label(window, text=terminal2)
    terminal2_label.pack()

    gate2_label = Label(window, text=gate2)
    gate2_label.pack()



def weather_labels(country):
    from weather import weather
    api_key = 'a90c4182b3d6f0099ca68e53d0b06386'  # api key
    country = country
    #weather_function = weather(api_key, country)  # calls the function

    blank = Label(window, text="")
    blank.pack()

    country = Label(window, text= f"Weather in {weather(api_key, country, 1)}:")
    country.pack()

    Temperature = Label(window, text= f"Temperature: {weather(api_key, country, 2)} °C ")
    Temperature.pack()

    Description = Label(window, text= f"Description: {weather(api_key, country, 3)}")
    Description.pack()

    security(f"Weather in {weather(api_key, country, 1)}:")
    security(f"Temperature: {weather(api_key, country, 2)} °C ")
    security(f"Description: {weather(api_key, country, 3)}")

def security(data):
    from Security import *

    hashdata(data)




# flightdate, flightstatus, departure, airport, timezone, terminal, gate, delay, scheduled, estimated, arrivaldestination, airport2, timezone2, terminal2, gate2
#example
plane_tracking_labels("2024-04-01", "scheduled", "departure:", "airport: Heathrow", "timezone: Europe/London", "terminal: 3", "gate : 7", "delay : 76",
       "scheduled: 2024-04-01T14:20:00+00:00", "estimated: 2024-04-01T14:20:00+00:00", "airport: Dubai", "timezone: Asia/Dubai", "terminal: 3", "gate: None")

weather_labels("England")

save = Button(window, text="save information", command = lambda: security)
save.pack()

window.mainloop()