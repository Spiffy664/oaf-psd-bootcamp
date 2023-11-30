import sqlite3
from datetime import datetime, timedelta
class WeatherDatabase:

    def __init__(self, db_file):

        self.conn = sqlite3.connect(db_file)

        self.cursor = self.conn.cursor()


        self.cursor.excute('''
            CREATE TABLE IF NOT EXISTS weather(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temperature REAL,
                timestamp TEXT
            )
        ''')

    def reset_database(self):

        self.cursor.execute('''
            DELETE FROM weather
        ''')
        self.conn.commit()
        print("Database deleted!")

    def insert_data(self, city, temperature, conditions):

        timestamp = datetime.now()

        self.cursor.execute('''
            SELECT * FROM weather
            WHERE city = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (city, ))
        
        data = self.cursor.fetchone()
        
        # Check if data exists and if it is older than 24 hours before inserting
        if data and datetime.strptime(data[4], "%Y-%m-%d %H:%M:%S") > timestamp - timedelta(hours=24):
            return data
        else:
            self.cursor.execute('''
            INSERT INTO weather (city, temperature, conditions, timestamp) VALUES (?, ?, ?, ?)
            ''', (city, temperature, conditions, timestamp.strftime("%Y-%m-%d %H:%M:%S")))
            self.conn.commit()
    
    def get_weather_data(self, weather_service, city):

        self.cursor.excute('''
            SELECT * FROM weather
            WHERE city = ?
        ''', (city,))
        data = self.cursor.fetchall()

        if data:
            return data
        else:
            weather_data = weather_service.get_weather_data(city)

            self.cursor.excute('''
                INSERT INTO weather (city, temperature)
                VALIES (?, ?)
            ''', (city, str(weather_data)))
            self.conn.commit()

            return weather_data
    
def close_connect(self):
    self.conn.close()
    print("Database connection closed")
