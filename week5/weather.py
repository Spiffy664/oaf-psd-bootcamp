import requests
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta


class AbstractDataService:
    def get_data(self, startDate: datetime, endDate: datetime):
        raise NotImplementedError("Subclasses must implement this method")

class MockedDataService(AbstractDataService):
    def get_data(self, startDatetime: datetime, endDatetime: datetime):
        # Mocked data retrieval logic
        mocked_data = {
            'time': [],
            'temperature_2m': []
        }

        start_temperature = 5.0
        end_temperature = 20.0
        # Generate mocked time and temperature data
        for i in range(72):  # Assuming 72 data points based on the provided results
            time = f'2023-11-26T{str(i).zfill(2)}:00'
            temperature = round(random.uniform(start_temperature, end_temperature), 1)

            mocked_data['time'].append(time)
            mocked_data['temperature_2m'].append(temperature)

        return mocked_data
    
    
class APICallingService(AbstractDataService):
    def get_data(self, startDate: datetime, endDate: datetime):
        print("placeholder test I'm kind of lost")

    def call_api(self, payload: dict, url: str):
        #return {"api_key": "api_value", "payload": payload}
        r = requests.get(url, params=payload)
        json_data = r.json()
        hourly_data = json_data.get("hourly", {})
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
mocked_service = factory.create_data_service("mocked")
print(f"Type of Mocked Service: {type(mocked_service)}")

# Create API Data Service
api_service = factory.create_data_service("api")
print(f"Type of API Service: {type(api_service)}")
print(type(datetime), "---------------")
beginDate = datetime.now() - timedelta(days=7)
endDate = datetime.now()

# Use DataSourceHandler to handle data from Mocked Service
mocked_data_handler = DataSourceHandler(mocked_service)
mocked_data_handler.handle_data(beginDate, endDate)

# Use DataSourceHandler to handle data from API Service
api_data_handler = DataSourceHandler(api_service)
api_data_handler.handle_data(beginDate, endDate)




mocked_service = MockedDataService()
print(type(mocked_service))
mocked_data = mocked_service.get_data(beginDate, endDate)

print(mocked_data)
# print(type(payload))


# r = requests.get(url, params=payload)

#json_data = r.json()
#hourly_data = json_data.get("hourly", {})
hourly_data = mocked_data


# print(hourly_data)

fig, ax = plt.subplots()


ax.set_xlabel("Time (hourly)")

ax.set_ylabel("temperature_2m")
ax.plot(hourly_data["time"], hourly_data["temperature_2m"])

plt.show()

print("Hurray")
