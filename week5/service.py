import geocoder
import requests

class WeatherService:


    def __init__(self, api_key):
        self.api_key = api_key

        
    def get_weather_data(self, city):
        # Check if data is present in the repository
        stored_data = self.data_repository.get_weather_data(city)
        if stored_data:
            return stored_data

        # If not, fetch data from the API
        # ... (your existing API fetching logic)
                # Get latitude and longitude for the cit
        else:
            g = geocoder.bing (city, key=self.api_key)
            results = g.json
            if results['status'] != 'OK':
                print("Error fetching weather data!")
            # Fetch weather data
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': results['lat'],
                'longitude': results['lng'],
                "hourly": "temperature_2m"
            }

            response = requests.get(url=url, params=params)
            if response.ok:
                weather_data = response.json()

            else:
                print("Error fetching weather data!")
                weather_data = None
            # Return weather data
            # TODO: Get data for closer timestamp
            data = weather_data["hourly"]["temperature_2m"] [0]
            print("Weather data fetched successfully!")

        # Store the fetched data in the repository
        self.data_repository.insert_weather_data(city, weather_data["temperature_2m"], weather_data["hourly"])

        return data
