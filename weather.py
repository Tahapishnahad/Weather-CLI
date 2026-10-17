import sys
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10

WEATHER_CODES = {
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
    99: "Thunderstorm with heavy hail",
}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        sys.exit("Usage: python Weather.py <city>")

    try:
        city_data = get_city_data(sys.argv[1].strip())
        city = extract_city(city_data)

        weather_data = get_weather_data(city)
        weather = extract_weather_data(weather_data)

        print_weather_data(weather, city)

    except requests.exceptions.Timeout:
        sys.exit("The request timed out. Please try again later.")

    except requests.exceptions.ConnectionError:
        sys.exit("Can't connect to the server. Check your internet connection.")

    except requests.RequestException:
        sys.exit("Couldn't retrieve data from the server. Please try again later.")

    except ValueError as error:
        sys.exit(str(error))


def get_city_data(city: str) -> dict:
    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        raise ValueError("The geocoding API returned invalid JSON.")


def extract_city(city_data: dict) -> tuple:
    results = city_data.get("results")

    if not results:
        raise ValueError(
            "City not found. Check the spelling and try again."
        )

    result = results[0]

    try:
        return (
            result["latitude"],
            result["longitude"],
            result["name"],
            result.get("country", "Unknown"),
        )
    except KeyError:
        raise ValueError("The geocoding API returned incomplete city data.")


def get_weather_data(city: tuple) -> dict:
    latitude, longitude, _, _ = city

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        raise ValueError("The weather API returned invalid JSON.")


def extract_weather_data(weather_data: dict) -> tuple:
    current = weather_data.get("current")
    units = weather_data.get("current_units")

    if not isinstance(current, dict) or not isinstance(units, dict):
        raise ValueError("Weather data is missing from the API response.")

    try:
        return (
            current["temperature_2m"],
            current["wind_speed_10m"],
            current["weather_code"],
            current["time"],
            units["temperature_2m"],
            units["wind_speed_10m"],
        )
    except KeyError:
        raise ValueError("The API returned incomplete weather data.")


def print_weather_data(weather: tuple, city: tuple):
    temperature, wind, code, timestamp, temp_unit, wind_unit = weather
    latitude, longitude, name, country = city

    condition = WEATHER_CODES.get(code, "Unknown weather condition")

    date, _, local_time = timestamp.partition("T")
    if not local_time:
        local_time = timestamp

    print(f"""
╔══════════════════════════════════╗
║          🌦 WEATHER CLI          ║
╚══════════════════════════════════╝

📍 {name} | {country}

🌡 Temperature : {temperature} {temp_unit}
💨 Wind        : {wind} {wind_unit}
☁️ Weather     : {condition}

🌎 Latitude    : {latitude:.2f}
🌎 Longitude   : {longitude:.2f}

──────────────────────────────────
🕐 Updated     : {date} | {local_time} (local time)
""")


if __name__ == "__main__":
    main()
