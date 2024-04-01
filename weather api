import requests  # import the requests module

def weather(api_key, country):
    base_url = 'http://api.openweathermap.org/data/2.5/weather' # url for the OpenWeatherMap api

    # parameters for the api request
    params = {
        'q': country,  # name of country
        'appid': api_key,  # api key
        'units': 'metric'  # units of the temp
    }

    # Make a GET request to the API
    response = requests.get(base_url, params=params) #request to the API

    
    if response.status_code == 200: # checks to see if the request was successful
        weatherData = response.json() # Parse the JSON response

        # relevant weather information
        cityName = weatherData['name']
        temperature = weatherData['main']['temp']
        weatherDescription = weatherData['weather'][0]['description']

        # weather info
        print(f"Weather in {cityName}:")
        print(f"Temperature: {temperature}°C")
        print(f"Description: {weatherDescription}")
    else:
        print(f"Failed to retrieve weather data. Status Code: {response.status_code}") # fail message if the code doesnt work.
        print(response.text)

api_key = 'a90c4182b3d6f0099ca68e53d0b06386' # api key

country = input("Enter the name of the country: ") # user input 

weather(api_key, country) # calls the function
