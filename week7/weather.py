import sys
import requests
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta
from weather_database import WeatherDatabase
from geopy.geocoders import Photon
Latitude = "25.594095"
Longitude = "85.137566"
 

geolocator = Photon(user_agent="geoapiExercises")
Latitude = "25.594095"
Longitude = "85.137566"
 
location = geolocator.reverse(Latitude+","+Longitude)
 
# Display
#print(location)
#print(type(location))
print(type(location))
print(location.raw.keys())
print(location.raw.values())
address = location.raw['properties']

#print(address)


city = address.get('city', '')
state = address.get('state', '')
country = address.get('country', '')
code = address.get('country_code')
zipcode = address.get('postcode')
print('City : ',city)
print('State : ',state)
print('Country : ',country)
print('Zip Code : ', zipcode)

class VisualizationHandler():
    def visualize_data(self, hourly_data: dict):

        fig, ax = plt.subplots()


        ax.set_xlabel("Time (hourly)")

        ax.set_ylabel("temperature_2m")
        print(hourly_data)
        print(type(hourly_data))
        ax.plot(hourly_data["time"], hourly_data["temperature_2m"])

        plt.show()

    def utilize_data(self, hourly_data: dict, weather_db: WeatherDatabase):
            city = hourly_data.get('city', '')
            temperature = hourly_data.get('temperature_2m', [])
            time = hourly_data.get('time', [])

            # Store data in the database
            for i in range(len(time)):
                weather_db.insert_data(city, temperature[i], time[i])

            # Additional data utilization logic can be added here
            # For example, you can perform analysis on the data, generate reports, etc.

            print("Data utilization completed.")

    def analyze_data(self, weather_db: WeatherDatabase):
        # Calculate average temperature for each city
        cities = weather_db.get_all_cities()
        average_temperatures = []

        for city_info in location_lookups:
            city = city_info["name"]
            if city in cities:
                data = weather_db.get_weather_data_for_city(city)
                temperatures = [entry[2] for entry in data]  # Assuming the temperature is at index 2
                average_temperature = sum(temperatures) / len(temperatures)
                average_temperatures.append(average_temperature)
                print(f"Average temperature for {city}: {average_temperature:.2f}°C")
            else:
                print(f"No data available for {city}")

        # Plotting the bar chart
        self.plot_average_temperatures(location_lookups, average_temperatures)

    def plot_average_temperatures(self, cities, average_temperatures):
        plt.figure(figsize=(10, 6))
        plt.bar(cities, average_temperatures, color='blue')
        plt.xlabel('Cities')
        plt.ylabel('Average Temperature (°C)')
        plt.title('Average Temperature for Five Cities')
        plt.show()

class AbstractDataService:
    def get_data(self, startDate: datetime, endDate: datetime):
        raise NotImplementedError("Subclasses must implement this method")
    
    def utilize_data(self, hourly_data: dict, weather_db: WeatherDatabase):
        raise NotImplementedError("Subclasses must implement this method")

class MockedDataService(AbstractDataService):
    def get_data(self, startDatetime: datetime, endDatetime: datetime):
        # Mocked data retrieval logic
        mocked_data = {
            'time': [],
            'temperature_2m': [],
            'city': []
        }

        start_temperature = 5.0
        end_temperature = 20.0
        # Generate mocked time and temperature data
        for i in range(72):  # Assuming 72 data points based on the provided results
            time = f'2023-11-26T{str(i).zfill(2)}:00'
            temperature = round(random.uniform(start_temperature, end_temperature), 1)

            mocked_data['time'].append(time)
            mocked_data['temperature_2m'].append(temperature)
            mocked_data['city'].append("test city")

        return mocked_data
    
    def utilize_data(self, hourly_data: dict, weather_db: WeatherDatabase):
        print("we should do stuff here")
    
class APICallingService(AbstractDataService):
    def get_data(self, startDate: datetime, endDate: datetime, weather_db: WeatherDatabase):
        # Check the database for existing data first
        cached_data = weather_db.get_weather_data(self, city)
        if cached_data:
            print("Using cached data from the database.")
            return cached_data

        # If data is not found in the database, make an API call
        print("Making API call to fetch new data...")
        api_data = self.call_api(payload, url)

        if api_data:
            # Store the newly fetched data in the database
            self.utilize_data(api_data, weather_db)
            return api_data
        else:
            print("Error fetching data from API.")
            return None

    def utilize_data(self, hourly_data: dict, weather_db: WeatherDatabase):
        print("we should do stuff here")
        
    def call_api(self, payload: dict, url: str):
        try:
            r = requests.get(url, params=payload)
            r.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx status codes)
            json_data = r.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return None

        hourly_data = json_data.get("hourly", {})

        if hourly_data is None:
            print("Error: No 'hourly' data in API response.")
            return None
        # Append latitude and longitude to hourly_data
        hourly_data['latitude'] = payload.get('latitude')
        hourly_data['longitude'] = payload.get('longitude')
        Longitude = str(payload.get('longitude'))
        Latitude = str(payload.get('latitude'))
        #Is this now tightly coupled because we're using the geolocator insdie the call_api, inside the serivce API?
        #Should we put the geolocator inside a class and access it via an interface or something?
        #Figure out the city from the payload longitude + latitude
        geolocator = Photon(user_agent="geoapiExercises")
        location = geolocator.reverse(Latitude+","+Longitude)
        city = location.raw['properties']['city']
        hourly_data['city'] = city

        print("Fetching air quality data...")
        air_quality_payload = {
            'lat': payload.get('latitude'),
            'lon': payload.get('longitude'),
            'appid': 'ff8ef6c023a22aa043afef8f7e308d67'  # Replace with your API key
        }
        r = requests.get("https://api.openweathermap.org/data/2.5/air_pollution", params=air_quality_payload)
        json_air_data = r.json()
        air_data = json_air_data.get("list", {})
        #print(json_air_data)
        print(air_data)


        #hourly_data['city'].append("test city")
        # Implement logic to call the external API with the provided payload
        # Return the API response
        #return {"api_key": "api_value"}
        return hourly_data
    


