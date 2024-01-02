import sqlite3
from datetime import datetime, timedelta

class WeatherDatabase:

    def __init__(self, db_file):

        self.conn = sqlite3.connect(":memory:")

        self.cursor = self.conn.cursor()


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temperature REAL,
                time TEXT
            )
        ''')

    def insert_data(self, city, temperature, time):

        timestamp = datetime.now()

        self.cursor.execute('''
            SELECT * FROM weather
            WHERE city = ?
            ORDER BY time DESC
            LIMIT 1
        ''', (city, ))
        
        data = self.cursor.fetchone()
        
        # Check if data exists and if it is older than 24 hours before inserting
        if data and datetime.strptime(data[4], "%Y-%m-%d %H:%M:%S") > timestamp - timedelta(hours=24):
            return data
        else:
            self.cursor.execute('''
            INSERT INTO weather (city, temperature, time, timestamp) VALUES (?, ?, ?, ?)
            ''', (city, temperature, time, timestamp.strftime("%Y-%m-%d %H:%M:%S")))
            self.conn.commit()

    def get_weather_data(self, city):
        self.cursor.execute('''
            SELECT * FROM weather
            WHERE city = ?
            ORDER BY time DESC
            LIMIT 1
        ''', (city,))

        data = self.cursor.fetchone()

        if data:
            return data[2]  # Return the temperature from the cached data
        else:
            return None
        

    def get_all_cities(self):
        self.cursor.execute('''
            SELECT DISTINCT city FROM weather
        ''')
        cities = [entry[0] for entry in self.cursor.fetchall()]
        return cities

    def get_weather_data_for_city(self, city):
        self.cursor.execute('''
            SELECT * FROM weather
            WHERE city = ?
        ''', (city,))
        data = self.cursor.fetchall()
        return data
        
    def open_connect(self):
        print("Database connection opened")

    def close_connect(self):
        self.conn.close()
        print("Database connection closed")
