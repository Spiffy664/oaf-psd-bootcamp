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



class AbstractDataService:
    def get_data(self, startDate: datetime, endDate: datetime):
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
    
    
class APICallingService(AbstractDataService):
    def get_data(self, startDate: datetime, endDate: datetime):
        print("placeholder test I'm kind of lost")

    def call_api(self, payload: dict, url: str):
        #return {"api_key": "api_value", "payload": payload}
        r = requests.get(url, params=payload)
        json_data = r.json()
        hourly_data = json_data.get("hourly", {})
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
            'appid': '########################'  # Replace with your API key
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
    def __init__(self, data_service):
        self.data_service = data_service

    def handle_data(self, startDate: datetime, endDate: datetime):
        data = self.data_service.get_data(startDate, endDate)
        # Implement handling logic
        print("Handling data:")
        print(data)
        return data
    
    
class DataServiceFactory:
    def create_data_service(self, service_type):
        if service_type == "mocked":
            return MockedDataService()
        elif service_type == "api":
            return APICallingService()
        else:
            raise ValueError("Invalid service type")
    

url = "https://api.open-meteo.com/v1/forecast"

payload = {'latitude': 37.7723281,
           'longitude': -122.4530167,
           'hourly': 'temperature_2m'}



# Example usage
factory = DataServiceFactory()

# Create Mocked Data Service
#mocked_service = factory.create_data_service("mocked")
#print(f"Type of Mocked Service: {type(mocked_service)}")

# Create API Data Service
api_service = factory.create_data_service("api")
print(f"Type of API Service: {type(api_service)}")
#print(type(datetime), "---------------")
#beginDate = datetime.now() - timedelta(days=7)
#endDate = datetime.now()

# Use DataSourceHandler to handle data from Mocked Service
#mocked_data_handler = DataSourceHandler(mocked_service)
#mocked_data_handler.handle_data(beginDate, endDate)

# Use DataSourceHandler to handle data from API Service
#api_data_handler = DataSourceHandler(api_service)
#api_data_handler.handle_data(beginDate, endDate)




#mocked_service = MockedDataService()
#print(type(mocked_service))
#mocked_data = mocked_service.get_data(beginDate, endDate)

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
weather_db.close_connect()
#insert_data(self, city, temperature, time):
#weather_db.insert_data()
# View items
#print("Items:", hourly_data.items())


# print(hourly_data)

fig, ax = plt.subplots()


ax.set_xlabel("Time (hourly)")

ax.set_ylabel("temperature_2m")
ax.plot(hourly_data["time"], hourly_data["temperature_2m"])

plt.show()

print("Hurray")

