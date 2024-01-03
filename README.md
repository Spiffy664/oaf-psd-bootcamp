# oaf-psd-bootcamp
# Weather App

## Overview

The Weather App is designed to provide users with real-time weather and air quality information for a given location. This README.md file outlines the data utilization strategy, including the sources of data, API integration, and how the data is processed and presented in the application.

## Data Sources

The Weather App utilizes two primary data sources:

1. **Weather Data:**
   - Open-Meteo API: Used to fetch hourly weather forecasts based on geographical coordinates.
   - Endpoint: `https://api.open-meteo.com/v1/forecast`

2. **Air Quality Data:**
   - OpenWeatherMap API: Used to retrieve air quality information for a specific location.
   - Endpoint: `https://api.openweathermap.org/data/2.5/air_pollution`

## API Key Requirements

To use the Weather App, you need to obtain API keys for both data sources:

- Open-Meteo API: No API key is required for the Open-Meteo API.
- OpenWeatherMap API: Sign up for a free account and obtain an API key from [OpenWeatherMap](https://openweathermap.org/api).

## Project Structure

The project is structured into several components:

1. **APICallingService:**
   - Manages the interaction with the Open-Meteo and OpenWeatherMap APIs.
   - Fetches weather and air quality data.

2. **DataSourceHandler:**
   - Takes care of handling and combining data from multiple sources.
   - Responsible for further data processing.

3. **MockedDataService:**
   - Provides mocked data for testing purposes.

4. **WeatherDatabase:**
   - Handles interactions with the weather database.

5. **Main Script:**
   - Combines data from different sources and visualizes it using Matplotlib.

## Data Utilization Strategy

1. **Weather Data:**
   - The Weather App retrieves hourly weather forecasts using the Open-Meteo API.
   - The data includes time, temperature at 2 meters, and the city.

2. **Air Quality Data:**
   - The OpenWeatherMap API is used to obtain air quality information.
   - The air quality index (AQI) is extracted and combined with weather data.

3. **Combining Data:**
   - The `APICallingService` fetches data separately from weather and air quality APIs.
   - The `DataSourceHandler` combines these datasets into a unified format.

4. **Visualization:**
   - Matplotlib is used for visualizing the combined data.
   - The script generates a plot displaying the temperature trend and air quality index over time.

## Usage

1. **Obtain API Keys:**
   - Sign up for OpenWeatherMap API and obtain the API key.
   - Replace 'YOUR_OPENWEATHERMAP_API_KEY' in the code with your actual API key.

2. **Run the App:**
   - Execute the main script to fetch and visualize weather and air quality data.