class DataSourceHandler:
    def __init__(self, data_service: AbstractDataService, visualization_handler: VisualizationHandler):
        self.data_service = data_service
        self.visualization_handler = visualization_handler

    def handle_data(self, startDate: datetime, endDate: datetime, weather_db: WeatherDatabase):
        if(weather_db is None):
            print("No weather database provided")
            data = self.data_service.get_data(startDate, endDate)
        else:
            print("Weather database provided")
            data = self.data_service.get_data(startDate, endDate, weather_db)
        # Implement handling logic
        print("Handling data:")
        print(data)
        print(startDate)
        print(endDate)
        # Use the provided VisualizationHandler

        self.visualization_handler.visualize_data(data)

        # Utilize data in the database
        self.data_service.utilize_data(data, weather_db)
    
    
class DataServiceFactory:
    def create_data_service(self, service_type: str):
        if service_type == "mocked":
            return MockedDataService()
        elif service_type == "api":
            return APICallingService()
        else:
            raise ValueError("Invalid service type")
    

url = "https://api.open-meteo.com/v1/forecast"

location_lookups = [
        {
            "name": "Detroit",
            "longitude": 83.0458,
            "latitude": 42.3314
        },
        {
            "name": "Marquette",
            "longitude": 87.3956,
            "latitude": 46.5436
        },
        {
            "name": "San Jose",
            "longitude": -121.8863,
            "latitude": 37.3382
        },
        {
            "name": "Miami",
            "longitude": -80.1918,
            "latitude":  25.7617
        }
    ]

payload = {'latitude': 37.7723281,
           'longitude': -122.4530167,
           'hourly': 'temperature_2m'}



# Example usage
factory = DataServiceFactory()

# Create Mocked Data Service
#mocked_service = factory.create_data_service("mocked")
#print(f"Type of Mocked Service: {type(mocked_service)}")-
/*--

# Create API Data Service
api_service = factory.create_data_service("api")
print(f"Type of API Service: {type(api_service)}")
#print(type(datetime), "---------------")
#beginDate = datetime.now() - timedelta(days=7)
#endDate = datetime.now()

# Use DataSourceHandler to handle data from Mocked Servic-
/*--
#mocked_data_handler = DataSourceHandler(mocked_service)
#mocked_data_handler.handle_data(beginDate, endDate)

# Use DataSourceHandler to handle data from API Service
#api_data_handler = DataSourceHandler(api_service)
#api_data_handler.handle_data(beginDate, endDate)




#mocked_service = MockedDataService()
#print(type(mocked_service))
#mocked_data = mocked_service.get_data(beginDate, endDate-
/*--

#print(mocked_data)

#api_service = APICallingService()
hourly_data = api_service.call_api(payload, url)
# print(type(payload))


# r = requests.get(url, params=payload)

#json_data = r.json()
#hourly_data = json_data.get("hourly", {})
#hourly_data = mocked_data
print(type(hourly_data["time"]))
print(type(hourly_data["temperature_2m"]))
print(type(hourly_data["city"]))
# View keys
print("Keys:", hourly_data.keys())

# View values
print("Values:", hourly_data.values())
DB_File = "weather_db"
weather_db = WeatherDatabase(DB_File)
#weather_db.close_connect()
#insert_data(self, city, temperature, time):
#weather_db.insert_data()
# View items
#print("Items:", hourly_data.items())


# print(hourly_data)
print(type(hourly_data))
vizHandler = VisualizationHandler()
vizHandler.visualize_data(hourly_data)


print("Hurray")





# Modify the main part of the code to utilize the data
#if __name__ == "__main__":
usable_service = factory.create_data_service("api")
data_handler = DataSourceHandler(usable_service, Visualiz-
/*--
dler())

# Define the database file
#DB_File = "weather_db"

# Create an instance of the WeatherDatabase 
#weather_db = WeatherDatabase(DB_File)

# Open the database connection
#weather_db.open_connect()

# Handle data and utilize it
beginDate = datetime.now() - timedelta(days=7)
endDate = datetime.now()
data_handler.handle_data(beginDate, endDate, weather_db)


# Use DataSourceHandler to handle data from API Service
api_data_handler = DataSourceHandler(api_service, Visuali-
/*--
ndler())
api_data_handler.handle_data(beginDate, endDate, weather_-
/*--

# Analyze and plot average temperatures for cities
vizHandler.analyze_data(weather_db, location_lookups)

# Close the database connection
weather_db.close_connect()

