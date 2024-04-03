import tkinter as tk
from tkinter import *
#from PlaneTracker_2 import planeInfo
from EncryptUnecryptData import *
from LoginAuthenticationSystem import *


def plane_tracking_labels(flightDetails,WeatherDetails):
    flightDetails_label = Label(window, text=scheduled)
    WeatherDetails_label = Label(window, text=scheduled)

    for pack_ in (flightDetails_label,WeatherDetails_label): 
        pack_.pack()

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

    encryptdata(f"Weather in {weather(api_key, country, 1)}:")
    encryptdata(f"Temperature: {weather(api_key, country, 2)} °C ")
    encryptdata(f"Description: {weather(api_key, country, 3)}")

    save = Button(window, text="save information", command=lambda: encryptdata)
    save.pack()

def encryptdata(data):
    hashdata(data)

from LoginAuthenticationSystem import window,login
login_window = window()

window = tk.Tk()
window.geometry("1280x720")

plane_tracking_labels()

weather_labels("England")



window.mainloop()
