import sys
import requests

def main():
    if len(sys.argv) == 2:
        try:
            row_city = get_city_data(sys.argv[1])
            city = extract_city(row_city)
            row_weather = get_weather_data(city)
            weather = extract_weather_data(row_weather)

            print_weather_data(weather, city)
        except requests.exceptions.ConnectionError:
            sys.exit("Can't connect to the server. Please try again later.")
        except ValueError as e:
            sys.exit(e)
        except requests.RequestException:
            sys.exit("Can't get data. please try again later.")
    else:
        sys.exit("Invalid Arguments")

def get_city_data(city:str):
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")

    response.raise_for_status()
    return response.json()

def extract_city(city_data:dict):
    if not ("results" in city_data.keys()):
        raise ValueError("Can not find result for this city. Check the typo and try again.")

    if len(city_data["results"]) == 0:
        raise ValueError("Can not find result for this city. No data has returned")
    
    result_data = city_data["results"][0]
    return (result_data["latitude"], result_data["longitude"], result_data["name"], result_data.get("country", "Unknown"))

def get_weather_data(arg:tuple):
    latitude, longitude, _, _ = arg

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto"
    }

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=params
    )

    response.raise_for_status()
    return response.json()

def extract_weather_data(weather_data:dict):
    if not ("current" in weather_data):
        raise ValueError("Weather data not found.")
    
    units = weather_data["current"]
    unit = weather_data["current_units"]
    return (
        units["temperature_2m"], units["wind_speed_10m"], units["weather_code"], units["time"],
        unit["temperature_2m"], unit["wind_speed_10m"]
    )

def print_weather_data(weather_data:tuple, city_data:tuple):
    weather_code = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        97: "Heavy thunderstorm",
        99: "Thunderstorm with heavy hail"
    }

    temperature, winds, wcode, time, temperature_unit, winds_unit = weather_data
    lat, lon, name, country = city_data
    date, time = str(time).split("T")

    print(f"""
    ╔══════════════════════════════════╗
    ║          🌦 WEATHER CLI          ║
    ╚══════════════════════════════════╝

    📍 {name} | {country}

    🌡 Temperature : {temperature} {temperature_unit}
    💨 Wind       : {winds} {winds_unit}
    ☁️ Weather    : {weather_code[wcode]}

    🌎 Latitude   : {lat:.2f}
    🌎 Longitude   : {lon:.2f}

    ──────────────────────────────────
    🕐 Updated : {date} | {time} in time of {country}
    """)

main()