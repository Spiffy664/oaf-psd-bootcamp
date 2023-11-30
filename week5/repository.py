#my idea for this file is to make repostiroy a interface layer that works between the database and other classes but I don't know if this is necessary to decouple the design / classes.
class WeatherDataRepository:
    def __init__(self, database):
        self.database = database

    def get_weather_data(self, city):
        return self.database.get_weather_data(city)

    def insert_weather_data(self, city, temperature, conditions):
        self.database.insert_data(city, temperature, conditions)
